"""Data transfer objects for CORTEX Repository Grading Engine."""

from dataclasses import dataclass, field


@dataclass
class CategoryScores:
    """5 Consolidated Category Scores (0-100)."""

    security_score: float = 0.0
    architecture_score: float = 0.0
    code_quality_score: float = 0.0
    maintainability_score: float = 0.0
    community_velocity_score: float = 0.0


# Backward compatibility alias
SubsystemScores = CategoryScores


@dataclass
class MaturityClassification:
    """Engineering maturity classification."""

    level: str  # Prototype | Personal Project | Learning Project | Production Ready | Enterprise Ready | Open Source Mature
    reasons: list[str] = field(default_factory=list)


@dataclass
class TechnicalDebtItem:
    """Itemized technical debt finding."""

    category: str  # Architecture | Security | Testing | Documentation | Maintainability | Dependency | Configuration
    description: str
    estimated_hours: float
    source_finding_id: str | None = None


@dataclass
class TechnicalDebtResult:
    """Technical debt estimation result."""

    total_hours: float = 0.0
    total_days: float = 0.0
    category_breakdown: dict[str, float] = field(default_factory=dict)
    items: list[TechnicalDebtItem] = field(default_factory=list)


@dataclass
class RecommendationItem:
    """Improvement recommendation item."""

    category: str
    title: str
    description: str
    timeframe: str  # Immediate | Short-term | Medium-term | Long-term
    priority: str  # Critical | High | Medium | Low
    difficulty: str  # Easy | Medium | Hard
    estimated_hours: float = 4.0


@dataclass
class StrengthsWeaknessesResult:
    """Repository strengths, weaknesses, and recommendations."""

    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    recommendations: list[RecommendationItem] = field(default_factory=list)


@dataclass
class BenchmarkResultDTO:
    """Industry benchmarking percentile scores."""

    overall_percentile: float = 50.0
    quality_percentile: float = 50.0
    security_percentile: float = 50.0
    architecture_percentile: float = 50.0
    maintainability_percentile: float = 50.0


@dataclass
class RepositoryGradeReportDTO:
    """Complete aggregated CORTEX Grade Report."""

    overall_score: float = 0.0
    overall_grade: str = "C"
    capped: bool = False
    cap_reason: str | None = None

    category_scores: CategoryScores = field(default_factory=CategoryScores)
    maturity: MaturityClassification = field(
        default_factory=lambda: MaturityClassification(level="Prototype")
    )
    debt: TechnicalDebtResult = field(default_factory=TechnicalDebtResult)
    insights: StrengthsWeaknessesResult = field(
        default_factory=StrengthsWeaknessesResult
    )
    benchmark: BenchmarkResultDTO = field(default_factory=BenchmarkResultDTO)

    narrative_summary: str = ""
    executive_summary: str = ""
    technical_summary: str = ""
    architecture_summary: str = ""
    security_summary: str = ""
    maintainability_summary: str = ""
    recruiter_summary: str = ""
    engineering_manager_summary: str = ""


# Backward compatibility alias
RepositoryIQResult = RepositoryGradeReportDTO
