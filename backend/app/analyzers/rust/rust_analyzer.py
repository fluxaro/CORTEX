"""Rust code analyzer."""

import re

from app.analyzers.base.base_analyzer import BaseLanguageAnalyzer
from app.analyzers.shared.metrics import calculate_maintainability_index
from app.analyzers.shared.models import (
    ClassAnalysisResult,
    FileAnalysisResult,
    FunctionAnalysisResult,
)


class RustAnalyzer(BaseLanguageAnalyzer):
    """Rust source code analyzer."""

    FUNC_PATTERN = re.compile(
        r"(?:pub(?:\([^)]*\))?\s+)?(?:async\s+)?fn\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)"
    )
    STRUCT_PATTERN = re.compile(
        r"(?:pub(?:\([^)]*\))?\s+)?(?:struct|enum|trait)\s+([a-zA-Z0-9_]+)"
    )
    USE_PATTERN = re.compile(r"use\s+([a-zA-Z0-9_:]+);")
    COMPLEXITY_KEYWORDS = re.compile(r"\b(if|else\s+if|for|while|match|loop|&&|\|\|)\b")

    @property
    def language_name(self) -> str:
        return "Rust"

    @property
    def supported_extensions(self) -> list[str]:
        return [".rs"]

    def analyze_file(
        self,
        rel_path: str,
        content: str,
        file_size: int = 0,
    ) -> FileAnalysisResult:
        loc, comment_lines, blank_lines, code_lines = self.count_lines(content)

        functions: list[FunctionAnalysisResult] = []
        classes: list[ClassAnalysisResult] = []
        imports = self.USE_PATTERN.findall(content)

        for match in self.STRUCT_PATTERN.finditer(content):
            struct_name = match.group(1)
            classes.append(
                ClassAnalysisResult(
                    name=struct_name,
                )
            )

        for match in self.FUNC_PATTERN.finditer(content):
            fn_name = match.group(1)
            raw_params = match.group(2)
            params = [p.strip() for p in raw_params.split(",") if p.strip()]
            visibility = (
                "public"
                if "pub " in match.group(0) or "pub(" in match.group(0)
                else "private"
            )

            functions.append(
                FunctionAnalysisResult(
                    name=fn_name,
                    parameters=params,
                    visibility=visibility,
                    line_count=10,
                    complexity=1,
                )
            )

        file_complexity = max(1, len(self.COMPLEXITY_KEYWORDS.findall(content)))
        mi = calculate_maintainability_index(code_lines, file_complexity, comment_lines)

        return FileAnalysisResult(
            path=rel_path,
            language=self.language_name,
            loc=loc,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            code_lines=code_lines,
            function_count=len(functions),
            class_count=len(classes),
            import_count=len(imports),
            file_size=file_size,
            complexity=file_complexity,
            maintainability_index=mi,
            functions=functions,
            classes=classes,
            imports=imports,
        )
