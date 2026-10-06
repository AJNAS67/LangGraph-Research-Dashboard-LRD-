from app.tools.factory import get_search_tool, set_search_tool_override
from app.tools.mock_search import MockSearchTool
from app.tools.tavily_search import TavilySearchTool
from app.config.settings import settings


def test_factory_default_fallback():
    # Reset any overrides
    set_search_tool_override(None)

    # When provider is mock
    tool = get_search_tool(provider="mock")
    assert isinstance(tool, MockSearchTool)


def test_factory_tavily_fallback_when_no_key(monkeypatch):
    set_search_tool_override(None)
    monkeypatch.setattr(settings, "TAVILY_API_KEY", "your_tavily_api_key_here")

    # Should safely fallback to MockSearchTool
    tool = get_search_tool(provider="tavily")
    assert isinstance(tool, MockSearchTool)


def test_factory_tavily_with_valid_key(monkeypatch):
    set_search_tool_override(None)
    monkeypatch.setattr(settings, "TAVILY_API_KEY", "tvly-valid-prod-key")

    tool = get_search_tool(provider="tavily")
    assert isinstance(tool, TavilySearchTool)
    assert tool.api_key == "tvly-valid-prod-key"


def test_factory_dependency_injection_override():
    class CustomTestTool(MockSearchTool):
        pass

    custom_tool = CustomTestTool()
    set_search_tool_override(custom_tool)

    # Regardless of requested provider, override should take precedence
    tool = get_search_tool(provider="tavily")
    assert tool is custom_tool

    # Clean up override
    set_search_tool_override(None)
