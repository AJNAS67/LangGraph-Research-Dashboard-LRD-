# Comprehensive Implementation Plan: LangGraph Research Dashboard (LRD)

**Document Version**: 1.0.0  
**Author**: Senior Software Architect & Lead AI Engineer  
**Target Repository**: `langgraph-research-dashboard`  
**Scope**: End-to-End Implementation Blueprint for Phases 1 through 11  

---

## 1. Plan Overview & Engineering Philosophy

This document provides the definitive, granular engineering execution plan for building the **LangGraph Research Dashboard (LRD)**. Every phase is treated as an atomic, testable, and independently verifiable milestone. 

No phase may be started before the preceding phase is verified, tested, and approved.

### Core Implementation Principles
1. **Incremental Completeness**: Each phase produces working, executed, and covered code. No stubs without implementations.
2. **Deterministic Graph Mechanics**: Strict separation between the deterministic graph orchestration (LangGraph) and external non-deterministic I/O (LLMs, Search APIs, Web Scraping).
3. **Resilient Circuit Breakers**: Every loopback in the graph is strictly bounded by state counters to prevent runaway cost or infinite loops.
4. **Strong Typing Everywhere**: Pydantic v2 schemas for all backend models; TypeScript interfaces mirroring backend contracts for frontend components.
5. **Clean Dependency Isolation**: External vendors (OpenAI, Anthropic, Tavily) sit behind abstract interfaces to prevent vendor lock-in and simplify testing.

---

## 2. Phase-by-Phase Detailed Implementation Blueprint

---

### PHASE 1 — LangGraph Foundation (Core State Machine)

#### 1.1 Objective
Construct the core linear LangGraph workflow with deterministic execution flow:
`START -> Planner -> Researcher (Mocked) -> Analyzer -> Report Generator -> END`
Establish strongly typed state, Pydantic structured outputs, and unit test coverage.

#### 1.2 Architecture
```
[START] 
   │
   ▼
[Planner Node] ────────► Extracts objective, decomposes into 2-4 subtasks with search queries
   │
   ▼
[Researcher Node] ─────► Executes queries against MockSearchAdapter; normalizes sources
   │
   ▼
[Analyzer Node] ───────► Synthesizes notes, clusters agreements and contradictions
   │
   ▼
[Report Node] ─────────► Synthesizes structured final report in Markdown
   │
   ▼
 [END]
```

#### 1.3 Step-by-Step Task Breakdown
- **Task 1.1 (Environment & Dependencies)**: Create `backend/requirements.txt` (`langgraph`, `langchain`, `langchain-openai`, `pydantic>=2.7`, `pytest`, `pytest-asyncio`, `python-dotenv`). Set up Python virtual environment.
- **Task 1.2 (Configuration Module)**: Implement `backend/app/config/settings.py` using `pydantic-settings` to safely load environment variables with validation.
- **Task 1.3 (State Schema Definition)**: Implement `backend/app/schemas/state.py` defining `ResearchState` (`TypedDict`), `Subtask`, `CollectedSource`, `AnalysisResult`, and `FinalReport`.
- **Task 1.4 (LLM Provider Interface)**: Implement `backend/app/services/llm.py` with factory function `get_llm()` returning a configured `BaseChatModel` supporting structured outputs.
- **Task 1.5 (Mock Search Tool)**: Implement `backend/app/tools/search_interface.py` and `backend/app/tools/mock_search.py` returning deterministic, topical search extracts.
- **Task 1.6 (Planner Node)**: Implement `backend/app/nodes/planner.py` using structured output prompt.
- **Task 1.7 (Researcher Node)**: Implement `backend/app/nodes/researcher.py` reading subtasks and generating sources via search adapter.
- **Task 1.8 (Analyzer Node)**: Implement `backend/app/nodes/analyzer.py` synthesizing findings and contradictions.
- **Task 1.9 (Report Generator Node)**: Implement `backend/app/nodes/report_generator.py` formatting the complete report.
- **Task 1.10 (Graph Assembly)**: Implement `backend/app/graph/builder.py` assembling the `StateGraph`, adding nodes, linear edges, and compiling the runnable graph.
- **Task 1.11 (Test Suite)**: Create unit tests for nodes (`tests/unit/test_nodes.py`) and workflow integration tests (`tests/graph/test_foundation_graph.py`).

#### 1.4 Files to Create
```
backend/requirements.txt
backend/app/config/settings.py
backend/app/schemas/state.py
backend/app/schemas/research.py
backend/app/services/llm.py
backend/app/tools/search_interface.py
backend/app/tools/mock_search.py
backend/app/nodes/planner.py
backend/app/nodes/researcher.py
backend/app/nodes/analyzer.py
backend/app/nodes/report_generator.py
backend/app/graph/builder.py
backend/tests/conftest.py
backend/tests/unit/test_state.py
backend/tests/unit/test_nodes.py
backend/tests/graph/test_foundation_graph.py
```

#### 1.5 Verification Criteria
- `pytest backend/tests` passes with 100% green tests.
- Graph successfully takes `"Research impact of AI in 2026"` and outputs a valid `FinalReport` containing executive summary, methodology, findings, and citations.
- State properly accumulates without mutation errors.

---

### PHASE 2 — Real Web Research & Source Collection

#### 2.1 Objective
Replace the mock search provider with live web intelligence retrieval using **Tavily Search API**. Implement URL deduplication, content snippet extraction, source metadata normalization, and resilient error recovery.

#### 2.2 Architecture
```
[Researcher Node]
       │
       ├─► Check State: Has URL already been processed? (Deduplication)
       ├─► Call TavilySearchAdapter (async HTTP client with rate-limiting backoff)
       ├─► Parse organic results: Title, URL, Content, Score, Published Date
       └─► Return new sources and atomic research notes via operator.add reducer
```

#### 2.3 Step-by-Step Task Breakdown
- **Task 2.1 (Tavily Adapter Implementation)**: Implement `backend/app/tools/tavily_search.py` implementing `SearchToolInterface`.
- **Task 2.2 (Tool Factory & DI)**: Implement `backend/app/tools/factory.py` to seamlessly toggle between `tavily` and `mock` based on `SEARCH_PROVIDER` env variable.
- **Task 2.3 (URL Normalization & Deduplication)**: Implement helper `normalize_url()` and in-state deduplication to prevent duplicate API hits.
- **Task 2.4 (Content Scraping & Sanitization)**: Add optional web page text extraction with HTML sanitization (stripping `<script>`, CSS, and tracking tags).
- **Task 2.5 (Network Resilience & Backoff)**: Wrap Tavily calls with retry logic using `tenacity` for HTTP 429 (Rate Limit) and HTTP 5xx errors.
- **Task 2.6 (Update Researcher Node)**: Update `backend/app/nodes/researcher.py` to use the tool factory and handle empty or failed search results gracefully.
- **Task 2.7 (Integration Tests)**: Implement `tests/unit/test_tavily_adapter.py` (with `pytest-mock` and VCR/recorded responses) and live integration tests.

#### 2.4 Files to Create / Modify
```
backend/app/tools/tavily_search.py           [CREATE]
backend/app/tools/scraper.py                 [CREATE]
backend/app/tools/factory.py                 [CREATE]
backend/app/nodes/researcher.py              [MODIFY - live tool injection]
backend/tests/unit/test_tavily_adapter.py    [CREATE]
backend/tests/unit/test_deduplication.py     [CREATE]
```

#### 2.5 Verification Criteria
- Queries execute live searches via Tavily (or mocked responses in CI).
- URLs are normalized; duplicate queries within the same session are skipped.
- Failed search queries do not crash the pipeline; fallback notes are appended to `errors`.

---

### PHASE 3 — Conditional Agent & Validation Loops

#### 3.1 Objective
Introduce the **Validator Node** and **Conditional Routing**. Transform the linear workflow into a self-critiquing agent that evaluates evidence sufficiency and loops back to the Researcher when information is incomplete or contradictory, bounded by a hard retry cap (`max_retries`).

#### 3.2 Architecture
```
                  ┌────────────────────────────────────────┐
                  ▼                                        │
[START] ──► [Planner] ──► [Researcher] ──► [Analyzer] ──► [Validator]
                                                               │
                                       ┌───────────────────────┴───────────────────────┐
                                       │ Needs more info & retry_count < max_retries   │ Evidence sufficient OR
                                       ▼                                               │ retry_count >= max_retries
                                [Loop Back to Researcher]                              ▼
                                                                                 [Report Generator] ──► [END]
```

#### 3.3 Step-by-Step Task Breakdown
- **Task 3.1 (Validation Schema)**: Extend `ValidationResult` in `backend/app/schemas/research.py` to capture `needs_more_research: bool`, `reason: str`, `missing_aspects: List[str]`, and `suggested_queries: List[str]`.
- **Task 3.2 (Validator Node Implementation)**: Implement `backend/app/nodes/validator.py`. Prompts LLM to evaluate whether user query requirements are satisfied and detect unresolved contradictions.
- **Task 3.3 (Conditional Routing Logic)**: Implement `backend/app/graph/routing.py` with `should_continue_research(state: ResearchState) -> str`.
- **Task 3.4 (Loopback Query Handling in Researcher)**: Update `Researcher` node to prioritize `suggested_queries` from the validator during loopback iterations.
- **Task 3.5 (Circuit Breaker & Counter Guard)**: Enforce incrementation of `retry_count` in state. If `retry_count >= max_retries`, route to `report_generator` even if `needs_more_research` is True, documenting shortcomings in report limitations.
- **Task 3.6 (Update Graph Builder)**: Register `validator` node and `add_conditional_edges("validator", should_continue_research, ...)` in `backend/app/graph/builder.py`.
- **Task 3.7 (Comprehensive Graph Tests)**:
  - Test Case 1: First-pass sufficiency (`VALID -> Report Generator`).
  - Test Case 2: Successful loopback (`NEEDS_MORE_RESEARCH -> Researcher -> Analyzer -> Validator -> VALID -> Report Generator`).
  - Test Case 3: Infinite loop circuit breaker (`NEEDS_MORE_RESEARCH` triggers max retries -> forced `Report Generator`).

#### 3.4 Files to Create / Modify
```
backend/app/nodes/validator.py               [CREATE]
backend/app/graph/routing.py                 [CREATE]
backend/app/graph/builder.py                 [MODIFY - register validator and conditional edge]
backend/app/nodes/researcher.py              [MODIFY - support validator refinement queries]
backend/tests/graph/test_conditional_graph.py[CREATE]
```

#### 3.5 Verification Criteria
- Graph dynamically branches based on validation output.
- Circuit breaker tests verify graph NEVER exceeds `max_retries` (guaranteed loop termination).
- Accumulated citations across multiple research loops are preserved using `operator.add`.

---

### PHASE 4 — FastAPI Backend & REST API Layer

#### 4.1 Objective
Expose the LangGraph research engine via a production-grade asynchronous FastAPI service with OpenAPI 3.1 documentation, request validation, background worker execution, and status polling endpoints.

#### 4.2 Architecture
```
[Client (HTTP)] 
      │
      ▼
[FastAPI Router: /api/v1/research]
      │
      ├─► POST   /              --> Validate payload, spawn background task, return 201 Created
      ├─► GET    /              --> Return paginated sessions list
      ├─► GET    /{id}          --> Return detailed session state & subtasks
      ├─► GET    /{id}/status   --> Fast lightweight node & progress status
      ├─► GET    /{id}/sources  --> List discovered sources and metadata
      ├─► GET    /{id}/report   --> Retrieve finalized markdown report
      └─► POST   /{id}/cancel   --> Signal cancellation token
```

#### 4.3 Step-by-Step Task Breakdown
- **Task 4.1 (FastAPI Application Setup)**: Implement `backend/app/main.py` with CORS middleware, lifespan events, exception handlers, and API router mounting.
- **Task 4.2 (API Request/Response Schemas)**: Implement `backend/app/schemas/api.py` (`CreateResearchRequest`, `ResearchResponse`, `SessionStatusResponse`, `SourceListResponse`, `ReportResponse`).
- **Task 4.3 (Execution Service & Task Registry)**: Implement `backend/app/services/research_service.py` to manage running graph executions, track thread state, and provide async background scheduling.
- **Task 4.4 (REST Routes Implementation)**:
  - `backend/app/api/v1/research.py`: Endpoints for CRUD, status, sources, report, and cancellation.
- **Task 4.5 (RFC 7807 Exception Handlers)**: Implement standard problem details error response handler in `backend/app/api/errors.py`.
- **Task 4.6 (API Test Suite)**: Implement `backend/tests/api/test_research_api.py` using `httpx.AsyncClient` testing input validation, lifecycle status changes, and 404/400 error codes.

#### 4.4 Files to Create / Modify
```
backend/app/main.py                          [CREATE]
backend/app/api/__init__.py                  [MODIFY]
backend/app/api/v1/__init__.py               [CREATE]
backend/app/api/v1/research.py               [CREATE]
backend/app/api/errors.py                    [CREATE]
backend/app/schemas/api.py                   [CREATE]
backend/app/services/research_service.py     [CREATE]
backend/tests/api/test_research_api.py       [CREATE]
```

#### 4.5 Verification Criteria
- `uvicorn app.main:app` boots cleanly with OpenAPI docs at `/docs`.
- `POST /api/v1/research` returns `201 Created` with unique session UUID.
- Querying `/api/v1/research/{id}/status` reflects progress through `planner -> researcher -> analyzer -> validator -> report_generator -> completed`.
- `GET /api/v1/research/{id}/report` returns formatted report on completion.

---

### PHASE 5 — PostgreSQL Persistence & Alembic Migrations

#### 5.1 Objective
Introduce enterprise relational persistence using **PostgreSQL 16**, **SQLAlchemy 2.0 (asyncio)**, and **Alembic**. Persist sessions, subtasks, web sources, reports, and execution events.

#### 5.2 Architecture
```
[FastAPI Service / Graph Nodes]
               │
               ▼ (Async SQLAlchemy 2.0 Engine via asyncpg)
┌────────────────────────────────────────────────────────┐
│                   PostgreSQL 16                        │
│  - research_sessions (UUID PK, query, depth, status)   │
│  - research_subtasks (FK to session, order, queries)   │
│  - research_sources  (FK to session, url, extracts)    │
│  - research_reports  (FK to session, raw markdown)     │
│  - research_events   (FK to session, audit logs)       │
└────────────────────────────────────────────────────────┘
```

#### 5.3 Step-by-Step Task Breakdown
- **Task 5.1 (Database Engine & Async Session)**: Implement `backend/app/database/session.py` with `create_async_engine` and `async_sessionmaker`.
- **Task 5.2 (Declarative Models)**: Implement SQLAlchemy models in `backend/app/models/`:
  - `session.py`: `ResearchSessionModel`
  - `subtask.py`: `ResearchSubtaskModel`
  - `source.py`: `ResearchSourceModel`
  - `report.py`: `ResearchReportModel`
  - `event.py`: `ResearchEventModel`
- **Task 5.3 (Alembic Configuration)**: Set up Alembic with `backend/alembic/env.py` configured for asynchronous migrations. Generate initial migration `001_initial_schema.py`.
- **Task 5.4 (Repository Layer)**: Implement database access repositories in `backend/app/database/repository.py` for atomic CRUD operations.
- **Task 5.5 (Service Integration)**: Connect `research_service.py` with database repositories so all session updates, discovered sources, and generated reports persist to Postgres.
- **Task 5.6 (Database Integration Tests)**: Implement `backend/tests/database/test_persistence.py` with test container or test database.

#### 5.4 Files to Create / Modify
```
backend/alembic.ini                          [CREATE]
backend/alembic/env.py                       [CREATE]
backend/alembic/versions/001_initial.py      [CREATE]
backend/app/database/session.py              [CREATE]
backend/app/database/repository.py           [CREATE]
backend/app/models/__init__.py               [MODIFY]
backend/app/models/session.py                [CREATE]
backend/app/models/subtask.py                [CREATE]
backend/app/models/source.py                 [CREATE]
backend/app/models/report.py                 [CREATE]
backend/app/models/event.py                  [CREATE]
backend/app/services/research_service.py     [MODIFY - add DB persistence]
backend/tests/database/test_persistence.py   [CREATE]
```

#### 5.5 Verification Criteria
- `alembic upgrade head` applies cleanly against PostgreSQL.
- Sessions, subtasks, sources, and reports survive server restarts and persist reliably in Postgres.
- Queries for `/api/v1/research` retrieve historical sessions with accurate counts.

---

### PHASE 6 — React Dashboard & Frontend Visualization

#### 6.1 Objective
Construct the modern React 18 + TypeScript + Vite + Tailwind CSS dashboard. Implement the complete user interface: Dashboard overview, New Research modal/form, interactive SVG Workflow Visualizer, Source Explorer, and Markdown Report Viewer.

#### 6.2 Architecture
```
[React SPA Root]
   ├── [Navigation Bar / Header] (Brand, Status, Mode)
   ├── [Dashboard View] (Metrics, Recent Sessions list, Launch CTA)
   ├── [New Research Flow] (Form with validation, depth picker, submit)
   └── [Session Details View]
         ├── [Session Header & Status Badges]
         ├── [Interactive SVG Workflow Visualizer] (Live node status, loop indicators)
         └── [Tabbed Workspace]
               ├── Tab 1: Research Plan (Subtasks list with status icons)
               ├── Tab 2: Sources Explorer (Grid/cards with relevance, URL, extracts)
               └── Tab 3: Final Report (Markdown renderer, copy, download)
```

#### 6.3 Step-by-Step Task Breakdown
- **Task 6.1 (Vite & TypeScript Scaffolding)**: Initialize `frontend/package.json`, `vite.config.ts`, `tsconfig.json`, Tailwind CSS configuration, and PostCSS.
- **Task 6.2 (Design Tokens & Global CSS)**: Configure `frontend/src/index.css` with dark/light variables, Inter font, custom scrollbars, and animations.
- **Task 6.3 (TypeScript API Interfaces)**: Implement `frontend/src/types/research.ts` mirroring backend schemas.
- **Task 6.4 (API Client & TanStack Query)**: Implement `frontend/src/services/api.ts` with Axios client and query hooks in `frontend/src/hooks/useResearch.ts`.
- **Task 6.5 (Reusable UI Component Library)**:
  - Button, Input, Select, Badge, Card, Modal, Tabs, Skeleton loader, Tooltip.
- **Task 6.6 (Interactive Graph Visualizer Component)**:
  - Implement `frontend/src/features/workflow/GraphVisualizer.tsx`: Clean SVG rendering showing nodes (`Planner`, `Researcher`, `Analyzer`, `Validator`, `Report`), directional arrows, pulsing active glow, and conditional loopback arrow.
- **Task 6.7 (Source Explorer Component)**:
  - Implement `frontend/src/features/sources/SourceList.tsx`: Filterable card list with relevance scores, source type tags, domain favicons, and extracts.
- **Task 6.8 (Report Viewer Component)**:
  - Implement `frontend/src/features/report/ReportViewer.tsx`: Render report using `react-markdown` with syntax highlighting and export to Markdown/PDF.
- **Task 6.9 (Pages Assembly & Routing)**:
  - `pages/Dashboard.tsx`, `pages/NewResearch.tsx`, `pages/SessionView.tsx`, `pages/History.tsx`.
- **Task 6.10 (Component Tests)**: Implement Vitest tests for components and form validation.

#### 6.4 Files to Create
```
frontend/package.json
frontend/vite.config.ts
frontend/tailwind.config.js
frontend/postcss.config.js
frontend/src/index.css
frontend/src/main.tsx
frontend/src/App.tsx
frontend/src/types/research.ts
frontend/src/services/api.ts
frontend/src/hooks/useResearch.ts
frontend/src/components/ui/Button.tsx
frontend/src/components/ui/Badge.tsx
frontend/src/components/ui/Card.tsx
frontend/src/components/ui/Tabs.tsx
frontend/src/features/workflow/GraphVisualizer.tsx
frontend/src/features/sources/SourceList.tsx
frontend/src/features/report/ReportViewer.tsx
frontend/src/pages/Dashboard.tsx
frontend/src/pages/SessionView.tsx
frontend/src/pages/History.tsx
frontend/src/tests/GraphVisualizer.test.tsx
```

#### 6.5 Verification Criteria
- `npm run build` succeeds without TypeScript or ESLint errors.
- Browser test: Submitting a research query transitions to session viewer.
- The SVG workflow updates to show the active node and completed nodes.
- Discovered sources and markdown reports render cleanly with responsive layout.

---

### PHASE 7 — Real-Time Streaming & Live Workflow Updates

#### 7.1 Objective
Implement real-time workflow event streaming from LangGraph to the React dashboard using **Server-Sent Events (SSE)**. Replace client polling with push notifications for node transitions, subtask completions, discovered sources, and validation critiques.

#### 7.2 Architecture
```
[LangGraph execution: astream_events()]
         │
         ▼
[Research Event Queue] 
         │
         ▼
[FastAPI Route: GET /api/v1/research/{id}/events] (text/event-stream)
         │
         ▼ (SSE Stream over HTTP)
[React Hook: useResearchStream()] ──► Instantly updates React Query cache & UI Graph state
```

#### 7.3 Step-by-Step Task Breakdown
- **Task 7.1 (Graph Event Stream Adapter)**: Implement generator in `backend/app/graph/streaming.py` that listens to LangGraph `graph.astream_events(version="v2")` and normalizes events (`node_start`, `node_complete`, `source_added`, `validation_decision`).
- **Task 7.2 (SSE FastAPI Route)**: Implement `GET /api/v1/research/{id}/events` using `starlette.responses.StreamingResponse` with heartbeat pings every 15s to keep connections alive.
- **Task 7.3 (Frontend SSE Hook)**: Implement `frontend/src/hooks/useResearchStream.ts` utilizing the browser native `EventSource` with auto-reconnection logic.
- **Task 7.4 (Live Visualizer Animation)**: Bind `useResearchStream` events to `GraphVisualizer.tsx` to animate active nodes, transition lines, and loopbacks in real time.
- **Task 7.5 (Live Citation Feed)**: Animate new sources sliding into the Source Explorer as they are discovered.
- **Task 7.6 (Streaming Tests)**: Test SSE endpoint disconnect handling and event formatting with `pytest`.

#### 7.4 Files to Create / Modify
```
backend/app/graph/streaming.py               [CREATE]
backend/app/api/v1/research.py               [MODIFY - add SSE endpoint]
frontend/src/hooks/useResearchStream.ts      [CREATE]
frontend/src/features/workflow/GraphVisualizer.tsx [MODIFY - add stream animations]
frontend/src/features/sources/LiveSourceFeed.tsx   [CREATE]
backend/tests/api/test_streaming.py          [CREATE]
```

#### 7.5 Verification Criteria
- SSE connection opens immediately on research creation.
- Frontend graph node glows and animates when the backend enters that node.
- Live sources appear on screen without manual page refreshes.

---

### PHASE 8 — Checkpointing, Recovery & State Persistence

#### 8.1 Objective
Integrate LangGraph's native checkpointer (`AsyncPostgresSaver`) to persist the exact binary state of the graph after every node execution. Enable workflow pauses, server crash recovery, state inspection, and time-travel replay.

#### 8.2 Architecture
```
[LangGraph Node Execution]
         │
         ▼
[AsyncPostgresSaver] 
         │
         ▼
[PostgreSQL Checkpoint Tables: checkpoints, checkpoint_blobs, checkpoint_writes]
         │
         ├─► Allows resuming workflow after server crash or planned restart
         └─► Enables inspecting exact state snapshots at any historical step
```

#### 8.3 Step-by-Step Task Breakdown
- **Task 8.1 (Checkpoint DB Setup)**: Configure LangGraph's `AsyncPostgresSaver` connection pool pointing to `LANGGRAPH_CHECKPOINT_DATABASE_URL`. Initialize checkpoint tables.
- **Task 8.2 (Checkpointer Injection into Graph)**: Update `backend/app/graph/builder.py` to compile graphs with `checkpointer=async_postgres_saver`.
- **Task 8.3 (Session Recovery Service)**: Implement `resume_research_session(session_id: str)` to pick up interrupted sessions from their last checkpointed state.
- **Task 8.4 (Checkpoint Inspection API)**: Implement `GET /api/v1/research/{id}/history` to return state snapshots at each node for auditability.
- **Task 8.5 (Recovery Tests)**: Create automated test simulating process interruption mid-workflow, verifying execution continues from the saved checkpoint to report completion.

#### 8.4 Files to Create / Modify
```
backend/app/database/checkpointer.py         [CREATE]
backend/app/graph/builder.py                 [MODIFY - attach checkpointer]
backend/app/services/recovery_service.py     [CREATE]
backend/app/api/v1/research.py               [MODIFY - add history inspection endpoint]
backend/tests/graph/test_checkpointing.py    [CREATE]
```

#### 8.5 Verification Criteria
- Checkpoints table in PostgreSQL populated after each node step.
- Simulating worker restart successfully resumes workflow from last saved checkpoint without starting over from `Planner`.

---

### PHASE 9 — RAG Integration & Document-Aware Research

#### 9.1 Objective
Enhance research capabilities with Document-Aware RAG. Allow users to upload PDFs or documents alongside their query, chunk and embed them into PostgreSQL via **pgvector**, and synthesize both web and local document sources in the final report.

#### 9.2 Architecture
```
[User Uploads PDF] ──► [Document Ingestion Service]
                                │
                                ├─► PyPDF / pdfplumber text extraction
                                ├─► RecursiveCharacterTextSplitter (chunk_size=1000, overlap=150)
                                ├─► Embedding Generation (OpenAI text-embedding-3-small)
                                └─► Store in PostgreSQL table `document_embeddings` with pgvector
                                           │
[Researcher Node] ─────────────────────────┴──► Hybrid Retrieval: Web Search + pgvector similarity
```

#### 9.3 Step-by-Step Task Breakdown
- **Task 9.1 (pgvector Extension & Schema)**: Add Alembic migration creating `research_documents` and `document_embeddings` tables with `vector(1536)` and HNSW cosine distance index.
- **Task 9.2 (Document Ingestion Service)**: Implement `backend/app/services/document_service.py` to extract text from PDFs, split into chunks, and compute embeddings.
- **Task 9.3 (Document Retriever Tool)**: Implement `backend/app/tools/document_retriever.py` to query pgvector via cosine similarity.
- **Task 9.4 (Hybrid Researcher Node)**: Update `Researcher` node to query both Tavily Web Search and local Document Retriever, attributing sources as `"document"` vs `"web"`.
- **Task 9.5 (Document Upload API & UI)**: Implement `POST /api/v1/research/{id}/documents` and file dropzone in the New Research form.
- **Task 9.6 (RAG Tests)**: Unit and integration tests for document chunking, embedding generation, and hybrid retrieval.

#### 9.4 Files to Create / Modify
```
backend/alembic/versions/002_add_pgvector_rag.py [CREATE]
backend/app/models/document.py               [CREATE]
backend/app/services/document_service.py     [CREATE]
backend/app/tools/document_retriever.py      [CREATE]
backend/app/nodes/researcher.py              [MODIFY - hybrid retrieval]
frontend/src/components/ui/Dropzone.tsx      [CREATE]
backend/tests/unit/test_rag.py               [CREATE]
```

#### 9.5 Verification Criteria
- PDF document parsed and stored in pgvector.
- Generated final report specifically cites uploaded documents with page numbers alongside web citations.

---

### PHASE 10 — Human-in-the-Loop (HITL) & Interactive Plan Approval

#### 10.1 Objective
Introduce interactive human oversight. After the `Planner` generates subtasks and search queries, pause execution using LangGraph's `interrupt()` mechanism, allowing the user to approve, modify, add, or reject subtasks before costly research operations occur.

#### 10.2 Architecture
```
[START] ──► [Planner Node] 
                 │
                 ▼
      [Human Review Interruption] ◄── Workflow PAUSES; State Checkpointed
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
[User Approves]      [User Edits Plan]
      │                     │
      └──────────┬──────────┘
                 ▼
        [Resume Workflow] ──► [Researcher Node] ──► ...
```

#### 10.3 Step-by-Step Task Breakdown
- **Task 10.1 (LangGraph Interrupt Hook)**: Configure graph interruption after `planner` node using LangGraph `interrupt()` or `interrupt_before=["researcher"]`.
- **Task 10.2 (Approval API Endpoints)**: Implement `POST /api/v1/research/{id}/approve` (accept current plan) and `POST /api/v1/research/{id}/plan` (update subtasks and resume).
- **Task 10.3 (Frontend Plan Approval UI)**: Implement interactive modal in the frontend displaying the generated subtasks, allowing inline editing, adding/deleting subtasks, and an "Approve & Run" action button.
- **Task 10.4 (Workflow Resumption Logic)**: Update `research_service.py` to command LangGraph to resume thread execution with updated state.
- **Task 10.5 (HITL Tests)**: Automated tests verifying workflow pauses at the gate, rejects unauthorized continuation, and successfully runs with human-modified subtasks.

#### 10.4 Files to Create / Modify
```
backend/app/graph/builder.py                 [MODIFY - add interruption config]
backend/app/api/v1/research.py               [MODIFY - add approval routes]
backend/app/services/research_service.py     [MODIFY - handle resume commands]
frontend/src/features/workflow/PlanApprovalModal.tsx [CREATE]
backend/tests/graph/test_hitl.py             [CREATE]
```

#### 10.5 Verification Criteria
- Research pauses after planning; status indicates `awaiting_approval`.
- User can delete a subtask in the UI and click "Approve".
- Execution resumes with the modified subtasks, bypassing deleted queries.

---

### PHASE 11 — Production Hardening, Security & Operations

#### 11.1 Objective
Prepare the platform for enterprise production deployment. Implement JWT authentication, rate limiting, structured logging, Prometheus observability metrics, multi-stage Docker builds, and CI/CD pipelines.

#### 11.2 Architecture
```
[Client] ──► [Nginx / Cloudflare (SSL, DDoS, Security Headers)]
                 │
                 ▼
     [FastAPI Application Gateway]
         ├── JWT Authentication & API Key verification
         ├── Redis Rate Limiting (Token Bucket)
         ├── Prometheus /metrics exporter
         └── Structured JSON Logger (Logfire / Structlog)
```

#### 11.3 Step-by-Step Task Breakdown
- **Task 11.1 (Security Middleware & Auth)**: Add API Key or JWT Bearer authentication to protect research endpoints. Add CORS domain restrictions and security headers (`HSTS`, `X-Content-Type-Options`).
- **Task 11.2 (Rate Limiting)**: Implement token-bucket rate limiter via `slowapi` or Redis to protect search APIs from exhaustion.
- **Task 11.3 (Structured Logging)**: Configure `structlog` for JSON logs with `session_id`, `trace_id`, and duration metrics.
- **Task 11.4 (Observability & Metrics)**: Expose `/metrics` endpoint with Prometheus counters for workflow runtimes, token usage, tool latencies, and error rates.
- **Task 11.5 (Production Docker Configuration)**: Multi-stage Dockerfiles for backend (Python slim) and frontend (Nginx alpine). Production `docker-compose.prod.yml`.
- **Task 11.6 (CI/CD Pipeline)**: GitHub Actions workflow (`.github/workflows/ci.yml`) running linting (`ruff`, `eslint`), unit tests, and Docker builds on every pull request.

#### 11.4 Files to Create / Modify
```
backend/app/api/middleware/auth.py           [CREATE]
backend/app/api/middleware/rate_limit.py     [CREATE]
backend/app/config/logging.py                [CREATE]
backend/Dockerfile                           [CREATE]
frontend/Dockerfile                          [CREATE]
docker-compose.prod.yml                      [CREATE]
.github/workflows/ci.yml                     [CREATE]
```

#### 11.5 Verification Criteria
- `docker compose -f docker-compose.prod.yml up` starts the complete production environment cleanly.
- Rate limiting returns `429 Too Many Requests` when limits are exceeded.
- GitHub Actions CI builds and passes all tests automatically.

---

## 3. Master Phase Progression Checklist

| Phase | Description | Prerequisite | Verification Gate |
|---|---|---|---|
| **Phase 0** | **Product & Architecture Planning** | None | Architecture docs, ADRs, Scaffolding verified |
| **Phase 1** | **LangGraph Foundation** | Phase 0 Approved | Linear graph unit tests pass 100% |
| **Phase 2** | **Real Web Research** | Phase 1 Verified | Live Tavily search integration tested |
| **Phase 3** | **Conditional Agent** | Phase 2 Verified | Validator loopback & circuit breaker tests pass |
| **Phase 4** | **FastAPI Backend** | Phase 3 Verified | OpenAPI endpoints & background runner tested |
| **Phase 5** | **PostgreSQL Persistence** | Phase 4 Verified | Alembic migrations & DB persistence tested |
| **Phase 6** | **React Dashboard** | Phase 5 Verified | UI components & visualizer tested in browser |
| **Phase 7** | **Real-Time Streaming** | Phase 6 Verified | Live SSE stream tested with UI updates |
| **Phase 8** | **Checkpointing & Memory** | Phase 7 Verified | State recovery & crash resumption tested |
| **Phase 9** | **RAG Integration** | Phase 8 Verified | pgvector semantic retrieval & PDF search tested |
| **Phase 10** | **Human-in-the-Loop** | Phase 9 Verified | `interrupt()` and plan approval modal tested |
| **Phase 11** | **Production Hardening** | Phase 10 Verified | Docker production build, auth & CI/CD tested |

---

## 4. Immediate Next Step

We are currently at the conclusion of **Phase 0**. All architectural specifications, database designs, ADRs, roadmap milestones, and this comprehensive implementation plan are complete.

**Next Action**: Waiting for explicit approval to begin **Phase 1: LangGraph Foundation**.
