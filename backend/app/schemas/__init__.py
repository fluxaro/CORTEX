"""Pydantic schemas module."""

from app.schemas.health import HealthResponse
from app.schemas.version import VersionResponse

__all__ = ["HealthResponse", "VersionResponse"]
