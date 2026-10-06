# Architecture Specification: LangGraph Research Dashboard (LRD)

## 1. System Overview

**LangGraph Research Dashboard (LRD)** is a production-grade, autonomous research platform designed to decompose complex queries, execute multi-step research plans, aggregate real-time web intelligence, validate findings against hallucination and contradiction, and synthesize structured, verifiable reports.

Unlike simple linear AI pipelines or standard conversational chat agents, LRD is engineered as a **stateful, cyclical graph-based workflow** managed by LangGraph. It provides deterministic control flow, conditional routing, loop back-off limits, human-in-the-loop inspection capabilities, and resilient state checkpointing.

---

## 2. Architectural Principles

1. **Clean Architecture & Domain Separation**: Separation between presentation (React/Vite), application orchestration (FastAPI REST/SSE), workflow engine (LangGraph StateGraph), and infrastructure (PostgreSQL/pgvector, Tavily Search, LLM providers).
2. **Pluggable & Isolated Adapters**:
   - The LLM interface is decoupled via LangChain's `BaseChatModel` abstraction, supporting OpenAI, Anthropic, Ollama, or custom self-hosted endpoints.
   - The Search interface is decoupled behind an abstract `SearchToolInterface`, allowing instant switching between Tavily, Serper, Bing, or offline test harnesses.
3. **Explicit, Strongly Typed State**: All state transformations within the graph are governed by immutable or additive Pydantic/TypedDict models. Node outputs are strictly validated via structured schema outputs.
4. **Resilience & Infinite-Loop Prevention**: Every cyclical path in the workflow (e.g., `Validator -> Researcher`) contains an explicit counter (`retry_count`) bounded by hard system thresholds (`MAX_RESEARCH_RETRIES`).
5. **Full Observability & Auditability**: Every step, node transition, retrieved URL, confidence score, and validation critique is persisted as an immutable event in PostgreSQL and streamed to the UI via Server-Sent Events (SSE).

---

## 3. High-Level Architecture Diagram

```
┌────────────────────────────────────────────────────────────────────────┐
│                        PRESENTATION LAYER                              │
│                                                                        │
│   React 18 + TypeScript + Vite + Tailwind CSS + TanStack Query         │
│   ┌───────────────────────┐  ┌─────────────────────────────────────┐   │
│   │  Research Input & Plan│  │  Interactive Graph Visualizer (SVG) │   │
│   └───────────────────────┘  └─────────────────────────────────────┘   │
│   ┌───────────────────────┐  ┌─────────────────────────────────────┐   │
│   │  Source Explorer Tab  │  │  Structured Report Viewer (Markdown)│   │
│   └───────────────────────┘  └─────────────────────────────────────┘   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP REST (Session CRUD)
                                    │ SSE Stream (Live Node Updates)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        APPLICATION & API LAYER                         │
│                                                                        │
│   FastAPI (Asynchronous Python 3.11+)                                  │
│   ├── /api/research         [POST: Initialize, GET: List & Details]    │
│   ├── /api/research/{id}    [GET: Status, Sources, Report, Cancel]     │
│   └── /api/research/{id}/sse[GET: Real-Time Event Stream]              │
│                                                                        │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ Research Orchestrator & Execution Manager                      │   │
│   │ - Session Lifecycle Management                                 │   │
│   │ - LangGraph Thread & Checkpoint Handler                        │   │
│   │ - Event Dispatcher & Message Queue                             │   │
│   └───────────────────────────────┬────────────────────────────────┘   │
└───────────────────────────────────┼────────────────────────────────────┘
                                    │ Dispatches Typed Execution
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      LANGGRAPH ORCHESTRATION LAYER                     │
│                                                                        │
│   StateGraph[ResearchState]                                            │
│   ┌───────────────┐     ┌──────────────────┐     ┌─────────────────┐   │
│   │ Planner Node  │ ──> │ Researcher Node  │ ──> │  Analyzer Node  │   │
│   └───────────────┘     └─────────▲────────┘     └────────┬────────┘   │
│                                   │                       │            │
│                        NEEDS_MORE │                       ▼            │
│                         _RESEARCH └────────────── ┌─────────────────┐   │
│                                                   │ Validator Node  │   │
│                                                   └───────┬─────────┘   │
│                                                           │ VALID       │
│   ┌───────────────────────┐                               ▼            │
│   │  END State / Storage  │ ◄──────────────────── ┌─────────────────┐   │
│   └───────────────────────┘                       │ Report Node     │   │
│                                                   └─────────────────┘   │
└──────────────┬────────────────────────┬─────────────────────┬──────────┘
               │                        │                     │
               ▼                        ▼                     ▼
┌────────────────────────┐  ┌────────────────────────┐  ┌────────────────┐
│   LLM Service Layer    │  │  Tooling / Search Layer│  │ Checkpointer   │
│  - OpenAI / Anthropic  │  │  - Tavily Search API   │  │  - Async Postgres│
│  - Structured Output   │  │  - Web Content Scraper │  │    Saver        │
│  - Temperature / Seeds │  │  - Document Parser     │  │  - State Snap  │
└────────────────────────┘  └────────────────────────┘  └────────────────┘
               │                        │                     │
               └───────────────────┬────┴─────────────────────┘
                                   │ Persistence & Vector Store
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        DATA PERSISTENCE LAYER                          │
│                                                                        │
│   PostgreSQL 16 + pgvector                                             │
│   ├── research_sessions      (Session metadata, user query, status)    │
│   ├── research_subtasks      (Planned milestones & execution status)   │
│   ├── research_sources       (Discovered URLs, extracts, relevance)    │
│   ├── research_reports       (Synthesized markdown, executive summary) │
│   ├── research_events        (Granular node audit log for replay)      │
│   ├── checkpoints            (LangGraph state binary & metadata)       │
│   └── research_embeddings    (pgvector chunks for document RAG)        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Key Subsystem Boundaries

### 4.1 Frontend Layer (`frontend/`)
- Pure client-side single page application built on Vite.
- React Router manages navigation across **Dashboard**, **New Research**, **Live Session Viewer**, and **History**.
- TanStack Query caches REST API responses and synchronizes session state.
- EventSource client hooks consume the `/api/research/{id}/sse` endpoint to trigger fine-grained reactive state updates without polling.
- Graph visualization renders the active node, completed path, retry cycles, and execution latencies using clean SVG nodes.

### 4.2 FastAPI Service Layer (`backend/app/api/`)
- Asynchronous ASGI service powered by Uvicorn.
- Exposes versioned REST endpoints (`/api/v1/research/...`) with strict Pydantic schemas for request validation and response serialization.
- Provides SSE streaming endpoints with heartbeat pings to maintain persistent connection health through firewalls and reverse proxies.
- Background task execution uses FastAPI background worker patterns or asynchronous task pools for workflow invocations.

### 4.3 Graph Workflow Layer (`backend/app/graph/` & `backend/app/nodes/`)
- Encapsulates LangGraph `StateGraph`.
- Receives a strongly-typed `ResearchState`.
- Implements stateless nodes that take state in and return state updates.
- Uses conditional routing functions that evaluate state fields (`validation_result.status`, `retry_count`) to return the next node string.

### 4.4 Tool Infrastructure (`backend/app/tools/`)
- Encapsulates network communication with external search APIs and webpage scrapers.
- Implements fallback mechanisms (e.g. rate limit retries, timeout cutoffs, malformed HTML parsing protection).
- Formats external raw outputs into standardized `CollectedSource` records.

### 4.5 Persistence Layer (`backend/app/database/` & `backend/app/models/`)
- SQLAlchemy 2.0 (asyncio) + Alembic migrations.
- Stores operational session entities and analytical events.
- Houses LangGraph's checkpoint tables (`checkpoints`, `checkpoint_blobs`, `checkpoint_writes`) allowing workflows to be paused, resumed, or inspected at any historical step.
