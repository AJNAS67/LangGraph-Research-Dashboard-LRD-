import pytest
import httpx
from app.tools.tavily_search import TavilySearchTool


@pytest.mark.asyncio
async def test_tavily_missing_or_placeholder_key():
    tool = TavilySearchTool(api_key="your_tavily_api_key_here")
    results = await tool.search("quantum computing")
    assert results == []

    tool_none = TavilySearchTool(api_key="")
    results_none = await tool_none.search("quantum computing")
    assert results_none == []


@pytest.mark.asyncio
async def test_tavily_successful_response(monkeypatch):
    mock_response_data = {
        "query": "LangGraph multi agent workflows",
        "results": [
            {
                "title": "Stateful Agents with LangGraph",
                "url": "https://research.arxiv.org/abs/2026.1234?utm_source=twitter#intro",
                "content": "<p>LangGraph introduces cyclical state machines for autonomous agents.</p>",
                "score": 0.94,
                "published_date": "2026-02-15",
            },
            {
                "title": "TechCrunch AI Industry Report",
                "url": "https://techcrunch.com/2026/01/ai-agents-breakthrough/",
                "content": "Enterprise adoption of AI agents accelerated across software engineering.",
                "score": 0.88,
                "published_date": "2026-01-20",
            },
        ],
    }

    async def mock_post(*args, **kwargs):
        request = httpx.Request("POST", "https://api.tavily.com/search")
        return httpx.Response(200, json=mock_response_data, request=request)

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    tool = TavilySearchTool(api_key="tvly-valid-test-key-123")
    results = await tool.search("LangGraph multi agent workflows", max_results=2)

    assert len(results) == 2

    # Check source 1 (academic detection & URL normalization)
    src1 = results[0]
    assert src1.title == "Stateful Agents with LangGraph"
    assert src1.url == "https://research.arxiv.org/abs/2026.1234"  # utm and fragment stripped
    assert src1.source_type == "academic"
    assert src1.relevance_score == 0.94
    assert "<p>" not in src1.summary
    assert src1.raw_metadata.get("engine") == "tavily"

    # Check source 2 (news detection)
    src2 = results[1]
    assert src2.source_type == "news"
    assert src2.relevance_score == 0.88


@pytest.mark.asyncio
async def test_tavily_http_401_unauthorized(monkeypatch):
    async def mock_post(*args, **kwargs):
        request = httpx.Request("POST", "https://api.tavily.com/search")
        return httpx.Response(401, text="Unauthorized", request=request)

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    tool = TavilySearchTool(api_key="tvly-invalid-key")
    results = await tool.search("test query")
    assert results == []


@pytest.mark.asyncio
async def test_tavily_http_429_rate_limited(monkeypatch):
    async def mock_post(*args, **kwargs):
        request = httpx.Request("POST", "https://api.tavily.com/search")
        return httpx.Response(429, text="Rate limit exceeded", request=request)

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    tool = TavilySearchTool(api_key="tvly-test-key")
    results = await tool.search("test query")
    assert results == []


@pytest.mark.asyncio
async def test_tavily_timeout_exception(monkeypatch):
    async def mock_post(*args, **kwargs):
        raise httpx.TimeoutException("Read timed out")

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)

    tool = TavilySearchTool(api_key="tvly-test-key", timeout=1.0)
    results = await tool.search("test query")
    assert results == []
