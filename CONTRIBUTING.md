# Contributing to ProjectIQ

Thank you for your interest in contributing to ProjectIQ! 🎉

ProjectIQ is an open-source project and we welcome contributions from the community, whether that's bug fixes, new features, documentation improvements, or test coverage additions.

---

## 📋 Before You Start

1. **Search existing issues** — your issue may already be reported or your feature already planned.
2. **Open a discussion** — for major features, please open a [GitHub Discussion](https://github.com/me-hv/ProjectIQ/discussions) first to align before writing code.
3. **Read the [Developer Guide](docs/wiki/Developer-Guide.md)** — covers local development setup.

---

## 🔧 Development Setup

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/ProjectIQ.git
cd ProjectIQ

# Backend
python -m venv .venv
.venv\Scripts\activate            # Windows
source .venv/bin/activate         # macOS / Linux
pip install -r backend/requirements.txt

# Frontend
cd frontend && npm install && cd ..

# Start dependencies
docker-compose up -d postgres redis

# Run migrations
alembic -c backend/alembic.ini upgrade head
```

---

## 🌿 Branch Strategy

| Branch Name | Purpose |
| :--- | :--- |
| `feat/your-feature-name` | New features |
| `fix/bug-description` | Bug fixes |
| `docs/topic` | Documentation only |
| `test/coverage-area` | Test additions |
| `chore/task` | Maintenance tasks |

---

## ✅ Code Quality Standards

All contributions must pass the following checks before merging:

```bash
# Lint
.venv\Scripts\ruff.exe check --fix backend

# Format
.venv\Scripts\black.exe backend

# Type check
$env:PYTHONPATH="backend"; .venv\Scripts\mypy.exe --config-file backend/pyproject.toml backend/app

# Tests
$env:PYTHONPATH="backend"; .venv\Scripts\pytest.exe backend/tests

# Frontend
cd frontend && npm run build
```

All checks must pass with **zero errors**.

---

## 📝 Commit Convention

ProjectIQ follows [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add repository comparison engine
fix: correct cyclomatic complexity for nested Go functions
docs: update Installation wiki page
test: add RBAC permission boundary tests
chore: bump FastAPI to 0.116.0
refactor: extract secret scanner into dedicated module
```

---

## 🔄 Pull Request Process

1. Ensure all quality checks pass locally.
2. Update relevant documentation (README, wiki pages, docstrings).
3. Add tests for any new logic.
4. Fill in the [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md) completely.
5. Request a review from at least one maintainer.
6. PRs require at least **1 approval** and a passing CI build to merge.

---

## 🐛 Reporting Bugs

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md). Include:
- Steps to reproduce
- Expected vs. actual behavior
- ProjectIQ version
- Operating system and Python/Node version

---

## 🔒 Security Vulnerabilities

**Do not open a public issue for security vulnerabilities.** Follow the responsible disclosure process in [SECURITY.md](SECURITY.md).

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

*Thank you for making ProjectIQ better! ❤️*
