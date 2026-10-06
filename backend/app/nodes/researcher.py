import logging
from typing import Dict, Any, List, Optional
from app.schemas.state import ResearchState
from app.schemas.research import CollectedSource
from app.tools.search_interface import SearchToolInterface
from app.tools.factory import get_search_tool
from app.tools.scraper import normalize_url

logger = logging.getLogger(__name__)


async def researcher_node(
    state: ResearchState,
    search_tool: Optional[SearchToolInterface] = None,
) -> Dict[str, Any]:
    """LangGraph Node: Researcher.

    Executes search queries across planned subtasks, retrieves external sources
    via the configured SearchToolInterface, deduplicates URLs, and extracts factual notes.
    """
    logger.info("Executing Researcher Node for research_id: %s", state.get("research_id"))
    tool = search_tool or get_search_tool()

    subtasks = state.get("subtasks", [])
    existing_sources = state.get("collected_sources", [])
    existing_urls = {
        normalize_url(src.get("url"))
        for src in existing_sources
        if isinstance(src, dict) and src.get("url")
    }

    new_sources: List[Dict[str, Any]] = []
    new_notes: List[str] = []
    new_errors: List[str] = []

    # Gather search queries from subtasks
    queries_to_run: List[str] = []
    for subtask in subtasks:
        for q in subtask.get("queries", []):
            if q and q not in queries_to_run:
                queries_to_run.append(q)

    # Fallback to the main user query if no queries were planned
    if not queries_to_run and state.get("user_query"):
        queries_to_run.append(state.get("user_query"))

    # Execute search queries
    for query in queries_to_run:
        try:
            results: List[CollectedSource] = await tool.search(query, max_results=3)
            for res in results:
                cleaned_url = normalize_url(res.url)
                if cleaned_url and cleaned_url not in existing_urls:
                    existing_urls.add(cleaned_url)
                    # Ensure normalized URL is saved
                    res_dict = res.model_dump()
                    res_dict["url"] = cleaned_url
                    new_sources.append(res_dict)
                    new_notes.append(f"[{res.title}] ({cleaned_url}): {res.summary}")
        except Exception as exc:
            err_msg = f"Search query '{query}' encountered error: {str(exc)}"
            logger.error(err_msg)
            new_errors.append(err_msg)

    logger.info("Researcher Node discovered %d new sources across %d queries", len(new_sources), len(queries_to_run))

    return {
        "collected_sources": new_sources,
        "research_notes": new_notes,
        "errors": new_errors,
        "current_node": "researcher",
        "execution_status": "analyzing",
    }
