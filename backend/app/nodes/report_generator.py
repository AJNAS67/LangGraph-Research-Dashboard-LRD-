import logging
from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from app.schemas.state import ResearchState
from app.schemas.research import FinalReport
from app.services.llm import get_llm

logger = logging.getLogger(__name__)

REPORT_SYSTEM_PROMPT = """You are a Lead Research Director and Technical Author.
Your mission is to synthesize all accumulated research findings, sources, and analysis into an exhaustive, publication-grade research report.

Core Principles:
1. Clearly distinguish between verified Evidence, analytical Interpretation, and strategic Inference.
2. Adhere strictly to the required structured schema.
3. Explicitly report all contradictions discovered across sources.
4. Transparently disclose limitations and unresolved gaps.
5. In 'raw_markdown', generate a beautifully formatted, comprehensive Markdown document with headers, bullet points, and source citations.
"""


def _render_markdown_report(report: FinalReport, sources: List[Dict[str, Any]]) -> str:
    """Helper to assemble a clean, publication-grade markdown document."""
    findings_md = "\n".join(f"- {f}" for f in report.key_findings)
    contradictions_md = (
        "\n".join(f"- {c}" for c in report.contradictions)
        if report.contradictions
        else "- No significant contradictions detected among collected sources."
    )
    limitations_md = (
        "\n".join(f"- {l}" for l in report.limitations)
        if report.limitations
        else "- Standard search depth constraints apply."
    )
    sources_md = "\n".join(
        f"- [{src.get('title', 'Source')}]({src.get('url', '#')}): {src.get('summary', '')}"
        for src in sources
    )

    return f"""# {report.title}

## Executive Summary
{report.executive_summary}

## Research Methodology
{report.methodology}

## Key Findings
{findings_md}

## Detailed Analysis
{report.detailed_analysis}

## Discrepancies & Contradictions
{contradictions_md}

## Limitations & Gaps
{limitations_md}

## Conclusion & Strategic Outlook
{report.conclusion}

## References & Sources Cited
{sources_md}
"""


async def report_generator_node(state: ResearchState) -> Dict[str, Any]:
    """LangGraph Node: Report Generator.

    Synthesizes the final structured report and renders complete markdown.
    """
    logger.info("Executing Report Generator Node for research_id: %s", state.get("research_id"))
    user_query = state.get("user_query", "")
    objective = state.get("research_objective", "")
    analysis = state.get("analysis", {})
    sources = state.get("collected_sources", [])

    sources_summary = "\n".join(
        f"- {s.get('title')} ({s.get('url')}): {s.get('summary')}"
        for s in sources
    ) if sources else "No sources collected."

    analysis_summary = f"""
Findings: {analysis.get('synthesized_findings', [])}
Agreements: {analysis.get('agreements', [])}
Contradictions: {analysis.get('contradictions', [])}
Gaps: {analysis.get('observed_gaps', [])}
"""

    llm = get_llm()
    structured_report_gen = llm.with_structured_output(FinalReport)

    prompt = ChatPromptTemplate.from_messages([
        ("system", REPORT_SYSTEM_PROMPT),
        (
            "human",
            "User Query: {user_query}\n"
            "Objective: {objective}\n\n"
            "Analysis:\n{analysis_summary}\n\n"
            "Collected Sources:\n{sources_summary}",
        ),
    ])

    chain = prompt | structured_report_gen

    try:
        report: FinalReport = await chain.ainvoke({
            "user_query": user_query,
            "objective": objective,
            "analysis_summary": analysis_summary,
            "sources_summary": sources_summary,
        })
    except Exception as exc:
        logger.error("Report generator LLM invocation failed: %s", exc)
        report = FinalReport(
            title=f"Research Report: {user_query}",
            executive_summary=f"Analysis conducted on: {user_query}",
            methodology="Automated research workflow execution.",
            key_findings=["Research completed with available sources."],
            detailed_analysis=f"Synthesis of findings addressing: {objective}",
            contradictions=[],
            limitations=["LLM generation fallback utilized."],
            conclusion="Further investigation recommended.",
            sources_cited=[s.get("url", "") for s in sources],
        )

    # Ensure raw_markdown is populated and rendered cleanly
    if not report.raw_markdown or report.raw_markdown.strip().endswith("..."):
        report.raw_markdown = _render_markdown_report(report, sources)

    return {
        "final_report": report.model_dump(),
        "current_node": "report_generator",
        "execution_status": "completed",
    }
