# ADR 0004: Why FastAPI

## Status
Accepted

## Context
ProjectIQ requires a high-performance async Python API framework supporting OpenAPI generation, Pydantic v2 data validation, and straightforward async SQLAlchemy integration.

## Decision
Use **FastAPI** as the primary API framework.

## Rationale
- **Native async/await**: First-class support for Python's `asyncio`, critical for non-blocking SQLAlchemy 2.x async sessions and Celery task dispatch.
- **Automatic OpenAPI 3.1 generation**: Zero-configuration Swagger UI at `/docs` and ReDoc at `/redoc` — essential for an API-centric SaaS product.
- **Pydantic v2 integration**: FastAPI 0.115+ has native Pydantic v2 support, enabling schema-first validation without boilerplate.
- **Dependency injection**: Clean, testable service injection via `Depends()` — allows mocking DB sessions in Pytest.
- **Performance**: FastAPI benchmarks at 3–5x faster than Flask and comparable to Node.js Express.
- **Ecosystem**: Uvicorn, Gunicorn, Starlette middleware, and async test clients are all first-class.

## Alternatives Considered
| Alternative | Rejection Reason |
| :--- | :--- |
| Django REST Framework | Synchronous by default; heavier ORM coupling; slower startup |
| Flask + marshmallow | No native async; manual OpenAPI; verbose validation |
| aiohttp | No built-in routing, DI, or OpenAPI; too low-level |

## Consequences
- API layer is strictly async-only; synchronous blocking calls are prohibited.
- Middleware must be Starlette-compatible.
