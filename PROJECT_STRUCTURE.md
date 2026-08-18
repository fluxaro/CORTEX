# ProjectIQ — Comprehensive Project Structure & Active Features Guide

> **ProjectIQ** is an enterprise-grade Repository Intelligence Platform that inspects any public or private Git repository using static analysis, AI, and industry benchmarking to produce a comprehensive engineering quality report — without executing any untrusted code.

---

## 📑 Table of Contents

1. [System Architecture Overview](#1-system-architecture-overview)
2. [Project Directory & File-by-File Reference](#2-project-directory--file-by-file-reference)
   - [Root Directory Configuration & Infrastructure](#root-directory-configuration--infrastructure)
   - [GitHub CI/CD & Workflows (`.github/`)](#github-cicd--workflows-github)
   - [Portfolio (`portfolio/`)](#portfolio-portfolio)
   - [Documentation & ADRs (`docs/`)](#documentation--adrs-docs)
   - [Assets (`assets/`)](#assets-assets)
   - [Backend Core Architecture (`backend/app/`)](#backend-core-architecture-backendapp)
   - [Backend Analysis Engines (`backend/app/analyzers/`)](#backend-analysis-engines-backendappanalyzers)
   - [Backend Tasks & Async Workers (`backend/app/tasks/` & `workers/`)](#backend-tasks--async-workers-backendapptasks--workers)
   - [Backend Database & Migrations (`backend/alembic/` & `database/`)](#backend-database--migrations-backendalembic--database)
   - [Backend Models & Schemas (`backend/app/models/` & `schemas/`)](#backend-models--schemas-backendappmodels--schemas)
   - [Backend API Endpoints (`backend/app/api/v1/`)](#backend-api-endpoints-backendappapiv1)
   - [Backend Services (`backend/app/services/`)](#backend-services-backendappservices)
   - [Backend Test Suite (`backend/tests/`)](#backend-test-suite-backendtests)
   - [Frontend Architecture (`frontend/src/`)](#frontend-architecture-frontend-src)
3. [Actively Working Features & Subsystems](#3-actively-working-features--subsystems)
   - [1. Static Code Analysis Subsystem](#1-static-code-analysis-subsystem)
   - [2. Architecture Intelligence Engine](#2-architecture-intelligence-engine)
   - [3. Security Intelligence Engine (SAST)](#3-security-intelligence-engine-sast)
   - [4. Maintainability & Repository Intelligence](#4-maintainability--repository-intelligence)
   - [5. Repository IQ Engine & AI Intelligence](#5-repository-iq-engine--ai-intelligence)
   - [6. Enterprise Collaboration Platform](#6-enterprise-collaboration-platform)
   - [7. Modern SaaS Frontend Subsystem](#7-modern-saas-frontend-subsystem)
4. [Data Flow & Analysis Pipeline Execution](#4-data-flow--analysis-pipeline-execution)

---

## 1. System Architecture Overview

ProjectIQ follows a decoupled, async-first microservices architecture:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         Frontend (React 18 + Vite)                       │
│    Landing · Dashboard · Analysis · Architecture · Security · IQ Report  │
│          Workspaces · Trends · Comparison · Audit Logs · Members         │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │ REST API (JSON / JWT)
┌───────────────────────────────▼──────────────────────────────────────────┐
│                      FastAPI REST API (Python 3.13)                      │
│   Rate Limiting · Request ID · JWT Auth · RBAC · OpenAPI 3.1 Validation   │
│     /api/v1/repositories · /analysis · /architecture · /security        │
│         /iq · /workspaces · /auth · /trends · /comparison · /logs        │
└───────────┬──────────────────────────────────────┬───────────────────────┘
            │ Async SQLAlchemy 2.x                  │ Celery Pipeline
┌───────────▼───────────┐                  ┌───────▼───────────────────────┐
│  PostgreSQL 15 (DB)   │                  │    Celery + Redis Worker      │
│  44+ Enterprise &     │                  │  clone · index · analyze      │
│  Analysis Tables      │                  │  security · arch · IQ · sync  │
└───────────────────────┘                  └───────────────────────────────┘
```

---

## 2. Project Directory & File-by-File Reference

### Root Directory Configuration & Infrastructure

| File Name | Purpose & Function |
| :--- | :--- |
| [`Dockerfile`](file:///home/lordex/ProjectIQ/Dockerfile) | Multi-stage Docker container specification for packaging the Python 3.13 FastAPI backend application. |
| [`docker-compose.yml`](file:///home/lordex/ProjectIQ/docker-compose.yml) | Orchestrates full stack services: PostgreSQL 15, Redis 7, FastAPI backend, Celery worker, and Vite frontend. |
| [`.env.example`](file:///home/lordex/ProjectIQ/.env.example) | Template listing required environment variables (PostgreSQL URI, Redis URL, JWT secrets, AI API keys, CORS). |
| [`.dockerignore`](file:///home/lordex/ProjectIQ/.dockerignore) | Excludes node_modules, Python virtual environments, Git histories, and temporary files from Docker image builds. |
| [`.editorconfig`](file:///home/lordex/ProjectIQ/.editorconfig) | Standardizes formatting rules (indentation size, charsets, trailing newlines) across different editors. |
| [`.gitignore`](file:///home/lordex/ProjectIQ/.gitignore) | Configures Git to ignore temporary files, secrets, build outputs, and node_modules. |
| [`.pre-commit-config.yaml`](file:///home/lordex/ProjectIQ/.pre-commit-config.yaml) | Pre-commit hook configuration running Ruff, Black, and Mypy checks automatically before commits. |
| [`README.md`](file:///home/lordex/ProjectIQ/README.md) | Primary project documentation containing badges, features, architecture diagrams, installation instructions, and API references. |
| [`CHANGELOG.md`](file:///home/lordex/ProjectIQ/CHANGELOG.md) | Tracks version history, new features, improvements, and bug fixes across releases. |
| [`CONTRIBUTING.md`](file:///home/lordex/ProjectIQ/CONTRIBUTING.md) | Guidelines for community code contributions, PR workflow, testing standards, and git branch naming. |
| [`CODE_OF_CONDUCT.md`](file:///home/lordex/ProjectIQ/CODE_OF_CONDUCT.md) | Contributor Covenant code of conduct outlining community behavior expectations. |
| [`SECURITY.md`](file:///home/lordex/ProjectIQ/SECURITY.md) | Security vulnerability disclosure process and posture details. |
| [`LICENSE`](file:///home/lordex/ProjectIQ/LICENSE) | Open-source MIT License text. |

---

### GitHub CI/CD & Workflows (`.github/`)

| File / Path | Purpose & Function |
| :--- | :--- |
| [`.github/workflows/ci.yml`](file:///home/lordex/ProjectIQ/.github/workflows/ci.yml) | GitHub Actions CI pipeline executing Ruff linting, Black formatting checks, Mypy type validation, Pytest suite (61 tests), and Vite build on every push/PR. |
| [`.github/workflows/release.yml`](file:///home/lordex/ProjectIQ/.github/workflows/release.yml) | Release workflow triggered on git tag publication to generate release notes and build artifacts. |
| [`.github/ISSUE_TEMPLATE/bug_report.md`](file:///home/lordex/ProjectIQ/.github/ISSUE_TEMPLATE/bug_report.md) | Standardized issue template for reporting bugs with steps to reproduce. |
| [`.github/PULL_REQUEST_TEMPLATE.md`](file:///home/lordex/ProjectIQ/.github/PULL_REQUEST_TEMPLATE.md) | PR template checklist verifying unit tests, documentation, and code formatting. |
| [`.github/CODEOWNERS`](file:///home/lordex/ProjectIQ/.github/CODEOWNERS) | Maps code directories to designated maintainer reviewers. |
| [`.github/dependabot.yml`](file:///home/lordex/ProjectIQ/.github/dependabot.yml) | Automated dependency update scanner configuration for GitHub. |

---

### Portfolio (`portfolio/`)

| File Path | Purpose & Function |
| :--- | :--- |
| [`portfolio/PROJECT.md`](file:///home/lordex/ProjectIQ/portfolio/PROJECT.md) | Comprehensive engineering portfolio document detailing the problem, solution, engineering challenges, architecture highlights, tech stack rationale, performance metrics, and future roadmap. |

---

### Documentation & ADRs (`docs/`)

| File Path | Purpose & Function |
| :--- | :--- |
| [`docs/RELEASE-NOTES-v1.0.0.md`](file:///home/lordex/ProjectIQ/docs/RELEASE-NOTES-v1.0.0.md) | Formal release notes for version 1.0.0 highlighting major subsystems and metrics. |
| [`docs/adr/0001-architecture-intelligence-engine-static-parsing.md`](file:///home/lordex/ProjectIQ/docs/adr/0001-architecture-intelligence-engine-static-parsing.md) | ADR 0001: Architecture Intelligence via pure static AST parsing vs dynamic execution. |
| [`docs/adr/0002-repository-iq-weighted-scoring-model.md`](file:///home/lordex/ProjectIQ/docs/adr/0002-repository-iq-weighted-scoring-model.md) | ADR 0002: Repository IQ weighted scoring algorithm definition and subsystem balance. |
| [`docs/adr/0003-enterprise-rbac-and-workspace-isolation.md`](file:///home/lordex/ProjectIQ/docs/adr/0003-enterprise-rbac-and-workspace-isolation.md) | ADR 0003: Multi-tenant workspace data isolation and 5-level RBAC authorization model. |
| [`docs/adr/0004-why-fastapi.md`](file:///home/lordex/ProjectIQ/docs/adr/0004-why-fastapi.md) | ADR 0004: Selection of FastAPI for async performance and OpenAPI 3.1 autogeneration. |
| [`docs/adr/0005-why-postgresql.md`](file:///home/lordex/ProjectIQ/docs/adr/0005-why-postgresql.md) | ADR 0005: Rationale for PostgreSQL relational schema and JSONB metrics storage. |
| [`docs/adr/0006-why-celery-and-redis.md`](file:///home/lordex/ProjectIQ/docs/adr/0006-why-celery-and-redis.md) | ADR 0006: Asynchronous task pipeline using Celery and Redis as message broker. |
| [`docs/adr/0007-why-react-vite-tanstack-query.md`](file:///home/lordex/ProjectIQ/docs/adr/0007-why-react-vite-tanstack-query.md) | ADR 0007: Single Page Application architecture using React 18, Vite, and TanStack Query. |
| [`docs/adr/0008-why-sqlalchemy-repository-pattern.md`](file:///home/lordex/ProjectIQ/docs/adr/0008-why-sqlalchemy-repository-pattern.md) | ADR 0008: Async SQLAlchemy 2.x ORM coupled with the Repository Pattern. |
| [`docs/adr/0009-why-ai-provider-abstraction.md`](file:///home/lordex/ProjectIQ/docs/adr/0009-why-ai-provider-abstraction.md) | ADR 0009: Pluggable AI Provider factory supporting OpenAI, Gemini, Anthropic, and offline fallback. |
| [`docs/adr/0010-why-docker.md`](file:///home/lordex/ProjectIQ/docs/adr/0010-why-docker.md) | ADR 0010: Containerization standard using Docker and Docker Compose. |
| [`docs/system-design/high-level-design.md`](file:///home/lordex/ProjectIQ/docs/system-design/high-level-design.md) | High-level system architecture and component interaction diagram. |
| [`docs/system-design/authentication-flow.md`](file:///home/lordex/ProjectIQ/docs/system-design/authentication-flow.md) | Detailed authentication sequence (JWT issuing, refresh tokens, OAuth 2.0 flow). |
| [`docs/system-design/repository-analysis-pipeline.md`](file:///home/lordex/ProjectIQ/docs/system-design/repository-analysis-pipeline.md) | Pipeline sequence diagram detailing repository ingestion, indexing, static analysis, SAST, and IQ scoring. |
| [`docs/demo/demo-script.md`](file:///home/lordex/ProjectIQ/docs/demo/demo-script.md) | Interactive demonstration walkthrough script for presenting ProjectIQ features. |
| [`docs/wiki/`](file:///home/lordex/ProjectIQ/docs/wiki/) | Complete set of 14 GitHub Wiki pages (Getting-Started, API-Guide, Database-Schema, System-Architecture, etc.). |

---

### Assets (`assets/`)

| File Path | Purpose & Function |
| :--- | :--- |
| [`assets/screenshots/README.md`](file:///home/lordex/ProjectIQ/assets/screenshots/README.md) | Catalog of application UI screenshots embedded across project documentation. |

---

### Backend Core Architecture (`backend/app/`)

| File Path | Purpose & Function |
| :--- | :--- |
| [`backend/app/main.py`](file:///home/lordex/ProjectIQ/backend/app/main.py) | FastAPI application factory, middleware registration (CORS, Request ID, Rate Limiting), global exception handling, lifecycle events, and router inclusion. |
| [`backend/app/core/config/settings.py`](file:///home/lordex/ProjectIQ/backend/app/core/config/settings.py) | Pydantic `BaseSettings` manager validating environment variables, database connections, Redis URLs, JWT secrets, and AI provider configurations. |
| [`backend/app/core/logging.py`](file:///home/lordex/ProjectIQ/backend/app/core/logging.py) | Structured JSON logging setup injecting unique request IDs into log records for end-to-end tracing. |
| [`backend/app/core/security/jwt.py`](file:///home/lordex/ProjectIQ/backend/app/core/security/jwt.py) | Lightweight JWT encoding, decoding, and validation using Python standard library (`hmac`, `hashlib`, `json`, `base64`). |
| [`backend/app/core/security/password.py`](file:///home/lordex/ProjectIQ/backend/app/core/security/password.py) | Argon2 / Bcrypt secure password hashing and verification functions. |
| [`backend/app/core/security/rbac.py`](file:///home/lordex/ProjectIQ/backend/app/core/security/rbac.py) | Role-Based Access Control matrix enforcing 5 permission tiers (Owner, Admin, Maintainer, Developer, Viewer). |
| [`backend/app/core/oauth/providers.py`](file:///home/lordex/ProjectIQ/backend/app/core/oauth/providers.py) | OAuth client integrations for authenticating users via GitHub, GitLab, and Bitbucket. |
| [`backend/app/core/ai/base_provider.py`](file:///home/lordex/ProjectIQ/backend/app/core/ai/base_provider.py) | `BaseAIProvider` abstract interface defining requirements for AI summary generation implementations. |
| [`backend/app/core/ai/factory.py`](file:///home/lordex/ProjectIQ/backend/app/core/ai/factory.py) | `AIProviderFactory` instantiating requested providers (OpenAI, Anthropic, Gemini, Azure OpenAI, Ollama, or MockProvider). |
| [`backend/app/core/ai/providers/mock_provider.py`](file:///home/lordex/ProjectIQ/backend/app/core/ai/providers/mock_provider.py) | Offline mock AI provider producing realistic executive, technical, and recruiter summaries without API calls. |
| [`backend/app/core/ai/prompts/templates.py`](file:///home/lordex/ProjectIQ/backend/app/core/ai/prompts/templates.py) | Prompt templates for persona-based summaries (Executive, Technical, Recruiter, Engineering Manager). |
| [`backend/app/middleware/request_id.py`](file:///home/lordex/ProjectIQ/backend/app/middleware/request_id.py) | HTTP middleware attaching a unique UUID request ID header (`X-Request-ID`) to every incoming request. |
| [`backend/app/middleware/rate_limit.py`](file:///home/lordex/ProjectIQ/backend/app/middleware/rate_limit.py) | Token bucket rate limiting middleware enforcing client request thresholds. |
| [`backend/app/exceptions/custom_exceptions.py`](file:///home/lordex/ProjectIQ/backend/app/exceptions/custom_exceptions.py) | Application domain exceptions (e.g. `RepositoryNotFoundException`, `UnauthorizedException`). |
| [`backend/app/exceptions/handlers.py`](file:///home/lordex/ProjectIQ/backend/app/exceptions/handlers.py) | Global exception handlers converting python exceptions into standardized JSON error responses. |

---

### Backend Analysis Engines (`backend/app/analyzers/`)

| File Path | Purpose & Function |
| :--- | :--- |
| [`backend/app/analyzers/detector.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/detector.py) | Core analyzer dispatcher routing source code files to language-specific parsers based on extension and contents. |
| [`backend/app/analyzers/base/base_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/base/base_analyzer.py) | Abstract base class for all language-specific code analyzers. |
| [`backend/app/analyzers/base/engine.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/base/engine.py) | Orchestration engine running configured code analyzers against file trees. |
| [`backend/app/analyzers/base/registry.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/base/registry.py) | Dynamic registry tracking active language analyzers. |
| [`backend/app/analyzers/shared/metrics.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/shared/metrics.py) | Math formulas calculating Cyclomatic Complexity and Maintainability Index (0–100). |
| [`backend/app/analyzers/shared/smells.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/shared/smells.py) | Rules for identifying code smells (Long Function, God Class, Deep Nesting, Large File). |
| [`backend/app/analyzers/shared/duplication.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/shared/duplication.py) | Window-hash rolling fingerprinting algorithm detecting cross-file code duplication. |
| [`backend/app/analyzers/python/python_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/python/python_analyzer.py) | Python AST parser extracting class/function nodes, cyclomatic complexity, docstrings, imports. |
| [`backend/app/analyzers/typescript/typescript_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/typescript/typescript_analyzer.py) | TypeScript & JavaScript static analyzer parsing functions, classes, interfaces, imports. |
| [`backend/app/analyzers/javascript/javascript_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/javascript/javascript_analyzer.py) | JavaScript static analyzer parsing JS/JSX structures. |
| [`backend/app/analyzers/go/go_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/go/go_analyzer.py) | Go static analyzer extracting packages, structs, functions, channels, and complexity. |
| [`backend/app/analyzers/java/java_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/java/java_analyzer.py) | Java static analyzer parsing classes, interfaces, annotations, methods, and complexity. |
| [`backend/app/analyzers/rust/rust_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/rust/rust_analyzer.py) | Rust static analyzer parsing modules, functions, structs, impl blocks, and macros. |
| [`backend/app/analyzers/architecture/engine.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/architecture/engine.py) | Orchestration engine coordinating architecture detectors and dependency graph creation. |
| [`backend/app/analyzers/architecture/detectors/arch_detector.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/architecture/detectors/arch_detector.py) | Classifies repository architecture style (Clean Architecture, Hexagonal, Layered, MVC, MVVM, Microservices, CQRS, Monolith). |
| [`backend/app/analyzers/architecture/detectors/pattern_detector.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/architecture/detectors/pattern_detector.py) | AST structural matching engine detecting 20+ design patterns (Singleton, Factory, Repository, Observer, Strategy, Decorator, Adapter, Facade, Command, etc.). |
| [`backend/app/analyzers/architecture/detectors/dependency_graph.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/architecture/detectors/dependency_graph.py) | Builds module-level import dependency maps and generates React Flow node/edge structures. |
| [`backend/app/analyzers/architecture/detectors/layer_detector.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/architecture/detectors/layer_detector.py) | Flags architectural boundary violations (e.g., presentation layer directly querying database). |
| [`backend/app/analyzers/architecture/detectors/framework_detector.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/architecture/detectors/framework_detector.py) | Identifies backend and frontend frameworks (FastAPI, Django, React, Next.js, Spring Boot, Express, Gin). |
| [`backend/app/analyzers/architecture/detectors/config_tech_detector.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/architecture/detectors/config_tech_detector.py) | Identifies infrastructure technologies (Docker, Kubernetes, Terraform, GitHub Actions, Redis, Postgres). |
| [`backend/app/analyzers/security/engine.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/security/engine.py) | SAST security engine coordinator running all security scanners. |
| [`backend/app/analyzers/security/base_scanner.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/security/base_scanner.py) | Abstract base class for security scanner modules. |
| [`backend/app/analyzers/security/registry.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/security/registry.py) | Registry tracking available SAST scanners. |
| [`backend/app/analyzers/security/scanners/secret_detector.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/security/scanners/secret_detector.py) | Secret scanner combining Shannon entropy calculations with regex pattern signatures for cloud API keys, OAuth tokens, SSH keys, JWT secrets. |
| [`backend/app/analyzers/security/scanners/sast_rules.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/security/scanners/sast_rules.py) | Static security rule engine identifying SQL injection, path traversal, XSS, dangerous functions (`eval`, `exec`), and unsafe deserialization. |
| [`backend/app/analyzers/security/scanners/dependency_scanner.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/security/scanners/dependency_scanner.py) | Dependency vulnerability scanner auditing `package.json`, `requirements.txt`, `Cargo.toml`, and `go.mod` against known CVEs. |
| [`backend/app/analyzers/security/scanners/config_scanner.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/security/scanners/config_scanner.py) | Infrastructure configuration scanner auditing Dockerfile (root execution), Kubernetes YAMLs, and CI/CD workflow security flags. |
| [`backend/app/analyzers/security/scanners/auth_scanner.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/security/scanners/auth_scanner.py) & [`authz_scanner.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/security/scanners/authz_scanner.py) | Scans for authentication and authorization flaws (weak password hashing, insecure CORS, missing HttpOnly flags, unauthenticated routes). |
| [`backend/app/analyzers/maintainability/engine.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/maintainability/engine.py) | Maintainability intelligence coordinator running documentation, testing, and repository analyzers. |
| [`backend/app/analyzers/maintainability/analyzers/readme_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/maintainability/analyzers/readme_analyzer.py) | Evaluates README.md completeness against 19 standard engineering documentation sections. |
| [`backend/app/analyzers/maintainability/analyzers/testing_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/maintainability/analyzers/testing_analyzer.py) | Analyzes testing maturity: framework detection (Pytest, Jest, JUnit, cargo test), test file count, test assertion density, estimated coverage. |
| [`backend/app/analyzers/maintainability/analyzers/ci_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/maintainability/analyzers/ci_analyzer.py) | Inspects CI/CD automation pipelines (.github/workflows, .gitlab-ci.yml, Jenkinsfile). |
| [`backend/app/analyzers/maintainability/analyzers/git_history_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/maintainability/analyzers/git_history_analyzer.py) | Computes Git velocity metrics: commit frequency, active authors, velocity trends, Conventional Commit compliance %. |
| [`backend/app/analyzers/maintainability/analyzers/community_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/maintainability/analyzers/community_analyzer.py) | Inspects community governance files (CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, issue templates). |
| [`backend/app/analyzers/maintainability/analyzers/license_changelog_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/maintainability/analyzers/license_changelog_analyzer.py) | Audits open-source license presence, validity, and CHANGELOG maintenance. |
| [`backend/app/analyzers/maintainability/analyzers/package_quality_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/maintainability/analyzers/package_quality_analyzer.py) | Checks package manifest configuration quality (pyproject.toml, package.json, Cargo.toml). |
| [`backend/app/analyzers/maintainability/analyzers/docs_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/maintainability/analyzers/docs_analyzer.py) | Measures in-code documentation and docstring coverage percentages across functions and classes. |
| [`backend/app/analyzers/iq/engine.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/iq/engine.py) | Main coordinator for the Repository IQ Engine. |
| [`backend/app/analyzers/iq/scorers/iq_scorer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/iq/scorers/iq_scorer.py) | Aggregates all 8 subsystem scores into a single weighted Repository IQ Score (0–100). |
| [`backend/app/analyzers/iq/weights.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/iq/weights.py) | Configurable weighted scoring matrix rules (ADR 0002). |
| [`backend/app/analyzers/iq/scorers/maturity_classifier.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/iq/scorers/maturity_classifier.py) | Classifies repository engineering maturity (Prototype, Personal, Learning, Production, Enterprise, Open Source Mature). |
| [`backend/app/analyzers/iq/scorers/technical_debt_calculator.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/iq/scorers/technical_debt_calculator.py) | Quantifies technical debt into hours and days, categorized by complexity, testing, security, and documentation. |
| [`backend/app/analyzers/iq/scorers/benchmarker.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/iq/scorers/benchmarker.py) | Computes percentile rankings against benchmark baselines. |
| [`backend/app/analyzers/iq/scorers/strengths_weaknesses_analyzer.py`](file:///home/lordex/ProjectIQ/backend/app/analyzers/iq/scorers/strengths_weaknesses_analyzer.py) | Extracts top repository strengths and actionable weaknesses with file citations. |

---

### Backend Tasks & Async Workers (`backend/app/tasks/` & `workers/`)

| File Path | Purpose & Function |
| :--- | :--- |
| [`backend/app/workers/celery_app.py`](file:///home/lordex/ProjectIQ/backend/app/workers/celery_app.py) | Celery worker application configuration connecting to Redis broker and result backend. |
| [`backend/app/tasks/repository_tasks.py`](file:///home/lordex/ProjectIQ/backend/app/tasks/repository_tasks.py) | Async tasks for cloning Git repositories safely and indexing file trees. |
| [`backend/app/tasks/analysis_tasks.py`](file:///home/lordex/ProjectIQ/backend/app/tasks/analysis_tasks.py) | Async task pipeline orchestrating language-specific static analysis. |
| [`backend/app/tasks/architecture_tasks.py`](file:///home/lordex/ProjectIQ/backend/app/tasks/architecture_tasks.py) | Async tasks executing architecture pattern detection and building dependency graphs. |
| [`backend/app/tasks/security_tasks.py`](file:///home/lordex/ProjectIQ/backend/app/tasks/security_tasks.py) | Async tasks executing SAST scanning, secret detection, and vulnerability audits. |
| [`backend/app/tasks/repository_intelligence_tasks.py`](file:///home/lordex/ProjectIQ/backend/app/tasks/repository_intelligence_tasks.py) | Async tasks computing maintainability metrics, README scores, and test coverage. |
| [`backend/app/tasks/repository_iq_tasks.py`](file:///home/lordex/ProjectIQ/backend/app/tasks/repository_iq_tasks.py) | Async tasks computing final weighted IQ scores, technical debt estimates, and AI summaries. |
| [`backend/app/tasks/enterprise_tasks.py`](file:///home/lordex/ProjectIQ/backend/app/tasks/enterprise_tasks.py) | Async tasks running scheduled repository background scans and multi-platform sync. |

---

### Backend Database & Migrations (`backend/alembic/` & `database/`)

| File Path | Purpose & Function |
| :--- | :--- |
| [`backend/alembic.ini`](file:///home/lordex/ProjectIQ/backend/alembic.ini) | Configuration file for Alembic database migration runner. |
| [`backend/alembic/env.py`](file:///home/lordex/ProjectIQ/backend/alembic/env.py) | Alembic migration script loading async engine and SQLAlchemy models metadata. |
| [`backend/alembic/versions/`](file:///home/lordex/ProjectIQ/backend/alembic/versions/) | 7 SQL migration scripts creating and updating 44+ PostgreSQL database tables (`001_initial_schema.py` through `007_...py`). |
| [`backend/app/database/base.py`](file:///home/lordex/ProjectIQ/backend/app/database/base.py) | Base class for declarative SQLAlchemy ORM models. |
| [`backend/app/database/session.py`](file:///home/lordex/ProjectIQ/backend/app/database/session.py) | Async SQLAlchemy engine factory (`create_async_engine`) and session generator (`get_db`). |

---

### Backend Models & Schemas (`backend/app/models/` & `schemas/`)

| Entity File | Purpose & Function |
| :--- | :--- |
| `models/base.py` | Shared mixin providing UUID primary keys, `created_at`, and `updated_at` timestamps. |
| `models/repository.py` | ORM tables for `Repository`, `Workspace`, `Organization`, `WorkspaceMember`, `GitPlatformConfig`. |
| `models/analysis.py` | ORM tables for `AnalysisRun`, `FileIndex`, `ComplexityMetric`, `CodeSmell`, `DuplicationMatch`. |
| `models/architecture.py` | ORM tables for `ArchitectureAnalysis`, `DesignPatternFinding`, `ModuleDependency`, `LayerViolation`. |
| `models/security.py` | ORM tables for `SecurityScan`, `SecretFinding`, `VulnerabilityFinding`, `ConfigFinding`, `AuthRuleFinding`. |
| `models/maintainability.py` | ORM tables for `MaintainabilityScore`, `ReadmeMetric`, `TestMetric`, `CiMetric`, `GitVelocityMetric`. |
| `models/iq.py` | ORM tables for `RepositoryIQScore`, `SubsystemScore`, `TechnicalDebtEstimate`, `BenchmarkPercentile`, `AISummary`. |
| `models/enterprise.py` | ORM tables for `AuditLog`, `Notification`, `ScheduledScan`, `TrendMetric`. |
| `schemas/*.py` | Pydantic v2 schemas mirroring models for request validation and typed JSON responses. |

---

### Backend API Endpoints (`backend/app/api/v1/`)

| Endpoint File | URI Route Prefix | Functionality |
| :--- | :--- | :--- |
| [`router.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/router.py) | `/api/v1` | Master router aggregating all REST endpoint sub-routers. |
| [`health.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/health.py) | `/health` | Health check endpoint returning database and Redis ping status. |
| [`version.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/version.py) | `/version` | System version and environment info. |
| [`auth.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/auth.py) | `/auth` | User login, registration, token refresh, and user profile (`/me`). |
| [`workspaces.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/workspaces.py) | `/workspaces` | Multi-tenant workspace CRUD, member management, and workspace switching. |
| [`organizations.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/organizations.py) | `/organizations` | Enterprise organization management and seat administration. |
| [`repositories.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/repositories.py) | `/repositories` | Repository registration, deletion, detail fetch, and status polling. |
| [`analysis.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/analysis.py) | `/repositories/{id}/analysis` | Static code analysis metrics, cyclomatic complexity, code smells, duplication. |
| [`architecture.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/architecture.py) | `/repositories/{id}/architecture` | Architecture style, design pattern findings, and module dependency graph payload. |
| [`security.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/security.py) | `/repositories/{id}/security` | SAST security vulnerabilities, detected secrets, CVEs, config flaws. |
| [`maintainability.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/maintainability.py) | `/repositories/{id}/maintainability` | Maintainability scores, README checklist, test metrics, Git velocity. |
| [`iq.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/iq.py) | `/repositories/{id}/iq` | Overall Repository IQ Score, technical debt breakdown, percentiles, AI summaries. |
| [`trends.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/trends.py) | `/trends` | Time-series historical trend metrics for repositories and workspaces. |
| [`comparison.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/comparison.py) | `/comparison` | Side-by-side comparative matrix across multiple repositories. |
| [`audit_logs.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/audit_logs.py) | `/audit-logs` | Queryable immutable enterprise audit trail logs. |
| [`notifications.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/notifications.py) | `/notifications` | User system notifications and read status toggle. |
| [`git_platforms.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/git_platforms.py) | `/git-platforms` | OAuth connection management for GitHub, GitLab, and Bitbucket. |
| [`webhooks.py`](file:///home/lordex/ProjectIQ/backend/app/api/v1/endpoints/webhooks.py) | `/webhooks` | Inbound webhooks handling push events and pull requests from Git platforms. |

---

### Backend Services (`backend/app/services/`)

| File Path | Purpose & Function |
| :--- | :--- |
| [`auth_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/auth_service.py) | Handles user authentication, password verification, registration, and JWT token issuance. |
| [`repository_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/repository_service.py) | Repository CRUD business logic, workspace scoping, and cloning trigger. |
| [`analysis_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/analysis_service.py) | Executes static code analysis, complexity scoring, and stores file metrics. |
| [`architecture_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/architecture_service.py) | Architecture analysis workflow, pattern extraction, dependency graph generation. |
| [`security_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/security_service.py) | Security SAST scan execution, secret detection, vulnerability classification. |
| [`maintainability_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/maintainability_service.py) | Maintainability calculation, test maturity evaluation, README documentation scoring. |
| [`iq_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/iq_service.py) | Weighted IQ score computation, technical debt estimation, benchmarking, AI summaries. |
| [`workspace_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/workspace_service.py) | Workspace creation, multi-tenant isolation, member role assignments. |
| [`audit_log_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/audit_log_service.py) | Writes immutable security audit records for all destructive or administrative operations. |
| [`git_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/git_service.py) | Safely clones public/private repositories into isolated temporary directories. |
| [`github_client.py`](file:///home/lordex/ProjectIQ/backend/app/services/github_client.py) | GitHub API client fetching metadata, commit history, issues, pull requests, releases. |
| [`git_platform_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/git_platform_service.py) | Unified abstraction layer for multi-platform sync (GitHub, GitLab, Bitbucket). |
| [`indexer_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/indexer_service.py) | Deep directory file tree indexer classifying languages and file structures. |
| [`comparison_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/comparison_service.py) | Computes side-by-side benchmark matrices comparing multiple repositories. |
| [`trend_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/trend_service.py) | Aggregates historical metrics over time for trend line visualizations. |
| [`notification_service.py`](file:///home/lordex/ProjectIQ/backend/app/services/notification_service.py) | Dispatches in-app notifications to workspace members. |

---

### Backend Test Suite (`backend/tests/`)

ProjectIQ includes 61 automated tests passing across the backend:

| Test File Name | Purpose & Coverage |
| :--- | :--- |
| `test_analysis_api.py` | Validates static analysis REST endpoints and file metric responses. |
| `test_architecture_api.py` | Tests architecture intelligence endpoints, design pattern findings, and graphs. |
| `test_security_api.py` | Tests SAST security REST endpoints and secret reporting. |
| `test_iq_api.py` | Validates Repository IQ score calculation endpoints and debt output. |
| `test_repositories_api.py` | Tests repository registration, list filters, and status polling. |
| `test_maintainability_api.py` | Tests maintainability endpoints, test scores, and README checklist. |
| `test_health.py` & `test_version.py` | Validates system health check and version endpoints. |
| `test_startup.py` | Verifies FastAPI application initialization and middleware setup. |
| `test_python_analyzer.py` | Tests Python AST parsing, cyclomatic complexity, function/class detection. |
| `test_typescript_analyzer.py` | Tests TypeScript & JavaScript AST & regex static parsing. |
| `test_go_analyzer.py` | Tests Go language parser for structs, functions, and metrics. |
| `test_pattern_detector.py` | Tests AST pattern detector for Singleton, Factory, Repository, Strategy, etc. |
| `test_arch_detector.py` | Tests architecture style classification (Clean, Layered, Hexagonal). |
| `test_dependency_graph.py` | Verifies module dependency graph generation logic. |
| `test_secret_detector.py` | Tests Shannon entropy secret scanning and regex token matching. |
| `test_sast_rules.py` | Tests static security rules (SQL injection, path traversal, XSS, eval). |
| `test_dependency_scanner.py` | Tests CVE dependency scanner across package manifests. |
| `test_config_scanner.py` | Tests Dockerfile, Kubernetes, and CI/CD security audit rules. |
| `test_auth_authz_scanner.py` | Tests authentication and authorization security scanner rules. |
| `test_readme_analyzer.py` | Tests README completeness scoring across documentation sections. |
| `test_testing_analyzer.py` | Tests test framework detection and coverage estimation. |
| `test_ci_analyzer.py` | Tests CI/CD pipeline automation scanner. |
| `test_git_history_analyzer.py` | Tests Git velocity, commit frequency, and author metrics. |
| `test_iq_scorer.py` | Tests weighted scoring matrix aggregation and subsystem balancing. |
| `test_maturity_classifier.py` | Tests engineering maturity stage classification algorithm. |
| `test_technical_debt_calculator.py` | Tests technical debt conversion formulas (hours/days by category). |
| `test_complexity_metrics.py` | Tests Cyclomatic Complexity and Maintainability Index math. |
| `test_duplicate_detection.py` | Tests window-hash rolling duplication detector. |
| `test_docs_analyzer.py` | Tests in-code docstring coverage analyzer. |
| `test_ai_provider.py` | Tests `AIProviderFactory` and `MockProvider` summary generation. |
| `test_prompt_engine.py` | Tests executive, technical, and recruiter prompt templates. |
| `test_github_client.py` & `test_git_service.py` | Tests GitHub API client and safe repository cloning service. |
| `test_indexer_service.py` | Tests file tree indexer and language detection. |
| `test_enterprise.py` | Tests multi-tenant workspace isolation, RBAC permissions, and audit logs. |
| `test_config_tech_detector.py` | Tests infrastructure tech detector. |
| `test_framework_detector.py` | Tests backend/frontend framework detector. |
| `test_analyzer_registry.py` | Tests dynamic code analyzer registry. |

---

### Frontend Architecture (`frontend/src/`)

#### Build & Configuration Files

| File Path | Purpose & Function |
| :--- | :--- |
| [`frontend/package.json`](file:///home/lordex/ProjectIQ/frontend/package.json) | Lists frontend npm dependencies (React 18, Vite, Tailwind, Recharts, React Flow, TanStack Query, Lucide icons). |
| [`frontend/tsconfig.json`](file:///home/lordex/ProjectIQ/frontend/tsconfig.json) | TypeScript configuration for React SPA build. |
| [`frontend/vite.config.ts`](file:///home/lordex/ProjectIQ/frontend/vite.config.ts) | Vite build tool configuration, dev server proxy, and path aliases. |
| [`frontend/tailwind.config.js`](file:///home/lordex/ProjectIQ/frontend/tailwind.config.js) | Custom Tailwind theme (dark mode color palette, typography, custom animations). |
| [`frontend/postcss.config.js`](file:///home/lordex/ProjectIQ/frontend/postcss.config.js) | PostCSS plugin configuration processing Tailwind CSS. |
| [`frontend/src/index.css`](file:///home/lordex/ProjectIQ/frontend/src/index.css) | Global Tailwind directives, dark theme tokens, and custom scrollbar styling. |
| [`frontend/src/main.tsx`](file:///home/lordex/ProjectIQ/frontend/src/main.tsx) | React application DOM mounting entrypoint. |
| [`frontend/src/App.tsx`](file:///home/lordex/ProjectIQ/frontend/src/App.tsx) | Master React SPA router, layout shell, React Query client provider, and navigation routes. |

#### Services & API Integration (`frontend/src/services/`)

| File Path | Purpose & Function |
| :--- | :--- |
| [`apiClient.ts`](file:///home/lordex/ProjectIQ/frontend/src/services/apiClient.ts) | Axios HTTP client configured with request interceptors, JWT authorization header injection, and base URL config. |
| [`repositoryService.ts`](file:///home/lordex/ProjectIQ/frontend/src/services/repositoryService.ts) | API service methods wrapping backend REST endpoints (repositories, analysis, architecture, security, IQ, workspaces). |
| [`types.ts`](file:///home/lordex/ProjectIQ/frontend/src/services/types.ts) | TypeScript interfaces and types for API responses, repositories, findings, security alerts, and IQ scores. |
| [`mockData.ts`](file:///home/lordex/ProjectIQ/frontend/src/services/mockData.ts) & [`mockEnterpriseData.ts`](file:///home/lordex/ProjectIQ/frontend/src/services/mockEnterpriseData.ts) | Realistic mock datasets enabling full offline UI demonstration without a running backend. |

#### UI Components (`frontend/src/components/ui/`)

| Component File | Purpose & Function |
| :--- | :--- |
| `cn.ts` | Utility helper merging Tailwind classes cleanly using `clsx` and `tailwind-merge`. |
| `Button.tsx` | Reusable button component with variants (primary, secondary, outline, danger, ghost, small/large). |
| `Card.tsx` | Container card component with header, title, action buttons, and content body. |
| `Badge.tsx` | Status and severity pill badge component (success, warning, error, info, high, critical). |
| `Modal.tsx` | Accessible overlay modal dialog component. |
| `Alert.tsx` | Alert banner component for displaying warnings, error messages, or info callouts. |
| `ProgressBar.tsx` | Visual progress bar component with custom color accents and percentage fill. |
| `SkeletonLoader.tsx` | Skeleton loading placeholder component for asynchronous data loading states. |
| `EmptyState.tsx` | Visual empty state placeholder component when search or lists return zero results. |
| `SearchModal.tsx` | Command palette modal triggered via `Ctrl+K` for global search across repositories and pages. |

#### Data Visualization Charts (`frontend/src/components/charts/`)

| Chart Component File | Purpose & Function |
| :--- | :--- |
| `ScoreGauge.tsx` | Circular SVG score gauge component displaying Repository IQ (0–100) with dynamic color gradient. |
| `RadarScoreChart.tsx` | Recharts radar chart component rendering score breakdowns across all 8 engineering dimensions. |
| `TechnicalDebtChart.tsx` | Recharts bar and pie chart displaying technical debt hours broken down by subsystem category. |
| `DependencyGraphVisualizer.tsx` | Interactive React Flow graph component rendering module import dependencies with zoom, drag, and node selection. |

#### Layout & Action Components (`frontend/src/components/`)

| Component File | Purpose & Function |
| :--- | :--- |
| `Navbar.tsx` | Top header navigation bar with logo, workspace selector, `Ctrl+K` search bar, notification counter, and user profile menu. |
| `AddRepoModal.tsx` | Modal dialog for registering a new public or private Git repository URL for static analysis. |

#### Page Views (`frontend/src/pages/`)

| Page Component | Path Route | Description & Capabilities |
| :--- | :--- | :--- |
| `LandingPage.tsx` | `/` | Product homepage featuring headline banner, problem statement, interactive feature breakdown, architecture overview, and quickstart instructions. |
| `LoginPage.tsx` | `/login` | User login screen with JWT authentication form and OAuth social login buttons. |
| `RegisterPage.tsx` | `/register` | User sign-up screen with account creation and initial workspace setup. |
| `WorkspaceDashboardPage.tsx` | `/dashboard` | Main workspace dashboard showing average IQ score, top repositories, recent activity feed, and quick actions. |
| `OrganizationDashboardPage.tsx` | `/organization` | Enterprise organization management page showing member seats, organization settings, and overall team performance. |
| `RepoListPage.tsx` | `/repositories` | Searchable, filterable list of indexed repositories with status indicators, language tags, and IQ badges. |
| `RepoOverviewPage.tsx` | `/repositories/:id` | Repository hero overview dashboard summarizing key health indicators, language composition, commit velocity, and recent analysis status. |
| `RepositoryIQPage.tsx` | `/repositories/:id/iq` | Full Repository IQ report page featuring 0–100 gauge score, radar chart, engineering maturity classification, technical debt breakdown, percentile benchmarks, and AI executive summary. |
| `StaticAnalysisPage.tsx` | `/repositories/:id/analysis` | Deep code quality view listing cyclomatic complexity metrics per function/class, maintainability index, detected code smells, and cross-file duplication findings. |
| `ArchitecturePage.tsx` | `/repositories/:id/architecture` | Architecture view showing detected architecture style, 20+ design pattern findings, framework detection, and interactive React Flow dependency graph. |
| `SecurityPage.tsx` | `/repositories/:id/security` | SAST security dashboard listing detected secrets (with Shannon entropy score), static code security vulnerabilities, CVEs, Docker/K8s config flaws, and auth rules. |
| `TrendAnalysisPage.tsx` | `/repositories/:id/trends` | Historical time-series trend line charts tracking IQ score changes, security vulnerability resolution, and technical debt reduction over time. |
| `RepoComparisonPage.tsx` | `/comparison` | Side-by-side comparative matrix comparing two or more repositories across IQ score, complexity, debt, and security metrics. |
| `ScanHistoryPage.tsx` | `/repositories/:id/history` | Audit log history of all past analysis runs with execution durations and completion statuses. |
| `MembersPage.tsx` | `/members` | Workspace member administration page managing team seats and assigning RBAC roles (Owner, Admin, Maintainer, Developer, Viewer). |
| `AuditLogsPage.tsx` | `/audit-logs` | Enterprise security audit trail table displaying searchable logs of administrative and destructive workspace actions. |
| `NotificationsPage.tsx` | `/notifications` | In-app user notifications list with filterable unread status and system alerts. |
| `RepoSyncPage.tsx` | `/repo-sync` | Git platform sync page managing GitHub, GitLab, and Bitbucket OAuth connections and webhook settings. |
| `SettingsPage.tsx` | `/settings` | Account and workspace settings page for configuring user preferences and API credentials. |
| `DocumentationPage.tsx` | `/docs` | Integrated in-app documentation center and API guide. |
| `NotFoundPage.tsx` | `*` | Custom 404 page screen for handling invalid routes. |

---

## 3. Actively Working Features & Subsystems

ProjectIQ features **7 actively working engineering subsystems**:

### 1. Static Code Analysis Subsystem
- **Multi-Language AST Parsing**: Supports Python, TypeScript, JavaScript, Go, Java, and Rust AST analysis without code execution.
- **Complexity Metrics**: Computes Cyclomatic Complexity and Maintainability Index (0–100) per function, method, and class.
- **Code Smell Detection**: Rules detecting Long Functions, God Classes, Deep Nesting (>4 levels), and Large Files (>500 lines).
- **Cross-File Duplication Detection**: Rolling window-hash algorithm (Rabin fingerprinting) identifying duplicate code blocks across files.

### 2. Architecture Intelligence Engine
- **Architecture Style Detection**: Classifies codebases into 10+ architectural styles (Clean Architecture, Hexagonal, Layered, MVC, MVVM, Microservices, CQRS, Monolith).
- **Design Pattern Detector**: Uses AST structural matching to identify 20+ design patterns (Singleton, Factory, Builder, Repository, Strategy, Observer, Adapter, Decorator, Facade, Command, etc.).
- **Dependency Graph Engine**: Extracts module-level import dependencies and constructs node/edge payloads for visual rendering.
- **Layer Boundary Enforcement**: Flags architectural violations where higher-level tiers bypass domain constraints.
- **Tech Stack & Framework Identification**: Auto-detects frameworks (FastAPI, Django, React, Next.js, Spring Boot, Express) and infra tech (Docker, Kubernetes, Terraform).

### 3. Security Intelligence Engine (SAST)
- **Secret Scanning with Shannon Entropy**: Detects AWS/GCP/Azure cloud keys, OAuth tokens, Stripe keys, SSH/PEM keys, and JWT secrets using high-entropy calculation and regex signatures.
- **Static Vulnerability Scanner (SAST)**: Rules identifying SQL Injection, Path Traversal, Cross-Site Scripting (XSS), dangerous dynamic functions (`eval`, `exec`), and weak crypto.
- **Dependency CVE Audit**: Parses `package.json`, `requirements.txt`, `Cargo.toml`, and `go.mod` against known vulnerability records.
- **Infrastructure Config Security Audit**: Audits Dockerfiles (e.g. root user execution), Kubernetes YAML manifests, and GitHub Actions workflows for security misconfigurations.
- **Auth & Authorization Audit**: Checks password hashing algorithm quality, CORS policies, HttpOnly cookie flags, and unauthenticated endpoints.

### 4. Maintainability & Repository Intelligence
- **README Documentation Scorer**: Evaluates documentation completeness across 19 standard engineering sections (Installation, Usage, Architecture, License, API, etc.).
- **Test Suite Maturity Analysis**: Detects test frameworks (Pytest, Jest, Vitest, JUnit, Cargo test), computes test-to-code file ratios, assertion density, and estimated coverage.
- **CI/CD Pipeline Breakdown**: Inspects `.github/workflows`, `.gitlab-ci.yml`, `Jenkinsfile`, and CircleCI configurations.
- **Git Velocity Metrics**: Measures commit frequency, active author count, release cadence, and Conventional Commit adoption %.
- **Community & Governance Health**: Checks for `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and issue/PR templates.

### 5. Repository IQ Engine & AI Intelligence
- **Weighted IQ Score (0–100)**: Aggregates metrics across 8 dimensions using a documented weighted scoring matrix (ADR 0002).
- **Engineering Maturity Classifier**: Categorizes repositories into 6 maturity tiers (*Prototype*, *Personal*, *Learning*, *Production*, *Enterprise*, *Open Source Mature*).
- **Technical Debt Quantifier**: Converts quality findings into estimated hours and days of debt, broken down by category.
- **Industry Percentile Benchmarking**: Compares repository health against baseline percentiles.
- **Pluggable AI Provider Abstraction**: Supports OpenAI, Anthropic, Gemini, Azure OpenAI, Ollama, or an offline `MockProvider` generating persona-based executive and technical summaries.

### 6. Enterprise Collaboration Platform
- **Multi-Tenant Workspaces**: Isolated workspace contexts with unique data boundaries.
- **5-Level RBAC**: Permission enforcement across *Owner*, *Admin*, *Maintainer*, *Developer*, and *Viewer* roles.
- **Multi-Platform OAuth Integration**: Integration with GitHub, GitLab, and Bitbucket for repository imports and webhook automation.
- **Time-Series Trend Analysis**: Tracks IQ scores, vulnerability resolution, and technical debt over time.
- **Repository Comparison Engine**: Side-by-side comparative benchmarking matrix across multiple repositories.
- **Immutable Security Audit Log**: Immutable record of all workspace modifications and administrative actions.

### 7. Modern SaaS Frontend Subsystem
- **Dark-Mode Design System**: Styled dark mode inspired by modern developer platforms (Linear, Vercel, GitHub).
- **Interactive React Flow Dependency Graph**: Drag-and-drop, zoomable architecture visualizer.
- **Recharts Visualizations**: Score gauges, 8-dimension radar charts, technical debt bar charts, and trend lines.
- **Command Palette (`Ctrl+K`)**: Global search modal for jumping between pages and repositories.

---

## 4. Data Flow & Analysis Pipeline Execution

When a user submits a repository URL for analysis, ProjectIQ processes it through an asynchronous task pipeline:

```
[ User Input: Git URL ] 
          │
          ▼
[ POST /api/v1/repositories ] ── (Returns 202 Accepted + Task ID immediately)
          │
          ▼
[ Celery Task: repository_tasks.clone_and_index ]
    │ Clone repository safely to temp directory (No code execution)
    │ Index file tree, detect languages, count lines of code
    │
    ▼
[ Celery Task: analysis_tasks.run_static_analysis ]
    │ Parse Python, JS/TS, Go, Java, Rust ASTs
    │ Compute Cyclomatic Complexity, Maintainability Index, smells, duplication
    │
    ▼
[ Celery Task: architecture_tasks.run_architecture_analysis ]
    │ Detect architecture styles & 20+ design patterns
    │ Extract module dependencies & build React Flow graph nodes
    │
    ▼
[ Celery Task: security_tasks.run_security_scan ]
    │ Run secret detector (Shannon entropy + regex)
    │ Audit dependencies for CVEs & check Docker/K8s configs
    │
    ▼
[ Celery Task: repository_intelligence_tasks.run_maintainability_scan ]
    │ Score README sections, evaluate test maturity, check Git velocity
    │
    ▼
[ Celery Task: repository_iq_tasks.compute_iq_score ]
    │ Aggregate 8 subsystem scores into weighted 0-100 IQ Score
    │ Calculate technical debt hours & determine maturity tier
    │ Invoke AI Provider factory for summary generation
    │ Write complete report atomically to PostgreSQL
          │
          ▼
[ Frontend React App ] ── (Polls GET /repositories/{id}/iq -> Renders IQ Report & Dashboards)
```

---
*Created as an authoritative reference for ProjectIQ codebase architecture and active features.*
