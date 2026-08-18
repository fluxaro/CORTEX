# Installation Guide

This guide covers installation of Cortex for both **production** and **development** use.

---

## Docker Installation (Recommended)

Docker is the fastest and most reliable way to run Cortex.

### Prerequisites
- Docker Engine 24+
- Docker Compose v2+

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/me-hv/Cortex.git
cd Cortex

# 2. Copy environment template
cp .env.example .env

# 3. Edit .env — configure DATABASE_URL, REDIS_URL, SECRET_KEY, AI keys (optional)

# 4. Start all services
docker-compose up -d --build

# 5. Run database migrations
docker-compose exec api alembic -c /app/backend/alembic.ini upgrade head
```

### Services Started
| Service | Port | Purpose |
| :--- | :--- | :--- |
| `api` | 8000 | FastAPI backend |
| `worker` | — | Celery background worker |
| `postgres` | 5432 | PostgreSQL database |
| `redis` | 6379 | Message broker / cache |
| `frontend` | 5173 | React SaaS frontend |

Open `http://localhost:5173` to access the dashboard.

---

## Manual Installation

### Prerequisites
- Python 3.13+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+
- Git

### Backend Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt

# Configure environment
cp .env.example .env
# Edit .env — set DATABASE_URL, REDIS_URL, SECRET_KEY

# Run all database migrations
alembic -c backend/alembic.ini upgrade head

# Start the API server
uvicorn app.main:app --reload --app-dir backend --host 0.0.0.0 --port 8000

# Start the Celery worker (separate terminal)
celery -A app.workers.celery_app worker --loglevel=info --app-dir backend
```

### Frontend Setup

```bash
cd frontend

# Install Node dependencies
npm install

# Start development server
npm run dev
```

Open `http://localhost:5173` to access the dashboard.

---

## Verification

After installation, verify everything is working:

```bash
# Test the API health endpoint
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status":"healthy"}

# Test liveness probe
curl http://localhost:8000/api/v1/health/live
# {"status":"alive"}

# Test readiness probe
curl http://localhost:8000/api/v1/health/ready
# {"status":"ready","database":"connected"}
```
