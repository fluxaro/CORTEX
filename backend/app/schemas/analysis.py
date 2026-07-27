"""Pydantic v2 schemas for static analysis endpoints."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class AnalysisRunResponse(BaseModel):
    """Schema for analysis run status and response."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    repository_id: uuid.UUID
    status: str
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None
    commit_hash: str | None = None
    created_at: datetime
    updated_at: datetime


class RepositoryMetricsResponse(BaseModel):
    """Schema for aggregated repository metrics."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    analysis_run_id: uuid.UUID
    repository_id: uuid.UUID

    total_files: int
    source_files: int
    test_files: int

    blank_lines: int
    comment_lines: int
    code_lines: int
    total_loc: int
    comment_ratio: float

    avg_complexity: float
    max_complexity: int
    complexity_rank: str
    maintainability_index: float
    duplicate_percentage: float

    file_extension_dist: dict[str, Any]
    language_dist: dict[str, Any]

    created_at: datetime
    updated_at: datetime


class FileMetricsResponse(BaseModel):
    """Schema for file-level metrics."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    analysis_run_id: uuid.UUID
    repository_id: uuid.UUID

    path: str
    language: str
    loc: int
    comment_lines: int
    blank_lines: int
    code_lines: int

    function_count: int
    class_count: int
    import_count: int
    file_size: int

    complexity: int
    maintainability_index: float
    created_at: datetime


class FileMetricsListResponse(BaseModel):
    """Paginated list response for file metrics."""

    items: list[FileMetricsResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class FunctionMetricsResponse(BaseModel):
    """Schema for function-level metrics."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    analysis_run_id: uuid.UUID
    repository_id: uuid.UUID
    file_metrics_id: uuid.UUID

    name: str
    class_name: str | None = None
    parameters: list[str]
    return_annotation: str | None = None
    decorators: list[str]
    visibility: str
    method_type: str

    line_count: int
    complexity: int
    nesting_depth: int
    maintainability: float


class FunctionMetricsListResponse(BaseModel):
    """Paginated list response for function metrics."""

    items: list[FunctionMetricsResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ClassMetricsResponse(BaseModel):
    """Schema for class-level metrics."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    analysis_run_id: uuid.UUID
    repository_id: uuid.UUID
    file_metrics_id: uuid.UUID

    name: str
    base_classes: list[str]
    methods_count: int
    fields_count: int
    property_count: int

    public_methods: int
    private_methods: int
    static_methods: int
    abstract_methods: int


class ClassMetricsListResponse(BaseModel):
    """Paginated list response for class metrics."""

    items: list[ClassMetricsResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class CodeSmellResponse(BaseModel):
    """Schema for code smell findings."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    analysis_run_id: uuid.UUID
    repository_id: uuid.UUID

    file_path: str
    smell_type: str
    severity: str
    line_number: int
    symbol_name: str | None = None
    description: str


class CodeSmellListResponse(BaseModel):
    """Paginated list response for code smells."""

    items: list[CodeSmellResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
