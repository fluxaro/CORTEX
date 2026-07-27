"""Java code analyzer."""

import re

from app.analyzers.base.base_analyzer import BaseLanguageAnalyzer
from app.analyzers.shared.metrics import calculate_maintainability_index
from app.analyzers.shared.models import (
    ClassAnalysisResult,
    FileAnalysisResult,
    FunctionAnalysisResult,
)


class JavaAnalyzer(BaseLanguageAnalyzer):
    """Java source code analyzer."""

    CLASS_PATTERN = re.compile(
        r"(?:public|protected|private)?\s*(?:abstract|final)?\s*(?:class|interface|enum)\s+([a-zA-Z0-9_]+)(?:\s+extends\s+([a-zA-Z0-9_.<]+))?"
    )
    METHOD_PATTERN = re.compile(
        r"(?:public|protected|private)?\s*(?:static|final|abstract|synchronized)?\s*([a-zA-Z0-9_<>]+)\s+([a-zA-Z0-9_]+)\s*\(([^)]*)\)"
    )
    IMPORT_PATTERN = re.compile(r"import\s+(?:static\s+)?([a-zA-Z0-9_.*]+);")
    COMPLEXITY_KEYWORDS = re.compile(
        r"\b(if|else\s+if|for|while|switch|case|catch|&&|\|\|)\b"
    )

    @property
    def language_name(self) -> str:
        return "Java"

    @property
    def supported_extensions(self) -> list[str]:
        return [".java"]

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

        for match in self.CLASS_PATTERN.finditer(content):
            cls_name = match.group(1)
            base_cls = [match.group(2)] if match.group(2) else []
            classes.append(
                ClassAnalysisResult(
                    name=cls_name,
                    base_classes=base_cls,
                )
            )

        for match in self.METHOD_PATTERN.finditer(content):
            ret_type = match.group(1)
            method_name = match.group(2)
            raw_params = match.group(3)

            # Skip control structures falsely matched
            if method_name in ("if", "while", "for", "switch", "catch"):
                continue

            params = [p.strip() for p in raw_params.split(",") if p.strip()]

            functions.append(
                FunctionAnalysisResult(
                    name=method_name,
                    return_annotation=ret_type,
                    parameters=params,
                    visibility=(
                        "public"
                        if "public " + method_name in match.group(0)
                        else "private"
                    ),
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
