"""Tests for Engineering Maturity Model classifier."""

from app.analyzers.iq.models import SubsystemScores
from app.analyzers.iq.scorers.maturity_classifier import MaturityClassifier


def test_maturity_classifier() -> None:
    """Test classifying repository into engineering maturity levels."""
    subsystems_high = SubsystemScores(
        static_analysis_score=90.0,
        architecture_score=85.0,
        security_score=85.0,
        documentation_score=80.0,
        testing_score=80.0,
        ci_score=100.0,
    )
    mat_high = MaturityClassifier.classify(subsystems_high, has_ci=True)
    assert mat_high.level == "Enterprise Ready"

    subsystems_low = SubsystemScores(
        static_analysis_score=20.0,
        architecture_score=20.0,
        security_score=30.0,
        documentation_score=10.0,
        testing_score=0.0,
        ci_score=0.0,
    )
    mat_low = MaturityClassifier.classify(subsystems_low, has_ci=False)
    assert mat_low.level in ("Prototype", "Learning Project")
