# Development Roadmap & Phase Plan

The LangGraph Research Dashboard is developed systematically across 12 distinct phases (Phase 0 through Phase 11). Each phase delivers an independently testable, verified milestone.

---

## Roadmap Overview

| Phase | Title | Focus Area | Key Deliverable | Status |
|---|---|---|---|---|
| **Phase 0** | **Product & Architecture Planning** | System Architecture & Design | Architecture specifications, ER diagrams, ADRs, Roadmap | **Completed** |
| **Phase 1** | **LangGraph Foundation** | Core Linear Graph & State | State schema, Planner, Researcher (mocked), Analyzer, Report node, tests | **Completed** |
| **Phase 2** | **Real Web Research** | Search Tool Integration | Tavily search tool, scraper, URL deduplication, real source extraction | **Pending** |
| **Phase 3** | **Conditional Agent** | Dynamic Critique & Looping | Validator node, conditional edge, retry limits, anti-infinite-loop gates | Pending |
| **Phase 4** | **FastAPI Backend** | Application API Layer | REST API endpoints, Pydantic schemas, background worker, unit tests | Pending |
| **Phase 5** | **PostgreSQL Persistence** | Relational DB & Migrations | SQLAlchemy 2.0 async models, Alembic migrations, session/source persistence | Pending |
| **Phase 6** | **React Dashboard** | Frontend User Experience | Dashboard, New Research, Graph Visualizer, Source Explorer, Report view | Pending |
| **Phase 7** | **Streaming** | Real-Time Workflow Visibility | SSE endpoint, live node transition events, animated UI graph progress | Pending |
| **Phase 8** | **Checkpointing & Memory** | LangGraph State Persistence | PostgresSaver checkpointer, thread resumption, session replay | Pending |
| **Phase 9** | **RAG Integration** | Document-Aware Research | PDF upload, chunking, pgvector embeddings, hybrid web + doc retrieval | Pending |
| **Phase 10** | **Human-in-the-Loop** | Interactive Plan Control | LangGraph `interrupt()`, plan review, modification, human approval flow | Pending |
| **Phase 11** | **Production Hardening** | Security, Ops & Reliability | Auth, rate limiting, structured logging, CI/CD, production Docker containers | Pending |

---

## Detailed Phase Breakdown

### Phase 0: Product & Architecture Planning (Current Phase)
- **Objective**: Establish complete technical blueprint, requirements, system architecture, database design, API specification, testing strategy, and project scaffolding.
- **Verification**: Complete documentation suite created, zero unapproved premature agent code.

### Phase 1: LangGraph Foundation
- **Objective**: Construct the fundamental `StateGraph` with strongly typed state, executing `START -> Planner -> Researcher (mocked) -> Analyzer -> Report Generator -> END`.
- **Key Concepts**: `TypedDict` state, Nodes as pure functions, Static Edges, LLM structured outputs via Pydantic.
- **Verification**: Pytest test suite asserting graph state transitions and final report generation using mock LLM responses.

### Phase 2: Real Web Research
- **Objective**: Implement clean `SearchToolInterface` and Tavily search provider. Replace mock sources with live web research.
- **Key Concepts**: Tool execution within nodes, source metadata normalization, relevance scoring, URL deduplication.
- **Verification**: Integration tests validating retrieval of real web URLs and source attribution.

### Phase 3: Conditional Agent
- **Objective**: Add `Validator` node and conditional routing (`should_continue_research`). Enable cyclical feedback loops.
- **Key Concepts**: Conditional edges, feedback loops, counter guards (`retry_count < max_retries`), gap extraction.
- **Verification**: Tests validating both the single-pass happy path (`VALID`) and the loopback path (`NEEDS_MORE_RESEARCH`), verifying hard termination at `max_retries`.

### Phase 4: FastAPI Backend
- **Objective**: Expose the LangGraph engine over clean REST endpoints using FastAPI.
- **Key Concepts**: Async endpoints, background task scheduling, Pydantic request/response schemas, OpenAPI 3.1 documentation.
- **Verification**: Pytest test client testing `POST /api/v1/research`, `GET /status`, `GET /sources`, `GET /report`.

### Phase 5: PostgreSQL Persistence
- **Objective**: Integrate PostgreSQL using async SQLAlchemy and Alembic. Store all sessions, subtasks, sources, and reports.
- **Key Concepts**: Relational modeling, async database sessions, foreign key cascading, query indexing.
- **Verification**: Database migration runs cleanly; full research lifecycle persists to PostgreSQL.

### Phase 6: React Dashboard
- **Objective**: Build the user interface with React, TypeScript, Tailwind CSS, and TanStack Query.
- **Key Concepts**: Modern design aesthetics, interactive SVG graph visualizer, research creation forms, tabbed sources/report views.
- **Verification**: Vitest component tests and browser verification of the research creation and viewing experience.

### Phase 7: Real-Time Streaming
- **Objective**: Stream live node events from LangGraph to the frontend using Server-Sent Events (SSE).
- **Key Concepts**: LangGraph event streaming (`astream_events`), SSE protocol, React `EventSource` custom hook.
- **Verification**: Frontend visually reflects active node transitions and incoming source discoveries in real time.

### Phase 8: Checkpointing & State Recovery
- **Objective**: Integrate LangGraph `PostgresSaver` checkpointer for state persistence and workflow recovery.
- **Key Concepts**: Thread IDs, checkpoints, time-travel inspection, resuming interrupted or failed sessions.
- **Verification**: Ability to pause a workflow, restart backend, and resume execution without data loss.

### Phase 9: RAG (Retrieval-Augmented Generation)
- **Objective**: Support document-aware research by ingesting PDFs into pgvector.
- **Key Concepts**: Document chunking, vector embeddings, cosine distance similarity search, combining web + document sources.
- **Verification**: Semantic retrieval tests verifying uploaded documents are cited in the final report.

### Phase 10: Human-in-the-Loop (HITL)
- **Objective**: Introduce human review before executing expensive research subtasks.
- **Key Concepts**: LangGraph `interrupt()`, human-assisted state editing, workflow resumption.
- **Verification**: User can review the generated plan, edit subtasks, and approve execution before search starts.

### Phase 11: Production Hardening
- **Objective**: Enterprise production readiness.
- **Key Concepts**: API authentication, Redis rate limiting, Prometheus metrics, structured JSON logging, multi-stage Docker builds.
- **Verification**: Security scans, load testing, automated CI/CD pipeline runs.
