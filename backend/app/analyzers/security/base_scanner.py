"""Base interface for security scanners."""

from abc import ABC, abstractmethod
from typing import Any

from app.analyzers.security.models import SecurityAnalysisResult


class BaseSecurityScanner(ABC):
    """Abstract base security scanner interface."""

    @property
    @abstractmethod
    def scanner_name(self) -> str:
        """Name of security scanner."""
        pass

    @abstractmethod
    def scan(
        self,
        target_path: str,
        file_contents: dict[str, str],
        extra_context: dict[str, Any] | None = None,
    ) -> SecurityAnalysisResult:
        """Execute scan and return SecurityAnalysisResult."""
        pass
