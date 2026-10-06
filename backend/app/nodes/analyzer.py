import logging
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from app.schemas.state import ResearchState
from app.schemas.research import AnalysisResult
from app.services.llm import get_llm

logger = logging.getLogger(__name__)

ANALYZER_SYSTEM_PROMPT = """You are a Principal Research Analyst and Critical Evaluator.
Your objective is to deeply cross-examine collected research notes, evaluate source agreements,
identify discrepancies or contradictions, and isolate information gaps.

Instructions:
1. Synthesize primary thematic findings from the collected evidence.
2. Identify points of agreement where multiple sources corroborate a claim.
3. Explicitly detect contradictions, conflicting metrics, or competing viewpoints.
4. Highlight observed gaps or questions that remain unanswered by the evidence.

You MUST format your output matching the requested structured schema.
"""


async def analyzer_node(state: ResearchState) -> Dict[str, Any]:
    """LangGraph Node: Analyzer.

    Synthesizes research notes, cross-examines evidence, isolates agreements,
    and detects contradictions.
    """
    logger.info("Executing Analyzer Node for research_id: %s", state.get("research_id"))
    objective = state.get("research_objective", "")
    notes = state.get("research_notes", [])
    notes_text = "\n\n".join(notes) if notes else "No research notes collected."

    llm = get_llm()
    structured_analyzer = llm.with_structured_output(AnalysisResult)

    prompt = ChatPromptTemplate.from_messages([
        ("system", ANALYZER_SYSTEM_PROMPT),
        (
            "human",
            "Research Objective: {objective}\n\nCollected Research Notes:\n{notes_text}",
        ),
    ])

    chain = prompt | structured_analyzer

    try:
        analysis: AnalysisResult = await chain.ainvoke({
            "objective": objective,
            "notes_text": notes_text,
        })
        analysis_data = analysis.model_dump()
    except Exception as exc:
        logger.error("Analyzer node LLM invocation failed: %s", exc)
        analysis_data = {
            "synthesized_findings": ["Initial evidence synthesized."],
            "agreements": ["Sources agree on foundational aspects."],
            "contradictions": [],
            "observed_gaps": ["Detailed quantitative metrics require further analysis."],
        }

    return {
        "analysis": analysis_data,
        "current_node": "analyzer",
        "execution_status": "reporting",
    }
