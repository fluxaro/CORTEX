# ProjectIQ

> **Tagline**: *"Know your code before you clone it."*

ProjectIQ is an enterprise-grade, AI-powered Repository Intelligence Platform. The platform analyzes GitHub repositories and generates comprehensive, production-ready reports on Code Quality, Architecture, Security, Dependencies, Documentation, Git History, Testing, AI Summary, and Technical Debt.

---

## 🌟 Project Vision

Developers, team leads, and architects spend hours evaluating open-source software, legacy codebases, and third-party dependencies before integrating or cloning them. ProjectIQ bridges this gap by providing automated, deep-level repository intelligence before code lands on your local machine.

---

## 🏗️ Architecture & Engines

ProjectIQ uses an asynchronous background queue pipeline to handle repository ingestion, static code analysis, architecture intelligence, security intelligence, maintainability intelligence, and repository IQ calculation without blocking HTTP request execution.

```
+------------------+       +-------------------+       +-----------------------+
|  POST /repos     |  ---> | GitHub API Client |  ---> | Insert DB (PENDING)   |
+------------------+       +-------------------+       +-----------+-----------+
                                                                   |
                                                                   v
+--------------------+     +-------------------+       +-----------+-----------+
| Repository IQ Engine| <-- | Static, Arch, Sec |  <--- | Celery Git Clone Task |
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

### Maintainability & Repository Intelligence Engine Features (Deterministic, NO AI)
- **README & Documentation Analysis**: Markdown section parser evaluating 19 standard engineering sections, completeness percentage, badges, screenshots, architecture docs, API reference, deployment guides, developer guides, and doc generators (MkDocs, Docusaurus, Swagger, TypeDoc, Javadoc).
- **License & CHANGELOG Analysis**: Identifies licenses (MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, MPL-2.0, AGPL-3.0, LGPL-3.0, Unlicense, custom/missing), OSI approval, CHANGELOG presence, and Semantic Versioning compliance.
- **Testing Maturity Analysis**: Detects test runners (Pytest, Unittest, Jest, Vitest, Mocha, Ava, Go Test, JUnit, Cargo Test), counts test files/cases, unit/integration/e2e tests, mock/fixture usage, and computes testing score (0-100).
- **CI/CD Pipeline Analysis**: Detects CI providers (GitHub Actions, GitLab CI, Azure Pipelines, CircleCI, Jenkins, Travis CI) and classifies jobs for lint, test, build, deploy, release, security scans, and coverage.
- **Git History & Commit Quality**: Uses GitPython to extract commit count, contributor count, branch count, tag count, repository age, commit frequency (commits/week), inactive periods, Conventional Commits %, generic commits %, and commit quality score (0-100).
- **Open Source Community Standards**: Scans `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, issue templates, PR templates, and discussions.

### Repository IQ Engine & AI Intelligence Features
- **Weighted Repository IQ Score (0-100)**: Aggregates static analysis, architecture, security, documentation, testing, CI/CD, Git practices, health, and community scores using configurable weights.
- **Engineering Maturity Model**: Classifies repositories into *Prototype*, *Personal Project*, *Learning Project*, *Production Ready*, *Enterprise Ready*, or *Open Source Mature* with explainable criteria.
- **Technical Debt Estimation**: Estimates technical debt hours, days, and categories (Architecture, Security, Testing, Documentation, Maintainability, Dependency, Configuration) citing specific stored findings.
- **Industry Benchmarking**: Compares repository scores against best practice baselines and computes percentile rankings.
- **AI Provider Abstraction**: Extensible interface supporting OpenAI, Azure OpenAI, Anthropic, Gemini, Ollama, and a deterministic `MockProvider` for offline testing and fallback when credentials are unconfigured.
- **Prompt Engine**: Versioned prompt templates for Executive Summary, Technical Summary, Architecture Summary, Security Summary, Maintainability Summary, Improvement Roadmap, Technical Debt, Recruiter Summary, and Engineering Manager Summary.
- **Deterministic AI Generation**: The AI layer strictly consumes structured database metrics from previous phases without ever inspecting raw source code directly.

### Professional Frontend Dashboard Features
- **Modern SaaS UI Aesthetic**: Linear/Vercel/GitHub dark mode aesthetic with glassmorphic panels, glowing badges, tailored HSL color palettes, and micro-animations.
- **Complete Page Suite**: Landing Page, Repository List, Repository Overview, Static Analysis, Architecture with interactive React Flow dependency graph, Security SAST Findings, Documentation, Repository IQ & AI Insights, Settings, and 404.
- **Global Search Modal (Ctrl+K)**: Command palette keyboard shortcut search across repositories, security findings, and recommendations.
- **Interactive Recharts**: Radar charts, score gauges, technical debt breakdown bar charts, and industry benchmark percentile scores.
- **Responsive & Mobile Ready**: Full layout adaptation for Desktop, Tablet, and Mobile devices.

---

## 🗄️ Database Schema

### Ingestion & Static Analysis Tables
- `repositories`, `repository_file_indices`, `analysis_runs`, `repository_metrics`, `file_metrics`, `function_metrics`, `class_metrics`, `duplicate_groups`, `duplicate_files`, `code_smells`.

### Architecture Intelligence Engine Tables
- `architecture_analyses`, `architecture_layers`, `architecture_violations`, `detected_patterns`, `dependency_graphs`, `dependency_nodes`, `dependency_edges`, `framework_detections`, `technology_stacks`, `architecture_recommendation_placeholders`.

### Security Intelligence Engine Tables
- `security_analyses`, `security_findings`, `secret_findings`, `dependency_findings`, `configuration_findings`, `authentication_findings`, `authorization_findings`, `security_rules`, `security_references`, `security_summaries`.

### Maintainability Intelligence Engine Tables
- `documentation_analyses`, `documentation_sections`, `readme_analyses`, `testing_analyses`, `git_history_analyses`, `commit_analyses`, `release_analyses`, `community_analyses`, `ci_analyses`, `license_analyses`, `maintainability_metrics`, `repository_healths`.

### Repository IQ & AI Intelligence Tables
- `repository_iqs`, `repository_summaries`, `engineering_insights`, `technical_debts`, `improvement_recommendations`, `executive_summaries`, `technical_summaries`, `benchmark_results`, `ai_generations`, `prompt_templates`.

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

### Maintainability & Repository Intelligence Engine
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/v1/repositories/{id}/maintainability` | Trigger Maintainability Intelligence analysis |
| **GET** | `/api/v1/repositories/{id}/maintainability` | Get latest raw subsystem scores (Doc, Test, CI, Release, Health, Community) |
| **GET** | `/api/v1/repositories/{id}/documentation` | Get documentation completeness & README section breakdown |
| **GET** | `/api/v1/repositories/{id}/testing` | Get testing suite maturity & test file breakdown |
| **GET** | `/api/v1/repositories/{id}/git-history` | Get Git history, contributor count & development velocity |
| **GET** | `/api/v1/repositories/{id}/commits` | Get commit quality score & Conventional Commits percentage |
| **GET** | `/api/v1/repositories/{id}/releases` | Get release history & SemVer compliance |
| **GET** | `/api/v1/repositories/{id}/ci` | Get CI/CD automation providers & job breakdown |
| **GET** | `/api/v1/repositories/{id}/community` | Get open source community standards compliance |
| **GET** | `/api/v1/repositories/{id}/repository-health` | Get raw repository health breakdown metrics |

### Repository IQ Engine & AI Intelligence
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/v1/repositories/{id}/iq` | Trigger Repository IQ Engine calculation |
| **GET** | `/api/v1/repositories/{id}/iq` | Get overall Repository IQ report, score (0-100), and maturity classification |
| **GET** | `/api/v1/repositories/{id}/executive-summary` | Get Executive Summary report for executive leadership |
| **GET** | `/api/v1/repositories/{id}/technical-summary` | Get Technical Summary report for engineering managers |
| **GET** | `/api/v1/repositories/{id}/strengths` | Get identified repository architectural and code quality strengths |
| **GET** | `/api/v1/repositories/{id}/weaknesses` | Get identified repository architectural, security, and testing weaknesses |
| **GET** | `/api/v1/repositories/{id}/technical-debt` | Get technical debt hours, days, and category breakdown |
| **GET** | `/api/v1/repositories/{id}/recommendations` | Get paginated improvement recommendations categorized by timeframe and priority |
| **GET** | `/api/v1/repositories/{id}/benchmark` | Get industry benchmarking percentile scores against best practice baselines |

---

## 🛠️ Developer Guide

### 1. How to Run Frontend Locally
```bash
cd frontend
npm run dev
```

### 2. How to Build Frontend Production Bundle
```bash
cd frontend
npm run build
```

---

## 📁 Folder Structure

```
ProjectIQ/
├── backend/
│   ├── alembic/              # Database migration scripts (001 - 006)
│   ├── app/                  # FastAPI backend application
│   └── tests/                # Pytest test suite (52 tests)
├── frontend/
│   ├── src/
│   │   ├── components/       # Navbar, AddRepoModal, UI Components (Button, Card, Badge, ProgressBar, Modal, SearchModal)
│   │   │   └── charts/       # RadarScoreChart, TechnicalDebtChart, ScoreGauge, DependencyGraphVisualizer
│   │   ├── pages/            # LandingPage, RepoListPage, RepoOverviewPage, StaticAnalysisPage, ArchitecturePage, SecurityPage, DocumentationPage, RepositoryIQPage, SettingsPage, NotFoundPage
│   │   ├── services/         # apiClient, types, mockData, repositoryService
│   │   ├── App.tsx           # Primary routing & app container
│   │   ├── index.css         # Tailwind & glassmorphic styling
│   │   └── main.tsx          # React 18 DOM mount
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── Dockerfile                # Production multi-stage Dockerfile
├── docker-compose.yml        # Multi-container orchestration
└── README.md
```

---

## 🚀 Installation & Local Setup

### Prerequisites
- Python 3.13+
- Node.js 20+
- PostgreSQL & Redis (or Docker)

### Running the Application

1. **Backend**:
   ```bash
   uvicorn app.main:app --reload --app-dir backend
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access Application**:
   - **Frontend App**: `http://localhost:5173`
   - **Swagger Docs**: `http://localhost:8000/docs`

---

## 🗺️ Roadmap

- [x] **Phase 1**: Enterprise Foundation Architecture (FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, Celery, Redis, Docker, Quality tooling).
- [x] **Phase 2**: Repository Acquisition & Ingestion Pipeline (URL validation, GitHub REST Client, Git cloning, File Indexer, Celery Tasks, Paginated REST API).
- [x] **Phase 3**: Static Code Analysis Engine (Multi-language parsing for Python, TS, JS, Go, Java, Rust, Cyclomatic Complexity, Maintainability Index, Duplication Detection, Code Smells, Database Schema, Async Celery Pipeline & REST Endpoints).
- [x] **Phase 4**: Architecture Intelligence Engine (Architecture Style detection, Layer Detection, 20+ Design Patterns, Framework Conventions, Module Dependency Graph, Tech Stack Metadata, 10 DB Models, Celery Task & 7 REST Endpoints).
- [x] **Phase 5**: Security Intelligence Engine (SAST, Secret Detection, Infrastructure Config Scanner, Dependency Vulnerabilities, Static Security Rules, Auth/Authz Scanner, 10 DB Models, Celery Task & 8 REST Endpoints).
- [x] **Phase 6**: Maintainability & Repository Intelligence Engine (Deterministic evaluation of README completeness, Documentation structure, Testing maturity, CI/CD pipelines, Git history & Conventional Commits, Release tracking, Community standards, 12 DB Models, Celery Task & 10 REST Endpoints).
- [x] **Phase 7**: Repository IQ Engine & AI Intelligence (Weighted Repository IQ Score 0-100, Engineering Maturity Model, Technical Debt estimation, Industry benchmarking, AI Provider Abstraction, Prompt Engine, 10 DB Models, Celery Task & 9 REST Endpoints).
- [x] **Phase 8**: Professional Frontend Dashboard (React 19, TypeScript, Vite, Tailwind CSS, Recharts, React Flow, TanStack Query, Linear/Vercel SaaS design system, Full page suite, Ctrl+K Search).

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
