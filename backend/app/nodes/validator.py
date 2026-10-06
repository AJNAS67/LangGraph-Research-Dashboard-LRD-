import logging
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from app.schemas.state import ResearchState
from app.schemas.research import ValidationResult
from app.services.llm import get_llm

logger = logging.getLogger(__name__)

VALIDATOR_SYSTEM_PROMPT = """You are an Adversarial Fact-Checking & Research Quality Director.
Your task is to rigorously evaluate whether the collected evidence and synthesis sufficiently answer the user's research query.

Evaluation Criteria:
1. Completeness: Are all dimensions of the query directly addressed?
2. Source Quality: Are findings grounded in credible evidence?
3. Contradictions: Are there unresolved contradictions that require deeper inquiry?
4. Iteration Guardrail: If current retry_count is {retry_count} and max_retries is {max_retries}, judge strictly.

Return structured output:
- status: "VALID" or "NEEDS_MORE_RESEARCH"
- reason: Clear explanation of sufficiency or specific missing aspects
- needs_more_research: boolean
- missing_aspects: List of missing points (if any)
- suggested_queries: List of 1-3 targeted search queries to fill gaps (if needs_more_research is True)
"""


async def validator_node(state: ResearchState) -> Dict[str, Any]:
    """LangGraph Node: Validator.

    Critiques research sufficiency and controls whether the workflow loops back
    to the researcher or advances to final report generation.
    """
    logger.info("Executing Validator Node for research_id: %s", state.get("research_id"))
    user_query = state.get("user_query", "")
    objective = state.get("research_objective", "")
    analysis = state.get("analysis", {})
    sources = state.get("collected_sources", [])
    retry_count = state.get("retry_count", 0)
    max_retries = state.get("max_retries", 2)

    llm = get_llm()
    structured_validator = llm.with_structured_output(ValidationResult)

    analysis_summary = f"""
Findings: {analysis.get('synthesized_findings', [])}
Contradictions: {analysis.get('contradictions', [])}
Observed Gaps: {analysis.get('observed_gaps', [])}
Total Sources Collected: {len(sources)}
Current Retry Count: {retry_count} / {max_retries}
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", VALIDATOR_SYSTEM_PROMPT),
        (
            "human",
            "User Query: {user_query}\n"
            "Objective: {objective}\n\n"
            "Analysis & Evidence:\n{analysis_summary}",
        ),
    ])

    chain = prompt | structured_validator

    try:
        validation: ValidationResult = await chain.ainvoke({
            "user_query": user_query,
            "objective": objective,
            "analysis_summary": analysis_summary,
            "retry_count": retry_count,
            "max_retries": max_retries,
        })
        val_data = validation.model_dump()
    except Exception as exc:
        logger.error("Validator LLM invocation failed: %s", exc)
        # Safe fallback: assume valid to prevent hanging
        val_data = {
            "status": "VALID",
            "reason": "Default validation pass applied.",
            "needs_more_research": False,
            "missing_aspects": [],
            "suggested_queries": [],
        }

    # Bounded counter increment: if more research needed, increment retry count
    new_retry_count = retry_count + 1 if val_data.get("needs_more_research") else retry_count

    return {
        "validation_result": val_data,
        "retry_count": new_retry_count,
        "current_node": "validator",
        "execution_status": "validating",
    }
