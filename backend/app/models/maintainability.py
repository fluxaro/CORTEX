"""Database models for Maintainability & Repository Intelligence findings and metrics."""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, utc_now


class DocumentationAnalysis(Base):
    """Documentation structure and frameworks report."""

    __tablename__ = "documentation_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    documentation_score: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )
    has_architecture_docs: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    has_api_docs: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_deployment_guide: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    has_dev_guide: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    doc_frameworks: Mapped[list[str]] = mapped_column(
        JSON, default=list, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    readme_analysis: Mapped["ReadmeAnalysis | None"] = relationship(
        "ReadmeAnalysis",
        back_populates="documentation_analysis",
        uselist=False,
        cascade="all, delete-orphan",
    )
    sections: Mapped[list["DocumentationSection"]] = relationship(
        "DocumentationSection",
        back_populates="documentation_analysis",
        cascade="all, delete-orphan",
    )


class DocumentationSection(Base):
    """Specific documentation section record."""

    __tablename__ = "documentation_sections"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    documentation_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documentation_analyses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    section_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_present: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    content_snippet: Mapped[str | None] = mapped_column(Text, nullable=True)

    documentation_analysis: Mapped[DocumentationAnalysis] = relationship(
        "DocumentationAnalysis", back_populates="sections"
    )


class ReadmeAnalysis(Base):
    """README section completeness report."""

    __tablename__ = "readme_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    documentation_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documentation_analyses.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    completeness_percentage: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )
    missing_sections: Mapped[list[str]] = mapped_column(
        JSON, default=list, nullable=False
    )
    detected_sections: Mapped[list[str]] = mapped_column(
        JSON, default=list, nullable=False
    )
    has_badges: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_screenshots: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    documentation_analysis: Mapped[DocumentationAnalysis] = relationship(
        "DocumentationAnalysis", back_populates="readme_analysis"
    )


class TestingAnalysis(Base):
    """Testing suite maturity report."""

    __tablename__ = "testing_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    testing_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    frameworks: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    test_file_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    estimated_test_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    has_unit_tests: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_integration_tests: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    has_e2e_tests: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_mocks: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class GitHistoryAnalysis(Base):
    """Git repository history and contributor analytics."""

    __tablename__ = "git_history_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    commit_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    contributor_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    branch_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    tag_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    repo_age_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    commits_per_week: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    inactive_periods_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )
    development_velocity_score: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )

    commit_analysis: Mapped["CommitAnalysis | None"] = relationship(
        "CommitAnalysis",
        back_populates="git_history_analysis",
        uselist=False,
        cascade="all, delete-orphan",
    )


class CommitAnalysis(Base):
    """Commit message quality and Conventional Commits report."""

    __tablename__ = "commit_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    git_history_analysis_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("git_history_analyses.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    commit_quality_score: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )
    conventional_commits_percentage: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )
    generic_commits_percentage: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )
    commit_types_breakdown: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )

    git_history_analysis: Mapped[GitHistoryAnalysis] = relationship(
        "GitHistoryAnalysis", back_populates="commit_analysis"
    )


class ReleaseAnalysis(Base):
    """Git releases and SemVer compliance report."""

    __tablename__ = "release_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    release_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    release_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    has_changelog: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    uses_semver: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    latest_release_tag: Mapped[str | None] = mapped_column(String(100), nullable=True)
    days_since_last_release: Mapped[int | None] = mapped_column(Integer, nullable=True)


class CommunityAnalysis(Base):
    """Open source community standards compliance report."""

    __tablename__ = "community_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    community_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    has_contributing: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    has_code_of_conduct: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    has_security_policy: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    has_issue_templates: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    has_pr_templates: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    has_discussions: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )


class CiAnalysis(Base):
    """CI/CD automation pipelines report."""

    __tablename__ = "ci_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    ci_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    providers: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    has_test_jobs: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_lint_jobs: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_security_scans: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    has_build_jobs: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_deploy_jobs: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )


class LicenseAnalysis(Base):
    """License identification report."""

    __tablename__ = "license_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    spdx_identifier: Mapped[str] = mapped_column(
        String(50), default="NOASSERTION", nullable=False
    )
    is_osi_approved: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    has_license_file: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_consistent: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class MaintainabilityMetrics(Base):
    """Aggregated raw subsystem scores for maintainability."""

    __tablename__ = "maintainability_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    documentation_score: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )
    testing_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    ci_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    release_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    repository_health_score: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )
    community_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)


class RepositoryHealth(Base):
    """Raw repository health breakdown metrics."""

    __tablename__ = "repository_healths"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    analysis_run_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("analysis_runs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    repository_health_score: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )
    maintenance_frequency_score: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )
    community_readiness_score: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )
    contribution_readiness_score: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False
    )
