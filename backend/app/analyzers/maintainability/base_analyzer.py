"""Base interface for maintainability analyzers."""

from abc import ABC, abstractmethod
from typing import Any


class BaseMaintainabilityAnalyzer(ABC):
    """Abstract base class for repository maintainability analyzers."""

    @property
    @abstractmethod
    def analyzer_name(self) -> str:
        """Name of maintainability analyzer."""
        pass

    @abstractmethod
    def analyze(
        self,
        target_path: str,
        file_paths: list[str],
        file_contents: dict[str, str],
        extra_context: dict[str, Any] | None = None,
    ) -> None:
        """Analyze repository and populate relevant section in MaintainabilityAnalysisResult."""
        pass
