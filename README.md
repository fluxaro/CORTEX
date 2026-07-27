# ProjectIQ

> **Tagline**: *"Know your code before you clone it."*

ProjectIQ is an enterprise-grade, AI-powered Repository Intelligence Platform. The platform analyzes GitHub repositories and generates comprehensive, production-ready reports on Code Quality, Architecture, Security, Dependencies, Documentation, Git History, Testing, AI Summary, and Technical Debt.

---

## 🌟 Project Vision

Developers, team leads, and architects spend hours evaluating open-source software, legacy codebases, and third-party dependencies before integrating or cloning them. ProjectIQ bridges this gap by providing automated, deep-level repository intelligence before code lands on your local machine.

---

## 🏗️ Architecture & Ingestion Pipeline

ProjectIQ uses an asynchronous background queue pipeline to handle repository ingestion and metadata indexing cleanly without blocking HTTP request execution.

```
+------------------+       +-------------------+       +-----------------------+
|  POST /repos     |  ---> | GitHub API Client |  ---> | Insert DB (PENDING)   |
+------------------+       +-------------------+       +-----------+-----------+
                                                                   |
                                                                   v
+------------------+       +-------------------+       +-----------+-----------+
| Analysis QUEUED  |  <--- | File System Index |  <--- | Celery Git Clone Task |
+------------------+       +-------------------+       +-----------------------+
```

### Repository Lifecycle Statuses

- `PENDING`: Initial state when repository URL is submitted and validated.
- `CLONING`: Background Celery task actively cloning code into `storage/repositories/{id}`.
- `READY`: Repository successfully cloned and file system index created.
- `FAILED`: Ingestion or cloning failed due to network errors or invalid credentials.

---

## 🗄️ Database Schema

### `repositories` Table
- `id`: UUID (Primary Key)
- `name`: VARCHAR(255)
- `owner`: VARCHAR(255)
- `full_name`: VARCHAR(512) (Unique)
- `description`: TEXT
- `default_branch`: VARCHAR(255)
- `stars`: INTEGER
- `forks`: INTEGER
- `language`: VARCHAR(100)
- `license`: VARCHAR(255)
- `clone_url`: VARCHAR(1024)
- `html_url`: VARCHAR(1024)
- `visibility`: VARCHAR(50)
- `size`: INTEGER (in KB)
- `created_at`: TIMESTAMP WITH TIME ZONE
- `updated_at`: TIMESTAMP WITH TIME ZONE
- `last_pushed_at`: TIMESTAMP WITH TIME ZONE
- `status`: VARCHAR(50) (`PENDING`, `CLONING`, `READY`, `FAILED`)
- `analysis_status`: VARCHAR(50) (`PENDING`, `QUEUED`, `IN_PROGRESS`, `COMPLETED`, `FAILED`)
- `local_path`: VARCHAR(1024)
- `created_on`: TIMESTAMP WITH TIME ZONE
- `updated_on`: TIMESTAMP WITH TIME ZONE

### `repository_file_indices` Table
- `id`: UUID (Primary Key)
- `repository_id`: UUID (Foreign Key -> `repositories.id`)
- `folder_count`: INTEGER
- `file_count`: INTEGER
- `max_depth`: INTEGER
- `total_size_bytes`: INTEGER
- `largest_files`: JSON
- `file_extensions`: JSON
- `language_distribution`: JSON
- `created_at`: TIMESTAMP WITH TIME ZONE
- `updated_at`: TIMESTAMP WITH TIME ZONE

---

## 📡 REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/v1/health` | Service health status |
| **GET** | `/api/v1/version` | Service name and version |
| **POST** | `/api/v1/repositories` | Ingest new public GitHub repository |
| **GET** | `/api/v1/repositories` | List repositories (with pagination, filtering & sorting) |
| **GET** | `/api/v1/repositories/{id}` | Get repository details & file system index |
| **DELETE** | `/api/v1/repositories/{id}` | Delete repository & cleanup local clone storage |

### Query Parameters for `GET /api/v1/repositories`
- `page`: Page number (default: 1)
- `page_size`: Number of items per page (default: 10, max: 100)
- `status`: Filter by status (`PENDING`, `CLONING`, `READY`, `FAILED`)
- `owner`: Filter by repository owner login
- `language`: Filter by primary programming language
- `sort_by`: Sort field (`created_at`, `stars`, `updated_at`)
- `order`: Sort order (`asc`, `desc`)

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
│   │   ├── services/         # GitHubClient, GitService, FileIndexerService, RepositoryService
│   │   ├── repositories/     # Data access abstraction layer
│   │   ├── tasks/            # Celery asynchronous tasks (clone_repository_task, prepare_analysis_task)
│   │   ├── analyzers/        # Code analysis modules
│   │   ├── utils/            # Shared helper functions
│   │   ├── middleware/       # Custom FastAPI middlewares (RequestIDMiddleware)
│   │   ├── exceptions/       # Custom exceptions & global handlers
│   │   ├── dependencies/     # FastAPI dependency injection
│   │   ├── workers/          # Celery worker initialization
│   │   └── scripts/          # Database & maintenance scripts
│   ├── tests/                # Pytest test suite
│   ├── alembic.ini           # Alembic configuration
│   └── pyproject.toml        # Dependencies & tooling config (Ruff, Black, Mypy, Pytest)
├── storage/
│   └── repositories/         # Cloned repository code storage ({repository_id})
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
- **GitPython**: Git repository cloning and management
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

4. Run database migrations:
   ```bash
   alembic -c backend/alembic.ini upgrade head
   ```

5. Run the FastAPI development server:
   ```bash
   uvicorn app.main:app --reload --app-dir backend
   ```

6. Access endpoints:
   - **Health**: `http://localhost:8000/api/v1/health`
   - **Version**: `http://localhost:8000/api/v1/version`
   - **Repositories**: `http://localhost:8000/api/v1/repositories`
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
- [x] **Phase 2**: Repository Acquisition & Ingestion Pipeline (URL validation, GitHub REST Client, Git cloning, File Indexer, Celery Tasks, Paginated REST API).
- [ ] **Phase 3**: Static Code Quality & Security Analyzers.
- [ ] **Phase 4**: AI Summary & Technical Debt Scoring.
- [ ] **Phase 5**: Full Frontend SaaS Dashboard Integration.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on code of conduct and submitting pull requests.
