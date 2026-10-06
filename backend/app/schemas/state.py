import operator
from typing import TypedDict, List, Optional, Dict, Any, Annotated


class ResearchState(TypedDict):
    """The central state schema for the LangGraph Research workflow.

    Each node in the graph accepts this state and returns a partial
    dictionary update that merges into this state.
    """

    # Session & Query Context
    research_id: str
    user_query: str
    research_depth: str  # 'quick' | 'standard' | 'deep'

    # Planning
    research_objective: str
    subtasks: List[Dict[str, Any]]
    current_subtask_index: int

    # Evidence Collection (additive reducers merge new items rather than overwriting)
    collected_sources: Annotated[List[Dict[str, Any]], operator.add]
    research_notes: Annotated[List[str], operator.add]

    # Analysis & Synthesis
    analysis: Optional[Dict[str, Any]]

    # Validation & Loop Control
    validation_result: Optional[Dict[str, Any]]
    retry_count: int
    max_retries: int

    # Workflow Execution Status
    execution_status: str  # 'planning' | 'researching' | 'analyzing' | 'validating' | 'completed' | 'failed'
    current_node: str
    errors: Annotated[List[str], operator.add]

    # Final Output
    final_report: Optional[Dict[str, Any]]
