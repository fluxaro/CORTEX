"""Industry benchmarking percentile scorer."""

from app.analyzers.iq.models import BenchmarkResultDTO, SubsystemScores


class Benchmarker:
    """Compares repository scores against industry baselines and generates percentile scores."""

    @classmethod
    def calculate_percentiles(
        cls, overall_score: float, subsystems: SubsystemScores
    ) -> BenchmarkResultDTO:
        """Calculate percentile rankings."""
        overall_pct = min(max(overall_score * 0.95 + 5.0, 5.0), 99.0)
        quality_pct = min(max(subsystems.static_analysis_score * 0.9 + 10.0, 5.0), 99.0)
        sec_pct = min(max(subsystems.security_score * 0.95 + 5.0, 5.0), 99.0)
        arch_pct = min(max(subsystems.architecture_score * 0.9 + 10.0, 5.0), 99.0)
        maint_pct = min(max(subsystems.repository_health_score * 0.9 + 10.0, 5.0), 99.0)

        return BenchmarkResultDTO(
            overall_percentile=round(overall_pct, 1),
            quality_percentile=round(quality_pct, 1),
            security_percentile=round(sec_pct, 1),
            architecture_percentile=round(arch_pct, 1),
            maintainability_percentile=round(maint_pct, 1),
        )
