import asyncio
import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Set

from app.schemas.api import CreateResearchRequest
from app.schemas.state import ResearchState
from app.graph.builder import build_research_graph

logger = logging.getLogger(__name__)


class ResearchService:
    """Manages the lifecycle, background execution, and state storage

    of autonomous research sessions.
    """

    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._cancelled: Set[str] = set()
        self._tasks: Dict[str, asyncio.Task] = {}
        self._compiled_graph = build_research_graph()

    async def create_session(self, request: CreateResearchRequest) -> Dict[str, Any]:
        """Creates a session, prepares the initial state, and launches the

        LangGraph execution in a background task.
        """
        session_id = str(uuid.uuid4())
        now_iso = datetime.now(timezone.utc).isoformat()

        # Derive title
        title_snippet = request.query[:75].strip()
        title = title_snippet + ("..." if len(request.query) > 75 else "")

        initial_state: ResearchState = {
            "research_id": session_id,
            "user_query": request.query,
            "research_depth": request.research_depth,
            "research_objective": "",
            "subtasks": [],
            "current_subtask_index": 0,
            "collected_sources": [],
            "research_notes": [],
            "analysis": None,
            "validation_result": None,
            "retry_count": 0,
            "max_retries": 2 if request.research_depth == "standard" else (1 if request.research_depth == "quick" else 3),
            "execution_status": "planning",
            "current_node": "planner",
            "errors": [],
            "final_report": None,
        }

        session_record = {
            "id": session_id,
            "title": title,
            "user_query": request.query,
            "additional_instructions": request.additional_instructions,
            "research_depth": request.research_depth,
            "status": "running",
            "current_node": "planner",
            "retry_count": 0,
            "max_retries": initial_state["max_retries"],
            "research_objective": "",
            "subtasks": [],
            "collected_sources": [],
            "research_notes": [],
            "analysis": None,
            "validation_result": None,
            "final_report": None,
            "errors": [],
            "created_at": now_iso,
            "updated_at": now_iso,
            "completed_at": None,
        }

        self._sessions[session_id] = session_record

        # Spawn background task
        task = asyncio.create_task(self._run_workflow_background(session_id, initial_state))
        self._tasks[session_id] = task

        logger.info("Research session %s created and dispatched to background runner.", session_id)
        return session_record

    async def _run_workflow_background(self, session_id: str, state: ResearchState) -> None:
        """Asynchronously streams node updates from the StateGraph into the session record."""
        try:
            logger.info("Starting StateGraph execution for session: %s", session_id)
            async for event in self._compiled_graph.astream(state):
                if session_id in self._cancelled:
                    logger.info("Session %s cancellation detected; halting execution loop.", session_id)
                    self._sessions[session_id]["status"] = "cancelled"
                    self._sessions[session_id]["current_node"] = "cancelled"
                    self._sessions[session_id]["updated_at"] = datetime.now(timezone.utc).isoformat()
                    return

                for node_name, state_update in event.items():
                    now_iso = datetime.now(timezone.utc).isoformat()
                    record = self._sessions[session_id]
                    record["current_node"] = node_name
                    record["updated_at"] = now_iso

                    # Merge node updates
                    if "research_objective" in state_update:
                        record["research_objective"] = state_update["research_objective"]
                    if "subtasks" in state_update:
                        record["subtasks"] = state_update["subtasks"]
                    if "collected_sources" in state_update:
                        # Append new unique sources
                        existing_urls = {s["url"] for s in record["collected_sources"] if "url" in s}
                        for src in state_update["collected_sources"]:
                            if src.get("url") not in existing_urls:
                                record["collected_sources"].append(src)
                                existing_urls.add(src.get("url"))
                    if "analysis" in state_update:
                        record["analysis"] = state_update["analysis"]
                    if "validation_result" in state_update:
                        record["validation_result"] = state_update["validation_result"]
                    if "retry_count" in state_update:
                        record["retry_count"] = state_update["retry_count"]
                    if "errors" in state_update:
                        record["errors"].extend(state_update["errors"])
                    if "final_report" in state_update:
                        record["final_report"] = state_update["final_report"]
                        record["status"] = "completed"
                        record["completed_at"] = now_iso

            # Ensure status is marked completed if report exists
            if self._sessions[session_id].get("final_report"):
                self._sessions[session_id]["status"] = "completed"
                self._sessions[session_id]["current_node"] = "completed"

            logger.info("Session %s workflow execution completed successfully.", session_id)

        except Exception as exc:
            logger.error("Workflow failed for session %s: %s", session_id, exc, exc_info=True)
            if session_id in self._sessions:
                self._sessions[session_id]["status"] = "failed"
                self._sessions[session_id]["errors"].append(str(exc))
                self._sessions[session_id]["updated_at"] = datetime.now(timezone.utc).isoformat()

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        return self._sessions.get(session_id)

    def list_sessions(
        self,
        page: int = 1,
        page_size: int = 10,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        all_items = list(self._sessions.values())
        if status:
            all_items = [s for s in all_items if s.get("status") == status]

        # Sort newest first
        all_items.sort(key=lambda s: s.get("created_at", ""), reverse=True)

        total = len(all_items)
        start = (page - 1) * page_size
        end = start + page_size
        items = all_items[start:end]
        total_pages = max(1, (total + page_size - 1) // page_size)

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def cancel_session(self, session_id: str) -> bool:
        if session_id in self._sessions:
            self._cancelled.add(session_id)
            self._sessions[session_id]["status"] = "cancelled"
            return True
        return False


# Singleton service instance
research_service = ResearchService()
