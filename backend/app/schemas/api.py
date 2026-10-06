from datetime import datetime, timezone
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

ResearchDepth = Literal["quick", "standard", "deep"]
SessionStatus = Literal["pending", "running", "completed", "failed", "cancelled"]


class CreateResearchRequest(BaseModel):
    """Payload for initializing a new research task."""

    query: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Core research question or complex investigation prompt",
        examples=["Compare PostgreSQL vs MongoDB for modern AI agent state storage in 2026."],
    )
    additional_instructions: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional scoping guidelines or domain priorities",
        examples=["Focus on ACID transactions, schema agility, and vector extension benchmarks."],
    )
    research_depth: ResearchDepth = Field(
        default="standard",
        description="Determines subtask breadth and search query count (quick, standard, deep)",
    )


class SessionStatusResponse(BaseModel):
    """Lightweight response for polling workflow execution state."""

    id: str
    status: SessionStatus
    current_node: str
    retry_count: int
    error_count: int
    updated_at: str


class SourceListResponse(BaseModel):
    """List of all external citations discovered during the session."""

    session_id: str
    count: int
    sources: List[Dict[str, Any]]


class ReportResponse(BaseModel):
    """Final synthesized research report artifact."""

    session_id: str
    title: str
    executive_summary: str
    methodology: str
    key_findings: List[str]
    detailed_analysis: str
    contradictions: List[str]
    limitations: List[str]
    conclusion: str
    sources_cited: List[str]
    raw_markdown: str
    generated_at: str


class ResearchSessionResponse(BaseModel):
    """Complete research session model representation."""

    id: str
    title: str
    user_query: str
    additional_instructions: Optional[str] = None
    research_depth: str
    status: SessionStatus
    current_node: str
    retry_count: int
    research_objective: str
    subtasks: List[Dict[str, Any]] = Field(default_factory=list)
    sources_count: int = 0
    created_at: str
    completed_at: Optional[str] = None


class PaginatedSessionsResponse(BaseModel):
    """Paginated list of historical sessions."""

    items: List[ResearchSessionResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class CancelSessionResponse(BaseModel):
    id: str
    status: str
    message: str
