"""Database models for Architecture Intelligence metrics, patterns, and dependency graph."""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, utc_now


class ArchitectureAnalysis(Base):
    """Aggregated architecture intelligence analysis run for a repository."""

    __tablename__ = "architecture_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    arch_style: Mapped[str] = mapped_column(
        String(100), default="Monolith", nullable=False
    )
    confidence_score: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)

    layer_separation_score: Mapped[float] = mapped_column(
        Float, default=85.0, nullable=False
    )
    dependency_direction_score: Mapped[float] = mapped_column(
        Float, default=90.0, nullable=False
    )
    pattern_confidence: Mapped[float] = mapped_column(
        Float, default=80.0, nullable=False
    )
    project_organization_score: Mapped[float] = mapped_column(
        Float, default=85.0, nullable=False
    )
    coupling_score: Mapped[float] = mapped_column(Float, default=75.0, nullable=False)
    modularity_score: Mapped[float] = mapped_column(Float, default=80.0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )

    # Relationships
    layers: Mapped[list["ArchitectureLayer"]] = relationship(
        "ArchitectureLayer",
        back_populates="architecture_analysis",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    violations: Mapped[list["ArchitectureViolation"]] = relationship(
        "ArchitectureViolation",
        back_populates="architecture_analysis",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    patterns: Mapped[list["DetectedPattern"]] = relationship(
        "DetectedPattern",
        back_populates="architecture_analysis",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    frameworks: Mapped[list["FrameworkDetection"]] = relationship(
        "FrameworkDetection",
        back_populates="architecture_analysis",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    dependency_graph: Mapped["DependencyGraph | None"] = relationship(
        "DependencyGraph",
        back_populates="architecture_analysis",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    technology_stack: Mapped["TechnologyStack | None"] = relationship(
        "TechnologyStack",
        back_populates="architecture_analysis",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class ArchitectureLayer(Base):
    """Identified architectural layer in repository."""

    __tablename__ = "architecture_layers"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    architecture_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("architecture_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    file_paths: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)

    architecture_analysis: Mapped[ArchitectureAnalysis] = relationship(
        "ArchitectureAnalysis", back_populates="layers"
    )


class ArchitectureViolation(Base):
    """Architectural rule violation."""

    __tablename__ = "architecture_violations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    architecture_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("architecture_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    violation_type: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default="WARNING", nullable=False)
    source_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    target_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    architecture_analysis: Mapped[ArchitectureAnalysis] = relationship(
        "ArchitectureAnalysis", back_populates="violations"
    )


class DetectedPattern(Base):
    """Design pattern identified in codebase."""

    __tablename__ = "detected_patterns"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    architecture_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("architecture_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    pattern_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.8, nullable=False)
    location: Mapped[str] = mapped_column(String(1024), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    architecture_analysis: Mapped[ArchitectureAnalysis] = relationship(
        "ArchitectureAnalysis", back_populates="patterns"
    )


class DependencyGraph(Base):
    """Graph container for repository module dependencies."""

    __tablename__ = "dependency_graphs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    architecture_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("architecture_analyses.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    total_nodes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_edges: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    architecture_analysis: Mapped[ArchitectureAnalysis] = relationship(
        "ArchitectureAnalysis", back_populates="dependency_graph"
    )
    nodes: Mapped[list["DependencyNode"]] = relationship(
        "DependencyNode",
        back_populates="graph",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    edges: Mapped[list["DependencyEdge"]] = relationship(
        "DependencyEdge",
        back_populates="graph",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class DependencyNode(Base):
    """Node in module dependency graph."""

    __tablename__ = "dependency_nodes"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    dependency_graph_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dependency_graphs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    node_identifier: Mapped[str] = mapped_column(String(512), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    node_type: Mapped[str] = mapped_column(
        String(50), default="internal", nullable=False
    )
    layer_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    path: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    graph: Mapped[DependencyGraph] = relationship(
        "DependencyGraph", back_populates="nodes"
    )


class DependencyEdge(Base):
    """Directed edge in module dependency graph."""

    __tablename__ = "dependency_edges"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    dependency_graph_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("dependency_graphs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    source_node_id: Mapped[str] = mapped_column(String(512), nullable=False)
    target_node_id: Mapped[str] = mapped_column(String(512), nullable=False)
    import_type: Mapped[str] = mapped_column(
        String(50), default="direct", nullable=False
    )
    weight: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    graph: Mapped[DependencyGraph] = relationship(
        "DependencyGraph", back_populates="edges"
    )


class FrameworkDetection(Base):
    """Detected web/backend framework and convention findings."""

    __tablename__ = "framework_detections"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    architecture_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("architecture_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    detected_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    is_convention_compliant: Mapped[bool] = mapped_column(default=True, nullable=False)
    convention_findings: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, default=list, nullable=False
    )

    architecture_analysis: Mapped[ArchitectureAnalysis] = relationship(
        "ArchitectureAnalysis", back_populates="frameworks"
    )


class TechnologyStack(Base):
    """Categorized technology stack metadata."""

    __tablename__ = "technology_stacks"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    architecture_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("architecture_analyses.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    languages: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    frameworks: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    orms: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    databases: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    cloud: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    ci_cd: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    package_managers: Mapped[list[str]] = mapped_column(
        JSON, default=list, nullable=False
    )
    build_tools: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    testing_frameworks: Mapped[list[str]] = mapped_column(
        JSON, default=list, nullable=False
    )
    formatters: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    linters: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    containers: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    caching: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    auth: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    api_surfaces: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    architecture_analysis: Mapped[ArchitectureAnalysis] = relationship(
        "ArchitectureAnalysis", back_populates="technology_stack"
    )


class ArchitectureRecommendationPlaceholder(Base):
    """Placeholder model for architecture recommendations in future phases."""

    __tablename__ = "architecture_recommendation_placeholders"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    architecture_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("architecture_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
