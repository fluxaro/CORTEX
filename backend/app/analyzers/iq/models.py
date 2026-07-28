"""Data transfer objects for Repository IQ Engine."""

from dataclasses import dataclass, field


@dataclass
class SubsystemScores:
    """Raw subsystem scores (0-100)."""

    static_analysis_score: float = 0.0
    architecture_score: float = 0.0
    security_score: float = 0.0
    documentation_score: float = 0.0
    testing_score: float = 0.0
    ci_score: float = 0.0
    git_practices_score: float = 0.0
    repository_health_score: float = 0.0
    community_score: float = 0.0


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
class RepositoryIQResult:
    """Complete aggregated Repository IQ analysis report."""

    overall_score: float = 0.0
    subsystem_scores: SubsystemScores = field(default_factory=SubsystemScores)
    maturity: MaturityClassification = field(
        default_factory=lambda: MaturityClassification(level="Prototype")
    )
    debt: TechnicalDebtResult = field(default_factory=TechnicalDebtResult)
    insights: StrengthsWeaknessesResult = field(
        default_factory=StrengthsWeaknessesResult
    )
    benchmark: BenchmarkResultDTO = field(default_factory=BenchmarkResultDTO)

    executive_summary: str = ""
    technical_summary: str = ""
    architecture_summary: str = ""
    security_summary: str = ""
    maintainability_summary: str = ""
    recruiter_summary: str = ""
    engineering_manager_summary: str = ""
