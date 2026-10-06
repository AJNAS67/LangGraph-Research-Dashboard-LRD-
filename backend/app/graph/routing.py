import logging
from app.schemas.state import ResearchState

logger = logging.getLogger(__name__)


def should_continue_research(state: ResearchState) -> str:
    """Conditional Edge function for LangGraph.

    Evaluates the Validator's outcome:
    - If needs_more_research is True AND retry_count <= max_retries: loops back to 'researcher'
    - Otherwise (valid OR retry budget exhausted): advances to 'report_generator'
    """
    validation = state.get("validation_result") or {}
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 2)
    needs_more = validation.get("needs_more_research", False)

    if needs_more and retry_count <= max_retries:
        logger.info(
            "Conditional Routing: Validator determined additional research is required. "
            "Looping back to 'researcher' (Retry %d/%d).",
            retry_count,
            max_retries,
        )
        return "researcher"

    if needs_more and retry_count > max_retries:
        logger.warning(
            "Conditional Routing: Additional research was desired, but max_retries (%d) "
            "budget is exhausted. Circuit breaker triggered; advancing to 'report_generator'.",
            max_retries,
        )
    else:
        logger.info("Conditional Routing: Research is VALID. Advancing to 'report_generator'.")

    return "report_generator"
