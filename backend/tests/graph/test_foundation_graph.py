import pytest
from app.graph.builder import build_research_graph


@pytest.mark.asyncio
async def test_foundation_graph_end_to_end(sample_initial_state):
    """End-to-end integration test of the Phase 1 LangGraph workflow.

    Verifies the complete execution:
    START -> Planner -> Researcher -> Analyzer -> Report Generator -> END
    """
    graph = build_research_graph()
    assert graph is not None

    # Execute workflow asynchronously
    final_state = await graph.ainvoke(sample_initial_state)

    # Assertions on resulting state
    assert final_state is not None
    assert final_state["current_node"] == "report_generator"
    assert final_state["execution_status"] == "completed"

    # Verify Planner output
    assert len(final_state["research_objective"]) > 0
    assert len(final_state["subtasks"]) >= 1

    # Verify Researcher output
    assert len(final_state["collected_sources"]) >= 1
    assert len(final_state["research_notes"]) >= 1

    # Verify Analyzer output
    assert final_state["analysis"] is not None
    assert "synthesized_findings" in final_state["analysis"]

    # Verify Report Generator output
    assert final_state["final_report"] is not None
    report = final_state["final_report"]
    assert report["title"] is not None
    assert len(report["key_findings"]) >= 1
    assert len(report["raw_markdown"]) > 0
    assert "## Executive Summary" in report["raw_markdown"]
    assert "## Key Findings" in report["raw_markdown"]
