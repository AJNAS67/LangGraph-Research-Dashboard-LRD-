from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Subtask(BaseModel):
    """Represents an atomic, actionable research subtask."""

    id: str = Field(description="Unique identifier, e.g. subtask_1")
    title: str = Field(description="Actionable title of the subtask")
    description: str = Field(description="Detailed scope of required information")
    status: str = Field(default="pending", description="pending | in_progress | completed | failed")
    queries: List[str] = Field(default_factory=list, description="Targeted search queries for this subtask")


class ResearchPlanOutput(BaseModel):
    """Structured LLM output for the initial research decomposition."""

    objective: str = Field(description="Synthesized, explicit research objective")
    subtasks: List[Subtask] = Field(description="List of decomposed research subtasks")


class CollectedSource(BaseModel):
    """Represents a verified piece of external evidence or web citation."""

    id: str = Field(description="Unique ID or hash of the URL")
    title: str = Field(description="Title of the source or document")
    url: str = Field(description="Normalized absolute URL")
    source_type: str = Field(default="web", description="web | academic | document | news")
    summary: str = Field(description="Extracted key information relevant to the research query")
    relevance_score: float = Field(default=0.8, ge=0.0, le=1.0, description="Estimated relevance between 0.0 and 1.0")
    retrieved_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(),
        description="ISO 8601 timestamp of retrieval",
    )
    raw_metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata from search provider")


class AnalysisResult(BaseModel):
    """Structured LLM output for research analysis and cross-examination."""

    synthesized_findings: List[str] = Field(description="Key findings and common patterns discovered")
    agreements: List[str] = Field(description="Corroborated claims confirmed by multiple sources")
    contradictions: List[str] = Field(description="Contradictions, discrepancies, or conflicting viewpoints")
    observed_gaps: List[str] = Field(description="Information that could not be determined or is missing")


class ValidationResult(BaseModel):
    """Structured LLM output evaluating research sufficiency."""

    status: str = Field(description="VALID | NEEDS_MORE_RESEARCH | FAILED")
    reason: str = Field(description="Explanation of sufficiency assessment")
    needs_more_research: bool = Field(default=False)
    missing_aspects: List[str] = Field(default_factory=list, description="Missing components identified")
    suggested_queries: List[str] = Field(default_factory=list, description="Targeted queries to fill gaps")


class FinalReport(BaseModel):
    """Structured research report output."""

    title: str = Field(description="Authoritative, informative report title")
    executive_summary: str = Field(description="High-level synthesis for executive readers")
    methodology: str = Field(description="Overview of research scope, subtasks, and sources")
    key_findings: List[str] = Field(description="Bullet-point key findings")
    detailed_analysis: str = Field(description="Exhaustive thematic analysis in Markdown")
    contradictions: List[str] = Field(description="Identified contradictions or conflicting evidence")
    limitations: List[str] = Field(description="Known research limitations, caveats, or remaining unknowns")
    conclusion: str = Field(description="Strategic summary and outlook")
    sources_cited: List[str] = Field(description="List of cited source URLs")
    raw_markdown: str = Field(default="", description="Complete rendered markdown document")
