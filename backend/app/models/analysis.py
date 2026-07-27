"""Database models for static analysis metrics and findings."""

import enum
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, utc_now


class AnalysisRunStatus(enum.StrEnum):
    """Status of an analysis run."""

    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class AnalysisRun(Base):
    """Represents a single static analysis run for a repository."""

    __tablename__ = "analysis_runs"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(50), default=AnalysisRunStatus.PENDING.value, nullable=False, index=True
    )
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    commit_hash: Mapped[str | None] = mapped_column(String(100), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )

    # Relationships
    repository_metrics: Mapped["RepositoryMetrics | None"] = relationship(
        "RepositoryMetrics",
        back_populates="analysis_run",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    file_metrics: Mapped[list["FileMetrics"]] = relationship(
        "FileMetrics",
        back_populates="analysis_run",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    code_smells: Mapped[list["CodeSmell"]] = relationship(
        "CodeSmell",
        back_populates="analysis_run",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    duplicate_groups: Mapped[list["DuplicateGroup"]] = relationship(
        "DuplicateGroup",
        back_populates="analysis_run",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class RepositoryMetrics(Base):
    """Aggregated repository-level engineering metrics."""

    __tablename__ = "repository_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    total_files: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    source_files: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    test_files: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    blank_lines: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comment_lines: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    code_lines: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_loc: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comment_ratio: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    avg_complexity: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    max_complexity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    complexity_rank: Mapped[str] = mapped_column(String(5), default="A", nullable=False)
    maintainability_index: Mapped[float] = mapped_column(
        Float, default=100.0, nullable=False
    )
    duplicate_percentage: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )

    file_extension_dist: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )
    language_dist: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )

    analysis_run: Mapped[AnalysisRun] = relationship(
        "AnalysisRun", back_populates="repository_metrics"
    )


class FileMetrics(Base):
    """File-level code metrics."""

    __tablename__ = "file_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    path: Mapped[str] = mapped_column(String(1024), nullable=False, index=True)
    language: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    loc: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    comment_lines: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    blank_lines: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    code_lines: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    function_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    class_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    import_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    complexity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    maintainability_index: Mapped[float] = mapped_column(
        Float, default=100.0, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    analysis_run: Mapped[AnalysisRun] = relationship(
        "AnalysisRun", back_populates="file_metrics"
    )
    functions: Mapped[list["FunctionMetrics"]] = relationship(
        "FunctionMetrics",
        back_populates="file_metric",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    classes: Mapped[list["ClassMetrics"]] = relationship(
        "ClassMetrics",
        back_populates="file_metric",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class FunctionMetrics(Base):
    """Function-level code metrics."""

    __tablename__ = "function_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_metrics_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("file_metrics.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    class_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    parameters: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    return_annotation: Mapped[str | None] = mapped_column(String(255), nullable=True)
    decorators: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    visibility: Mapped[str] = mapped_column(
        String(50), default="public", nullable=False
    )
    method_type: Mapped[str] = mapped_column(
        String(50), default="instance", nullable=False
    )

    line_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    complexity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    nesting_depth: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    maintainability: Mapped[float] = mapped_column(Float, default=100.0, nullable=False)

    file_metric: Mapped[FileMetrics] = relationship(
        "FileMetrics", back_populates="functions"
    )


class ClassMetrics(Base):
    """Class-level code metrics."""

    __tablename__ = "class_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_metrics_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("file_metrics.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    base_classes: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    methods_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    fields_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    property_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    public_methods: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    private_methods: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    static_methods: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    abstract_methods: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    file_metric: Mapped[FileMetrics] = relationship(
        "FileMetrics", back_populates="classes"
    )


class DuplicateGroup(Base):
    """Group of identical or near-duplicate code blocks."""

    __tablename__ = "duplicate_groups"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    duplicate_hash: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    line_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    instance_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    analysis_run: Mapped[AnalysisRun] = relationship(
        "AnalysisRun", back_populates="duplicate_groups"
    )
    duplicate_files: Mapped[list["DuplicateFile"]] = relationship(
        "DuplicateFile",
        back_populates="duplicate_group",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class DuplicateFile(Base):
    """Single file occurrence location inside a duplicate group."""

    __tablename__ = "duplicate_files"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    duplicate_group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("duplicate_groups.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    start_line: Mapped[int] = mapped_column(Integer, nullable=False)
    end_line: Mapped[int] = mapped_column(Integer, nullable=False)

    duplicate_group: Mapped[DuplicateGroup] = relationship(
        "DuplicateGroup", back_populates="duplicate_files"
    )


class CodeSmell(Base):
    """Code quality finding / smell instance."""

    __tablename__ = "code_smells"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    file_path: Mapped[str] = mapped_column(String(1024), nullable=False, index=True)
    smell_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    severity: Mapped[str] = mapped_column(String(50), default="WARNING", nullable=False)

    line_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    symbol_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    analysis_run: Mapped[AnalysisRun] = relationship(
        "AnalysisRun", back_populates="code_smells"
    )
