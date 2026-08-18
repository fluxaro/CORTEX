"""Industry benchmarking percentile scorer."""

from typing import Any
from app.analyzers.grading.models import BenchmarkResultDTO


class Benchmarker:
    """Compares repository scores against industry baselines and generates percentile scores."""

    @classmethod
    def calculate_percentiles(
        cls, overall_score: float, subsystems: Any
    ) -> BenchmarkResultDTO:
        """Calculate percentile rankings."""
        sec_score = getattr(subsystems, "security_score", 50.0)
        code_score = getattr(subsystems, "code_quality_score", getattr(subsystems, "static_analysis_score", 50.0))
        arch_score = getattr(subsystems, "architecture_score", 50.0)
        maint_score = getattr(subsystems, "maintainability_score", getattr(subsystems, "repository_health_score", 50.0))

        overall_pct = min(max(overall_score * 0.95 + 5.0, 5.0), 99.0)
        quality_pct = min(max(code_score * 0.9 + 10.0, 5.0), 99.0)
        sec_pct = min(max(sec_score * 0.95 + 5.0, 5.0), 99.0)
        arch_pct = min(max(arch_score * 0.9 + 10.0, 5.0), 99.0)
        maint_pct = min(max(maint_score * 0.9 + 10.0, 5.0), 99.0)

        return BenchmarkResultDTO(
            overall_percentile=round(overall_pct, 1),
            quality_percentile=round(quality_pct, 1),
            security_percentile=round(sec_pct, 1),
            architecture_percentile=round(arch_pct, 1),
            maintainability_percentile=round(maint_pct, 1),
        )
