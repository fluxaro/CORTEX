# ProjectIQ

> **Tagline**: *"Know your code before you clone it."*

ProjectIQ is an enterprise-grade, AI-powered Repository Intelligence Platform. The platform analyzes GitHub, GitLab, and Bitbucket repositories and generates comprehensive, production-ready reports on Code Quality, Architecture, Security, Dependencies, Documentation, Git History, Testing, AI Summary, and Technical Debt.

---

## 🌟 Project Vision

Developers, team leads, and architects spend hours evaluating open-source software, legacy codebases, and third-party dependencies before integrating or cloning them. ProjectIQ bridges this gap by providing automated, deep-level repository intelligence before code lands on your local machine.

---

## 🏗️ Architecture & Engines

ProjectIQ uses an asynchronous background queue pipeline to handle repository ingestion, static code analysis, architecture intelligence, security intelligence, maintainability intelligence, repository IQ calculation, git platform synchronization, and enterprise webhooks without blocking HTTP request execution.

```
+------------------+       +-------------------+       +-----------------------+
|  POST /repos     |  ---> | Git Platform Client| ---> | Insert DB (PENDING)   |
+------------------+       +-------------------+       +-----------+-----------+
                                                                   |
                                                                   v
+--------------------+     +-------------------+       +-----------+-----------+
| Enterprise & IQ    | <-- | Static, Arch, Sec |  <--- | Celery Git Clone Task |
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

### Enterprise Collaboration & Git Integration Features (Phase 9)
- **Multi-Tenant Workspaces & Organizations**: Supports Personal Workspaces, Enterprise Organization Workspaces, member seats, and workspace settings.
- **Role-Based Access Control (RBAC)**: Enforces permission hierarchy across `OWNER`, `ADMIN`, `MAINTAINER`, `DEVELOPER`, and `VIEWER` roles.
- **Authentication & OAuth**: PBKDF2 password hashing, JWT Access & Refresh token management, and OAuth authorization flows for GitHub, GitLab, and Bitbucket.
- **Git Platform Integrations**: Repository import, metadata synchronization, default branch selection, and webhook registration across GitHub, GitLab, and Bitbucket.
- **Webhooks Infrastructure**: Handles incoming `push`, `pull_request`, `release`, `tag`, and `branch` events with background Celery task dispatching.
- **Scheduled Scans & History**: Automated daily, weekly, and monthly scan schedules, execution history logs, cancellation, and retries.
- **Time-Series Trend Analysis**: Computes and stores historical snapshots of Repository IQ, Security, Architecture, Complexity, and Technical Debt over time with interactive Recharts line charts.
- **Repository Comparison Engine**: Side-by-side comparative matrix comparing multiple repositories or scan versions across engineering metrics.
- **In-App Notifications**: Real-time notification infrastructure for security findings, scan completions, and invitations.
- **Immutable Audit Logging**: Compliance audit trail logging authentication, repository imports, permission updates, and setting modifications.

---

## 🗄️ Database Schema

### Enterprise Tables (Phase 9)
- `users`, `user_preferences`, `organizations`, `workspaces`, `memberships`, `invitations`, `api_tokens`, `repository_syncs`, `webhooks`, `notifications`, `audit_logs`, `scan_histories`, `trend_metrics`, `repository_comparisons`.

### Core Repository IQ & Intelligence Tables
- `repositories`, `repository_file_indices`, `analysis_runs`, `repository_metrics`, `file_metrics`, `function_metrics`, `class_metrics`, `duplicate_groups`, `duplicate_files`, `code_smells`, `architecture_analyses`, `security_analyses`, `maintainability_metrics`, `repository_iqs`, `repository_summaries`, `engineering_insights`, `technical_debts`, `improvement_recommendations`, `benchmark_results`, `ai_generations`.

---

## 📡 REST API Endpoints

### Enterprise & Authentication
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/v1/auth/register` | Register new user account |
| **POST** | `/api/v1/auth/login` | Authenticate user with email & password |
| **POST** | `/api/v1/auth/refresh` | Refresh JWT access token |
| **GET** | `/api/v1/auth/oauth/{provider}` | Get OAuth authorization URL |
| **GET** | `/api/v1/workspaces` | List user workspaces |
| **POST** | `/api/v1/workspaces` | Create personal or org workspace |
| **GET** | `/api/v1/workspaces/{id}/members` | List workspace active members |
| **POST** | `/api/v1/workspaces/{id}/invitations` | Invite team member with RBAC role |
| **POST** | `/api/v1/organizations` | Create enterprise organization |
| **POST** | `/api/v1/git-platforms/{provider}/import` | Import remote repo from GitHub, GitLab, Bitbucket |
| **POST** | `/api/v1/webhooks/{provider}` | Webhook receiver endpoint |
| **GET** | `/api/v1/repositories/{id}/trends` | Get time-series trend metrics |
| **POST** | `/api/v1/comparison/compare` | Compare multiple repositories |
| **GET** | `/api/v1/notifications` | List user in-app notifications |
| **GET** | `/api/v1/audit-logs` | Fetch immutable audit trail |

---

## 🛠️ Developer Guide

### 1. How to Run Backend Tests & Linting
```bash
# Pytest Test Suite (61 passing tests)
$env:PYTHONPATH="backend"; .venv\Scripts\pytest.exe backend/tests

# Code Quality Audits
.venv\Scripts\ruff.exe check backend
.venv\Scripts\black.exe --check backend
$env:PYTHONPATH="backend"; .venv\Scripts\mypy.exe --config-file backend/pyproject.toml backend/app
```

### 2. How to Build Frontend Production Bundle
```bash
cd frontend
npm run build
```

---

## 🗺️ Roadmap

- [x] **Phase 1**: Enterprise Foundation Architecture
- [x] **Phase 2**: Repository Acquisition & Ingestion Pipeline
- [x] **Phase 3**: Static Code Analysis Engine
- [x] **Phase 4**: Architecture Intelligence Engine
- [x] **Phase 5**: Security Intelligence Engine (SAST)
- [x] **Phase 6**: Maintainability & Repository Intelligence Engine
- [x] **Phase 7**: Repository IQ Engine & AI Intelligence
- [x] **Phase 8**: Professional Frontend Dashboard
- [x] **Phase 9**: Enterprise Platform & Git Platform Integration

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
