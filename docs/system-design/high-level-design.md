# System Design — High Level Design

## Overview

Cortex is an **AI-enhanced static analysis platform** that inspects source code repositories without executing untrusted code and produces a structured engineering intelligence report.

---

## High Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                 CLIENT TIER                                  │
│                                                                              │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │             React 18 SaaS Frontend (Vite + TypeScript)              │   │
│   │         Tailwind CSS · Recharts · React Flow · TanStack Query       │   │
│   └──────────────────────────────┬──────────────────────────────────────┘   │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │ HTTPS / REST JSON
┌─────────────────────────────────▼───────────────────────────────────────────┐
│                              API GATEWAY TIER                                │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                   FastAPI (Python 3.13 + Uvicorn)                   │    │
│  │   Rate Limit · Request ID · JWT Auth · RBAC · OpenAPI 3.1 · CORS   │    │
│  └──────────┬──────────────────────────────────────┬───────────────────┘    │
└─────────────┼────────────────────────────────────  ┼──────────────────────  ┘
              │ SQLAlchemy 2.x Async                  │ Celery Task dispatch
┌─────────────▼──────────────┐          ┌─────────────▼───────────────────────┐
│       DATA TIER            │          │          WORKER TIER                 │
│                            │          │                                      │
│  ┌──────────────────────┐  │          │  ┌────────────────────────────────┐  │
│  │    PostgreSQL 15     │  │          │  │         Celery Workers         │  │
│  │  44+ analysis tables │  │          │  │   clone · index · parse        │  │
│  │  Enterprise schema   │  │          │  │   architecture · security      │  │
│  └──────────────────────┘  │          │  │   maintainability · iq · sync  │  │
│                            │          │  └────────────────────────────────┘  │
│  ┌──────────────────────┐  │          │                                      │
│  │      Redis 7         │  │◄─────────│   Celery broker (task queue)        │
│  │  Task queue · Cache  │  │          │   Result backend                     │
│  └──────────────────────┘  │          │                                      │
└────────────────────────────┘          └─────────────────────────────────────┘
                                                        │
                                         ┌──────────────▼──────────────────────┐
                                         │         ANALYSIS ENGINES            │
                                         │                                     │
                                         │  Static · Architecture · Security   │
                                         │  Maintainability · IQ · AI         │
                                         └─────────────────────────────────────┘
```

---

## Data Flow: Repository Analysis Pipeline

```
1. User submits URL via POST /api/v1/repositories
        ↓
2. FastAPI validates URL, creates Repository record (status=PENDING)
        ↓
3. Celery clone_and_index_task queued to Redis
        ↓
4. Worker: git clone → file system indexer → Repository (status=INDEXING)
        ↓
5. Celery static_analysis_task queued
        ↓
6. Worker: AST parser for each file → metrics aggregation → (status=ANALYZING)
        ↓
7. Parallel Celery tasks:
   ├─ architecture_analysis_task  → layer detection, patterns, dependency graph
   ├─ security_analysis_task      → SAST, secrets, CVEs, config audit
   └─ maintainability_task        → docs, testing, CI, Git history
        ↓
8. All sub-analyses complete → iq_engine_task
        ↓
9. IQ Engine: weighted scoring, maturity, debt, benchmarking, AI prompts
        ↓
10. Repository (status=COMPLETE) — frontend polls and displays results
```

---

## Security Architecture

- All repositories are cloned to a **sandboxed local directory** (`/tmp/cortex/clones/`).
- **No code execution** at any phase of analysis.
- Secrets are masked in the database before storage.
- JWT tokens expire after 30 minutes. Refresh tokens after 7 days.
- All passwords are hashed with **PBKDF2 HMAC-SHA256** (100,000 iterations).
- RBAC is enforced at the service layer, not just the API layer.
- Rate limiting applies to all `/api/v1/` endpoints.
- Request IDs are propagated through all Celery tasks via task headers.

---

## Scalability Design

| Concern | Solution |
| :--- | :--- |
| High API throughput | Async FastAPI + Uvicorn with async SQLAlchemy |
| Many concurrent analyses | Horizontal Celery worker scaling |
| Large repository parsing | Chunked file processing, streaming AST parsing |
| Database read performance | PostgreSQL indexes on all foreign keys and status columns |
| Caching | Redis for rate limit counters and Celery result cache |
| Frontend performance | Vite code splitting, lazy route loading, TanStack Query caching |
