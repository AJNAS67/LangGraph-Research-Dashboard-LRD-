import logging
from langgraph.graph import StateGraph, START, END
from app.schemas.state import ResearchState
from app.nodes.planner import planner_node
from app.nodes.researcher import researcher_node
from app.nodes.analyzer import analyzer_node
from app.nodes.report_generator import report_generator_node

logger = logging.getLogger(__name__)


def build_research_graph(checkpointer=None):
    """Assembles and compiles the Phase 1 LangGraph Research Workflow.

    Topology:
        START -> Planner -> Researcher -> Analyzer -> Report Generator -> END
    """
    logger.info("Assembling LangGraph Research Workflow...")
    workflow = StateGraph(ResearchState)

    # Register Nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("report_generator", report_generator_node)

    # Add Edges (Phase 1 Linear Foundation)
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "analyzer")
    workflow.add_edge("analyzer", "report_generator")
    workflow.add_edge("report_generator", END)

    compiled_graph = workflow.compile(checkpointer=checkpointer)
    logger.info("LangGraph Research Workflow successfully compiled.")
    return compiled_graph
