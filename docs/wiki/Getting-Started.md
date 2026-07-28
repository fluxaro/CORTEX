# Getting Started with ProjectIQ

Welcome to ProjectIQ! This guide helps you set up and run ProjectIQ locally.

## Prerequisites
- Python 3.13+
- Node.js 20+
- PostgreSQL & Redis (or Docker)

## Quickstart

### 1. Clone Repository
```bash
git clone https://github.com/me-hv/ProjectIQ.git
cd ProjectIQ
```

### 2. Backend Setup
```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run migrations
alembic -c backend/alembic.ini upgrade head

# Start FastAPI dev server
uvicorn app.main:app --reload --app-dir backend
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` to explore the ProjectIQ dashboard!
