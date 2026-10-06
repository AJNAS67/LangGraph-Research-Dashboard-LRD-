import hashlib
from datetime import datetime, timezone
from typing import List
from app.tools.search_interface import SearchToolInterface
from app.schemas.research import CollectedSource


class MockSearchTool(SearchToolInterface):
    """Deterministic mock search tool for testing and Phase 1 offline workflows."""

    def __init__(self, predefined_results: List[CollectedSource] = None):
        self._predefined = predefined_results or []

    async def search(self, query: str, max_results: int = 5) -> List[CollectedSource]:
        if self._predefined:
            return self._predefined[:max_results]

        normalized_query = query.lower()
        now_iso = datetime.now(timezone.utc).isoformat()
        
        # Deterministic generation based on query content
        query_hash = hashlib.md5(query.encode("utf-8")).hexdigest()[:8]
        
        if "coding" in normalized_query or "tool" in normalized_query or "assist" in normalized_query:
            return [
                CollectedSource(
                    id=f"mock_src_1_{query_hash}",
                    title="2026 Developer Velocity & AI Coding Assistant Benchmark",
                    url=f"https://research.techbenchmarks.org/ai-coding-2026-{query_hash}",
                    source_type="academic",
                    summary="Empirical evaluation reveals 25-35% velocity gains in routine scaffolding and unit testing, but highlights challenges in large legacy refactorings.",
                    relevance_score=0.92,
                    retrieved_at=now_iso,
                    raw_metadata={"author": "Benchmark Labs", "published": "2026-01-15"},
                ),
                CollectedSource(
                    id=f"mock_src_2_{query_hash}",
                    title="Enterprise Security and Intellectual Property Risks in AI Generation",
                    url=f"https://infosec-journal.org/ai-risks-governance-2026-{query_hash}",
                    source_type="news",
                    summary="Surveys show 42% of enterprise CTOs mandate air-gapped or private VPC LLM gateways due to token leakage and dependency license risks.",
                    relevance_score=0.88,
                    retrieved_at=now_iso,
                    raw_metadata={"author": "InfoSec Weekly", "published": "2026-02-02"},
                ),
            ]

        # Generic factual mock source
        return [
            CollectedSource(
                id=f"mock_src_gen_{query_hash}",
                title=f"Comprehensive Findings on {query.title()}",
                url=f"https://research-gateway.io/topic/{query_hash}",
                source_type="web",
                summary=f"Analysis of {query} highlights key technological advances, adoption drivers, and implementation trade-offs observed in 2026 industry deployments.",
                relevance_score=0.85,
                retrieved_at=now_iso,
                raw_metadata={"query": query},
            )
        ]
