"""Tests for CiAnalyzer automation detector."""

from app.analyzers.maintainability.analyzers.ci_analyzer import CiAnalyzer


def test_ci_analyzer() -> None:
    """Test detecting GitHub Actions workflows and job types."""
    file_paths = [".github/workflows/ci.yml"]
    file_contents = {
        ".github/workflows/ci.yml": "name: CI\njobs:\n  build:\n    runs-on: ubuntu-latest\n    steps:\n      - run: pytest\n      - run: ruff check\n"
    }

    res = CiAnalyzer.analyze(file_paths, file_contents)

    assert "GitHub Actions" in res.providers
    assert res.has_test_jobs is True
    assert res.has_lint_jobs is True
    assert res.ci_score > 50.0
