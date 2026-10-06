import operator
import pytest
from app.schemas.research import (
    Subtask,
    CollectedSource,
    AnalysisResult,
    FinalReport,
)
from app.schemas.state import ResearchState


def test_subtask_model_validation():
    subtask = Subtask(
        id="subtask_1",
        title="Test Subtask",
        description="Verify subtask behavior",
        queries=["query 1", "query 2"],
    )
    assert subtask.id == "subtask_1"
    assert subtask.status == "pending"
    assert len(subtask.queries) == 2


def test_collected_source_model_validation():
    source = CollectedSource(
        id="src_1",
        title="Source 1",
        url="https://example.com/test",
        summary="A test summary of findings.",
        relevance_score=0.95,
    )
    assert source.id == "src_1"
    assert source.source_type == "web"
    assert source.relevance_score == 0.95
    assert source.retrieved_at is not None


def test_analysis_result_model():
    analysis = AnalysisResult(
        synthesized_findings=["Finding A"],
        agreements=["Agreement 1"],
        contradictions=["Contradiction 1"],
        observed_gaps=["Gap 1"],
    )
    assert len(analysis.synthesized_findings) == 1
    assert len(analysis.contradictions) == 1


def test_final_report_model():
    report = FinalReport(
        title="Test Report",
        executive_summary="Summary",
        methodology="Methodology",
        key_findings=["Finding 1"],
        detailed_analysis="Detailed body text",
        contradictions=[],
        limitations=[],
        conclusion="Conclusion",
        sources_cited=["https://example.com"],
    )
    assert report.title == "Test Report"
    assert len(report.sources_cited) == 1


def test_reducer_addition_behavior():
    """Verify that operator.add combines lists properly as used in ResearchState."""
    sources_a = [{"id": "s1", "title": "Source 1"}]
    sources_b = [{"id": "s2", "title": "Source 2"}]
    merged = operator.add(sources_a, sources_b)
    assert len(merged) == 2
    assert merged[0]["id"] == "s1"
    assert merged[1]["id"] == "s2"
