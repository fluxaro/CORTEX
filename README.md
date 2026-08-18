<div align="center">

# ⚡ CORTEX

### *Instant, Zero-Execution Codebase Auditing & Repository IQ Engine*

**Know your codebase before you clone, integrate, or deploy.**

<br/>

[![Release](https://img.shields.io/github/v/release/fluxaro/CORTEX?color=6366f1&label=Release&style=for-the-badge)](https://github.com/fluxaro/CORTEX/releases)
[![License](https://img.shields.io/github/license/fluxaro/CORTEX?color=10b981&style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Build](https://img.shields.io/github/actions/workflow/status/fluxaro/CORTEX/ci.yml?label=Build&style=for-the-badge)](https://github.com/fluxaro/CORTEX/actions)
[![Stars](https://img.shields.io/github/stars/fluxaro/CORTEX?color=f59e0b&style=for-the-badge)](https://github.com/fluxaro/CORTEX/stargazers)
[![Issues](https://img.shields.io/github/issues/fluxaro/CORTEX?color=ef4444&style=for-the-badge)](https://github.com/fluxaro/CORTEX/issues)

<br/>

> **CORTEX** is an enterprise-grade Repository Intelligence Platform that audits any GitHub, GitLab, or Bitbucket codebase and produces an interactive **Repository IQ Score (0–100)**. It synthesizes deep static code analysis, architectural pattern recognition, SAST security audits, and technical debt estimations into actionable engineering reports — **with 100% deterministic safety and zero execution of untrusted code.**

<br/>

[📖 Documentation](https://github.com/fluxaro/CORTEX/wiki) •
[🚀 Quick Start](#-quick-start) •
[⚡ Core Engines](#-core-intelligence-engines) •
[🏗️ System Architecture](#️-system-architecture) •
[🤝 Community & Contributing](#-contributing)

<br/>

---

</div>

## 📑 Table of Contents

- [Overview](#-overview)
- [Why Cortex?](#-why-cortex)
- [Core Intelligence Engines](#-core-intelligence-engines)
- [System Architecture](#️-system-architecture)
- [Tech Stack](#-tech-stack)
- [Repository Structure](#-repository-structure)
- [Quick Start](#-quick-start)
  - [Docker Setup (Recommended)](#-docker-setup-recommended)
  - [Manual Development Setup](#-manual-development-setup)
- [Environment Configuration](#-environment-configuration)
- [API Reference](#-api-reference)
- [Performance & Benchmarks](#-performance--benchmarks)
- [Product Roadmap](#-product-roadmap)
- [Security Disclosure](#-security-disclosure)
- [License & Credits](#-license--credits)

---

## 🎯 Overview

Cloning an unfamiliar repository often comes with unpleasant surprises: unhandled security vulnerabilities, missing tests, hidden architectural flaws, and undocumented technical debt.

**CORTEX automates the code review process.** Point Cortex to any repository URL, and within minutes, receive an executive-grade technical analysis report detailing code maintainability, architectural design patterns, secret leaks, and an overall **Repository IQ Score**.

> [!IMPORTANT]
> **Zero Code Execution Safety**
> Cortex uses pure Abstract Syntax Tree (AST) parsing, pattern scanning, and structural indexing. Code is analyzed safely without running arbitrary build scripts or executing untrusted code.

---

## ⚖️ Why Cortex?

| Dimension | Manual Code Audit | Traditional SAST | ⚡ Cortex Platform |
| :--- | :--- | :--- | :--- |
| **Speed** | 2–5 Business Days | 10–30 Minutes | **< 3 Minutes** |
| **Architectural Vision** | High (human intuition) | None (syntax only) | **Automated (10+ patterns & DAGs)** |
| **Tech Debt Quantification** | Qualitative estimates | Rule counts | **Actionable Hours/Days Breakdown** |
| **Security & Secrets** | Spotty / Human Error | High false positives | **Context-Aware Secret & CVE Audit** |
| **Explainability** | Manual notes | Raw log snippets | **Scored (0–100) + Line-level Citations** |
| **AI Integration** | None | Generic chat overlays | **Structured Summaries & Benchmarks** |

---

## 🔬 Core Intelligence Engines

Cortex synthesizes findings across **8 core analytical dimensions**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           INPUT REPOSITORY URL                              │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
  ┌───────────────────────────┐                 ┌───────────────────────────┐
  │  Multi-Language AST Engine│                 │ Architectural Style Engine│
  │  Complexities, smells,    │                 │ Clean, Hexagonal, MVC,    │
  │  maintainability index    │                 │ React Flow graphs         │
  └─────────────┬─────────────┘                 └─────────────┬─────────────┘
                │                                             │
                ├──────────────────────┬──────────────────────┤
                ▼                      ▼                      ▼
  ┌───────────────────────────┐ ┌───────────────┐ ┌───────────────────────────┐
  │ SAST & Secret Scanner     │ │ Git & Testing │ │ Repository IQ Scoring     │
  │ Secrets, CVEs, OWASP      │ │ Velocity, CI, │ │ Weighted 0-100 metric,    │
  │ config vulnerabilities    │ │ coverage, docs│ │ AI Executive Summaries    │
  └───────────────────────────┘ └───────────────┘ └───────────────────────────┘
```

### 1. 🔬 Static Code Analysis Engine
* **Polyglot AST Parsing**: Deep parsing for Python, TypeScript, JavaScript, Go, Java, and Rust.
* **Metrics Calculation**: Computes Cyclomatic Complexity, Halstead metrics, and Maintainability Index per class and function.
* **Code Smell Detection**: Automatically tags God objects, long methods, excessive nesting, and magic numbers.
* **Duplication Fingerprinting**: Detects duplicate code blocks using rolling window hashes across files.

### 2. 🏛️ Architecture Intelligence Engine
* **Pattern Recognition**: Detects 10+ architectural styles (Clean Architecture, Hexagonal, Layered, Microservices, CQRS, MVC) and 20+ design patterns (Repository, Factory, Singleton, Strategy, Observer).
* **Dependency Visualizer**: Renders interactive module dependency graphs using **React Flow**.
* **Framework Audit**: Verifies compliance with best practices for FastAPI, Django, React, Next.js, and Spring Boot.

### 3. 🔒 Security Intelligence Engine (SAST)
* **Secret Leak Detection**: Scans for AWS keys, GCP credentials, GitHub tokens, JWTs, Stripe/Firebase keys, and private SSH blocks.
* **Dependency CVE Auditing**: Evaluates vulnerabilities across `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`, and `pom.xml`.
* **Static Vulnerability Checks**: Flags SQL Injection risks, XSS vectors, unhandled `eval()` invocations, path traversals, and CORS misconfigurations.

### 4. 📊 Maintainability & Documentation Scorer
* **Documentation Grading**: Evaluates README quality across 19 standard structural sections.
* **Testing Maturity Assessment**: Analyzes Pytest, Jest, Vitest, JUnit, and Cargo test setups alongside coverage heuristics.
* **CI/CD Pipeline Breakdown**: Parses GitHub Actions, GitLab CI, CircleCI, and Docker configs.

### 5. 🧠 Repository IQ & Technical Debt Estimator
* **Repository IQ Score (0–100)**: Single, transparent metric calculated via customizable weighted formulas.
* **Technical Debt Estimation**: Translates code smells and structural flaws into estimated remediations in developer-hours.
* **AI Executive Summaries**: Integrates with OpenAI, Anthropic, Gemini, Azure OpenAI, Ollama, or an offline MockProvider to summarize code health for engineers, recruiters, and CTOs.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            FRONTEND LAYER                                   │
│                        React 18 · TypeScript · Vite                         │
│         Tailwind CSS · Recharts · React Flow · TanStack Query              │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ REST / JSON API
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                             BACKEND API LAYER                               │
│                         FastAPI · Async Python 3.13                         │
│            JWT Security · Rate Limiting · Request ID Tracing                │
└──────────────────┬──────────────────────────────────────┬───────────────────┘
                   │ SQLAlchemy 2.x (Async)               │ Background Tasks
┌──────────────────▼──────────────────┐  ┌────────────────▼───────────────────┐
│         POSTGRESQL 15               │  │          CELERY + REDIS            │
│   Workspaces · Repositories         │  │   Git Clone · AST Parsers          │
│   Analysis Runs · Scored Findings   │  │   SAST Scanners · IQ Calculator    │
└─────────────────────────────────────┘  └────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Domain | Technology | Usage / Details |
| :--- | :--- | :--- |
| **Backend Core** | Python 3.13+ / FastAPI | High-performance asynchronous API framework |
| **ORM & Database** | SQLAlchemy 2.0 / PostgreSQL 15 | Async database queries and migrations via Alembic |
| **Task Queue** | Celery 5.x / Redis 7 | Asynchronous background cloning, indexing, and scanning |
| **Frontend UI** | React 18 / TypeScript 5 / Vite | Modern, clean UI styled with Tailwind CSS |
| **Visualizations** | React Flow / Recharts | Interactive architectural graphs and metric charts |
| **AI Integration** | OpenAI / Gemini / Claude / Ollama | Extensible provider abstraction with offline mock fallback |
| **Quality & Tooling**| Pytest / Ruff / Black / Mypy | Strict linting, formatting, and test automation |

---

## 📁 Repository Structure

```
CORTEX/
├── .github/                  # CI/CD Workflows (lint, test, build, release)
├── backend/
│   ├── alembic/              # Database migration scripts (001–007)
│   ├── app/
│   │   ├── api/v1/           # Modular REST API endpoints & routers
│   │   ├── core/             # Configuration, security, OAuth, and logging
│   │   ├── engines/          # AST, Architecture, SAST, Maintainability & IQ engines
│   │   ├── models/           # SQLAlchemy database schemas
│   │   ├── schemas/          # Pydantic validation schemas
│   │   ├── services/         # Core business logic layer
│   │   └── tasks/            # Celery worker task definitions
│   └── tests/                # Comprehensive Pytest suite
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable UI elements, modals, graphs & charts
│   │   ├── pages/            # Dashboard, Repository, Security & IQ pages
│   │   └── services/         # API clients and data transformers
│   └── vite.config.ts
├── docs/                     # System design, ADRs, and API wiki
├── docker-compose.yml        # One-command orchestration
└── README.md
```

---

## ⚡ Quick Start

### 🐳 Docker Setup (Recommended)

Get Cortex up and running in under **2 minutes**:

```bash
# 1. Clone the repository
git clone git@github.com:fluxaro/CORTEX.git
cd CORTEX

# 2. Prepare environment file
cp .env.example .env

# 3. Spin up all services
docker compose up -d --build
```

Access the services:
* **Frontend Web App**: `http://localhost:5173`
* **FastAPI Swagger Docs**: `http://localhost:8000/docs`

---

### 💻 Manual Development Setup

#### Prerequisites
* **Python**: 3.13+
* **Node.js**: 20+
* **PostgreSQL**: 15+
* **Redis**: 7+

#### 1. Backend Setup
```bash
# Navigate to project root
cd CORTEX

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Environment configuration
cp .env.example .env
# Edit .env to set DATABASE_URL and REDIS_URL

# Run database migrations
alembic -c backend/alembic.ini upgrade head

# Start FastAPI server
uvicorn app.main:app --reload --app-dir backend --host 0.0.0.0 --port 8000
```

#### 2. Celery Worker (In a separate terminal)
```bash
source .venv/bin/activate
celery -A app.workers.celery_app worker --loglevel=info --app-dir backend
```

#### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## ⚙️ Environment Configuration

Sample configuration variables (`.env`):

```env
# General
APP_NAME=CORTEX
APP_VERSION=1.0.0
DEBUG=false
SECRET_KEY=your-secure-random-secret-key-at-least-64-chars

# Database & Cache
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/cortex_db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# AI Provider (optional - defaults to MockProvider if omitted)
AI_PROVIDER=openai  # openai | anthropic | gemini | ollama | mock
OPENAI_API_KEY=sk-proj-...

# Git Platform Integration (optional)
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

---

## 📡 API Reference

Interactive docs available at `/docs` (Swagger UI) or `/redoc` (ReDoc).

### Key Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/repositories` | Register and queue a repository for analysis |
| `GET` | `/api/v1/repositories` | List analyzed repositories with filtering & search |
| `GET` | `/api/v1/repositories/{id}/iq` | Retrieve Repository IQ score breakdown & AI summary |
| `GET` | `/api/v1/repositories/{id}/architecture` | Get architecture pattern detection & dependency graph |
| `GET` | `/api/v1/repositories/{id}/security` | Get SAST findings, secret leaks, and dependency CVEs |
| `GET` | `/api/v1/repositories/{id}/technical-debt` | Retrieve estimated technical debt in hours |
| `POST` | `/api/v1/comparison/compare` | Compare metrics across multiple repositories |

---

## 📊 Performance & Benchmarks

| Milestone / Metric | Baseline Target | Measured Result |
| :--- | :--- | :--- |
| **API Response Time (p95)** | < 150ms | ✅ **~85ms** |
| **Small Repo Analysis (< 10k LOC)** | < 60 seconds | ✅ **~32 seconds** |
| **Large Repo Analysis (> 100k LOC)** | < 5 minutes | ✅ **~3.1 minutes** |
| **Frontend Lighthouse Score** | 90+ across all metrics | ✅ **Performance: 94, A11y: 96, SEO: 98** |

---

## 🗺️ Product Roadmap

- [x] **v1.0.0 — Launch Release**
  - Polyglot static analysis engine (Python, TS/JS, Go, Java, Rust).
  - SAST security & secret audit engines.
  - Interactive React Flow architectural graph visualization.
  - Repository IQ scoring algorithm and multi-provider AI summaries.
  - Docker Compose setup & full OpenAPI spec.

- [ ] **v1.1.0 — Real-Time Insights & Extensions** *(In Progress)*
  - Live analysis progress streaming via WebSockets.
  - GitHub App integration for automated Pull Request checks.
  - IDE Extensions (VS Code extension for local IQ scoring).

- [ ] **v2.0.0 — Deep Intelligence**
  - Automated pull request remediation generation via AI agents.
  - Support for private SSH keys and self-hosted GitLab/Bitbucket Enterprise instances.

---

## 🔒 Security Disclosure

If you discover a potential security vulnerability within Cortex, please review our [Security Policy](SECURITY.md) and submit your report privately. **Do not create public issues for security vulnerabilities.**

---

## 📜 License & Credits

Released under the **MIT License**. See [`LICENSE`](LICENSE) for full details.

> Built with passion by the **Cortex Core Engineering Team**. If Cortex brings value to your workflow, consider starring the repo! ⭐
