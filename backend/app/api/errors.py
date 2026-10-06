from typing import Optional, Any
from fastapi import Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None


class APIErrorResponse(BaseModel):
    error: ErrorDetail


class LRDException(Exception):
    """Base exception for domain errors in LangGraph Research Dashboard."""

    def __init__(self, code: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, details: Any = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class SessionNotFoundException(LRDException):
    def __init__(self, session_id: str):
        super().__init__(
            code="SESSION_NOT_FOUND",
            message=f"Research session with ID '{session_id}' was not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class ReportNotFoundException(LRDException):
    def __init__(self, session_id: str):
        super().__init__(
            code="REPORT_NOT_FOUND",
            message=f"Research report for session '{session_id}' is not yet finalized or generated.",
            status_code=status.HTTP_404_NOT_FOUND,
        )


async def lrd_exception_handler(request: Request, exc: LRDException) -> JSONResponse:
    """Formats LRD domain exceptions into clean JSON responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global catch-all exception handler to prevent leaking raw tracebacks."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred while processing the request.",
                "details": str(exc),
            }
        },
    )
