import sys
from pathlib import Path
import pytest

# Ensure backend root is in sys.path
backend_path = Path(__file__).resolve().parent.parent
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

from app.schemas.state import ResearchState


@pytest.fixture
def sample_initial_state() -> ResearchState:
    """Fixture providing clean initial state for research workflow."""
    return {
        "research_id": "test_session_101",
        "user_query": "Research the impact of AI coding assistants on developer productivity in 2026.",
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
