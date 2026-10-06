import logging
from typing import Dict, Any, List
from app.schemas.state import ResearchState
from app.schemas.research import CollectedSource
from app.tools.search_interface import SearchToolInterface
from app.tools.mock_search import MockSearchTool

logger = logging.getLogger(__name__)


async def researcher_node(
    state: ResearchState,
    search_tool: SearchToolInterface = None,
) -> Dict[str, Any]:
    """LangGraph Node: Researcher.

    Executes search queries across subtasks, collects verifiable sources,
    and extracts factual research notes.
    """
    logger.info("Executing Researcher Node for research_id: %s", state.get("research_id"))
    tool = search_tool or MockSearchTool()
    
    subtasks = state.get("subtasks", [])
    existing_sources = state.get("collected_sources", [])
    existing_urls = {src.get("url") for src in existing_sources if isinstance(src, dict)}

    new_sources: List[Dict[str, Any]] = []
    new_notes: List[str] = []

    # Gather search queries from pending subtasks
    queries_to_run: List[str] = []
    for subtask in subtasks:
        for q in subtask.get("queries", []):
            if q not in queries_to_run:
                queries_to_run.append(q)

    # If no queries were defined, fallback to user query
    if not queries_to_run and state.get("user_query"):
        queries_to_run.append(state.get("user_query"))

    # Execute search queries
    for query in queries_to_run:
        try:
            results: List[CollectedSource] = await tool.search(query, max_results=3)
            for res in results:
                if res.url not in existing_urls:
                    existing_urls.add(res.url)
                    new_sources.append(res.model_dump())
                    new_notes.append(f"[{res.title}] ({res.url}): {res.summary}")
        except Exception as exc:
            logger.error("Search failed for query '%s': %s", query, exc)

    logger.info("Researcher Node discovered %d new sources", len(new_sources))

    return {
        "collected_sources": new_sources,
        "research_notes": new_notes,
        "current_node": "researcher",
        "execution_status": "analyzing",
    }
