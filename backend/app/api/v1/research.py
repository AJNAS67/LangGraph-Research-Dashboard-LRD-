from typing import Optional
from fastapi import APIRouter, status, Query
from app.schemas.api import (
    CreateResearchRequest,
    ResearchSessionResponse,
    SessionStatusResponse,
    SourceListResponse,
    ReportResponse,
    PaginatedSessionsResponse,
    CancelSessionResponse,
)
from app.services.research_service import research_service
from app.api.errors import SessionNotFoundException, ReportNotFoundException

router = APIRouter(prefix="/research", tags=["Research"])


@router.post(
    "",
    response_model=ResearchSessionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Initialize an autonomous research workflow",
)
async def create_research_session(payload: CreateResearchRequest):
    """Initializes a new LangGraph research session and schedules background execution."""
    session = await research_service.create_session(payload)
    return ResearchSessionResponse(
        id=session["id"],
        title=session["title"],
        user_query=session["user_query"],
        additional_instructions=session.get("additional_instructions"),
        research_depth=session["research_depth"],
        status=session["status"],
        current_node=session["current_node"],
        retry_count=session["retry_count"],
        research_objective=session.get("research_objective", ""),
        subtasks=session.get("subtasks", []),
        sources_count=len(session.get("collected_sources", [])),
        created_at=session["created_at"],
        completed_at=session.get("completed_at"),
    )


@router.get(
    "",
    response_model=PaginatedSessionsResponse,
    summary="List research sessions with pagination",
)
async def list_research_sessions(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    status: Optional[str] = Query(default=None),
):
    """Retrieves paginated list of all created research sessions."""
    result = research_service.list_sessions(page=page, page_size=page_size, status=status)
    items = [
        ResearchSessionResponse(
            id=s["id"],
            title=s["title"],
            user_query=s["user_query"],
            additional_instructions=s.get("additional_instructions"),
            research_depth=s["research_depth"],
            status=s["status"],
            current_node=s["current_node"],
            retry_count=s["retry_count"],
            research_objective=s.get("research_objective", ""),
            subtasks=s.get("subtasks", []),
            sources_count=len(s.get("collected_sources", [])),
            created_at=s["created_at"],
            completed_at=s.get("completed_at"),
        )
        for s in result["items"]
    ]
    return PaginatedSessionsResponse(
        items=items,
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
    )


@router.get(
    "/{session_id}",
    response_model=ResearchSessionResponse,
    summary="Get complete session state and subtasks",
)
async def get_research_session(session_id: str):
    session = research_service.get_session(session_id)
    if not session:
        raise SessionNotFoundException(session_id)

    return ResearchSessionResponse(
        id=session["id"],
        title=session["title"],
        user_query=session["user_query"],
        additional_instructions=session.get("additional_instructions"),
        research_depth=session["research_depth"],
        status=session["status"],
        current_node=session["current_node"],
        retry_count=session["retry_count"],
        research_objective=session.get("research_objective", ""),
        subtasks=session.get("subtasks", []),
        sources_count=len(session.get("collected_sources", [])),
        created_at=session["created_at"],
        completed_at=session.get("completed_at"),
    )


@router.get(
    "/{session_id}/status",
    response_model=SessionStatusResponse,
    summary="Lightweight polling endpoint for node execution progress",
)
async def get_session_status(session_id: str):
    session = research_service.get_session(session_id)
    if not session:
        raise SessionNotFoundException(session_id)

    return SessionStatusResponse(
        id=session["id"],
        status=session["status"],
        current_node=session["current_node"],
        retry_count=session["retry_count"],
        error_count=len(session.get("errors", [])),
        updated_at=session["updated_at"],
    )


@router.get(
    "/{session_id}/sources",
    response_model=SourceListResponse,
    summary="Retrieve all discovered sources for a session",
)
async def get_session_sources(session_id: str):
    session = research_service.get_session(session_id)
    if not session:
        raise SessionNotFoundException(session_id)

    sources = session.get("collected_sources", [])
    return SourceListResponse(
        session_id=session_id,
        count=len(sources),
        sources=sources,
    )


@router.get(
    "/{session_id}/report",
    response_model=ReportResponse,
    summary="Retrieve finalized research report",
)
async def get_session_report(session_id: str):
    session = research_service.get_session(session_id)
    if not session:
        raise SessionNotFoundException(session_id)

    report = session.get("final_report")
    if not report:
        raise ReportNotFoundException(session_id)

    return ReportResponse(
        session_id=session_id,
        title=report["title"],
        executive_summary=report["executive_summary"],
        methodology=report["methodology"],
        key_findings=report.get("key_findings", []),
        detailed_analysis=report["detailed_analysis"],
        contradictions=report.get("contradictions", []),
        limitations=report.get("limitations", []),
        conclusion=report["conclusion"],
        sources_cited=report.get("sources_cited", []),
        raw_markdown=report.get("raw_markdown", ""),
        generated_at=session.get("completed_at", session["updated_at"]),
    )


@router.post(
    "/{session_id}/cancel",
    response_model=CancelSessionResponse,
    summary="Cancel a running research workflow",
)
async def cancel_research_session(session_id: str):
    session = research_service.get_session(session_id)
    if not session:
        raise SessionNotFoundException(session_id)

    success = research_service.cancel_session(session_id)
    return CancelSessionResponse(
        id=session_id,
        status="cancelled" if success else session["status"],
        message="Workflow execution cancellation requested.",
    )
