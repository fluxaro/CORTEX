"""Database models for Repository IQ Engine, AI summaries, technical debt, and recommendations."""

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, utc_now


class RepositoryIQ(Base):
    """Primary Repository IQ overall score and maturity classification."""

    __tablename__ = "repository_iqs"

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
    maturity_level: Mapped[str] = mapped_column(
        String(100), default="Prototype", nullable=False
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
        back_populates="repository_iq",
        uselist=False,
        cascade="all, delete-orphan",
    )
    technical_debt: Mapped["TechnicalDebt | None"] = relationship(
        "TechnicalDebt",
        back_populates="repository_iq",
        uselist=False,
        cascade="all, delete-orphan",
    )
    benchmark: Mapped["BenchmarkResult | None"] = relationship(
        "BenchmarkResult",
        back_populates="repository_iq",
        uselist=False,
        cascade="all, delete-orphan",
    )
    recommendations: Mapped[list["ImprovementRecommendation"]] = relationship(
        "ImprovementRecommendation",
        back_populates="repository_iq",
        cascade="all, delete-orphan",
    )
    insights: Mapped["EngineeringInsight | None"] = relationship(
        "EngineeringInsight",
        back_populates="repository_iq",
        uselist=False,
        cascade="all, delete-orphan",
    )


class RepositorySummary(Base):
    """AI generated summaries for executive, technical, recruiter, and manager audiences."""

    __tablename__ = "repository_summaries"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_iqs.id", ondelete="CASCADE"),
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

    repository_iq: Mapped[RepositoryIQ] = relationship(
        "RepositoryIQ", back_populates="summary"
    )


class EngineeringInsight(Base):
    """Strengths and weaknesses findings."""

    __tablename__ = "engineering_insights"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_iqs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    strengths: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    weaknesses: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    repository_iq: Mapped[RepositoryIQ] = relationship(
        "RepositoryIQ", back_populates="insights"
    )


class TechnicalDebt(Base):
    """Technical debt estimation and category breakdown."""

    __tablename__ = "technical_debts"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_iqs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    total_hours: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_days: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    category_breakdown: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )
    items: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON, default=list, nullable=False
    )

    repository_iq: Mapped[RepositoryIQ] = relationship(
        "RepositoryIQ", back_populates="technical_debt"
    )


class ImprovementRecommendation(Base):
    """Actionable improvement roadmap item."""

    __tablename__ = "improvement_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_iqs.id", ondelete="CASCADE"), nullable=False, index=True
    )

    category: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    timeframe: Mapped[str] = mapped_column(String(50), nullable=False)
    priority: Mapped[str] = mapped_column(String(50), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=False)
    estimated_hours: Mapped[float] = mapped_column(Float, default=4.0, nullable=False)

    repository_iq: Mapped[RepositoryIQ] = relationship(
        "RepositoryIQ", back_populates="recommendations"
    )


class ExecutiveSummary(Base):
    """Executive structured report."""

    __tablename__ = "executive_summaries"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_iqs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    report_json: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )


class TechnicalSummary(Base):
    """Technical structured report."""

    __tablename__ = "technical_summaries"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_iqs.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    summary_text: Mapped[str] = mapped_column(Text, nullable=False)
    report_json: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )


class BenchmarkResult(Base):
    """Industry benchmark percentile scores."""

    __tablename__ = "benchmark_results"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_iqs.id", ondelete="CASCADE"),
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

    repository_iq: Mapped[RepositoryIQ] = relationship(
        "RepositoryIQ", back_populates="benchmark"
    )


class AiGeneration(Base):
    """Audit log of AI prompt generation executions."""

    __tablename__ = "ai_generations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    repository_iq_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repository_iqs.id", ondelete="CASCADE"), nullable=False, index=True
    )

    provider_name: Mapped[str] = mapped_column(String(50), nullable=False)
    prompt_name: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt_text: Mapped[str] = mapped_column(Text, nullable=False)
    response_text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class PromptTemplate(Base):
    """Versioned prompt templates."""

    __tablename__ = "prompt_templates"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, index=True
    )
    template_name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    version: Mapped[str] = mapped_column(String(20), default="1.0.0", nullable=False)
    template_text: Mapped[str] = mapped_column(Text, nullable=False)
