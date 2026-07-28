# Troubleshooting Guide

Solutions to the most common ProjectIQ setup and runtime issues.

---

## Installation Issues

### `ModuleNotFoundError: No module named 'app'`
**Cause:** `PYTHONPATH` is not set to `backend`.

**Fix:**
```bash
# Windows PowerShell
$env:PYTHONPATH="backend"; uvicorn app.main:app --reload

# macOS / Linux
PYTHONPATH=backend uvicorn app.main:app --reload
```

---

### `sqlalchemy.exc.OperationalError: could not connect to server`
**Cause:** PostgreSQL is not running or `DATABASE_URL` is misconfigured.

**Fix:**
```bash
# Start PostgreSQL with Docker
docker-compose up -d postgres

# Verify connection string format
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/projectiq_db
```

---

### Celery worker not processing tasks
**Cause:** Redis is not running or `CELERY_BROKER_URL` is misconfigured.

**Fix:**
```bash
# Start Redis with Docker
docker-compose up -d redis

# Verify Celery can connect
celery -A app.workers.celery_app inspect ping --app-dir backend
```

---

### `alembic.util.exc.CommandError: Can't locate revision identified by 'head'`
**Cause:** Migrations table doesn't exist yet.

**Fix:**
```bash
# Initialize Alembic and run all migrations
alembic -c backend/alembic.ini upgrade head
```

---

## Analysis Issues

### Repository clone fails with permission error
**Cause:** The repository is private and no access token is configured.

**Fix:** Ensure `GITHUB_ACCESS_TOKEN` is set in `.env` for private repositories.

---

### Analysis stuck in `PENDING` status
**Cause:** Celery worker is not running.

**Fix:** Start the Celery worker in a separate terminal:
```bash
celery -A app.workers.celery_app worker --loglevel=info --app-dir backend
```

---

## Frontend Issues

### `CORS Error` in browser console
**Cause:** The FastAPI `CORS_ORIGINS` setting does not include the frontend URL.

**Fix:** Add the frontend origin to `.env`:
```env
CORS_ORIGINS=["http://localhost:5173"]
```

---

## Test Failures

### `DeprecationWarning: datetime.datetime.utcnow()` in tests
**Cause:** Python 3.12+ deprecates `datetime.utcnow()`.

**Fix:** Use `datetime.now(datetime.UTC)`. This warning is non-blocking and tests pass.

---

## Getting More Help

- Check [GitHub Issues](https://github.com/me-hv/ProjectIQ/issues) for known bugs.
- Open a [GitHub Discussion](https://github.com/me-hv/ProjectIQ/discussions) for questions.
- Read the [FAQ](FAQ).
