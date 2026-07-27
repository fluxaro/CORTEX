# ProjectIQ

> **Tagline**: *"Know your code before you clone it."*

ProjectIQ is an enterprise-grade, AI-powered Repository Intelligence Platform. The platform analyzes GitHub repositories and generates comprehensive, production-ready reports on Code Quality, Architecture, Security, Dependencies, Documentation, Git History, Testing, AI Summary, and Technical Debt.

---

## 🌟 Project Vision

Developers, team leads, and architects spend hours evaluating open-source software, legacy codebases, and third-party dependencies before integrating or cloning them. ProjectIQ bridges this gap by providing automated, deep-level repository intelligence before code lands on your local machine.

---

## 🏗️ Architecture Overview

ProjectIQ is built with a modular, clean, and scalable architecture designed to support high-throughput asynchronous analysis.

```
                  +------------------------+
                  |  Vite + React Frontend |
                  +-----------+------------+
                              |
                              v (HTTP / REST API)
                  +-----------+------------+
                  |    FastAPI Backend     |
                  +-----+------------+-----+
                        |            |
                        v            v
           +------------+--+     +---+------------+
           | PostgreSQL DB |     | Redis + Celery |
           +---------------+     +----------------+
```

---

## 📁 Folder Structure

```
ProjectIQ/
├── backend/
│   ├── alembic/              # Database migration scripts
│   ├── app/
│   │   ├── api/              # API routes & versioning (/api/v1/)
│   │   ├── core/             # Configuration & logging system
│   │   ├── database/         # SQLAlchemy engine & session management
│   │   ├── models/           # Declarative ORM models & mixins
│   │   ├── schemas/          # Pydantic v2 validation models
│   │   ├── services/         # Business logic layer
│   │   ├── repositories/     # Data access abstraction layer
│   │   ├── tasks/            # Celery asynchronous tasks
│   │   ├── analyzers/        # Code analysis modules
│   │   ├── utils/            # Shared helper functions
│   │   ├── middleware/       # Custom FastAPI middlewares
│   │   ├── exceptions/       # Custom exceptions & handlers
│   │   ├── dependencies/     # FastAPI dependency injection
│   │   ├── workers/          # Celery worker initialization
│   │   └── scripts/          # Database & maintenance scripts
│   ├── tests/                # Pytest test suite
│   ├── alembic.ini           # Alembic configuration
│   └── pyproject.toml        # Dependencies & tooling config (Ruff, Black, Mypy, Pytest)
├── frontend/                 # Vite React TypeScript Tailwind CSS placeholder
├── Dockerfile                # Production multi-stage Dockerfile
├── docker-compose.yml        # Multi-container orchestration (Backend, Postgres, Redis, Worker)
└── README.md
```

---

## ⚡ Technology Stack

### Backend
- **Python 3.13 / 3.14**
- **FastAPI**: Modern, high-performance web framework
- **Pydantic v2**: Data validation and settings management
- **SQLAlchemy 2.x**: Async ORM & database Toolkit
- **Alembic**: Database migrations
- **PostgreSQL**: Primary relational database
- **Redis**: In-memory data store for caching and Celery broker
- **Celery**: Distributed task queue for asynchronous repository analysis
- **Quality & Testing**: Pytest, Ruff, Black, Mypy, Pre-commit

### Frontend (Placeholder)
- **React** with **TypeScript**
- **Vite** build tooling
- **Tailwind CSS**

---

## 🚀 Installation & Local Setup

### Prerequisites
- Python 3.13+
- Node.js 20+
- PostgreSQL & Redis (or Docker)

### Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -e ./backend
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

4. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --app-dir backend
   ```

5. Access endpoints:
   - **Health**: `http://localhost:8000/api/v1/health`
   - **Version**: `http://localhost:8000/api/v1/version`
   - **Swagger Docs**: `http://localhost:8000/docs`

---

## 🐳 Docker Deployment

To spin up the entire ecosystem (Backend, PostgreSQL, Redis, Celery worker):

```bash
docker-compose up --build
```

---

## 🗺️ Roadmap

- [x] **Phase 1**: Enterprise Foundation Architecture (FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, Celery, Redis, Docker, Quality tooling).
- [ ] **Phase 2**: Repository Cloning & File Parsing Engine.
- [ ] **Phase 3**: Static Code Quality & Security Analyzers.
- [ ] **Phase 4**: AI Summary & Technical Debt Scoring.
- [ ] **Phase 5**: Full Frontend SaaS Dashboard Integration.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on code of conduct and submitting pull requests.
