"""Static code smell detector."""

from app.analyzers.shared.models import (
    CodeSmellResult,
    FileAnalysisResult,
)


class CodeSmellDetector:
    """Detects architectural and code quality smells across files, functions, and classes."""

    @staticmethod
    def detect_file_smells(file_res: FileAnalysisResult) -> list[CodeSmellResult]:
        """Inspect a file analysis result and identify code smells."""
        smells: list[CodeSmellResult] = []
        path = file_res.path

        # 1. Long File
        if file_res.loc > 500:
            smells.append(
                CodeSmellResult(
                    file_path=path,
                    smell_type="Long File",
                    severity="WARNING",
                    line_number=1,
                    description=f"File '{path}' has {file_res.loc} lines of code (threshold: 500).",
                )
            )

        # 2. Function Smells
        for func in file_res.functions:
            # Long Function
            if func.line_count > 50:
                smells.append(
                    CodeSmellResult(
                        file_path=path,
                        smell_type="Long Function",
                        severity="WARNING",
                        line_number=1,
                        symbol_name=func.name,
                        description=f"Function '{func.name}' has {func.line_count} lines of code (threshold: 50).",
                    )
                )

            # Too Many Parameters
            if len(func.parameters) > 5:
                smells.append(
                    CodeSmellResult(
                        file_path=path,
                        smell_type="Too Many Parameters",
                        severity="WARNING",
                        line_number=1,
                        symbol_name=func.name,
                        description=f"Function '{func.name}' has {len(func.parameters)} parameters (threshold: 5).",
                    )
                )

            # Deep Nesting
            if func.nesting_depth > 4:
                smells.append(
                    CodeSmellResult(
                        file_path=path,
                        smell_type="Deep Nesting",
                        severity="WARNING",
                        line_number=1,
                        symbol_name=func.name,
                        description=f"Function '{func.name}' has nesting depth of {func.nesting_depth} (threshold: 4).",
                    )
                )

        # 3. Class Smells
        for cls in file_res.classes:
            # Large Class / God Object
            if cls.methods_count > 20:
                smells.append(
                    CodeSmellResult(
                        file_path=path,
                        smell_type="Large Class",
                        severity="WARNING",
                        line_number=1,
                        symbol_name=cls.name,
                        description=f"Class '{cls.name}' has {cls.methods_count} methods (threshold: 20).",
                    )
                )

        return smells
