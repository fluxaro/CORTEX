"""Main Static Analysis Engine orchestrator."""

import os
from dataclasses import dataclass, field

from app.analyzers.base.base_analyzer import BaseLanguageAnalyzer
from app.analyzers.base.registry import AnalyzerRegistry
from app.analyzers.detector import RepositoryFileDetector
from app.analyzers.go.go_analyzer import GoAnalyzer
from app.analyzers.java.java_analyzer import JavaAnalyzer
from app.analyzers.javascript.javascript_analyzer import JavaScriptAnalyzer
from app.analyzers.python.python_analyzer import PythonAnalyzer
from app.analyzers.rust.rust_analyzer import RustAnalyzer
from app.analyzers.shared.duplication import DuplicationDetector
from app.analyzers.shared.metrics import (
    calculate_complexity_grade,
    calculate_maintainability_index,
)
from app.analyzers.shared.models import (
    CodeSmellResult,
    DuplicateGroupResult,
    FileAnalysisResult,
)
from app.analyzers.shared.smells import CodeSmellDetector
from app.analyzers.typescript.typescript_analyzer import TypeScriptAnalyzer


def _initialize_registry() -> None:
    """Ensure standard language analyzers are registered."""
    AnalyzerRegistry.register(PythonAnalyzer())
    AnalyzerRegistry.register(TypeScriptAnalyzer())
    AnalyzerRegistry.register(JavaScriptAnalyzer())
    AnalyzerRegistry.register(GoAnalyzer())
    AnalyzerRegistry.register(JavaAnalyzer())
    AnalyzerRegistry.register(RustAnalyzer())


_initialize_registry()


@dataclass
class RepositoryAnalysisReport:
    """Complete aggregated static analysis report for a repository."""

    total_files: int = 0
    source_files: int = 0
    test_files: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    code_lines: int = 0
    total_loc: int = 0
    comment_ratio: float = 0.0

    avg_complexity: float = 1.0
    max_complexity: int = 1
    complexity_rank: str = "A"
    maintainability_index: float = 100.0
    duplicate_percentage: float = 0.0

    file_extension_dist: dict[str, int] = field(default_factory=dict)
    language_dist: dict[str, int] = field(default_factory=dict)

    file_results: list[FileAnalysisResult] = field(default_factory=list)
    duplicate_groups: list[DuplicateGroupResult] = field(default_factory=list)
    code_smells: list[CodeSmellResult] = field(default_factory=list)


class StaticAnalysisEngine:
    """Orchestrator for analyzing a cloned repository codebase."""

    def __init__(self, target_path: str) -> None:
        self.target_path = os.path.abspath(target_path)

    def run(self) -> RepositoryAnalysisReport:
        """Run complete static code analysis pipeline."""
        if not os.path.exists(self.target_path) or not os.path.isdir(self.target_path):
            raise ValueError(
                f"Repository path '{self.target_path}' does not exist or is not a directory."
            )

        discovered = RepositoryFileDetector.discover(self.target_path)
        report = RepositoryAnalysisReport()

        report.total_files = len(discovered.all_files)
        report.source_files = len(discovered.source_files)
        report.test_files = len(discovered.test_files)

        file_contents: dict[str, str] = {}
        all_smells: list[CodeSmellResult] = []

        for rel_path in discovered.all_files:
            full_path = os.path.join(self.target_path, rel_path)
            try:
                file_size = os.path.getsize(full_path)
                with open(full_path, encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except OSError:
                continue

            file_contents[rel_path] = content

            # Extension distribution
            _, ext = os.path.splitext(rel_path.lower())
            ext_key = ext if ext else "no_extension"
            report.file_extension_dist[ext_key] = (
                report.file_extension_dist.get(ext_key, 0) + 1
            )

            # Language analyzer lookup
            analyzer = AnalyzerRegistry.get_analyzer_for_file(rel_path)
            if analyzer:
                file_res = analyzer.analyze_file(rel_path, content, file_size)
            else:
                # Generic fallback for unknown extensions
                loc, c_lines, b_lines, code_l = BaseLanguageAnalyzer.count_lines(
                    content
                )
                file_res = FileAnalysisResult(
                    path=rel_path,
                    language="Text",
                    loc=loc,
                    comment_lines=c_lines,
                    blank_lines=b_lines,
                    code_lines=code_l,
                    file_size=file_size,
                    complexity=1,
                    maintainability_index=calculate_maintainability_index(
                        code_l, 1, c_lines
                    ),
                )

            # Language distribution by code lines
            report.language_dist[file_res.language] = (
                report.language_dist.get(file_res.language, 0) + file_res.code_lines
            )

            # File level metrics aggregation
            report.total_loc += file_res.loc
            report.comment_lines += file_res.comment_lines
            report.blank_lines += file_res.blank_lines
            report.code_lines += file_res.code_lines

            # Code Smells
            smells = CodeSmellDetector.detect_file_smells(file_res)
            file_res.smells = smells
            all_smells.extend(smells)

            report.file_results.append(file_res)

        # Duplication Detection
        dup_groups, dup_pct = DuplicationDetector.detect_duplicates(file_contents)
        report.duplicate_groups = dup_groups
        report.duplicate_percentage = dup_pct
        report.code_smells = all_smells

        # Calculate overall repository metrics
        if report.file_results:
            complexities = [f.complexity for f in report.file_results]
            report.avg_complexity = round(sum(complexities) / len(complexities), 2)
            report.max_complexity = max(complexities) if complexities else 1
            report.complexity_rank = calculate_complexity_grade(report.avg_complexity)
            report.maintainability_index = round(
                sum(f.maintainability_index for f in report.file_results)
                / len(report.file_results),
                2,
            )

        report.comment_ratio = (
            round((report.comment_lines / report.total_loc) * 100.0, 2)
            if report.total_loc > 0
            else 0.0
        )

        return report
