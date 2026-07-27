"""Pydantic v2 schemas for Architecture Intelligence endpoints."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ArchitectureLayerResponse(BaseModel):
    """Schema for architectural layer finding."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    category: str
    file_paths: list[str]
    description: str


class ArchitectureViolationResponse(BaseModel):
    """Schema for architecture violation finding."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    violation_type: str
    severity: str
    source_path: str
    target_path: str
    description: str


class DetectedPatternResponse(BaseModel):
    """Schema for design pattern finding."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    pattern_name: str
    category: str
    confidence_score: float
    location: str
    description: str


class DetectedPatternListResponse(BaseModel):
    """Paginated list response for design patterns."""

    items: list[DetectedPatternResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class DependencyNodeResponse(BaseModel):
    """Schema for node in module dependency graph."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    node_identifier: str
    name: str
    node_type: str
    layer_name: str | None = None
    path: str | None = None


class DependencyEdgeResponse(BaseModel):
    """Schema for edge in module dependency graph."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    source_node_id: str
    target_node_id: str
    import_type: str
    weight: int


class DependencyGraphResponse(BaseModel):
    """Schema for complete dependency graph."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    total_nodes: int
    total_edges: int
    nodes: list[DependencyNodeResponse]
    edges: list[DependencyEdgeResponse]
    created_at: datetime


class FrameworkDetectionResponse(BaseModel):
    """Schema for framework detection finding."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    category: str
    detected_version: str | None = None
    is_convention_compliant: bool
    convention_findings: list[dict[str, Any]]


class TechnologyStackResponse(BaseModel):
    """Schema for extracted technology stack metadata."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    languages: list[str]
    frameworks: list[str]
    orms: list[str]
    databases: list[str]
    cloud: list[str]
    ci_cd: list[str]
    package_managers: list[str]
    build_tools: list[str]
    testing_frameworks: list[str]
    formatters: list[str]
    linters: list[str]
    containers: list[str]
    caching: list[str]
    auth: list[str]
    api_surfaces: list[str]


class ArchitectureAnalysisResponse(BaseModel):
    """Schema for overall architecture intelligence report."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    repository_id: uuid.UUID
    analysis_run_id: uuid.UUID

    arch_style: str
    confidence_score: float

    layer_separation_score: float
    dependency_direction_score: float
    pattern_confidence: float
    project_organization_score: float
    coupling_score: float
    modularity_score: float

    layers: list[ArchitectureLayerResponse]
    violations: list[ArchitectureViolationResponse]
    patterns: list[DetectedPatternResponse]
    frameworks: list[FrameworkDetectionResponse]
    technology_stack: TechnologyStackResponse | None = None

    created_at: datetime
    updated_at: datetime
