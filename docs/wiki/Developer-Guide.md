# Developer Guide

This guide covers local development setup, code standards, and development workflows.

---

## Development Setup

```bash
git clone https://github.com/me-hv/ProjectIQ.git
cd ProjectIQ

# Backend
python -m venv .venv
.venv\Scripts\activate              # Windows
source .venv/bin/activate           # macOS / Linux
pip install -r backend/requirements.txt

# Frontend
cd frontend && npm install && cd ..
```

---

## Running Locally

```bash
# 1. Start PostgreSQL and Redis (Docker shortcut)
docker-compose up -d postgres redis

# 2. Run migrations
alembic -c backend/alembic.ini upgrade head

# 3. Start FastAPI (terminal 1)
uvicorn app.main:app --reload --app-dir backend

# 4. Start Celery worker (terminal 2)
celery -A app.workers.celery_app worker --loglevel=info --app-dir backend

# 5. Start frontend (terminal 3)
cd frontend && npm run dev
```

---

## Code Quality Commands

```bash
# Ruff linting (auto-fix)
.venv\Scripts\ruff.exe check --fix backend

# Black formatting
.venv\Scripts\black.exe backend

# Mypy type checking
$env:PYTHONPATH="backend"; .venv\Scripts\mypy.exe --config-file backend/pyproject.toml backend/app

# Run full test suite
$env:PYTHONPATH="backend"; .venv\Scripts\pytest.exe backend/tests

# Frontend build verification
cd frontend && npm run build
```

---

## Adding a New Analysis Engine Module

1. Create your engine in `backend/app/engines/{area}/your_engine.py`
2. Register a new Pydantic schema in `backend/app/schemas/`
3. Create SQLAlchemy models in `backend/app/models/`
4. Write an Alembic migration: `alembic revision --autogenerate -m "add your_table"`
5. Add service logic in `backend/app/services/`
6. Register API endpoint in `backend/app/api/v1/endpoints/`
7. Mount the router in `backend/app/api/v1/router.py`
8. Write Pytest tests in `backend/tests/`

---

## Branching Strategy

| Branch | Purpose |
| :--- | :--- |
| `main` | Production-ready. Protected. Only CI-verified PRs merge here. |
| `feat/your-feature` | Feature development branches |
| `fix/bug-description` | Bug fix branches |
| `docs/topic` | Documentation changes |

---

## Commit Convention

ProjectIQ follows [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add repository comparison engine
fix: correct cyclomatic complexity calculation for Go files
docs: add Getting Started wiki page
chore: update dependencies
refactor: simplify SAST rule matching logic
test: add integration tests for auth endpoints
```
