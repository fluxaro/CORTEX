"""Abstract base class for all language-specific code analyzers."""

from abc import ABC, abstractmethod

from app.analyzers.shared.models import FileAnalysisResult


class BaseLanguageAnalyzer(ABC):
    """Abstract base analyzer for parsing and extracting code metrics."""

    @property
    @abstractmethod
    def language_name(self) -> str:
        """Return the canonical language name (e.g. 'Python', 'TypeScript')."""
        pass

    @property
    @abstractmethod
    def supported_extensions(self) -> list[str]:
        """Return list of supported file extensions (e.g. ['.py', '.pyi'])."""
        pass

    @abstractmethod
    def analyze_file(
        self,
        rel_path: str,
        content: str,
        file_size: int = 0,
    ) -> FileAnalysisResult:
        """Analyze a single source code file and return FileAnalysisResult."""
        pass

    @staticmethod
    def count_lines(content: str) -> tuple[int, int, int, int]:
        """Utility to calculate (loc, comment_lines, blank_lines, code_lines)."""
        lines = content.splitlines()
        loc = len(lines)
        blank_lines = 0
        comment_lines = 0

        for line in lines:
            stripped = line.strip()
            if not stripped:
                blank_lines += 1
            elif (
                stripped.startswith("#")
                or stripped.startswith("//")
                or stripped.startswith("/*")
                or stripped.startswith("*")
            ):
                comment_lines += 1

        code_lines = loc - blank_lines - comment_lines
        return loc, comment_lines, blank_lines, max(0, code_lines)
