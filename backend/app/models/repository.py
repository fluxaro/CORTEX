"""Repository and File Index database models."""

import enum
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, utc_now


class RepositoryStatus(enum.StrEnum):
    """Lifecycle status of a repository ingestion."""

    PENDING = "PENDING"
    CLONING = "CLONING"
    READY = "READY"
    FAILED = "FAILED"


class AnalysisStatus(enum.StrEnum):
    """Analysis status of a repository."""

    PENDING = "PENDING"
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Repository(Base):
    """Repository database model."""

    __tablename__ = "repositories"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(
        String(512), unique=True, nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    default_branch: Mapped[str] = mapped_column(
        String(255), nullable=False, default="main"
    )
    stars: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    forks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    language: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    license: Mapped[str | None] = mapped_column(String(255), nullable=True)
    clone_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    html_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    visibility: Mapped[str] = mapped_column(
        String(50), default="public", nullable=False
    )
    size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    last_pushed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default=RepositoryStatus.PENDING.value,
        nullable=False,
        index=True,
    )
    analysis_status: Mapped[str] = mapped_column(
        String(50), default=AnalysisStatus.PENDING.value, nullable=False
    )
    local_path: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    # Auditing timestamps
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )

    # Relationship to File Index
    file_index: Mapped["RepositoryFileIndex | None"] = relationship(
        "RepositoryFileIndex",
        back_populates="repository",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class RepositoryFileIndex(Base):
    """File system index metadata for a cloned repository."""

    __tablename__ = "repository_file_indices"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    folder_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    file_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_depth: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_size_bytes: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    largest_files: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, default=list, nullable=False
    )
    file_extensions: Mapped[dict[str, int]] = mapped_column(
        JSON, default=dict, nullable=False
    )
    language_distribution: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )

    repository: Mapped[Repository] = relationship(
        "Repository", back_populates="file_index"
    )
