import pytest
from app.nodes.planner import planner_node
from app.nodes.researcher import researcher_node
from app.nodes.analyzer import analyzer_node
from app.nodes.report_generator import report_generator_node
from app.tools.mock_search import MockSearchTool


@pytest.mark.asyncio
async def test_planner_node(sample_initial_state):
    result = await planner_node(sample_initial_state)
    assert "research_objective" in result
    assert len(result["research_objective"]) > 0
    assert "subtasks" in result
    assert len(result["subtasks"]) >= 1
    assert result["current_node"] == "planner"
    assert result["execution_status"] == "researching"


@pytest.mark.asyncio
async def test_researcher_node(sample_initial_state):
    # Prepare state with subtasks
    sample_initial_state["subtasks"] = [
        {
            "id": "subtask_1",
            "title": "AI Tools",
            "description": "Examine tools",
            "status": "pending",
            "queries": ["ai coding tools productivity"],
        }
    ]
    tool = MockSearchTool()
    result = await researcher_node(sample_initial_state, search_tool=tool)

    assert "collected_sources" in result
    assert len(result["collected_sources"]) >= 1
    assert "research_notes" in result
    assert len(result["research_notes"]) >= 1
    assert result["current_node"] == "researcher"


@pytest.mark.asyncio
async def test_researcher_node_deduplication(sample_initial_state):
    tool = MockSearchTool()
    # First search pass
    sample_initial_state["subtasks"] = [
        {
            "id": "s1",
            "title": "T1",
            "description": "D1",
            "status": "pending",
            "queries": ["ai coding assistants"],
        }
    ]
    first_res = await researcher_node(sample_initial_state, search_tool=tool)
    assert len(first_res["collected_sources"]) > 0

    # Simulate second pass with already collected sources
    sample_initial_state["collected_sources"] = first_res["collected_sources"]
    second_res = await researcher_node(sample_initial_state, search_tool=tool)
    # The duplicate URLs must not be re-added
    assert len(second_res["collected_sources"]) == 0


@pytest.mark.asyncio
async def test_analyzer_node(sample_initial_state):
    sample_initial_state["research_objective"] = "Evaluate developer velocity."
    sample_initial_state["research_notes"] = [
        "[Benchmark Study] (https://example.com/1): Velocity increased 30%.",
        "[Security Audit] (https://example.com/2): IP leakage remains a primary concern.",
    ]
    result = await analyzer_node(sample_initial_state)

    assert "analysis" in result
    analysis = result["analysis"]
    assert "synthesized_findings" in analysis
    assert "agreements" in analysis
    assert "contradictions" in analysis
    assert result["current_node"] == "analyzer"


@pytest.mark.asyncio
async def test_report_generator_node(sample_initial_state):
    sample_initial_state["research_objective"] = "Assess AI coding tools in 2026."
    sample_initial_state["analysis"] = {
        "synthesized_findings": ["Velocity accelerated 30%."],
        "agreements": ["Testing benefits confirmed."],
        "contradictions": ["Vendor vs independent claims."],
        "observed_gaps": ["Legacy refactoring data scarce."],
    }
    sample_initial_state["collected_sources"] = [
        {
            "id": "s1",
            "title": "Benchmark Report",
            "url": "https://research.techbenchmarks.org/ai-coding-2026",
            "summary": "Velocity benchmark findings.",
        }
    ]

    result = await report_generator_node(sample_initial_state)

    assert "final_report" in result
    report = result["final_report"]
    assert report["title"] is not None
    assert len(report["key_findings"]) >= 1
    assert "raw_markdown" in report
    assert "# " in report["raw_markdown"]
    assert result["current_node"] == "report_generator"
    assert result["execution_status"] == "completed"
