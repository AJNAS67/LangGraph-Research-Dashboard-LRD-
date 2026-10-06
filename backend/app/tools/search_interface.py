from abc import ABC, abstractmethod
from typing import List
from app.schemas.research import CollectedSource


class SearchToolInterface(ABC):
    """Abstract interface for external search tools.

    Isolates nodes from specific search providers (Tavily, Mock, Bing, Google).
    """

    @abstractmethod
    async def search(self, query: str, max_results: int = 5) -> List[CollectedSource]:
        """Execute a search query and return normalized CollectedSource instances."""
        pass
