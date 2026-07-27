"""Repository file discovery and categorization module."""

import os
from dataclasses import dataclass, field

DEFAULT_IGNORE_DIRS = {
    ".git",
    "node_modules",
    "venv",
    ".venv",
    "dist",
    "build",
    "coverage",
    ".next",
    "target",
    "vendor",
    ".cache",
    "__pycache__",
    ".idea",
    ".vscode",
}

TEST_PATTERNS = {"test_", "_test.", "spec.", ".spec.", ".test.", "tests"}
DOC_EXTENSIONS = {".md", ".rst", ".txt", ".adoc"}
CONFIG_EXTENSIONS = {
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".xml",
    ".env",
    ".editorconfig",
    ".dockerignore",
}


@dataclass
class DiscoveredFiles:
    """Discovered repository files categorized by type."""

    source_files: list[str] = field(default_factory=list)
    test_files: list[str] = field(default_factory=list)
    config_files: list[str] = field(default_factory=list)
    doc_files: list[str] = field(default_factory=list)
    all_files: list[str] = field(default_factory=list)


class RepositoryFileDetector:
    """Discovers and categorizes all relevant repository files."""

    @staticmethod
    def discover(
        target_path: str,
        custom_ignore_dirs: set[str] | None = None,
    ) -> DiscoveredFiles:
        """Traverse target_path and categorize files."""
        abs_target_path = os.path.abspath(target_path)
        ignore_dirs = DEFAULT_IGNORE_DIRS.union(custom_ignore_dirs or set())

        result = DiscoveredFiles()

        for root, dirs, files in os.walk(abs_target_path):
            # Prune ignored directories in-place
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            for file_name in files:
                full_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(full_path, abs_target_path).replace(
                    "\\", "/"
                )
                result.all_files.append(rel_path)

                file_lower = file_name.lower()
                _, ext = os.path.splitext(file_lower)

                # Categorization rules
                if (
                    any(tp in file_lower for tp in TEST_PATTERNS)
                    or "/test/" in rel_path.lower()
                    or "/tests/" in rel_path.lower()
                ):
                    result.test_files.append(rel_path)
                elif ext in DOC_EXTENSIONS or file_lower in (
                    "license",
                    "changelog",
                    "readme",
                    "notice",
                ):
                    result.doc_files.append(rel_path)
                elif (
                    ext in CONFIG_EXTENSIONS
                    or file_lower.startswith(".env")
                    or file_lower.endswith("config")
                ):
                    result.config_files.append(rel_path)
                else:
                    result.source_files.append(rel_path)

        return result
