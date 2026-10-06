import logging
from langgraph.graph import StateGraph, START, END
from app.schemas.state import ResearchState
from app.nodes.planner import planner_node
from app.nodes.researcher import researcher_node
from app.nodes.analyzer import analyzer_node
from app.nodes.validator import validator_node
from app.nodes.report_generator import report_generator_node
from app.graph.routing import should_continue_research

logger = logging.getLogger(__name__)


def build_research_graph(checkpointer=None):
    """Assembles and compiles the full cyclical LangGraph Research Workflow.

    Topology:
        START -> Planner -> Researcher -> Analyzer -> Validator
                                ▲                         │
                                │   (needs_more_research) │
                                └─────────────────────────┤
                                                          ▼ (valid or max retries)
                                                    Report Generator -> END
    """
    logger.info("Assembling cyclical LangGraph Research Workflow...")
    workflow = StateGraph(ResearchState)

    # Register Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("validator", validator_node)
    workflow.add_node("report_generator", report_generator_node)

    # Deterministic Edges
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "analyzer")
    workflow.add_edge("analyzer", "validator")

    # Conditional Routing Edge after Validator
    workflow.add_conditional_edges(
        "validator",
        should_continue_research,
        {
            "researcher": "researcher",
            "report_generator": "report_generator",
        },
    )

    workflow.add_edge("report_generator", END)

    compiled_graph = workflow.compile(checkpointer=checkpointer)
    logger.info("Cyclical LangGraph Research Workflow compiled successfully.")
    return compiled_graph
