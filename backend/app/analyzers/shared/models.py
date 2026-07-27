"""Data transfer objects for static analysis results."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FunctionAnalysisResult:
    """Analysis result for a single function or method."""

    name: str
    class_name: str | None = None
    parameters: list[str] = field(default_factory=list)
    return_annotation: str | None = None
    decorators: list[str] = field(default_factory=list)
    visibility: str = "public"
    method_type: str = "instance"
    line_count: int = 0
    complexity: int = 1
    nesting_depth: int = 0
    maintainability: float = 100.0


@dataclass
class ClassAnalysisResult:
    """Analysis result for a single class definition."""

    name: str
    base_classes: list[str] = field(default_factory=list)
    methods_count: int = 0
    fields_count: int = 0
    property_count: int = 0
    public_methods: int = 0
    private_methods: int = 0
    static_methods: int = 0
    abstract_methods: int = 0


@dataclass
class CodeSmellResult:
    """Identified code smell finding."""

    file_path: str
    smell_type: str
    severity: str
    line_number: int = 1
    symbol_name: str | None = None
    description: str = ""


@dataclass
class DuplicateFileLocation:
    """Single file location inside a duplicate group."""

    file_path: str
    start_line: int
    end_line: int


@dataclass
class DuplicateGroupResult:
    """Group of duplicated code blocks."""

    duplicate_hash: str
    line_count: int
    instance_count: int
    locations: list[DuplicateFileLocation] = field(default_factory=list)


@dataclass
class FileAnalysisResult:
    """Analysis metrics result for a single source file."""

    path: str
    language: str
    loc: int = 0
    comment_lines: int = 0
    blank_lines: int = 0
    code_lines: int = 0
    function_count: int = 0
    class_count: int = 0
    import_count: int = 0
    file_size: int = 0
    complexity: int = 1
    maintainability_index: float = 100.0
    functions: list[FunctionAnalysisResult] = field(default_factory=list)
    classes: list[ClassAnalysisResult] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    smells: list[CodeSmellResult] = field(default_factory=list)
    extra_metadata: dict[str, Any] = field(default_factory=dict)
