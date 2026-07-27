"""Python AST-based static code analyzer."""

import ast

from app.analyzers.base.base_analyzer import BaseLanguageAnalyzer
from app.analyzers.shared.metrics import calculate_maintainability_index
from app.analyzers.shared.models import (
    ClassAnalysisResult,
    FileAnalysisResult,
    FunctionAnalysisResult,
)


class PythonComplexityVisitor(ast.NodeVisitor):
    """AST visitor to compute cyclomatic complexity and nesting depth for Python nodes."""

    def __init__(self) -> None:
        self.complexity = 1
        self.max_nesting = 0

    def visit_If(self, node: ast.If) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node: ast.With) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncWith(self, node: ast.AsyncWith) -> None:
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        self.complexity += 1
        self.generic_visit(node)


class PythonAnalyzer(BaseLanguageAnalyzer):
    """Python source code analyzer."""

    @property
    def language_name(self) -> str:
        return "Python"

    @property
    def supported_extensions(self) -> list[str]:
        return [".py", ".pyi"]

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

        try:
            tree = ast.parse(content, filename=rel_path)
            for node in ast.iter_child_nodes(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom) and node.module:
                        imports.append(node.module)

                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    func_res = self._analyze_function(node, class_name=None)
                    functions.append(func_res)

                elif isinstance(node, ast.ClassDef):
                    cls_res, cls_funcs = self._analyze_class(node)
                    classes.append(cls_res)
                    functions.extend(cls_funcs)

        except SyntaxError:
            # Fallback if file has syntax errors
            pass

        avg_comp = (
            sum(f.complexity for f in functions) / len(functions) if functions else 1.0
        )
        file_complexity = max(1, math_round(avg_comp))
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

    def _analyze_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
        class_name: str | None,
    ) -> FunctionAnalysisResult:
        visitor = PythonComplexityVisitor()
        visitor.visit(node)

        params = [arg.arg for arg in node.args.args]
        decorators = [
            ast.unparse(d) if hasattr(ast, "unparse") else "decorator"
            for d in node.decorator_list
        ]

        line_count = (node.end_lineno or node.lineno) - node.lineno + 1

        visibility = (
            "private"
            if node.name.startswith("_") and not node.name.startswith("__")
            else "public"
        )
        method_type = "instance"
        if "staticmethod" in decorators:
            method_type = "static"
        elif "classmethod" in decorators:
            method_type = "class"
        elif "abstractmethod" in decorators:
            method_type = "abstract"

        ret_annotation = (
            ast.unparse(node.returns)
            if node.returns and hasattr(ast, "unparse")
            else None
        )

        return FunctionAnalysisResult(
            name=node.name,
            class_name=class_name,
            parameters=params,
            return_annotation=ret_annotation,
            decorators=decorators,
            visibility=visibility,
            method_type=method_type,
            line_count=line_count,
            complexity=visitor.complexity,
            nesting_depth=0,
            maintainability=100.0,
        )

    def _analyze_class(
        self, node: ast.ClassDef
    ) -> tuple[ClassAnalysisResult, list[FunctionAnalysisResult]]:
        bases = [
            ast.unparse(b) if hasattr(ast, "unparse") else "Base" for b in node.bases
        ]
        methods: list[FunctionAnalysisResult] = []
        fields_count = 0
        property_count = 0

        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_res = self._analyze_function(item, class_name=node.name)
                methods.append(func_res)
                if "property" in func_res.decorators:
                    property_count += 1
            elif isinstance(item, ast.AnnAssign) or isinstance(item, ast.Assign):
                fields_count += 1

        pub_m = sum(1 for m in methods if m.visibility == "public")
        priv_m = sum(1 for m in methods if m.visibility == "private")
        stat_m = sum(1 for m in methods if m.method_type == "static")
        abstr_m = sum(1 for m in methods if m.method_type == "abstract")

        cls_res = ClassAnalysisResult(
            name=node.name,
            base_classes=bases,
            methods_count=len(methods),
            fields_count=fields_count,
            property_count=property_count,
            public_methods=pub_m,
            private_methods=priv_m,
            static_methods=stat_m,
            abstract_methods=abstr_m,
        )
        return cls_res, methods


def math_round(val: float) -> int:
    return int(round(val))
