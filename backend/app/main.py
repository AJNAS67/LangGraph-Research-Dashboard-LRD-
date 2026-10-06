import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.api.v1.research import router as research_router
from app.api.errors import LRDException, lrd_exception_handler, generic_exception_handler

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("lrd")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing LangGraph Research Dashboard API service...")
    yield
    logger.info("Shutting down LangGraph Research Dashboard API service...")


app = FastAPI(
    title="LangGraph Research Dashboard API",
    description="Production-quality autonomous research platform orchestrated via LangGraph.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
app.add_exception_handler(LRDException, lrd_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# API Routers
app.include_router(research_router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health_check():
    """System liveness and readiness probe."""
    return {
        "status": "healthy",
        "service": "langgraph-research-dashboard",
        "env": settings.APP_ENV,
        "search_provider": settings.SEARCH_PROVIDER,
    }


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to LangGraph Research Dashboard API",
        "docs_url": "/docs",
        "version": "1.0.0",
    }
