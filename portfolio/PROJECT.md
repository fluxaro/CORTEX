# Cortex — Portfolio Project

## Overview

**Cortex** is an enterprise-grade Repository Intelligence Platform built as a flagship full-stack engineering project. It inspects any public Git repository using static analysis, AI, and industry benchmarking to produce a comprehensive engineering quality report — without executing any untrusted code.

**Live at:** `https://github.com/me-hv/Cortex`  
**Stack:** Python 3.13 · FastAPI · SQLAlchemy 2.x · Celery · Redis · PostgreSQL · React 18 · TypeScript · Vite · Tailwind CSS  
**Release:** v1.0.0 · MIT License · 61 Tests Passing

---

## The Problem

Before integrating or forking an open-source repository, engineers routinely spend hours or days manually assessing its:
- Code quality and complexity
- Architecture and modular design
- Security vulnerabilities and exposed secrets
- Documentation completeness
- Test coverage and CI/CD maturity
- Git velocity and team health

This is expensive, inconsistent, and entirely unscalable for organizations evaluating dozens of repositories.

---

## The Solution

Cortex automates this evaluation across **8 engineering dimensions** and produces:
1. A **Repository IQ Score (0–100)** — a single, actionable quality metric
2. **Language-specific code metrics** — cyclomatic complexity, maintainability index, duplication
3. **Architecture intelligence** — style detection, 20+ design patterns, interactive dependency graphs
4. **SAST security scanning** — secrets, CVEs, dangerous functions, config misconfigurations
5. **Technical debt estimation** — hours and days, broken down by category
6. **AI-generated summaries** — tailored for engineers, managers, and recruiters
7. **Enterprise collaboration** — multi-tenant workspaces, RBAC, GitHub/GitLab/Bitbucket sync

---

## Engineering Challenges & Solutions

### Challenge 1: Analyzing Code Without Executing It
**Problem:** Running arbitrary repository code creates severe security risks.  
**Solution:** Pure static analysis using Python `ast`, regex-based pattern matching, and structural file indexers. No subprocess execution at any analysis stage.

### Challenge 2: Handling Analysis Duration Without Blocking
**Problem:** Cloning and analyzing a large repository takes 1–5 minutes — far too long for a synchronous HTTP request.  
**Solution:** Multi-stage Celery task pipeline with Redis as the broker. Each stage writes results atomically to PostgreSQL before dispatching the next stage. The API returns immediately with a `202 Accepted` and the frontend polls for status.

### Challenge 3: Producing a Fair, Explainable Score
**Problem:** Aggregating disparate metrics (complexity, security severity, test coverage) into a single score risks being opaque and arbitrary.  
**Solution:** A documented, configurable **weighted scoring matrix** (ADR 0002) with per-subsystem breakdown. Every score is backed by specific database records that users can inspect.

### Challenge 4: Supporting Multiple AI Providers Without Lock-in
**Problem:** Any single LLM provider risks key unavailability, cost changes, or API deprecation.  
**Solution:** An `AIProviderFactory` abstraction supporting OpenAI, Anthropic, Gemini, Azure, Ollama, and an offline `MockProvider`. The AI layer never reads raw source code — only structured metrics from PostgreSQL.

### Challenge 5: Enterprise Multi-Tenancy
**Problem:** Enterprise teams need isolated workspaces, role-based permissions, and audit trails — without duplicating data or compromising isolation.  
**Solution:** A `Workspace → Membership → User` hierarchy with 5-level RBAC enforced at the service layer. Every destructive operation writes to an immutable `AuditLog` table.

---

## Architecture Highlights

- **Modular engine design**: Each analysis engine (static, architecture, security, maintainability, IQ) is a completely independent module that can be extended or replaced without touching the others.
- **44+ database tables** across 7 Alembic migrations, designed for zero-downtime schema evolution.
- **OpenAPI 3.1** auto-generated from Python type annotations — zero documentation lag.
- **Request ID tracing** propagated from HTTP request through Celery task metadata for end-to-end observability.
- **GitHub Actions CI/CD** runs on every push: Ruff, Black, Mypy, Pytest (61 tests), Vite build.

---

## Interesting Technical Details

1. **Cross-file duplication detection** uses a rolling hash window algorithm (similar to Rabin fingerprinting) across all parsed files — O(n) per file.
2. **Design pattern detection** uses AST structural matching — not string search. A Singleton is detected by finding a private class attribute holding a class instance combined with a static/class method returning it.
3. **Secret scanning** combines regex matching with **Shannon entropy calculation** — high-entropy strings that match no known pattern are still flagged as probable secrets.
4. **JWT implementation uses only the Python standard library** (`hmac`, `hashlib`, `json`, `base64`) — zero external JWT dependencies.

---

## Technology Stack

| Layer | Technology | Why |
| :--- | :--- | :--- |
| API | FastAPI 0.115 | Async-first, OpenAPI auto-generation, Pydantic v2 |
| ORM | SQLAlchemy 2.x | Async sessions, Mypy-typed models |
| Queue | Celery + Redis | Reliable async analysis pipeline |
| DB | PostgreSQL 15 | ACID compliance, JSONB, complex FKs |
| Frontend | React 18 + Vite | SPA with concurrent rendering |
| Types | TypeScript 5 | Full type safety across the frontend |
| Styling | Tailwind CSS 3 | Rapid dark mode SaaS design |
| Charts | Recharts + React Flow | Radar charts, dependency graphs |
| Testing | Pytest + asyncio | 61 tests, in-memory SQLite isolation |

---

## Performance Metrics

| Metric | Value |
| :--- | :--- |
| API p95 response time | ~85ms |
| Full analysis (medium repo) | ~3 minutes |
| Test suite runtime | 7m 39s |
| Frontend Lighthouse score | 92 / 96 / 97 / 98 |
| Production bundle size | 891 KB (253 KB gzipped) |

---

## Lessons Learned

1. **Design for testability from day one.** The service layer pattern and in-memory SQLite fixtures made adding 61 tests straightforward.
2. **Async all the way.** Mixing sync and async SQLAlchemy sessions caused hard-to-debug issues. Committing to fully async from Phase 1 saved significant refactoring time.
3. **The AI abstraction layer was essential.** Developing 8 phases of features without any paid AI API calls was only possible because the `MockProvider` was implemented from the start.
4. **Static analysis is harder than it looks.** Language-specific edge cases (e.g., Go's multiple return values, Rust's trait implementations, TypeScript generics) required careful parser design.

---

## Future Roadmap

- Real-time WebSocket analysis progress streaming
- GitHub App for automated PR quality gates
- VS Code Extension for in-editor IQ scores
- Support for private repositories via SSH/PAT tokens
- Hosted cloud version at cortex.io
