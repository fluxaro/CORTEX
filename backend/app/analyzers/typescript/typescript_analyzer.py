"""TypeScript and TSX code analyzer."""

import re

from app.analyzers.base.base_analyzer import BaseLanguageAnalyzer
from app.analyzers.shared.metrics import calculate_maintainability_index
from app.analyzers.shared.models import (
    ClassAnalysisResult,
    FileAnalysisResult,
    FunctionAnalysisResult,
)


class TypeScriptAnalyzer(BaseLanguageAnalyzer):
    """TypeScript source code analyzer using pattern-based structural parsing."""

    FUNC_PATTERN = re.compile(
        r"(?:export\s+)?(?:async\s+)?function\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)"
    )
    ARROW_FUNC_PATTERN = re.compile(
        r"(?:export\s+)?(?:const|let|var)\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>"
    )
    CLASS_PATTERN = re.compile(
        r"(?:export\s+)?(?:abstract\s+)?class\s+([a-zA-Z0-9_]+)(?:\s+extends\s+([a-zA-Z0-9_.]+))?"
    )
    IMPORT_PATTERN = re.compile(r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]")
    COMPLEXITY_KEYWORDS = re.compile(
        r"\b(if|else\s+if|for|while|switch|case|catch|\?\?|&&|\|\|)\b"
    )

    @property
    def language_name(self) -> str:
        return "TypeScript"

    @property
    def supported_extensions(self) -> list[str]:
        return [".ts", ".tsx"]

    def analyze_file(
        self,
        rel_path: str,
        content: str,
        file_size: int = 0,
    ) -> FileAnalysisResult:
        loc, comment_lines, blank_lines, code_lines = self.count_lines(content)

        functions: list[FunctionAnalysisResult] = []
        classes: list[ClassAnalysisResult] = []
        imports = self.IMPORT_PATTERN.findall(content)

        # Class Extraction
        for match in self.CLASS_PATTERN.finditer(content):
            cls_name = match.group(1)
            base_cls = [match.group(2)] if match.group(2) else []
            classes.append(
                ClassAnalysisResult(
                    name=cls_name,
                    base_classes=base_cls,
                    methods_count=0,
                    fields_count=0,
                    public_methods=0,
                )
            )

        # Standard Function Extraction
        for match in self.FUNC_PATTERN.finditer(content):
            fn_name = match.group(1)
            raw_params = match.group(2)
            params = [
                p.strip().split(":")[0].strip()
                for p in raw_params.split(",")
                if p.strip()
            ]
            comp = (
                len(self.COMPLEXITY_KEYWORDS.findall(content))
                // max(1, len(functions) + 1)
                + 1
            )

            functions.append(
                FunctionAnalysisResult(
                    name=fn_name,
                    parameters=params,
                    visibility="public" if not fn_name.startswith("_") else "private",
                    line_count=10,
                    complexity=comp,
                )
            )

        # Arrow Function Extraction
        for match in self.ARROW_FUNC_PATTERN.finditer(content):
            fn_name = match.group(1)
            raw_params = match.group(2)
            params = [
                p.strip().split(":")[0].strip()
                for p in raw_params.split(",")
                if p.strip()
            ]

            functions.append(
                FunctionAnalysisResult(
                    name=fn_name,
                    parameters=params,
                    visibility="public" if not fn_name.startswith("_") else "private",
                    line_count=8,
                    complexity=1,
                )
            )

        total_comp_keywords = len(self.COMPLEXITY_KEYWORDS.findall(content))
        file_complexity = max(1, total_comp_keywords)
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
