"""CLI runner for testing the LangGraph Research workflow directly from the terminal."""

import asyncio
import sys
from pathlib import Path

# Add backend directory to path
backend_path = Path(__file__).resolve().parent.parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.graph.builder import build_research_graph
from app.schemas.state import ResearchState


async def main():
    query = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Research the impact of AI coding assistants on software developer productivity in 2026."
    )

    print("=" * 80)
    print(" LANGGRAPH RESEARCH DASHBOARD — WORKFLOW RUNNER (PHASE 1)")
    print("=" * 80)
    print(f"Query: {query}\n")

    initial_state: ResearchState = {
        "research_id": "cli_session_001",
        "user_query": query,
        "research_depth": "standard",
        "research_objective": "",
        "subtasks": [],
        "current_subtask_index": 0,
        "collected_sources": [],
        "research_notes": [],
        "analysis": None,
        "validation_result": None,
        "retry_count": 0,
        "max_retries": 2,
        "execution_status": "planning",
        "current_node": "start",
        "errors": [],
        "final_report": None,
    }

    graph = build_research_graph()

    print("[1/5] Executing LangGraph Workflow...")
    print(" -> START")

    # Stream node execution progress
    async for event in graph.astream(initial_state):
        for node_name, state_update in event.items():
            print(f" -> Completed Node: [{node_name.upper()}]")
            if node_name == "planner":
                print(f"    Objective: {state_update.get('research_objective')}")
                subtasks = state_update.get("subtasks", [])
                print(f"    Planned Subtasks: {len(subtasks)}")
                for st in subtasks:
                    print(f"      • {st.get('title')}")
            elif node_name == "researcher":
                sources = state_update.get("collected_sources", [])
                print(f"    Discovered Sources: {len(sources)}")
                for src in sources:
                    print(f"      • [{src.get('relevance_score'):.2f}] {src.get('title')}")
            elif node_name == "analyzer":
                analysis = state_update.get("analysis", {})
                findings = analysis.get("synthesized_findings", [])
                print(f"    Findings Synthesized: {len(findings)}")
            elif node_name == "report_generator":
                report = state_update.get("final_report", {})
                print(f"    Report Title: {report.get('title')}")

    print(" -> END")
    print("\n" + "=" * 80)
    print(" FINAL REPORT PREVIEW")
    print("=" * 80)
    report_dict = state_update.get("final_report", {})
    print(report_dict.get("raw_markdown", "No report generated."))
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
