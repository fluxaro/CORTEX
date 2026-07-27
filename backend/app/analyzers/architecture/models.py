"""Data transfer objects for Architecture Intelligence analysis."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DetectedPatternResult:
    """Design pattern finding result."""

    pattern_name: str
    category: str
    confidence_score: float
    location: str
    description: str


@dataclass
class FrameworkDetectionResult:
    """Framework detection result."""

    name: str
    category: str
    detected_version: str | None = None
    is_convention_compliant: bool = True
    convention_findings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class TechStackResult:
    """Structured technology stack metadata."""

    languages: list[str] = field(default_factory=list)
    frameworks: list[str] = field(default_factory=list)
    orms: list[str] = field(default_factory=list)
    databases: list[str] = field(default_factory=list)
    cloud: list[str] = field(default_factory=list)
    ci_cd: list[str] = field(default_factory=list)
    package_managers: list[str] = field(default_factory=list)
    build_tools: list[str] = field(default_factory=list)
    testing_frameworks: list[str] = field(default_factory=list)
    formatters: list[str] = field(default_factory=list)
    linters: list[str] = field(default_factory=list)
    containers: list[str] = field(default_factory=list)
    caching: list[str] = field(default_factory=list)
    auth: list[str] = field(default_factory=list)
    api_surfaces: list[str] = field(default_factory=list)


@dataclass
class LayerResult:
    """Architectural layer finding."""

    name: str
    category: str
    file_paths: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class ViolationResult:
    """Architectural rule violation."""

    violation_type: str
    severity: str
    source_path: str
    target_path: str
    description: str


@dataclass
class DependencyNodeResult:
    """Node in dependency graph."""

    node_id: str
    name: str
    node_type: str  # "internal" or "external"
    layer_name: str | None = None
    path: str | None = None


@dataclass
class DependencyEdgeResult:
    """Edge in dependency graph."""

    source_id: str
    target_id: str
    import_type: str = "direct"
    weight: int = 1


@dataclass
class DependencyGraphData:
    """Dependency graph nodes and directed edges."""

    nodes: list[DependencyNodeResult] = field(default_factory=list)
    edges: list[DependencyEdgeResult] = field(default_factory=list)


@dataclass
class ArchitectureAnalysisResult:
    """Aggregated report result from Architecture Intelligence Engine."""

    arch_style: str = "Monolith"
    confidence_score: float = 0.8
    layer_separation_score: float = 85.0
    dependency_direction_score: float = 90.0
    pattern_confidence: float = 80.0
    project_organization_score: float = 85.0
    coupling_score: float = 75.0
    modularity_score: float = 80.0

    layers: list[LayerResult] = field(default_factory=list)
    patterns: list[DetectedPatternResult] = field(default_factory=list)
    frameworks: list[FrameworkDetectionResult] = field(default_factory=list)
    violations: list[ViolationResult] = field(default_factory=list)
    tech_stack: TechStackResult = field(default_factory=TechStackResult)
    graph_data: DependencyGraphData = field(default_factory=DependencyGraphData)
