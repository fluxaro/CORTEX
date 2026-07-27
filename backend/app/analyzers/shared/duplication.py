"""Duplicate code block detection engine."""

import hashlib

from app.analyzers.shared.models import DuplicateFileLocation, DuplicateGroupResult


class DuplicationDetector:
    """Detects duplicated blocks of code across files using sliding window hashing."""

    @classmethod
    def _index_file_blocks(
        cls,
        rel_path: str,
        content: str,
        min_lines: int,
        block_map: dict[str, list[tuple[str, int, int]]],
    ) -> int:
        lines = [line.strip() for line in content.splitlines()]
        if len(lines) < min_lines:
            return len(lines)

        for i in range(len(lines) - min_lines + 1):
            window = [
                line
                for line in lines[i : i + min_lines]
                if line and line not in ("{", "}", ");", "end")
            ]
            if len(window) < min_lines // 2:
                continue

            window_str = "\n".join(window)
            block_hash = hashlib.sha256(window_str.encode("utf-8")).hexdigest()
            block_map.setdefault(block_hash, []).append(
                (rel_path, i + 1, i + min_lines)
            )

        return len(lines)

    @classmethod
    def detect_duplicates(
        cls,
        file_contents: dict[str, str],
        min_lines: int = 6,
    ) -> tuple[list[DuplicateGroupResult], float]:
        """Detect duplicated line blocks across file_contents mapping (rel_path -> source_code)."""
        block_map: dict[str, list[tuple[str, int, int]]] = {}
        total_source_lines = sum(
            cls._index_file_blocks(path, content, min_lines, block_map)
            for path, content in file_contents.items()
        )

        duplicated_lines_set: set[tuple[str, int]] = set()
        duplicate_groups: list[DuplicateGroupResult] = []

        for b_hash, locations in block_map.items():
            unique_locations: list[DuplicateFileLocation] = []
            seen_locs: set[tuple[str, int]] = set()

            for path, start_line, end_line in locations:
                key = (path, start_line)
                if key not in seen_locs:
                    seen_locs.add(key)
                    unique_locations.append(
                        DuplicateFileLocation(
                            file_path=path,
                            start_line=start_line,
                            end_line=end_line,
                        )
                    )
                    for line_no in range(start_line, end_line + 1):
                        duplicated_lines_set.add((path, line_no))

            if len(unique_locations) >= 2:
                duplicate_groups.append(
                    DuplicateGroupResult(
                        duplicate_hash=b_hash,
                        line_count=min_lines,
                        instance_count=len(unique_locations),
                        locations=unique_locations,
                    )
                )

        duplicate_percentage = (
            round((len(duplicated_lines_set) / total_source_lines) * 100.0, 2)
            if total_source_lines > 0
            else 0.0
        )

        return duplicate_groups, duplicate_percentage
