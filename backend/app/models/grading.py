"""Database models for CORTEX Repository Grade Reports, AI summaries, technical debt, and recommendations."""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, utc_now


class RepositoryGradeReport(Base):
    """Primary Repository Grade overall report, letter grade, and maturity classification."""

    __tablename__ = "repository_grade_reports"

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

    overall_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    overall_grade: Mapped[str] = mapped_column(
        String(10), default="C", nullable=False
    )
    capped: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    cap_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    maturity_level: Mapped[str] = mapped_column(
        String(100), default="Prototype", nullable=False
    )
    category_scores: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )
    subsystem_scores: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False
    )

    summary: Mapped["RepositorySummary | None"] = relationship(
        "RepositorySummary",
        back_populates="grade_report",
        uselist=False,
        cascade="all, delete-orphan",
    )
    technical_debt: Mapped["TechnicalDebt | None"] = relationship(
        "TechnicalDebt",
        back_populates="grade_report",
        uselist=False,
        cascade="all, delete-orphan",
    )
    benchmark: Mapped["BenchmarkResult | None"] = relationship(
        "BenchmarkResult",
        back_populates="grade_report",
        uselist=False,
        cascade="all, delete-orphan",
    )
    recommendations: Mapped[list["ImprovementRecommendation"]] = relationship(
        "ImprovementRecommendation",
        back_populates="grade_report",
        cascade="all, delete-orphan",
    )
    insights: Mapped["EngineeringInsight | None"] = relationship(
        "EngineeringInsight",
        back_populates="grade_report",
        uselist=False,
        cascade="all, delete-orphan",
    )


# Backward compatibility model alias
RepositoryIQ = RepositoryGradeReport


class RepositorySummary(Base):
    """AI generated summaries for executive, technical, recruiter, and manager audiences."""

    __tablename__ = "repository_summaries"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_grade_reports.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    executive_summary: Mapped[str] = mapped_column(Text, nullable=False)
    technical_summary: Mapped[str] = mapped_column(Text, nullable=False)
    architecture_summary: Mapped[str] = mapped_column(Text, nullable=False)
    security_summary: Mapped[str] = mapped_column(Text, nullable=False)
    maintainability_summary: Mapped[str] = mapped_column(Text, nullable=False)
    recruiter_summary: Mapped[str] = mapped_column(Text, nullable=False)
    engineering_manager_summary: Mapped[str] = mapped_column(Text, nullable=False)

    grade_report: Mapped[RepositoryGradeReport] = relationship(
        "RepositoryGradeReport", back_populates="summary"
    )
    repository_iq = grade_report


class ExecutiveSummary(Base):
    """Executive Summary ORM Model."""

    __tablename__ = "executive_summaries"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_grade_reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    report_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class TechnicalSummary(Base):
    """Technical Summary ORM Model."""

    __tablename__ = "technical_summaries"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_grade_reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    report_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)


class TechnicalDebt(Base):
    """Technical debt estimation summary and category metrics."""

    __tablename__ = "technical_debt_estimates"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_grade_reports.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    total_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_days: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    category_breakdown: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )

    grade_report: Mapped[RepositoryGradeReport] = relationship(
        "RepositoryGradeReport", back_populates="technical_debt"
    )
    repository_iq = grade_report
    items: Mapped[list["TechnicalDebtItem"]] = relationship(
        "TechnicalDebtItem",
        back_populates="technical_debt",
        cascade="all, delete-orphan",
    )


class TechnicalDebtItem(Base):
    """Itemized technical debt item."""

    __tablename__ = "technical_debt_items"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    technical_debt_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("technical_debt_estimates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    estimated_hours: Mapped[float] = mapped_column(Float, nullable=False)
    source_finding_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    technical_debt: Mapped[TechnicalDebt] = relationship(
        "TechnicalDebt", back_populates="items"
    )


class BenchmarkResult(Base):
    """Industry percentile benchmarking results."""

    __tablename__ = "benchmark_percentiles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_grade_reports.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    overall_percentile: Mapped[float] = mapped_column(
        Float, default=50.0, nullable=False
    )
    quality_percentile: Mapped[float] = mapped_column(
        Float, default=50.0, nullable=False
    )
    security_percentile: Mapped[float] = mapped_column(
        Float, default=50.0, nullable=False
    )
    architecture_percentile: Mapped[float] = mapped_column(
        Float, default=50.0, nullable=False
    )
    maintainability_percentile: Mapped[float] = mapped_column(
        Float, default=50.0, nullable=False
    )

    grade_report: Mapped[RepositoryGradeReport] = relationship(
        "RepositoryGradeReport", back_populates="benchmark"
    )
    repository_iq = grade_report


class ImprovementRecommendation(Base):
    """Actionable improvement recommendation item."""

    __tablename__ = "improvement_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_grade_reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    timeframe: Mapped[str] = mapped_column(String(50), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=False)
    estimated_hours: Mapped[float] = mapped_column(Float, default=4.0, nullable=False)

    grade_report: Mapped[RepositoryGradeReport] = relationship(
        "RepositoryGradeReport", back_populates="recommendations"
    )
    repository_iq = grade_report


class EngineeringInsight(Base):
    """Extracted top strengths, weaknesses, and key findings."""

    __tablename__ = "engineering_insights"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_grade_reports.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    strengths: Mapped[list[Any]] = mapped_column(JSON, default=list, nullable=False)
    weaknesses: Mapped[list[Any]] = mapped_column(JSON, default=list, nullable=False)

    grade_report: Mapped[RepositoryGradeReport] = relationship(
        "RepositoryGradeReport", back_populates="insights"
    )
    repository_iq = grade_report
