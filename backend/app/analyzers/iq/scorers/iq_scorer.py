"""Repository IQ score calculator."""

from app.analyzers.iq.models import SubsystemScores
from app.analyzers.iq.weights import SubsystemWeights


class IQScorer:
    """Calculates overall 0-100 Repository IQ score from weighted subsystem scores."""

    @classmethod
    def calculate_score(
        cls,
        subsystems: SubsystemScores,
        weights: SubsystemWeights | None = None,
    ) -> float:
        """Compute weighted Repository IQ score."""
        w = weights or SubsystemWeights()

        weighted_sum = (
            (subsystems.static_analysis_score * w.static_analysis)
            + (subsystems.architecture_score * w.architecture)
            + (subsystems.security_score * w.security)
            + (subsystems.documentation_score * w.documentation)
            + (subsystems.testing_score * w.testing)
            + (subsystems.ci_score * w.ci)
            + (subsystems.git_practices_score * w.git_practices)
            + (subsystems.repository_health_score * w.repository_health)
        )

        total_weight = (
            w.static_analysis
            + w.architecture
            + w.security
            + w.documentation
            + w.testing
            + w.ci
            + w.git_practices
            + w.repository_health
        )

        final_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        return round(max(min(final_score, 100.0), 0.0), 1)
