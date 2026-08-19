# Build stage
FROM python:3.13-slim as builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/pyproject.toml ./
RUN pip install --prefix=/install . || pip install --prefix=/install fastapi uvicorn pydantic pydantic-settings sqlalchemy alembic redis celery asyncpg psycopg2-binary httpx

# Final stage
FROM python:3.13-slim as runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev curl git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY backend /app/backend

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "backend"]