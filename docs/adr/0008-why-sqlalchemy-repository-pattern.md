# ADR 0008: Why SQLAlchemy + Repository Pattern

## Status
Accepted

## Context
Cortex has 44+ database tables across 7 schema areas. Direct SQL query strings scattered across API endpoints would make testing, refactoring, and adding new features error-prone and brittle.

## Decision
Use **SQLAlchemy 2.x** with the **async session pattern** and a **Service Layer** (a lightweight form of the Repository Pattern) to abstract database operations.

## Rationale
- **Type-safe ORM**: SQLAlchemy 2.x `Mapped[]` column declarations provide Mypy-verifiable type annotations on every model attribute.
- **Async-first**: `AsyncSession` with `select()` statements integrates cleanly with FastAPI's `async def` endpoints via `Depends(get_db)`.
- **Service layer**: Each domain area has a dedicated service class (`AuthService`, `WorkspaceService`, `TrendService`, etc.) that encapsulates all database interactions, making unit testing via mock sessions trivial.
- **Testability**: In-memory SQLite (`sqlite+aiosqlite:///:memory:`) is used in Pytest fixtures, providing complete database isolation per test without touching PostgreSQL.
- **Migration support**: Alembic integrates natively with SQLAlchemy models for version-controlled schema migrations.

## Consequences
- All database access goes through service classes — no direct session usage in API endpoint functions beyond injecting the session via `Depends(get_db)`.
- Raw SQL is only used in health check readiness probes (`SELECT 1`).
