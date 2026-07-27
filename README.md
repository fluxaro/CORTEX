# ProjectIQ

> **Tagline**: *"Know your code before you clone it."*

ProjectIQ is an enterprise-grade, AI-powered Repository Intelligence Platform. The platform analyzes GitHub repositories and generates comprehensive, production-ready reports on Code Quality, Architecture, Security, Dependencies, Documentation, Git History, Testing, AI Summary, and Technical Debt.

---

## 🌟 Project Vision

Developers, team leads, and architects spend hours evaluating open-source software, legacy codebases, and third-party dependencies before integrating or cloning them. ProjectIQ bridges this gap by providing automated, deep-level repository intelligence before code lands on your local machine.

---

## 🏗️ Architecture & Static Analysis Engine

ProjectIQ uses an asynchronous background queue pipeline to handle repository ingestion, metadata indexing, and static code analysis without blocking HTTP request execution.

```
+------------------+       +-------------------+       +-----------------------+
|  POST /repos     |  ---> | GitHub API Client |  ---> | Insert DB (PENDING)   |
+------------------+       +-------------------+       +-----------+-----------+
                                                                   |
                                                                   v
+--------------------+     +-------------------+       +-----------+-----------+
| Analysis COMPLETED | <-- | Static Engine     |  <--- | Celery Git Clone Task |
+--------------------+     +-------------------+       +-----------------------+
```

### Static Analysis Features
- **Multi-Language Parsing**: Dedicated AST & pattern parsers for **Python**, **TypeScript**, **JavaScript**, **Go**, **Java**, and **Rust**.
- **Metrics Calculation**: Cyclomatic complexity, Maintainability Index (0-100), LOC breakdown (code, blank, comment lines), comment ratios, complexity rank grading (A-F).
- **Code Smell Detector**: Long functions (>50 LOC), Large classes (>20 methods), Deep nesting (>4 levels), Too many parameters (>5 params), God objects, Long files (>500 LOC).
- **Duplication Analysis**: Cross-file window hashing algorithm returning duplicate groups, occurrence locations, and repository duplication percentage.

---

## 🗄️ Database Schema

### Ingestion Tables
- `repositories`: Main repository metadata and status (`PENDING`, `CLONING`, `READY`, `FAILED`).
- `repository_file_indices`: Directory structure stats, file count, max depth, largest files, extension distribution.

### Analysis Engine Tables
- `analysis_runs`: Tracks analysis execution status (`PENDING`, `RUNNING`, `COMPLETED`, `FAILED`), timestamps, commit hash.
- `repository_metrics`: Aggregated repository LOC, comment ratio, average/max cyclomatic complexity, complexity rank grade, maintainability index, duplicate percentage.
- `file_metrics`: Per-file metrics, function count, class count, import count, complexity, maintainability index.
- `function_metrics`: Function/method level metrics, parameters, return annotation, decorators, visibility (`public`/`private`), method type (`instance`/`static`/`class`/`abstract`), complexity, nesting depth.
- `class_metrics`: Class level metrics, base classes, method count, field count, property count, public/private method counts.
- `duplicate_groups` & `duplicate_files`: Identifies duplicate code hashes, line counts, instance counts, and exact file line ranges.
- `code_smells`: Catalog of architectural & quality smells with line numbers, severity, symbol names, and descriptions.

---

## 📡 REST API Endpoints

### Repository Management
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/v1/health` | Service health status |
| **GET** | `/api/v1/version` | Service name and version |
| **POST** | `/api/v1/repositories` | Ingest new public GitHub repository |
| **GET** | `/api/v1/repositories` | List repositories (with pagination, filtering & sorting) |
| **GET** | `/api/v1/repositories/{id}` | Get repository details & file system index |
| **DELETE** | `/api/v1/repositories/{id}` | Delete repository & cleanup local clone storage |

### Static Code Analysis
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/v1/repositories/{id}/analyze` | Trigger new static code analysis run |
| **GET** | `/api/v1/repositories/{id}/analysis` | Get status of latest analysis run |
| **GET** | `/api/v1/repositories/{id}/metrics` | Get aggregated repository engineering metrics |
| **GET** | `/api/v1/repositories/{id}/files` | Paginated file-level metrics |
| **GET** | `/api/v1/repositories/{id}/functions` | Paginated function-level metrics |
| **GET** | `/api/v1/repositories/{id}/classes` | Paginated class-level metrics |
| **GET** | `/api/v1/repositories/{id}/smells` | Paginated code smells & findings |

---

## 🛠️ Developer Guide: Adding a New Language Analyzer

To extend ProjectIQ with support for a new language (e.g. C++ or Kotlin):

1. **Implement `BaseLanguageAnalyzer`**:
   Create a new class under `app/analyzers/{language}/{language}_analyzer.py` subclassing `BaseLanguageAnalyzer`:
   ```python
   from app.analyzers.base.base_analyzer import BaseLanguageAnalyzer
   from app.analyzers.shared.models import FileAnalysisResult

   class KotlinAnalyzer(BaseLanguageAnalyzer):
       @property
       def language_name(self) -> str:
           return "Kotlin"

       @property
       def supported_extensions(self) -> list[str]:
           return [".kt", ".kts"]

       def analyze_file(self, rel_path: str, content: str, file_size: int = 0) -> FileAnalysisResult:
           loc, comment_lines, blank_lines, code_lines = self.count_lines(content)
           # Extract functions, classes, imports, complexity...
           return FileAnalysisResult(...)
   ```

2. **Register Analyzer**:
   In `app/analyzers/base/engine.py`, register the new analyzer instance with `AnalyzerRegistry.register(KotlinAnalyzer())`.

3. **Add Unit Tests**:
   Add unit tests in `tests/test_kotlin_analyzer.py` validating parsing and metric calculations.

---

## 📁 Folder Structure

```
ProjectIQ/
├── backend/
│   ├── alembic/              # Database migration scripts (001_create_repository, 002_create_analysis)
│   ├── app/
│   │   ├── api/              # API routes & versioning (/api/v1/)
│   │   ├── core/             # Configuration & logging system
│   │   ├── database/         # SQLAlchemy engine & session management
│   │   ├── models/           # Declarative ORM models (Repository, AnalysisRun, Metrics, Smells)
│   │   ├── schemas/          # Pydantic v2 validation models
│   │   ├── services/         # GitHubClient, GitService, FileIndexerService, AnalysisService
│   │   ├── repositories/     # Data access abstraction layer
│   │   ├── tasks/            # Celery tasks (clone_repository_task, static_analysis_task)
│   │   ├── analyzers/        # Extensible Static Code Analysis Engine
│   │   │   ├── base/         # BaseLanguageAnalyzer, AnalyzerRegistry, StaticAnalysisEngine
│   │   │   ├── shared/       # Models, metrics math, code smells, duplication detector
│   │   │   ├── python/       # Python AST analyzer
│   │   │   ├── typescript/   # TypeScript/TSX analyzer
│   │   │   ├── javascript/   # JavaScript/JSX analyzer
│   │   │   ├── go/           # Go analyzer
│   │   │   ├── java/         # Java analyzer
│   │   │   └── rust/         # Rust analyzer
│   │   ├── middleware/       # Custom FastAPI middlewares
│   │   ├── exceptions/       # Custom exceptions & global handlers
│   │   ├── dependencies/     # FastAPI dependency injection
│   │   └── workers/          # Celery worker initialization
│   ├── tests/                # Pytest test suite (27 tests covering ingestion, analyzers & APIs)
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
- [x] **Phase 3**: Static Code Analysis Engine (Multi-language parsing for Python, TS, JS, Go, Java, Rust, Cyclomatic Complexity, Maintainability Index, Duplication Detection, Code Smells, Database Schema, Async Celery Pipeline & REST Endpoints).
- [ ] **Phase 4**: Security, Dependency & AI Intelligence Engine.
- [ ] **Phase 5**: Full Frontend SaaS Dashboard Integration.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on code of conduct and submitting pull requests.
