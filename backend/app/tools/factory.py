import logging
from typing import Optional
from app.config.settings import settings
from app.tools.search_interface import SearchToolInterface
from app.tools.mock_search import MockSearchTool
from app.tools.tavily_search import TavilySearchTool

logger = logging.getLogger(__name__)

# Module-level dependency injection hook for testing
_search_tool_override: Optional[SearchToolInterface] = None


def set_search_tool_override(tool: Optional[SearchToolInterface]) -> None:
    """Sets a global search tool override (primarily for unit/integration tests)."""
    global _search_tool_override
    _search_tool_override = tool


def get_search_tool(provider: Optional[str] = None) -> SearchToolInterface:
    """Factory function returning the configured SearchToolInterface.

    Resolves between TavilySearchTool (production) and MockSearchTool (offline testing),
    falling back safely if external credentials are not set.
    """
    if _search_tool_override is not None:
        return _search_tool_override

    selected_provider = (provider or settings.SEARCH_PROVIDER).lower()

    if selected_provider == "tavily":
        api_key = settings.TAVILY_API_KEY
        if api_key and not api_key.startswith("your_"):
            logger.info("Initializing production TavilySearchTool")
            return TavilySearchTool(api_key=api_key)
        else:
            logger.warning(
                "SEARCH_PROVIDER is set to 'tavily', but TAVILY_API_KEY is not configured. "
                "Falling back to MockSearchTool for safe execution."
            )
            return MockSearchTool()

    logger.info("Initializing MockSearchTool for search operations")
    return MockSearchTool()
