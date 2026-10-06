# Architecture Decision Records (ADRs)

This document records the architectural choices, problem context, alternatives evaluated, and rationale for every major technical component in the **LangGraph Research Dashboard (LRD)**.

---

## ADR 001: LangGraph as the AI Workflow Engine

### Context
Autonomous research requires cyclical reasoning: planning, executing searches, analyzing results, critiquing evidence sufficiency, and potentially looping back to research missing angles. Standard LLM chains (e.g., standard LangChain `SequentialChain` or basic OpenAI function calling) assume linear execution and struggle with multi-step cycles, state persistence, and fine-grained control flow.

### Decision
Adopt **LangGraph** (`langgraph`) as the foundational workflow orchestration framework.

### Alternatives Considered
1. **Plain Sequential LLM Prompt Chains**:
   - *Pros*: Simple to implement.
   - *Cons*: Cannot handle loops, conditional retries, validation feedback, or state resumption. Degrades into messy imperative spaghetti code.
2. **CrewAI / AutoGen Multi-Agent Frameworks**:
   - *Pros*: High-level abstractions for multi-agent conversations.
   - *Cons*: Opaque control flow, high hallucination rate, conversational chatter overhead, non-deterministic agent loops, weak native state checkpointing.
3. **Custom State Machine (Python Dicts / Asyncio)**:
   - *Pros*: Zero external dependencies.
   - *Cons*: Reinventing checkpointing, state serialization, conditional branching, time-travel debugging, and streaming primitives.

### Trade-offs & Consequences
- **Positive**: Strict deterministic graph topology, first-class state checkpointing, native support for human-in-the-loop interruption, visualizable DAG/DCG, production-ready streaming events.
- **Negative**: Requires understanding graph paradigms (nodes, edges, reducers, checkpoint threads) instead of simple linear function calls.

---

## ADR 002: Backend Framework — FastAPI (Python 3.11+)

### Context
The backend must orchestrate asynchronous LLM calls, handle streaming HTTP connections, validate user payloads rigorously, and interface cleanly with Python-native AI libraries (LangGraph, LangChain, Pydantic).

### Decision
Use **FastAPI** with **Uvicorn** and Python 3.11+.

### Alternatives Considered
1. **Django / Django REST Framework**:
   - *Pros*: Batteries-included admin and ORM.
   - *Cons*: Heavy synchronous baggage, slower async support, excessive boilerplate for microservice architectures.
2. **Node.js / Express or NestJS**:
   - *Pros*: Excellent event-driven I/O.
   - *Cons*: Fractured Python AI ecosystem; LangGraph JS exists but Python has primary feature parity, faster library releases, and broader tool integrations.

### Trade-offs & Consequences
- **Positive**: Native Pydantic integration, automatic OpenAPI 3.1 documentation, first-class async/await support for high-concurrency LLM streaming, clean dependency injection.
- **Negative**: Requires careful connection pool management for async database sessions.

---

## ADR 003: Database & Vector Architecture — PostgreSQL 16 + pgvector

### Context
The system needs to persist:
1. Operational relational records (sessions, subtasks, web sources, reports, audit events).
2. LangGraph state checkpoints (binary state / thread metadata).
3. Document text embeddings for semantic retrieval (Phase 9 RAG).

### Decision
Consolidate on **PostgreSQL 16** with the **pgvector** extension using **SQLAlchemy 2.0 (asyncpg)**.

### Alternatives Considered
1. **Separate Relational DB (Postgres) + Dedicated Vector DB (Pinecone / Qdrant / Weaviate)**:
   - *Pros*: Dedicated vector indexing optimizations.
   - *Cons*: Two separate databases to deploy, maintain, pay for, and synchronize. Distributed transaction complexity when deleting or associating sources with sessions.
2. **MongoDB / DocumentDB**:
   - *Pros*: Schema flexibility for JSON dumps.
   - *Cons*: Lack of strict relational foreign keys for session/source cascades, poorer native support for LangGraph's SQL checkpointer.

### Trade-offs & Consequences
- **Positive**: Single ACID-compliant database for operational entities, graph checkpoints, and vector embeddings. Simplified Docker and production deployment. Native HNSW vector indexing.
- **Negative**: Slightly higher memory requirement for pgvector HNSW indexes compared to specialized vector microservices at massive scale (not an issue for enterprise research scale).

---

## ADR 004: Research Search Interface — Pluggable Interface with Tavily Search

### Context
Autonomous research agents need search engines that return clean, factual markdown/text extracts rather than messy HTML, SEO spam, or bot-blocked pagination pages.

### Decision
Create an abstract `SearchToolInterface` and provide **Tavily Search** as the primary production implementation, along with an offline/mock provider for deterministic CI testing.

### Alternatives Considered
1. **SerpAPI / Google Custom Search**:
   - *Pros*: Broad generic web index.
   - *Cons*: Returns only short 2-line snippets; requires separate web scraping infrastructure to read page content, which frequently breaks on anti-bot CAPTCHAs.
2. **Direct Headless Browser Scraping (Playwright / Puppeteer)**:
   - *Pros*: Maximum scraping autonomy.
   - *Cons*: Extremely resource-intensive, slow (10-30s per page), fragile, and easily blocked by Cloudflare/Akamai.

### Trade-offs & Consequences
- **Positive**: Tavily is explicitly designed for LLM agents, returning pre-filtered, extracted content chunks and high-relevance citations in a single API call.
- **Negative**: Dependency on an external third-party API; mitigated by our pluggable interface and offline test harness.

---

## ADR 005: Streaming Protocol — Server-Sent Events (SSE)

### Context
The user interface must reflect the real-time status of the LangGraph workflow (node transitions, queries launched, sources discovered, validator reasoning) as they happen.

### Decision
Use **Server-Sent Events (SSE)** over HTTP/1.1 or HTTP/2.

### Alternatives Considered
1. **WebSockets**:
   - *Pros*: Bi-directional communication.
   - *Cons*: More complex connection lifecycle, requires custom reconnection/heartbeat logic, challenges with certain corporate firewalls, overkill since streaming updates in Phase 7 are unidirectional (Server -> Client).
2. **Short Polling (`GET /status` every 1s)**:
   - *Pros*: Simplest implementation.
   - *Cons*: Unnecessary database read amplification, high latency (1s lag), poor user experience for real-time streaming tokens.

### Trade-offs & Consequences
- **Positive**: Standard HTTP protocol, automatic browser reconnection via native `EventSource`, simple text-based format, seamless integration with FastAPI's `StreamingResponse`.
- **Negative**: Unidirectional only; for Phase 10 Human-in-the-Loop, human inputs are sent via standard HTTP `POST /approve` endpoints, which is cleaner and more RESTful anyway.

---

## ADR 006: Frontend Stack — React 18, Vite, TypeScript, Tailwind CSS

### Context
The frontend must provide an interactive, fast, senior-grade dashboard displaying research workflows, interactive graph topologies, source lists, and rich markdown reports.

### Decision
Build a Single Page Application using **React 18**, **TypeScript**, **Vite**, and **Tailwind CSS**.

### Alternatives Considered
1. **Next.js (App Router / SSR)**:
   - *Pros*: Full-stack React framework with server-side rendering.
   - *Cons*: Unnecessary complexity for a dashboard that lives behind authentication; FastAPI already serves as the dedicated backend API; Next.js server actions duplicate FastAPI endpoints.
2. **Streamlit / Gradio**:
   - *Pros*: Rapid Python-only prototyping.
   - *Cons*: Produces clunky, non-production "demo" UIs with severe layout and UX limitations. Not suitable for a senior engineering portfolio.

### Trade-offs & Consequences
- **Positive**: Instant HMR development with Vite, strict type safety shared with backend API schemas, flexible utility-first styling with Tailwind CSS, clean SPA deployment.
- **Negative**: Requires managing separate frontend and backend dev servers (orchestrated seamlessly with Docker Compose).
