# Contributing to ProjectIQ

Thank you for considering contributing to ProjectIQ!

## Development Workflow

1. Fork the repository and create your branch from `main`.
2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```
3. Ensure all tests pass and code quality tools pass:
   ```bash
   pytest
   ruff check backend
   black --check backend
   mypy backend
   ```
4. Submit a pull request detailing your changes.

## Code Style

- Python code must conform to Black and Ruff style guidelines.
- Add type annotations for all new code.
- Write tests for any new features or bug fixes.
