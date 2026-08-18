# ADR 0005: Why PostgreSQL

## Status
Accepted

## Context
Cortex stores 44+ relational tables with complex foreign key hierarchies, JSON metadata columns, and requires efficient indexed lookups on analysis status, repository IDs, and severity fields.

## Decision
Use **PostgreSQL 15** as the primary data store.

## Rationale
- **ACID compliance**: Analysis pipeline stages must atomically write multi-table results. PostgreSQL's transactional guarantees prevent partial writes.
- **JSON/JSONB support**: Architecture findings, subsystem scores, and AI prompts are stored as structured JSON blobs alongside relational data.
- **Advanced indexing**: GIN indexes for JSONB columns, partial indexes on `status` columns for fast queue polling.
- **Foreign key integrity**: Complex cascading deletes across 44 tables are enforced at the database level.
- **Mature ecosystem**: SQLAlchemy 2.x async support, Alembic migrations, and pgAdmin tooling are all battle-tested.

## Alternatives Considered
| Alternative | Rejection Reason |
| :--- | :--- |
| MySQL / MariaDB | Weaker JSON support; weaker JSONB indexing |
| MongoDB | No referential integrity; poor for complex JOIN queries across 44 tables |
| SQLite | Single-writer limitation; not suitable for concurrent Celery workers |

## Consequences
- All SQLAlchemy ORM models use standard `JSON` type (not `JSONB`) to maintain Pytest SQLite compatibility.
- Alembic migrations are PostgreSQL-dialect compatible.
