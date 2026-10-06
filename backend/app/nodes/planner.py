import logging
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from app.schemas.state import ResearchState
from app.schemas.research import ResearchPlanOutput
from app.services.llm import get_llm

logger = logging.getLogger(__name__)

PLANNER_SYSTEM_PROMPT = """You are a Principal Research Architect and Senior AI Analyst.
Your task is to analyze the user's research query and construct a rigorous, structured research plan.

Instructions:
1. Synthesize an explicit, unambiguous 'research_objective'.
2. Decompose the objective into 2 to 4 atomic, non-overlapping subtasks.
3. For each subtask, specify:
   - A descriptive title
   - A detailed scope of required information
   - 2-3 precise search queries optimized for search retrieval (avoid punctuation and filler words).
4. Tailor the scope based on requested depth: {research_depth}.

You MUST return your output matching the requested structured schema.
"""


async def planner_node(state: ResearchState) -> Dict[str, Any]:
    """LangGraph Node: Planner.

    Decomposes the user research query into atomic subtasks with targeted search queries.
    """
    logger.info("Executing Planner Node for research_id: %s", state.get("research_id"))
    user_query = state.get("user_query", "")
    research_depth = state.get("research_depth", "standard")

    llm = get_llm()
    structured_planner = llm.with_structured_output(ResearchPlanOutput)

    prompt = ChatPromptTemplate.from_messages([
        ("system", PLANNER_SYSTEM_PROMPT),
        ("human", "Research Query: {user_query}"),
    ])

    chain = prompt | structured_planner

    try:
        plan: ResearchPlanOutput = await chain.ainvoke({
            "user_query": user_query,
            "research_depth": research_depth,
        })
        subtasks_data = [subtask.model_dump() for subtask in plan.subtasks]
        objective = plan.objective
    except Exception as exc:
        logger.error("Planner node LLM invocation failed: %s", exc)
        # Resilient fallback plan if LLM call fails
        objective = f"Investigate core questions around: {user_query}"
        subtasks_data = [
            {
                "id": "subtask_1",
                "title": "Primary Domain Investigation",
                "description": f"Gather primary factual evidence for: {user_query}",
                "status": "pending",
                "queries": [user_query],
            }
        ]

    return {
        "research_objective": objective,
        "subtasks": subtasks_data,
        "current_subtask_index": 0,
        "current_node": "planner",
        "execution_status": "researching",
    }
