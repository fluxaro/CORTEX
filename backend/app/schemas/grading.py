"""Pydantic v2 validation schemas for CORTEX Repository Grade Reports."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class CategoryScoresSchema(BaseModel):
    """5 Consolidated Category Scores schema (0-100)."""

    security: float = 0.0
    architecture: float = 0.0
    code_quality: float = 0.0
    maintainability: float = 0.0
    community_velocity: float = 0.0


# Backward compatibility alias schema
class SubsystemScoresSchema(BaseModel):
    """Subsystem scores schema."""

    static_analysis: float = 0.0
    architecture: float = 0.0
    security: float = 0.0
    documentation: float = 0.0
    testing: float = 0.0
    ci: float = 0.0
    git_practices: float = 0.0
    repository_health: float = 0.0
    community: float = 0.0


class RepositorySummarySchema(BaseModel):
    """Repository summaries schema."""

    narrative_summary: str = ""
    executive_summary: str = ""
    technical_summary: str = ""
    architecture_summary: str = ""
    security_summary: str = ""
    maintainability_summary: str = ""
    recruiter_summary: str = ""
    engineering_manager_summary: str = ""


class EngineeringInsightSchema(BaseModel):
    """Engineering strengths and weaknesses schema."""

    strengths: list[str] = []
    weaknesses: list[str] = []


class TechnicalDebtItemSchema(BaseModel):
    """Technical debt finding item schema."""

    category: str
    description: str
    estimated_hours: float


class TechnicalDebtSchema(BaseModel):
    """Technical debt estimation schema."""

    total_hours: float
    total_days: float
    category_breakdown: dict[str, float]
    items: list[TechnicalDebtItemSchema] = []


class ImprovementRecommendationSchema(BaseModel):
    """Improvement recommendation schema."""

    id: uuid.UUID
    category: str
    title: str
    description: str
    timeframe: str
    priority: str
    difficulty: str
    estimated_hours: float


class BenchmarkResultSchema(BaseModel):
    """Industry benchmark percentile scores schema."""

    overall_percentile: float
    quality_percentile: float
    security_percentile: float
    architecture_percentile: float
    maintainability_percentile: float


class ExecutiveSummaryResponse(BaseModel):
    """Executive Summary response."""

    repository_iq_id: uuid.UUID
    summary_text: str
    report_json: dict[str, Any]


class TechnicalSummaryResponse(BaseModel):
    """Technical Summary response."""

    repository_iq_id: uuid.UUID
    summary_text: str
    report_json: dict[str, Any]


class PersonaSummaryResponse(BaseModel):
    """Persona summary response schema."""

    repository_id: uuid.UUID
    persona: str  # executive | technical | recruiter | engineering_manager | general
    summary_text: str
    overall_grade: str
    overall_score: float
    capped: bool = False
    cap_reason: str | None = None


class RepositoryGradeReportResponse(BaseModel):
    """Complete CORTEX Repository Grade Report schema."""

    id: uuid.UUID
    repository_id: uuid.UUID
    analysis_run_id: uuid.UUID
    overall_score: float
    overall_grade: str = "C"
    capped: bool = False
    cap_reason: str | None = None
    maturity_level: str
    category_scores: CategoryScoresSchema
    subsystem_scores: SubsystemScoresSchema | None = None
    summary: RepositorySummarySchema | None = None
    insights: EngineeringInsightSchema | None = None
    technical_debt: TechnicalDebtSchema | None = None
    benchmark: BenchmarkResultSchema | None = None
    created_at: datetime
    updated_at: datetime


# Backward compatibility schema alias
RepositoryIQResponse = RepositoryGradeReportResponse
