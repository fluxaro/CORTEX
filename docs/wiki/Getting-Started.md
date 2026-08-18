# Getting Started with Cortex

Welcome to Cortex! This guide helps you set up and run Cortex locally.

## Prerequisites
- Python 3.13+
- Node.js 20+
- PostgreSQL & Redis (or Docker)

## Quickstart

### 1. Clone Repository
```bash
git clone https://github.com/me-hv/Cortex.git
cd Cortex
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

Open `http://localhost:5173` to explore the Cortex dashboard!
