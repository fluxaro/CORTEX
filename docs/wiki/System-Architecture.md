# System Architecture Overview

ProjectIQ follows a decoupled, asynchronous micro-architecture designed for performance, modularity, and scalability.

```
+-------------------+        +--------------------+        +---------------------+
| React 18 Frontend |  <---> | FastAPI REST API   |  <---> | PostgreSQL & Redis  |
+-------------------+        +---------+----------+        +----------+----------+
                                       |                              |
                                       v                              v
                             +--------------------+        +---------------------+
                             | Celery Workers     |  <---> | Analysis Engines    |
                             +--------------------+        +---------------------+
```

## Architectural Components

### 1. API Layer (FastAPI)
- Exposes RESTful endpoints under `/api/v1`.
- Enforces JWT authentication, RBAC authorization, Request ID tracking, and Rate Limiting.

### 2. Analysis Engines
- **Static Code Analysis**: AST parsers for Python, TS, JS, Go, Java, Rust.
- **Architecture Intelligence Engine**: Layer detection, 20+ design patterns, module dependency graphs.
- **Security Intelligence Engine (SAST)**: Secret scanner, config auditor, SAST static rules.
- **Maintainability Engine**: Documentation, testing, CI/CD, Git history velocity.
- **Repository IQ Engine**: Weighted 0-100 score, technical debt estimation, maturity classification, AI summary prompts.

### 3. Background Workers (Celery & Redis)
- Handles repository cloning, indexing, static parsing, and scheduled scans asynchronously without blocking API threads.
