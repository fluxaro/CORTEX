"""Tests for ConfigTechDetector technology stack extraction."""

from app.analyzers.architecture.detectors.config_tech_detector import ConfigTechDetector
from app.analyzers.shared.models import FileAnalysisResult


def test_tech_stack_extraction() -> None:
    """Test extracting tech stack, containers, DBs, and API surfaces."""
    paths = ["Dockerfile", "docker-compose.yml", "alembic.ini", "pyproject.toml"]
    file_res = FileAnalysisResult(
        path="app/main.py",
        language="Python",
        imports=["fastapi", "asyncpg", "redis", "celery", "pytest"],
    )

    tech = ConfigTechDetector.analyze_tech_stack(paths, [file_res])

    assert "Python" in tech.languages
    assert "Docker" in tech.containers
    assert "PostgreSQL" in tech.databases
    assert "Redis" in tech.caching
    assert "REST APIs" in tech.api_surfaces
    assert "Background Workers" in tech.api_surfaces
