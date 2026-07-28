# Changelog

All notable changes to ProjectIQ will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-07-28

### Added
- **Production Release v1.0.0**: Complete enterprise-grade Repository Intelligence Platform.
- **Enterprise Collaboration Platform**: Multi-tenant Workspaces, Organizations, Role-Based Access Control (RBAC), team invitations, and user management.
- **Authentication & Security**: PBKDF2 HMAC password hashing, JWT Access/Refresh tokens, GitHub/GitLab/Bitbucket OAuth authorization.
- **Git Platform Integrations**: Repository import, metadata synchronization, and webhook event processing for GitHub, GitLab, and Bitbucket.
- **Repository IQ Engine & AI Summaries**: 0-100 weighted Repository IQ score, engineering maturity classification, technical debt estimation, industry benchmarking, and prompt template engine.
- **Security Intelligence Engine (SAST)**: Secret scanning, infrastructure configuration audit, dependency vulnerability analysis, static SAST rules, and authentication/authorization checkers.
- **Architecture Intelligence Engine**: Architectural style detection, 20+ design patterns, framework conventions, and interactive React Flow module dependency graphs.
- **Static Code Analysis Engine**: Multi-language AST parsing (Python, TS, JS, Go, Java, Rust), cyclomatic complexity, maintainability index, code smell detection, and cross-file duplication hashing.
- **Maintainability Engine**: README section completeness, testing maturity analysis, CI/CD pipeline breakdown, Git velocity tracking, and open-source community standards.
- **Professional SaaS Frontend**: React 18, TypeScript, Vite, Tailwind CSS dark mode design system, Recharts visualizations, command palette (Ctrl+K), and responsive layouts.
- **Observability & Health Probes**: Request ID and Correlation ID tracking, rate limiting, structured logging, and Kubernetes `/live` and `/ready` probes.
- **Open Source Governance & CI/CD**: GitHub Actions CI/CD workflows, Dependabot security monitoring, CODEOWNERS, issue templates, PR template, ADRs, and GitHub Wiki documentation.

## [0.1.0] - 2026-07-27
- Initialized ProjectIQ foundation architecture.
- Modular FastAPI backend application factory.
- Configuration loading via Pydantic settings.
- Health endpoint (`GET /health`) and Version endpoint (`GET /version`).
- PostgreSQL configuration placeholder with SQLAlchemy 2.x and Alembic.
- Redis & Celery background worker setup.
- Comprehensive code quality tooling (Ruff, Black, Mypy, Pytest).
- Docker multi-stage build & docker-compose orchestration.
- Placeholder React Vite TypeScript frontend.
