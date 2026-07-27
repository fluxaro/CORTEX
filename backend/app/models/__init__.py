"""SQLAlchemy models module."""

from app.models.analysis import (
    AnalysisRun,
    AnalysisRunStatus,
    ClassMetrics,
    CodeSmell,
    DuplicateFile,
    DuplicateGroup,
    FileMetrics,
    FunctionMetrics,
    RepositoryMetrics,
)
from app.models.architecture import (
    ArchitectureAnalysis,
    ArchitectureLayer,
    ArchitectureRecommendationPlaceholder,
    ArchitectureViolation,
    DependencyEdge,
    DependencyGraph,
    DependencyNode,
    DetectedPattern,
    FrameworkDetection,
    TechnologyStack,
)
from app.models.base import Base
from app.models.repository import (
    AnalysisStatus,
    Repository,
    RepositoryFileIndex,
    RepositoryStatus,
)

__all__ = [
    "Base",
    "Repository",
    "RepositoryFileIndex",
    "RepositoryStatus",
    "AnalysisStatus",
    "AnalysisRun",
    "AnalysisRunStatus",
    "RepositoryMetrics",
    "FileMetrics",
    "FunctionMetrics",
    "ClassMetrics",
    "DuplicateGroup",
    "DuplicateFile",
    "CodeSmell",
    "ArchitectureAnalysis",
    "ArchitectureLayer",
    "ArchitectureViolation",
    "DetectedPattern",
    "DependencyGraph",
    "DependencyNode",
    "DependencyEdge",
    "FrameworkDetection",
    "TechnologyStack",
    "ArchitectureRecommendationPlaceholder",
]
