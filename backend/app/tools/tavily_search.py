import hashlib
import logging
from datetime import datetime, timezone
from typing import List, Optional
import httpx

from app.config.settings import settings
from app.tools.search_interface import SearchToolInterface
from app.tools.scraper import normalize_url, sanitize_text
from app.schemas.research import CollectedSource

logger = logging.getLogger(__name__)


class TavilySearchTool(SearchToolInterface):
    """Production web search tool adapter integrating with the Tavily Search API.

    Tavily is specifically designed for LLMs, returning pre-filtered content
    extracts rather than raw HTML or search engine link lists.
    """

    TAVILY_API_URL = "https://api.tavily.com/search"

    def __init__(self, api_key: Optional[str] = None, timeout: float = 15.0):
        self.api_key = api_key or settings.TAVILY_API_KEY
        self.timeout = timeout

    async def search(self, query: str, max_results: int = 5) -> List[CollectedSource]:
        """Executes a web search via the Tavily API and returns normalized CollectedSource models."""
        if not self.api_key or self.api_key.startswith("your_"):
            logger.warning("Tavily API key is missing or placeholder; search aborted.")
            return []

        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "basic",
            "include_answer": False,
            "include_raw_content": False,
            "max_results": max_results,
        }

        logger.info("Executing Tavily web search for query: '%s' (max_results=%d)", query, max_results)

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.TAVILY_API_URL, json=payload)

                if response.status_code == 401:
                    logger.error("Tavily authentication failed: Invalid or expired API key.")
                    return []
                elif response.status_code == 429:
                    logger.warning("Tavily rate limit exceeded (HTTP 429).")
                    return []
                elif response.is_error:
                    logger.error("Tavily API error: HTTP %d - %s", response.status_code, response.text)
                    return []

                data = response.json()
        except httpx.TimeoutException:
            logger.error("Tavily API request timed out after %.1f seconds for query: '%s'", self.timeout, query)
            return []
        except httpx.RequestError as exc:
            logger.error("Network error connecting to Tavily API: %s", exc)
            return []

        results = data.get("results", [])
        collected: List[CollectedSource] = []
        now_iso = datetime.now(timezone.utc).isoformat()

        for item in results:
            raw_url = item.get("url", "")
            if not raw_url:
                continue

            clean_url = normalize_url(raw_url)
            url_hash = hashlib.md5(clean_url.encode("utf-8")).hexdigest()[:12]
            title = item.get("title") or "Web Citation"
            raw_content = item.get("content") or ""
            summary = sanitize_text(raw_content)

            raw_score = item.get("score")
            relevance = float(raw_score) if raw_score is not None else 0.85
            # Clamp between 0.0 and 1.0
            relevance = max(0.0, min(1.0, relevance))

            source_type = "web"
            if any(term in clean_url for term in [".edu", "arxiv", "doi.org", "research", "ieee"]):
                source_type = "academic"
            elif any(term in clean_url for term in ["news", "reuters", "bloomberg", "techcrunch", "theverge"]):
                source_type = "news"

            collected.append(
                CollectedSource(
                    id=f"tavily_{url_hash}",
                    title=title,
                    url=clean_url,
                    source_type=source_type,
                    summary=summary,
                    relevance_score=relevance,
                    retrieved_at=now_iso,
                    raw_metadata={
                        "engine": "tavily",
                        "published_date": item.get("published_date"),
                        "raw_score": raw_score,
                    },
                )
            )

        logger.info("Tavily search retrieved %d parsed sources for '%s'", len(collected), query)
        return collected
