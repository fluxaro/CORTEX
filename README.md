# ProjectIQ

> **Tagline**: *"Know your code before you clone it."*

ProjectIQ is an enterprise-grade, AI-powered Repository Intelligence Platform. The platform analyzes GitHub repositories and generates comprehensive, production-ready reports on Code Quality, Architecture, Security, Dependencies, Documentation, Git History, Testing, AI Summary, and Technical Debt.

---

## 🌟 Project Vision

Developers, team leads, and architects spend hours evaluating open-source software, legacy codebases, and third-party dependencies before integrating or cloning them. ProjectIQ bridges this gap by providing automated, deep-level repository intelligence before code lands on your local machine.

---

## 🏗️ Architecture & Engines

ProjectIQ uses an asynchronous background queue pipeline to handle repository ingestion, static code analysis, architecture intelligence, and security intelligence without blocking HTTP request execution.

```
+------------------+       +-------------------+       +-----------------------+
|  POST /repos     |  ---> | GitHub API Client |  ---> | Insert DB (PENDING)   |
+------------------+       +-------------------+       +-----------+-----------+
                                                                   |
                                                                   v
+--------------------+     +-------------------+       +-----------+-----------+
| Security Engine    | <-- | Static & Arch     |  <--- | Celery Git Clone Task |
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

### Security Intelligence Engine Features (SAST)
- **Secret Detection**: Detects committed AWS keys, GCP keys, Azure keys, GitHub/GitLab tokens, OpenAI, Stripe, Twilio, Firebase, DB connection strings (Postgres, Mongo, Redis), JWT secrets, SSH/RSA/PEM keys, OAuth/Bearer tokens, Webhooks, Passwords, and high-entropy strings with masking and Shannon entropy scores.
- **Infrastructure Configuration Scanning**: Scans `.env`, `Dockerfile`, `docker-compose.yml`, GitHub Actions, K8s YAML, Terraform, Nginx, Apache configs for debug mode enabled, weak ports, missing security headers, default credentials, privileged/root containers, open ports, and dangerous Docker instructions.
- **Dependency Security Scanning**: Inspects `package.json`, `poetry.lock`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml` for outdated/deprecated packages, known CVEs, unmaintained libraries, license conflicts, CVSS scores, severity, and reference URLs.
- **Static Security Rules (SAST)**: Language-aware static analysis for dangerous functions (`eval`, `exec`, `pickle.loads`, `subprocess(shell=True)`, `os.system`, `Runtime.exec`), `dangerouslySetInnerHTML`, `innerHTML`, weak cryptography (MD5, SHA1), weak random, hardcoded credentials, string-concatenated SQL injection, path traversal, and unsafe YAML deserialization.
- **Authentication & Authorization Analysis**: Analyzes authentication mechanisms, password hashing algorithms (BCrypt, Argon2, PBKDF2, MD5, SHA1, missing hashing), web security controls (CORS, HttpOnly, Secure cookie flags), and authorization/RBAC protection on admin routes.
- **Severity Model**: Every finding is categorized into standard severity levels: `Critical`, `High`, `Medium`, `Low`, or `Informational`.

---

## 🗄️ Database Schema

### Ingestion & Static Analysis Tables
- `repositories`, `repository_file_indices`, `analysis_runs`, `repository_metrics`, `file_metrics`, `function_metrics`, `class_metrics`, `duplicate_groups`, `duplicate_files`, `code_smells`.

### Architecture Intelligence Engine Tables
- `architecture_analyses`, `architecture_layers`, `architecture_violations`, `detected_patterns`, `dependency_graphs`, `dependency_nodes`, `dependency_edges`, `framework_detections`, `technology_stacks`, `architecture_recommendation_placeholders`.

### Security Intelligence Engine Tables
- `security_analyses`: Primary run table storing finding counts by severity (`critical_count`, `high_count`, `medium_count`, `low_count`, `info_count`) and breakdown metrics.
- `security_findings`: Detailed SAST security findings with severity, confidence, category, language, file, line, column, description, remediation placeholder, reference URL, and CVSS score.
- `secret_findings`: Hardcoded secrets findings with entropy score and masked values.
- `dependency_findings`: Vulnerable third-party package dependencies with CVE ID, CVSS score, severity, and reference URLs.
- `configuration_findings`: Infrastructure misconfigurations in Dockerfiles, env files, and K8s configs.
- `authentication_findings`: Authentication weaknesses and password hashing findings.
- `authorization_findings`: Authorization and RBAC findings on endpoints.
- `security_rules`: Security rule definition catalog.
- `security_references`: Security reference links (CWE, OWASP, NVD).
- `security_summaries`: Summary metrics and most vulnerable files.

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

### Security Intelligence Engine (SAST)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/v1/repositories/{id}/security` | Trigger Security Intelligence analysis |
| **GET** | `/api/v1/repositories/{id}/security` | Get latest security report & raw dashboard metrics |
| **GET** | `/api/v1/repositories/{id}/security/findings` | Paginated SAST findings (filterable by severity, language, category) |
| **GET** | `/api/v1/repositories/{id}/security/secrets` | Paginated committed secret findings |
| **GET** | `/api/v1/repositories/{id}/security/dependencies` | Paginated dependency vulnerability findings |
| **GET** | `/api/v1/repositories/{id}/security/configuration` | Paginated configuration findings |
| **GET** | `/api/v1/repositories/{id}/security/authentication` | Paginated authentication findings |
| **GET** | `/api/v1/repositories/{id}/security/authorization` | Paginated authorization findings |

---

## 🛠️ Developer Guide

### 1. How to Create a New Security Rule
Add a new rule tuple to `SASTRules.SAST_RULES` in `app/analyzers/security/scanners/sast_rules.py`:
```python
("SEC-014", "Unsafe Deserialization", "Deserialization", r"marshal\.loads\(", "HIGH", "Python", "Unsafe marshal deserialization allows arbitrary code execution.")
```

### 2. How to Register a New Security Scanner
Create a scanner subclassing `BaseSecurityScanner` in `app/analyzers/security/scanners/my_scanner.py`:
```python
from app.analyzers.security.base_scanner import BaseSecurityScanner
from app.analyzers.security.models import SecurityAnalysisResult

class CustomSecurityScanner(BaseSecurityScanner):
    @property
    def scanner_name(self) -> str:
        return "CustomSecurityScanner"

    def scan(self, target_path: str, file_contents: dict[str, str], extra_context=None) -> SecurityAnalysisResult:
        # Perform custom scanning logic...
        return SecurityAnalysisResult(...)
```
Then register it in `SecurityScannerRegistry`:
```python
SecurityScannerRegistry.register(CustomSecurityScanner())
```

---

## 📁 Folder Structure

```
ProjectIQ/
├── backend/
│   ├── alembic/              # Database migration scripts (001, 002, 003, 004_create_security_tables)
│   ├── app/
│   │   ├── api/              # API routes & versioning (/api/v1/)
│   │   ├── core/             # Configuration & logging system
│   │   ├── database/         # SQLAlchemy engine & session management
│   │   ├── models/           # Declarative ORM models (Repository, Analysis, Architecture, Security)
│   │   ├── schemas/          # Pydantic v2 validation models
│   │   ├── services/         # RepositoryService, AnalysisService, ArchitectureService, SecurityService
│   │   ├── tasks/            # Celery tasks (clone, static_analysis, architecture_analysis, security_analysis)
│   │   ├── analyzers/        # Analysis Engines
│   │   │   ├── base/         # BaseLanguageAnalyzer, AnalyzerRegistry, StaticAnalysisEngine
│   │   │   ├── shared/       # Models, metrics math, code smells, duplication detector
│   │   │   ├── architecture/ # Architecture Intelligence Engine & Detectors
│   │   │   └── security/     # Security Intelligence Engine (SAST)
│   │   │       ├── base_scanner.py # BaseSecurityScanner interface
│   │   │       ├── registry.py     # SecurityScannerRegistry
│   │   │       ├── engine.py       # SecurityIntelligenceEngine
│   │   │       ├── models.py       # Data transfer objects
│   │   │       └── scanners/       # SecretDetector, ConfigScanner, DependencyScanner, SASTRules, AuthScanner, AuthzScanner
│   ├── tests/                # Pytest test suite (40 tests covering ingestion, static, architecture & security APIs)
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
- [x] **Phase 5**: Security Intelligence Engine (SAST, Secret Detection, Infrastructure Config Scanner, Dependency Vulnerabilities, Static Security Rules, Auth/Authz Scanner, 10 DB Models, Celery Task & 8 REST Endpoints).

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
