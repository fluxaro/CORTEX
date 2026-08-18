"""API v1 endpoints package."""

from app.api.v1.endpoints import (
    analysis,
    architecture,
    grading,
    health,
    maintainability,
    repositories,
    security,
    version,
)

# Backward compatibility alias
iq = grading

__all__ = [
    "health",
    "version",
    "repositories",
    "analysis",
    "architecture",
    "security",
    "maintainability",
    "grading",
    "iq",
]
