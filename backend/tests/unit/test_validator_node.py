import pytest
from app.nodes.validator import validator_node
from app.graph.routing import should_continue_research


@pytest.mark.asyncio
async def test_validator_node_default_valid(sample_initial_state):
    sample_initial_state["research_objective"] = "Evaluate developer velocity."
    sample_initial_state["analysis"] = {
        "synthesized_findings": ["Velocity increased by 30%."],
        "contradictions": [],
        "observed_gaps": [],
    }
    sample_initial_state["collected_sources"] = [{"id": "s1", "url": "https://example.com"}]

    result = await validator_node(sample_initial_state)

    assert "validation_result" in result
    val_data = result["validation_result"]
    assert "status" in val_data
    assert "reason" in val_data
    assert result["current_node"] == "validator"
    assert result["execution_status"] == "validating"


def test_routing_when_valid():
    state = {
        "validation_result": {"status": "VALID", "needs_more_research": False},
        "retry_count": 0,
        "max_retries": 2,
    }
    next_node = should_continue_research(state)
    assert next_node == "report_generator"


def test_routing_when_needs_more_research_under_limit():
    state = {
        "validation_result": {"status": "NEEDS_MORE_RESEARCH", "needs_more_research": True},
        "retry_count": 1,
        "max_retries": 2,
    }
    next_node = should_continue_research(state)
    assert next_node == "researcher"


def test_routing_circuit_breaker_when_retries_exceeded():
    state = {
        "validation_result": {"status": "NEEDS_MORE_RESEARCH", "needs_more_research": True},
        "retry_count": 3,
        "max_retries": 2,
    }
    # Circuit breaker: must route to report_generator despite needs_more_research
    next_node = should_continue_research(state)
    assert next_node == "report_generator"
