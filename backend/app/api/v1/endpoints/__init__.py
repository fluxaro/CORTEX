"""API v1 endpoints package."""

from app.api.v1.endpoints import (
    analysis,
    architecture,
    health,
    maintainability,
    repositories,
    security,
    version,
)

__all__ = [
    "health",
    "version",
    "repositories",
    "analysis",
    "architecture",
    "security",
    "maintainability",
]
