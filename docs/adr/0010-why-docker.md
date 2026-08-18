# ADR 0010: Why Docker for Deployment

## Status
Accepted

## Context
Cortex consists of 4 runtime components: FastAPI API server, Celery worker, PostgreSQL, and Redis. Coordinating these across different developer machines and cloud environments requires a consistent packaging strategy.

## Decision
Use **Docker** with a multi-stage `Dockerfile` and **Docker Compose** for local and production orchestration.

## Rationale
- **Reproducibility**: The exact same container image runs in development, CI, staging, and production — eliminating "works on my machine" issues.
- **Multi-stage builds**: A builder stage installs all Python dependencies; the final stage copies only the compiled artifacts, reducing image size.
- **Compose for local dev**: `docker-compose.yml` starts PostgreSQL, Redis, API, worker, and frontend with a single command.
- **Health checks**: Docker Compose `healthcheck` definitions ensure PostgreSQL and Redis are ready before API and worker containers start.
- **Cloud-agnostic**: The Docker image can be deployed to Render, Railway, Fly.io, GCP Cloud Run, AWS ECS, or any container platform without modification.

## Consequences
- Docker and Docker Compose are required for the recommended installation path.
- Environment variables are the exclusive configuration mechanism — no hardcoded secrets in images.
