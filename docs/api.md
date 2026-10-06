# API Specification: LangGraph Research Dashboard

## 1. Design Philosophy

The LRD API is built with **FastAPI** adhering to RESTful conventions, OpenAPI 3.1 standards, and Server-Sent Events (SSE) for low-latency streaming.

- **Base URL**: `/api/v1`
- **Content Type**: `application/json`
- **Streaming Content Type**: `text/event-stream`
- **Error Standard**: RFC 7807 Problem Details

---

## 2. API Endpoints

### 2.1 Research Session Lifecycle

#### `POST /api/v1/research`
Initiates a new autonomous research workflow session.

**Request Body**:
```json
{
  "query": "Compare state-of-the-art AI code generation tools in 2026, their productivity impact, security trade-offs, and enterprise adoption benchmarks.",
  "additional_instructions": "Focus especially on enterprise data governance and code leak risks.",
  "research_depth": "standard"
}
```
*Field Details*:
- `query` (string, required, length: 10 - 2000 chars)
- `additional_instructions` (string, optional, length: max 1000 chars)
- `research_depth` (enum: `"quick"` | `"standard"` | `"deep"`, default: `"standard"`)

**Response (`201 Created`)**:
```json
{
  "id": "e81d4c2b-923f-4e12-8e11-137a28e83b49",
  "title": "Impact and Enterprise Trade-offs of AI Code Generation Tools (2026)",
  "user_query": "Compare state-of-the-art AI code generation tools...",
  "research_depth": "standard",
  "status": "pending",
  "retry_count": 0,
  "current_node": "planner",
  "created_at": "2026-10-06T08:15:00Z",
  "updated_at": "2026-10-06T08:15:00Z"
}
```

---

#### `GET /api/v1/research`
Lists historical research sessions with pagination, status filters, and search capabilities.

**Query Parameters**:
- `page` (integer, default: 1)
- `page_size` (integer, default: 10, max: 50)
- `status` (optional string, enum: `pending` | `running` | `completed` | `failed`)
- `search` (optional string query)

**Response (`200 OK`)**:
```json
{
  "items": [
    {
      "id": "e81d4c2b-923f-4e12-8e11-137a28e83b49",
      "title": "Impact and Enterprise Trade-offs of AI Code Generation Tools (2026)",
      "user_query": "Compare state-of-the-art...",
      "research_depth": "standard",
      "status": "completed",
      "retry_count": 1,
      "sources_count": 8,
      "created_at": "2026-10-06T08:15:00Z",
      "completed_at": "2026-10-06T08:17:42Z"
    }
  ],
  "total": 42,
  "page": 1,
  "page_size": 10,
  "total_pages": 5
}
```

---

#### `GET /api/v1/research/{id}`
Retrieves complete details of a specific session, including subtasks, execution status, and node statistics.

**Response (`200 OK`)**:
```json
{
  "id": "e81d4c2b-923f-4e12-8e11-137a28e83b49",
  "title": "Impact and Enterprise Trade-offs of AI Code Generation Tools (2026)",
  "user_query": "Compare state-of-the-art...",
  "research_depth": "standard",
  "status": "running",
  "current_node": "researcher",
  "retry_count": 0,
  "subtasks": [
    {
      "id": "subtask_1",
      "title": "Landscape of 2026 AI Coding Assistants",
      "status": "completed",
      "queries": ["top enterprise AI coding tools 2026 benchmarks"]
    },
    {
      "id": "subtask_2",
      "title": "Productivity and Velocity Metrics",
      "status": "in_progress",
      "queries": ["developer productivity metrics AI assistance empirical studies 2025 2026"]
    }
  ],
  "created_at": "2026-10-06T08:15:00Z",
  "updated_at": "2026-10-06T08:15:30Z"
}
```

---

#### `GET /api/v1/research/{id}/status`
Lightweight polling endpoint to retrieve current workflow step and active node.

**Response (`200 OK`)**:
```json
{
  "id": "e81d4c2b-923f-4e12-8e11-137a28e83b49",
  "status": "running",
  "current_node": "analyzer",
  "retry_count": 0,
  "updated_at": "2026-10-06T08:16:10Z"
}
```

---

#### `GET /api/v1/research/{id}/sources`
Retrieves all retrieved web sources, citations, and relevance scores.

**Response (`200 OK`)**:
```json
{
  "session_id": "e81d4c2b-923f-4e12-8e11-137a28e83b49",
  "count": 2,
  "sources": [
    {
      "id": "7f8b9a10-4321-4def-9988-123456789abc",
      "title": "Empirical Developer Velocity Study: AI Code Pairings in 2026",
      "url": "https://research.acm.org/articles/ai-developer-velocity-2026",
      "source_type": "academic",
      "summary": "Study of 1,200 software engineers found a 26% reduction in cycle time for routine tasks, alongside a 14% increase in PR review review duration due to boilerplate bloat.",
      "relevance_score": 0.94,
      "retrieved_at": "2026-10-06T08:15:45Z"
    }
  ]
}
```

---

#### `GET /api/v1/research/{id}/report`
Retrieves the completed research report artifact. Returns `404` if the report is not yet finalized.

**Response (`200 OK`)**:
```json
{
  "session_id": "e81d4c2b-923f-4e12-8e11-137a28e83b49",
  "title": "Strategic Research: AI Coding Assistants in 2026",
  "executive_summary": "Modern AI coding tools deliver measurable velocity gains for repetitive tasks...",
  "methodology": "Multi-query web retrieval cross-referencing industry benchmarks and security audits...",
  "key_findings": [
    "26% median reduction in time-to-first-commit across tested engineering cohorts.",
    "Data privacy and token exposure remain the primary roadblock for enterprise adoption."
  ],
  "detailed_analysis": "### Tool Comparison\n\n...",
  "contradictions": [
    "Some vendor reports assert 55% productivity gains, whereas independent peer reviews show gains taper to 15-20% on complex legacy codebases."
  ],
  "limitations": [
    "Long-term codebase maintenance and technical debt data remains limited to 18-month longitudinal windows."
  ],
  "conclusion": "Organizations should adopt a tiered integration model...",
  "raw_markdown": "# Strategic Research: AI Coding Assistants in 2026\n\n## Executive Summary...",
  "generated_at": "2026-10-06T08:17:40Z"
}
```

---

#### `POST /api/v1/research/{id}/cancel`
Gracefully aborts a running workflow execution.

**Response (`200 OK`)**:
```json
{
  "id": "e81d4c2b-923f-4e12-8e11-137a28e83b49",
  "status": "cancelled",
  "message": "Workflow execution aborted by user request."
}
```

---

#### `POST /api/v1/research/{id}/approve` (Phase 10 Human-in-the-Loop)
Submits approval or plan modifications when a workflow is paused at a human review node.

---

### 2.2 Real-Time Streaming Endpoint (SSE)

#### `GET /api/v1/research/{id}/events`
Opens a Server-Sent Events (SSE) connection streaming real-time graph events to the frontend.

**Event Format**:
```
event: node_started
data: {"node": "planner", "timestamp": "2026-10-06T08:15:02Z"}

event: plan_created
data: {"subtasks_count": 3, "subtasks": [...]}

event: node_started
data: {"node": "researcher", "timestamp": "2026-10-06T08:15:10Z"}

event: source_discovered
data: {"title": "Study...", "url": "https://...", "relevance": 0.94}

event: node_started
data: {"node": "validator", "timestamp": "2026-10-06T08:16:15Z"}

event: validation_result
data: {"status": "VALID", "reason": "Sufficient evidence collected"}

event: report_completed
data: {"report_id": "...", "generated_at": "2026-10-06T08:17:40Z"}

event: done
data: {"status": "completed"}
```

---

## 3. Error Handling Schema

All non-2xx responses adhere to the standard JSON structure:
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Research session with id 'e81d4c2b' does not exist.",
    "details": null
  }
}
```
Standard status codes:
- `400 Bad Request`: Input validation failed (query too short/long, invalid depth).
- `404 Not Found`: Session ID or report does not exist.
- `409 Conflict`: Action incompatible with session state (e.g., trying to cancel a completed task).
- `500 Internal Server Error`: Unhandled backend exception.
