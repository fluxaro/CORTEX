"""File system indexer service for cloned repositories."""

import os
from typing import Any

# Standard language mapping by file extension
EXTENSION_TO_LANGUAGE: dict[str, str] = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript (React)",
    ".ts": "TypeScript",
    ".tsx": "TypeScript (React)",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".cc": "C++",
    ".h": "C/C++ Header",
    ".hpp": "C++ Header",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "Sass/SCSS",
    ".less": "Less",
    ".sql": "SQL",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".ps1": "PowerShell",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".json": "JSON",
    ".xml": "XML",
    ".md": "Markdown",
    ".rst": "ReStructuredText",
    ".dockerfile": "Dockerfile",
    ".kt": "Kotlin",
    ".swift": "Swift",
    ".dart": "Dart",
    ".scala": "Scala",
    ".lua": "Lua",
    ".r": "R",
    ".m": "Objective-C",
}


class FileIndexerService:
    """Service to scan a cloned repository directory and generate a file system index."""

    @staticmethod
    def index_directory(
        target_path: str, max_largest_files: int = 10
    ) -> dict[str, Any]:
        """Traverse target_path directory and compute file index metrics.

        Ignores `.git` directories and files.
        """
        abs_target_path = os.path.abspath(target_path)
        if not os.path.exists(abs_target_path) or not os.path.isdir(abs_target_path):
            raise ValueError(
                f"Directory '{abs_target_path}' does not exist or is not a directory."
            )

        folder_count = 0
        file_count = 0
        max_depth = 0
        total_size_bytes = 0

        all_file_records: list[dict[str, Any]] = []
        extension_counts: dict[str, int] = {}
        language_dist: dict[str, dict[str, int]] = {}

        base_depth = abs_target_path.rstrip(os.sep).count(os.sep)

        for root, dirs, files in os.walk(abs_target_path):
            # Prune .git directory
            if ".git" in dirs:
                dirs.remove(".git")

            # Calculate current depth relative to root directory
            current_depth = root.count(os.sep) - base_depth
            if current_depth > max_depth:
                max_depth = current_depth

            folder_count += len(dirs)

            for file_name in files:
                file_count += 1
                full_file_path = os.path.join(root, file_name)
                rel_path = os.path.relpath(full_file_path, abs_target_path).replace(
                    "\\", "/"
                )

                try:
                    file_stat = os.stat(full_file_path)
                    file_size = file_stat.st_size
                except OSError:
                    file_size = 0

                total_size_bytes += file_size

                # Extract extension
                _, ext = os.path.splitext(file_name)
                ext = ext.lower() if ext else "no_extension"

                extension_counts[ext] = extension_counts.get(ext, 0) + 1

                # Language mapping
                lang = EXTENSION_TO_LANGUAGE.get(ext, "Other")
                if lang not in language_dist:
                    language_dist[lang] = {"files": 0, "bytes": 0}
                language_dist[lang]["files"] += 1
                language_dist[lang]["bytes"] += file_size

                all_file_records.append(
                    {
                        "path": rel_path,
                        "size": file_size,
                    }
                )

        # Sort largest files by size descending
        all_file_records.sort(key=lambda x: x["size"], reverse=True)
        largest_files = all_file_records[:max_largest_files]

        return {
            "folder_count": folder_count,
            "file_count": file_count,
            "max_depth": max_depth,
            "total_size_bytes": total_size_bytes,
            "largest_files": largest_files,
            "file_extensions": extension_counts,
            "language_distribution": language_dist,
        }
