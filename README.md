# ProjectIQ

> **Tagline**: *"Know your code before you clone it."*

ProjectIQ is an enterprise-grade, AI-powered Repository Intelligence Platform. The platform analyzes GitHub repositories and generates comprehensive, production-ready reports on Code Quality, Architecture, Security, Dependencies, Documentation, Git History, Testing, AI Summary, and Technical Debt.

---

## 🌟 Project Vision

Developers, team leads, and architects spend hours evaluating open-source software, legacy codebases, and third-party dependencies before integrating or cloning them. ProjectIQ bridges this gap by providing automated, deep-level repository intelligence before code lands on your local machine.

---

## 🏗️ Architecture & Static Engines

ProjectIQ uses an asynchronous background queue pipeline to handle repository ingestion, static code analysis, and architecture intelligence without blocking HTTP request execution.

```
+------------------+       +-------------------+       +-----------------------+
|  POST /repos     |  ---> | GitHub API Client |  ---> | Insert DB (PENDING)   |
+------------------+       +-------------------+       +-----------+-----------+
                                                                   |
                                                                   v
+--------------------+     +-------------------+       +-----------+-----------+
| Arch Engine Done   | <-- | Static & Arch     |  <--- | Celery Git Clone Task |
+--------------------+     +-------------------+       +-----------------------+
```

### Static Analysis Features
- **Multi-Language Parsing**: Dedicated AST & pattern parsers for **Python**, **TypeScript**, **JavaScript**, **Go**, **Java**, and **Rust**.
- **Metrics Calculation**: Cyclomatic complexity, Maintainability Index (0-100), LOC breakdown, comment ratios, complexity rank grading (A-F).
- **Code Smell Detector**: Long functions (>50 LOC), Large classes (>20 methods), Deep nesting (>4 levels), Too many parameters (>5 params), God objects, Long files (>500 LOC).
- **Duplication Analysis**: Cross-file window hashing algorithm returning duplicate groups, occurrence locations, and repository duplication percentage.

### Architecture Intelligence Engine Features
- **Supported Architecture Styles**: Monolith, Layered Architecture, Clean Architecture, Hexagonal/Ports & Adapters, Onion, Feature-Based, MVC, MVVM, Microservices, Event-Driven, CQRS.
- **Framework Detection & Conventions**: Detects FastAPI, Django, Flask, Next.js, React, Express, NestJS, Spring Boot, Gin, Echo, Fiber, Actix, Rocket, Axum and validates convention compliance.
- **20+ Design Patterns**: Detects Repository, Factory, Singleton, Builder, Strategy, Observer, Decorator, Facade, Adapter, Proxy, DI, Command, State, Chain of Resp., Template Method, Specification, Unit of Work, DTO, Mapper, Service Locator with confidence scores.
- **Module Dependency Graph**: Directed graph tracking internal/external dependencies, circular import detection, cross-layer violation validation, coupling score, modularity score, layer separation score, and dependency direction score.
- **Tech Stack & API Surface**: Extracted metadata for containers, CI/CD, DBs, ORMs, and API surfaces (REST, GraphQL, gRPC, WebSocket, SSE, Background Workers, Cron Jobs).

---

## 🗄️ Database Schema

### Ingestion & Static Analysis Tables
- `repositories`, `repository_file_indices`, `analysis_runs`, `repository_metrics`, `file_metrics`, `function_metrics`, `class_metrics`, `duplicate_groups`, `duplicate_files`, `code_smells`.

### Architecture Intelligence Engine Tables
- `architecture_analyses`: Primary table for architecture style, confidence score, and raw score metrics (layer separation, dependency direction, pattern confidence, organization, coupling, modularity).
- `architecture_layers`: Mapped file hierarchy across Presentation, Application, Domain, Infrastructure, and Utilities/Shared.
- `architecture_violations`: Cross-layer violations, circular import loops, and dependency direction inversions.
- `detected_patterns`: Identified design patterns with category and confidence score.
- `dependency_graphs`, `dependency_nodes`, `dependency_edges`: Full directed module import graph.
- `framework_detections`: Installed framework findings and convention compliance.
- `technology_stacks`: Extracted tech stack metadata (languages, frameworks, DBs, CI/CD, containers, etc.).
- `architecture_recommendation_placeholders`: Placeholder table for future recommendation engines.

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

### Architecture Intelligence Engine
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/v1/repositories/{id}/architecture` | Trigger Architecture Intelligence analysis |
| **GET** | `/api/v1/repositories/{id}/architecture` | Get latest architecture report & scores |
| **GET** | `/api/v1/repositories/{id}/patterns` | Paginated design patterns findings |
| **GET** | `/api/v1/repositories/{id}/layers` | Identified architectural layers & files |
| **GET** | `/api/v1/repositories/{id}/dependency-graph` | Full module dependency graph (nodes & edges) |
| **GET** | `/api/v1/repositories/{id}/frameworks` | Detected frameworks & convention compliance |
| **GET** | `/api/v1/repositories/{id}/technologies` | Extracted technology stack metadata |

---

## 🛠️ Developer Guide

### 1. How to Implement a New Language Analyzer
Subclass `BaseLanguageAnalyzer` under `app/analyzers/{language}/{language}_analyzer.py` and register it with `AnalyzerRegistry.register(...)` in `app/analyzers/base/engine.py`.

### 2. How to Implement a New Architecture Detector
Add detection rules in `ArchDetector` under `app/analyzers/architecture/detectors/arch_detector.py`:
```python
if "domain/" in paths_str and "infrastructure/" in paths_str:
    return "MyCustomArchitecture", 0.90
```

### 3. How to Implement a New Framework Detector
Add a new tuple definition in `FrameworkDetector.FRAMEWORK_INDICATORS` under `app/analyzers/architecture/detectors/framework_detector.py`:
```python
("SvelteKit", "Fullstack Framework", r"(?i)@sveltejs/kit", "TypeScript")
```

---

## 📁 Folder Structure

```
ProjectIQ/
├── backend/
│   ├── alembic/              # Database migration scripts (001, 002, 003_create_architecture)
│   ├── app/
│   │   ├── api/              # API routes & versioning (/api/v1/)
│   │   ├── core/             # Configuration & logging system
│   │   ├── database/         # SQLAlchemy engine & session management
│   │   ├── models/           # Declarative ORM models (Repository, Analysis, Architecture)
│   │   ├── schemas/          # Pydantic v2 validation models
│   │   ├── services/         # RepositoryService, AnalysisService, ArchitectureService
│   │   ├── tasks/            # Celery tasks (clone, static_analysis, architecture_analysis)
│   │   ├── analyzers/        # Static Analysis & Architecture Intelligence Engines
│   │   │   ├── base/         # BaseLanguageAnalyzer, AnalyzerRegistry, StaticAnalysisEngine
│   │   │   ├── shared/       # Models, metrics math, code smells, duplication detector
│   │   │   ├── python/       # Python AST analyzer
│   │   │   ├── typescript/   # TypeScript/TSX analyzer
│   │   │   ├── javascript/   # JavaScript/JSX analyzer
│   │   │   ├── go/           # Go analyzer
│   │   │   ├── java/         # Java analyzer
│   │   │   ├── rust/         # Rust analyzer
│   │   │   └── architecture/ # Architecture Intelligence Engine & Detectors
│   │   │       ├── detectors/# ArchDetector, LayerDetector, PatternDetector, FrameworkDetector, DependencyGraphBuilder, ConfigTechDetector
│   │   │       ├── engine.py # ArchitectureIntelligenceEngine
│   │   │       └── models.py # Data transfer objects
│   ├── tests/                # Pytest test suite (34 tests covering ingestion, analyzers, architecture & APIs)
│   ├── alembic.ini           # Alembic configuration
│   └── pyproject.toml        # Tooling config (Ruff, Black, Mypy, Pytest)
├── storage/
│   └── repositories/         # Cloned repository code storage ({repository_id})
├── frontend/                 # Vite React TypeScript Tailwind CSS placeholder
├── Dockerfile                # Production multi-stage Dockerfile
├── docker-compose.yml        # Multi-container orchestration (Backend, Postgres, Redis, Worker)
└── README.md
```

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
   - **Swagger Docs**: `http://localhost:8000/docs`

---

## 🗺️ Roadmap

- [x] **Phase 1**: Enterprise Foundation Architecture (FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, Celery, Redis, Docker, Quality tooling).
- [x] **Phase 2**: Repository Acquisition & Ingestion Pipeline (URL validation, GitHub REST Client, Git cloning, File Indexer, Celery Tasks, Paginated REST API).
- [x] **Phase 3**: Static Code Analysis Engine (Multi-language parsing for Python, TS, JS, Go, Java, Rust, Cyclomatic Complexity, Maintainability Index, Duplication Detection, Code Smells, Database Schema, Async Celery Pipeline & REST Endpoints).
- [x] **Phase 4**: Architecture Intelligence Engine (Architecture Style detection, Layer Detection, 20+ Design Patterns, Framework Conventions, Module Dependency Graph, Tech Stack Metadata, 10 DB Models, Celery Task & 7 REST Endpoints).
- [ ] **Phase 5**: Full Frontend SaaS Dashboard Integration.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
