"""Tests for Repository IQ Scorer and weighting."""

from app.analyzers.iq.models import SubsystemScores
from app.analyzers.iq.scorers.iq_scorer import IQScorer
from app.analyzers.iq.weights import SubsystemWeights


def test_iq_scorer_calculation() -> None:
    """Test calculating weighted Repository IQ score."""
    subsystems = SubsystemScores(
        static_analysis_score=80.0,
        architecture_score=90.0,
        security_score=70.0,
        documentation_score=85.0,
        testing_score=75.0,
        ci_score=100.0,
        git_practices_score=80.0,
        repository_health_score=85.0,
    )

    weights = SubsystemWeights(
        static_analysis=0.15,
        architecture=0.15,
        security=0.25,
        documentation=0.10,
        testing=0.15,
        ci=0.05,
        git_practices=0.05,
        repository_health=0.10,
    )

    score = IQScorer.calculate_score(subsystems, weights)
    assert 75.0 <= score <= 85.0
