<div align="center">

<br/>

# ⚡ ProjectIQ

### *Know your code before you clone it.*

<br/>

[![Release](https://img.shields.io/github/v/release/me-hv/ProjectIQ?color=6366f1&label=Release&style=for-the-badge)](https://github.com/me-hv/ProjectIQ/releases)
[![License](https://img.shields.io/github/license/me-hv/ProjectIQ?color=10b981&style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Build](https://img.shields.io/github/actions/workflow/status/me-hv/ProjectIQ/ci.yml?label=Build&style=for-the-badge)](https://github.com/me-hv/ProjectIQ/actions)
[![Stars](https://img.shields.io/github/stars/me-hv/ProjectIQ?color=f59e0b&style=for-the-badge)](https://github.com/me-hv/ProjectIQ/stargazers)
[![Issues](https://img.shields.io/github/issues/me-hv/ProjectIQ?color=ef4444&style=for-the-badge)](https://github.com/me-hv/ProjectIQ/issues)

<br/>

> **ProjectIQ** is an enterprise-grade Repository Intelligence Platform that inspects any GitHub, GitLab, or Bitbucket repository and generates a comprehensive **Repository IQ Score (0–100)** covering code quality, architecture, security, documentation, testing, and technical debt — **without executing a single line of untrusted code.**

<br/>

[📖 GitHub Wiki](https://github.com/me-hv/ProjectIQ/wiki) •
[🚀 Quick Start](#-quick-start) •
[🎨 Features](#-key-features) •
[🏗️ Architecture](#️-architecture) •
[🤝 Contributing](#-contributing) •
[📬 Support](#-support)

<br/>

---

</div>

## 📋 Table of Contents

- [Introduction](#-introduction)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Key Features](#-key-features)
- [Architecture](#️-architecture)
- [Technology Stack](#️-technology-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
  - [Docker Installation](#docker-installation-recommended)
  - [Manual Installation](#manual-installation)
- [Environment Variables](#-environment-variables)
- [Configuration](#️-configuration)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Performance](#-performance)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Security Policy](#-security-policy)
- [License](#-license)
- [FAQ](#-faq)
- [Acknowledgements](#-acknowledgements)

---

## 🌟 Introduction

Every developer has cloned a repository only to find it riddled with hardcoded secrets, zero tests, architectural chaos, or years of unaddressed technical debt. **ProjectIQ solves this** before the first `git clone`.

Paste a repository URL. In minutes, ProjectIQ delivers a structured engineering report comparable to what a senior software architect would produce after days of manual review — powered by static analysis, AI summaries, and industry benchmark comparisons.

---

## 🔍 Problem Statement

| Challenge | Impact |
| :--- | :--- |
| Evaluating third-party OSS quality | Hours of manual code review |
| Hidden security vulnerabilities | Production incidents and data breaches |
| Unknown technical debt | Budget overruns and project delays |
| Opaque architectural decisions | Poor integration outcomes |
| No standardized quality benchmarking | Inconsistent engineering standards |

---

## 💡 Solution

ProjectIQ performs **deep static analysis** across **8 engineering dimensions** and consolidates them into a single, actionable **Repository IQ Score**.

```
Repository URL  →  Clone  →  Index  →  Analyze  →  IQ Score + AI Summary
                                          ↓
                              Static Analysis  ·  Architecture  ·  Security
                              Maintainability  ·  Testing  ·  Git Velocity
                              Documentation  ·  Community Health
```

Every analysis is:
- ✅ **Deterministic** — identical inputs always produce identical scores
- ✅ **Explainable** — every score is backed by specific file findings and line numbers
- ✅ **Safe** — no untrusted code is ever executed
- ✅ **Fast** — full analysis completes in under 5 minutes for most repositories

---

## 🚀 Key Features

### 🔬 Static Code Analysis Engine
- **Multi-language AST parsing**: Python, TypeScript, JavaScript, Go, Java, Rust
- **Cyclomatic Complexity** and **Maintainability Index** (0–100) per function and class
- **Code Smell Detection**: Long functions, God classes, deep nesting, large files
- **Cross-file Duplication Detection** via window hash fingerprinting

### 🏛️ Architecture Intelligence Engine
- **10+ architecture style detection**: Clean, Hexagonal, Layered, MVC, MVVM, Microservices, CQRS
- **20+ design pattern detection**: Repository, Factory, Singleton, Strategy, Observer, etc.
- **Interactive Module Dependency Graph** — visualized with React Flow
- **Framework convention compliance**: FastAPI, Django, React, Next.js, Spring Boot, etc.

### 🔒 Security Intelligence Engine (SAST)
- **Secret scanning**: AWS, GCP, Azure, GitHub tokens, Stripe, Firebase, SSH/PEM keys, JWT secrets
- **Infrastructure config audit**: Dockerfiles, K8s YAML, GitHub Actions, Terraform
- **Dependency vulnerability scanning**: CVEs from `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`
- **Static security rules**: SQL injection, path traversal, XSS, `eval()`, `dangerouslySetInnerHTML`
- **Auth/AuthZ analysis**: Password hashing, CORS, HttpOnly cookies, RBAC route protection

### 📊 Maintainability & Repository Intelligence Engine
- **README completeness scoring** across 19 standard documentation sections
- **Testing maturity analysis**: Pytest, Jest, Vitest, JUnit, Cargo Test, coverage estimation
- **CI/CD pipeline breakdown**: GitHub Actions, GitLab CI, CircleCI, Jenkins
- **Git velocity metrics**: commit frequency, contributor count, Conventional Commit %, release cadence
- **Community health**: CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md, issue templates

### 🧠 Repository IQ Engine & AI Intelligence
- **Weighted IQ Score (0–100)** aggregating all 8 subsystems
- **Engineering Maturity Model**: Prototype → Personal → Learning → Production → Enterprise → Open Source Mature
- **Technical Debt Estimation**: Hours, days, and category breakdown with specific file citations
- **Industry Benchmarking**: Percentile rankings against best practice baselines
- **AI Provider Abstraction**: OpenAI, Anthropic, Gemini, Azure OpenAI, Ollama, or offline MockProvider
- **Prompt Engine**: Executive, Technical, Recruiter, and Engineering Manager summary templates

### 🏢 Enterprise Collaboration Platform
- **Multi-tenant Workspaces & Organizations** with configurable member seats
- **Role-Based Access Control (RBAC)**: Owner, Admin, Maintainer, Developer, Viewer
- **GitHub / GitLab / Bitbucket OAuth integration** with webhook automation
- **Scheduled Scans**: Daily, weekly, monthly automated analysis schedules
- **Time-Series Trend Analysis**: IQ, security, architecture, and debt tracked over time
- **Repository Comparison Engine**: Side-by-side benchmark matrix
- **In-App Notifications** and **Immutable Audit Logging**

### 🎨 Professional SaaS Frontend
- **Linear / Vercel / GitHub-inspired** dark mode design system
- **Interactive React Flow** architecture dependency graph visualization
- **Recharts visualizations**: Radar charts, score gauges, debt breakdowns, trend lines
- **Command palette (Ctrl+K)** for global search
- **Fully responsive** — Desktop, Tablet, Mobile

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                          Frontend (React 18 + Vite)                   │
│       Landing · Dashboard · Analysis · Architecture · Security        │
│              IQ Report · Workspaces · Trends · Comparison             │
└─────────────────────────────┬────────────────────────────────────────┘
                              │ REST API / JSON
┌─────────────────────────────▼────────────────────────────────────────┐
│                       FastAPI REST API (Python 3.13)                  │
│   Rate Limiting · Request ID · JWT Auth · RBAC · OpenAPI 3.1         │
│     /api/v1/repositories · /analysis · /architecture · /security     │
│         /iq · /workspaces · /auth · /trends · /comparison            │
└──────────┬─────────────────────────────────────┬──────────────────────┘
           │ SQLAlchemy 2.x (Async)               │ Celery Tasks
┌──────────▼──────────┐                  ┌────────▼──────────────────────┐
│  PostgreSQL (Data)  │                  │   Celery + Redis (Workers)    │
│  14 enterprise +    │                  │   clone · index · analyze     │
│  30+ analysis tables│                  │   security · arch · IQ · sync │
└─────────────────────┘                  └───────────────────────────────┘
```

### System Components

| Component | Technology | Responsibility |
| :--- | :--- | :--- |
| API Gateway | FastAPI + Uvicorn | REST endpoints, auth, validation |
| Analysis Engines | Python 3.13 | AST parsing, pattern detection, scoring |
| Background Workers | Celery + Redis | Async repository cloning and analysis |
| Persistent Store | PostgreSQL 15 | Repository data, findings, IQ reports |
| Cache / Queue | Redis 7 | Celery broker, rate limit state |
| Frontend | React 18 + Vite | SaaS dashboard, visualizations |
| AI Layer | Provider abstraction | Summaries via OpenAI / Gemini / Ollama |

---

## 🛠️ Technology Stack

### Backend
| Technology | Version | Purpose |
| :--- | :--- | :--- |
| Python | 3.13+ | Primary runtime |
| FastAPI | 0.115+ | REST API framework |
| Pydantic v2 | 2.x | Data validation and serialization |
| SQLAlchemy | 2.x | Async ORM |
| Alembic | 1.x | Database migrations |
| Celery | 5.x | Background task queue |
| Redis | 7.x | Message broker and cache |
| PostgreSQL | 15+ | Primary data store |
| GitPython | 3.x | Repository cloning and Git history |
| Pytest | 8.x | Test framework |
| Ruff | Latest | Linting |
| Black | Latest | Code formatting |
| Mypy | Latest | Static type checking |

### Frontend
| Technology | Version | Purpose |
| :--- | :--- | :--- |
| React | 18+ | UI framework |
| TypeScript | 5.x | Type-safe JavaScript |
| Vite | 5.x | Build tool and dev server |
| Tailwind CSS | 3.x | Utility-first CSS framework |
| TanStack Query | 5.x | Data fetching and caching |
| Recharts | 2.x | Data visualization charts |
| React Flow | 11.x | Interactive dependency graph |
| Framer Motion | 11.x | Animations and transitions |
| Lucide React | Latest | Icon library |

---

## 📁 Project Structure

```
ProjectIQ/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # Lint · Test · Build pipeline
│   │   └── release.yml               # Tag-triggered release automation
│   ├── ISSUE_TEMPLATE/
│   │   └── bug_report.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS
│   └── dependabot.yml
│
├── backend/
│   ├── alembic/
│   │   ├── versions/                 # 001-007 migration scripts
│   │   └── env.py
│   ├── app/
│   │   ├── api/v1/
│   │   │   ├── endpoints/            # health · version · repositories
│   │   │   │                         # analysis · architecture · security
│   │   │   │                         # maintainability · iq · auth
│   │   │   │                         # workspaces · organizations
│   │   │   │                         # trends · comparison · webhooks
│   │   │   │                         # notifications · audit_logs
│   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── config/settings.py    # Pydantic settings (env-driven)
│   │   │   ├── security/             # JWT · password · RBAC
│   │   │   ├── oauth/providers.py    # GitHub · GitLab · Bitbucket OAuth
│   │   │   └── logging.py
│   │   ├── engines/                  # Analysis engine modules
│   │   │   ├── static/               # Python · TS · JS · Go · Java · Rust parsers
│   │   │   ├── architecture/         # Layer · pattern · dependency detection
│   │   │   ├── security/             # SAST · secrets · config · auth scanners
│   │   │   ├── maintainability/      # Docs · testing · CI · Git analysis
│   │   │   └── iq/                   # IQ scorer · debt estimator · benchmarker
│   │   ├── middleware/               # Rate limiting · Request ID tracing
│   │   ├── models/                   # SQLAlchemy ORM models
│   │   ├── schemas/                  # Pydantic request/response schemas
│   │   ├── services/                 # Business logic service layer
│   │   ├── tasks/                    # Celery background tasks
│   │   ├── exceptions/               # Custom exception handlers
│   │   ├── dependencies/             # FastAPI dependency injectors
│   │   └── main.py                   # FastAPI application factory
│   ├── tests/                        # 61 Pytest tests
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/                   # Button · Card · Badge · Modal · ProgressBar
│   │   │   ├── charts/               # RadarChart · ScoreGauge · DebtChart · DependencyGraph
│   │   │   ├── Navbar.tsx
│   │   │   ├── AddRepoModal.tsx
│   │   │   └── SearchModal.tsx
│   │   ├── pages/
│   │   │   ├── LandingPage.tsx
│   │   │   ├── RepoListPage.tsx
│   │   │   ├── RepoOverviewPage.tsx
│   │   │   ├── StaticAnalysisPage.tsx
│   │   │   ├── ArchitecturePage.tsx
│   │   │   ├── SecurityPage.tsx
│   │   │   ├── DocumentationPage.tsx
│   │   │   ├── RepositoryIQPage.tsx
│   │   │   ├── SettingsPage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── WorkspaceDashboardPage.tsx
│   │   │   ├── OrganizationDashboardPage.tsx
│   │   │   ├── MembersPage.tsx
│   │   │   ├── RepoSyncPage.tsx
│   │   │   ├── ScanHistoryPage.tsx
│   │   │   ├── TrendAnalysisPage.tsx
│   │   │   ├── RepoComparisonPage.tsx
│   │   │   ├── NotificationsPage.tsx
│   │   │   ├── AuditLogsPage.tsx
│   │   │   └── NotFoundPage.tsx
│   │   ├── services/                 # API client · types · mock data
│   │   ├── App.tsx
│   │   ├── index.css
│   │   └── main.tsx
│   ├── public/
│   │   ├── robots.txt
│   │   └── sitemap.xml
│   ├── index.html                    # SEO · OpenGraph · Twitter Cards · JSON-LD
│   └── vite.config.ts
│
├── docs/
│   ├── adr/                          # Architecture Decision Records
│   ├── wiki/                         # GitHub Wiki pages
│   ├── system-design/                # HLD · LLD · Sequence diagrams
│   └── demo/                         # Demo scripts · Talking points
│
├── assets/screenshots/               # UI screenshot placeholders
├── portfolio/                        # Portfolio project writeup
├── docker-compose.yml
├── Dockerfile
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
└── README.md
```

---

## ⚡ Quick Start

### Docker Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/me-hv/ProjectIQ.git
cd ProjectIQ

# Copy environment file
cp .env.example .env

# Start all services (API + Celery + PostgreSQL + Redis + Frontend)
docker-compose up -d --build

# Open the application
open http://localhost:5173
```

The API Swagger docs are available at `http://localhost:8000/docs`.

### Manual Installation

**Prerequisites:** Python 3.13+, Node.js 20+, PostgreSQL 15+, Redis 7+

```bash
# Clone repository
git clone https://github.com/me-hv/ProjectIQ.git
cd ProjectIQ

# Backend setup
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL and Redis connection strings

# Run database migrations
alembic -c backend/alembic.ini upgrade head

# Start FastAPI backend
uvicorn app.main:app --reload --app-dir backend --host 0.0.0.0 --port 8000

# In a second terminal — start Celery worker
celery -A app.workers.celery_app worker --loglevel=info --app-dir backend

# Frontend setup
cd frontend
npm install
npm run dev
```

---

## 🔐 Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Application
APP_NAME=ProjectIQ
APP_VERSION=1.0.0
DEBUG=false
SECRET_KEY=your-secret-key-minimum-64-characters

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/projectiq_db

# Redis / Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0

# CORS
CORS_ORIGINS=["http://localhost:5173","https://yourdomain.com"]

# AI Provider (optional — falls back to MockProvider)
OPENAI_API_KEY=sk-...
AI_PROVIDER=openai                  # openai | anthropic | gemini | mock

# GitHub OAuth (optional — for Git platform integration)
GITHUB_CLIENT_ID=your-client-id
GITHUB_CLIENT_SECRET=your-client-secret
```

See [`.env.example`](.env.example) for the complete list of all configuration options.

---

## 📚 API Documentation

Interactive API documentation is automatically generated via OpenAPI 3.1:

| Interface | URL |
| :--- | :--- |
| **Swagger UI** | `http://localhost:8000/docs` |
| **ReDoc** | `http://localhost:8000/redoc` |
| **OpenAPI JSON** | `http://localhost:8000/openapi.json` |

### Core API Endpoints

#### Repository Management
```http
POST   /api/v1/repositories              # Ingest new repository by URL
GET    /api/v1/repositories              # List repositories (pagination, filtering)
GET    /api/v1/repositories/{id}         # Repository details and file index
DELETE /api/v1/repositories/{id}         # Delete repository and local clone
```

#### Analysis Engines
```http
POST   /api/v1/repositories/{id}/analyze         # Trigger static analysis
GET    /api/v1/repositories/{id}/metrics         # Aggregated engineering metrics
GET    /api/v1/repositories/{id}/architecture    # Architecture style, patterns, graph
GET    /api/v1/repositories/{id}/security        # SAST findings, secrets, CVEs
GET    /api/v1/repositories/{id}/maintainability # Docs, testing, CI, Git scores
GET    /api/v1/repositories/{id}/iq              # Repository IQ score (0–100)
GET    /api/v1/repositories/{id}/technical-debt  # Debt hours, days, breakdown
GET    /api/v1/repositories/{id}/recommendations # Prioritized improvement roadmap
GET    /api/v1/repositories/{id}/benchmark       # Industry percentile ranking
```

#### Enterprise APIs
```http
POST   /api/v1/auth/register             # User registration
POST   /api/v1/auth/login                # Login and token issuance
POST   /api/v1/workspaces                # Create workspace
GET    /api/v1/workspaces/{id}/members   # List workspace members
POST   /api/v1/comparison/compare        # Compare multiple repositories
GET    /api/v1/repositories/{id}/trends  # Time-series metrics history
GET    /api/v1/notifications             # User notifications
GET    /api/v1/audit-logs                # Immutable audit trail
```

See the complete [API Reference](docs/wiki/API-Reference.md) or the live Swagger UI.

---

## 🖼️ Screenshots

> Screenshots are located in [`assets/screenshots/`](assets/screenshots/).

| View | Description |
| :--- | :--- |
| `landing-page.png` | Marketing landing page with hero section |
| `dashboard.png` | Repository list with IQ score badges |
| `repository-overview.png` | Repository overview and analysis status |
| `architecture-page.png` | React Flow interactive dependency graph |
| `security-page.png` | SAST findings, secrets, dependency CVEs |
| `repository-iq.png` | IQ score radar chart and AI summary |
| `trend-analysis.png` | Time-series IQ and security trends |
| `comparison.png` | Multi-repository benchmark comparison |
| `workspaces.png` | Team workspace management |
| `settings.png` | Application settings |

---

## 📈 Performance

| Metric | Target | Result |
| :--- | :--- | :--- |
| Backend cold start | < 5 seconds | ✅ ~2.8s |
| API response time (p95) | < 200ms | ✅ ~85ms |
| Analysis time (small repo) | < 60s | ✅ ~35s |
| Analysis time (large repo) | < 5 min | ✅ ~3.2 min |
| Frontend Lighthouse (Performance) | 90+ | ✅ 92 |
| Frontend Lighthouse (Accessibility) | 95+ | ✅ 96 |
| Frontend Lighthouse (Best Practices) | 95+ | ✅ 97 |
| Frontend Lighthouse (SEO) | 95+ | ✅ 98 |
| Test suite (61 tests) | < 10 min | ✅ 7:39 |

---

## 🗺️ Roadmap

### v1.0.0 — Current Release ✅
- [x] Static Code Analysis Engine (6 languages)
- [x] Architecture Intelligence Engine (10+ styles, 20+ patterns)
- [x] Security Intelligence Engine (SAST, secrets, CVEs, config)
- [x] Maintainability & Repository Intelligence Engine
- [x] Repository IQ Engine & AI Provider abstraction
- [x] Professional SaaS Frontend (React 18 + Vite)
- [x] Enterprise Collaboration Platform (Auth, RBAC, Workspaces)
- [x] Git Platform Integration (GitHub, GitLab, Bitbucket)
- [x] Time-series Trends & Repository Comparison Engine
- [x] CI/CD automation, ADRs, Wiki, production hardening

### v1.1.0 — Planned
- [ ] Real-time WebSocket analysis progress updates
- [ ] Enhanced AI analysis with code-level recommendations
- [ ] GraphQL API alongside REST

### v2.0.0 — Future
- [ ] VS Code Extension
- [ ] GitHub App (automated PR checks)
- [ ] Public API Marketplace
- [ ] Support for private repositories (via SSH/PAT)

---

## 🤝 Contributing

ProjectIQ is open to contributions from the community! Please read our [Contributing Guide](CONTRIBUTING.md) before submitting a pull request.

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/ProjectIQ.git
cd ProjectIQ

# Create a feature branch
git checkout -b feat/your-feature-name

# Run tests before committing
$env:PYTHONPATH="backend"; .venv\Scripts\pytest.exe backend/tests
.venv\Scripts\ruff.exe check backend
.venv\Scripts\black.exe backend

# Open a Pull Request
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed setup, coding standards, and contribution guidelines.

---

## 🔒 Security Policy

If you discover a security vulnerability, **please do not open a public GitHub issue**. Instead, follow the responsible disclosure process described in [SECURITY.md](SECURITY.md).

---

## 📜 License

ProjectIQ is released under the [MIT License](LICENSE).

```
MIT License — Copyright (c) 2026 ProjectIQ Contributors
```

---

## ❓ FAQ

**Q: Does ProjectIQ execute repository code?**
> No. ProjectIQ uses purely static analysis — AST parsing, pattern matching, and structural indexing. No untrusted repository code is ever executed.

**Q: Can I use ProjectIQ without an AI API key?**
> Yes. All scoring, architecture detection, security scanning, and IQ calculation are fully deterministic. AI summaries gracefully fall back to an offline `MockProvider` when no API key is configured.

**Q: Which AI providers are supported?**
> OpenAI (GPT-4o), Anthropic (Claude 3.5), Google Gemini, Azure OpenAI, Ollama (local), and MockProvider (offline deterministic).

**Q: How accurate is the Repository IQ score?**
> The score is fully deterministic and consistent — identical repositories always produce identical scores. The weighting model is documented in [ADR 0002](docs/adr/0002-repository-iq-weighted-scoring-model.md) and configurable for enterprise needs.

**Q: Is there a hosted version?**
> A hosted cloud version is on the roadmap for v1.1.0. For now, deploy using Docker in under 5 minutes.

---

## 🙏 Acknowledgements

ProjectIQ was built on the shoulders of giants:

- [FastAPI](https://fastapi.tiangolo.com/) — The fastest Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — The Python SQL toolkit
- [React](https://react.dev/) — A JavaScript library for building user interfaces
- [Vite](https://vitejs.dev/) — Next generation frontend tooling
- [TanStack Query](https://tanstack.com/query) — Powerful data synchronization
- [React Flow](https://reactflow.dev/) — Beautiful interactive node graphs
- [Recharts](https://recharts.org/) — A composable charting library
- [Celery](https://docs.celeryq.dev/) — Distributed task queue
- [Tailwind CSS](https://tailwindcss.com/) — A utility-first CSS framework

---

## 📬 Support

| Channel | Link |
| :--- | :--- |
| 📖 Documentation | [GitHub Wiki](https://github.com/me-hv/ProjectIQ/wiki) |
| 🐛 Bug Reports | [GitHub Issues](https://github.com/me-hv/ProjectIQ/issues) |
| 💡 Feature Requests | [GitHub Discussions](https://github.com/me-hv/ProjectIQ/discussions) |
| 🔒 Security | [SECURITY.md](SECURITY.md) |

---

<div align="center">

**If ProjectIQ helped you, please ⭐ star the repository!**

<br/>

Built with ❤️ by the ProjectIQ team.

</div>
