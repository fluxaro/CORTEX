"""Dependency injection placeholders package."""

from app.dependencies.db import get_db

__all__ = ["get_db"]
