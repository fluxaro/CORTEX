"""Go language code analyzer."""

import re

from app.analyzers.base.base_analyzer import BaseLanguageAnalyzer
from app.analyzers.shared.metrics import calculate_maintainability_index
from app.analyzers.shared.models import (
    ClassAnalysisResult,
    FileAnalysisResult,
    FunctionAnalysisResult,
)


class GoAnalyzer(BaseLanguageAnalyzer):
    """Go source code analyzer."""

    FUNC_PATTERN = re.compile(
        r"func\s+(?:\((?:[a-zA-Z0-9_*]+\s+)?([a-zA-Z0-9_*]+)\)\s+)?([a-zA-Z0-9_]+)\s*\(([^)]*)\)"
    )
    STRUCT_PATTERN = re.compile(r"type\s+([a-zA-Z0-9_]+)\s+(?:struct|interface)\s*\{")
    IMPORT_PATTERN = re.compile(
        r"import\s+(?:\(\s*([\s\S]*?)\s*\)|[\"']([^\"']+)[\"'])"
    )
    COMPLEXITY_KEYWORDS = re.compile(r"\b(if|else|for|switch|case|select|&&|\|\|)\b")

    @property
    def language_name(self) -> str:
        return "Go"

    @property
    def supported_extensions(self) -> list[str]:
        return [".go"]

    def analyze_file(
        self,
        rel_path: str,
        content: str,
        file_size: int = 0,
    ) -> FileAnalysisResult:
        loc, comment_lines, blank_lines, code_lines = self.count_lines(content)

        functions: list[FunctionAnalysisResult] = []
        classes: list[ClassAnalysisResult] = []
        imports: list[str] = []

        # Extract Imports
        for match in self.IMPORT_PATTERN.finditer(content):
            if match.group(2):
                imports.append(match.group(2))
            elif match.group(1):
                block_imports = re.findall(r"[\"']([^\"']+)[\"']", match.group(1))
                imports.extend(block_imports)

        # Extract Structs / Interfaces as Classes
        for match in self.STRUCT_PATTERN.finditer(content):
            struct_name = match.group(1)
            classes.append(
                ClassAnalysisResult(
                    name=struct_name,
                )
            )

        # Extract Functions
        for match in self.FUNC_PATTERN.finditer(content):
            receiver = match.group(1)
            fn_name = match.group(2)
            raw_params = match.group(3)
            params = [p.strip() for p in raw_params.split(",") if p.strip()]

            # Exported (capital letter) vs Unexported (lowercase)
            visibility = "public" if fn_name[0].isupper() else "private"

            functions.append(
                FunctionAnalysisResult(
                    name=fn_name,
                    class_name=receiver.replace("*", "") if receiver else None,
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
