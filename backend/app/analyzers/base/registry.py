"""Central registry for language analyzers."""

import os
from typing import ClassVar

from app.analyzers.base.base_analyzer import BaseLanguageAnalyzer


class AnalyzerRegistry:
    """Registry mapping file extensions and language names to analyzer instances."""

    _analyzers_by_ext: ClassVar[dict[str, BaseLanguageAnalyzer]] = {}
    _analyzers_by_lang: ClassVar[dict[str, BaseLanguageAnalyzer]] = {}

    @classmethod
    def register(cls, analyzer: BaseLanguageAnalyzer) -> None:
        """Register a language analyzer instance."""
        cls._analyzers_by_lang[analyzer.language_name.lower()] = analyzer
        for ext in analyzer.supported_extensions:
            cls._analyzers_by_ext[ext.lower()] = analyzer

    @classmethod
    def get_analyzer_for_extension(cls, extension: str) -> BaseLanguageAnalyzer | None:
        """Get analyzer registered for a file extension."""
        return cls._analyzers_by_ext.get(extension.lower())

    @classmethod
    def get_analyzer_for_file(cls, file_path: str) -> BaseLanguageAnalyzer | None:
        """Get analyzer for a file path based on extension."""
        _, ext = os.path.splitext(file_path)
        if not ext and file_path.lower().endswith("dockerfile"):
            ext = ".dockerfile"
        return cls.get_analyzer_for_extension(ext)

    @classmethod
    def get_analyzer_for_language(cls, language: str) -> BaseLanguageAnalyzer | None:
        """Get analyzer registered for a canonical language name."""
        return cls._analyzers_by_lang.get(language.lower())

    @classmethod
    def clear(cls) -> None:
        """Clear all registered analyzers (useful for testing)."""
        cls._analyzers_by_ext.clear()
        cls._analyzers_by_lang.clear()
