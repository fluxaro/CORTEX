"""Tests for Engineering Maturity Model classifier."""

from app.analyzers.grading.models import CategoryScores
from app.analyzers.grading.scorers.maturity_classifier import MaturityClassifier


def test_maturity_classifier() -> None:
    """Test classifying repository into engineering maturity levels."""
    categories_high = CategoryScores(
        security_score=85.0,
        architecture_score=85.0,
        code_quality_score=90.0,
        maintainability_score=80.0,
        community_velocity_score=80.0,
    )
    mat_high = MaturityClassifier.classify(categories_high, has_ci=True)
    assert mat_high.level == "Enterprise Ready"

    categories_low = CategoryScores(
        security_score=20.0,
        architecture_score=20.0,
        code_quality_score=20.0,
        maintainability_score=10.0,
        community_velocity_score=0.0,
    )
    mat_low = MaturityClassifier.classify(categories_low, has_ci=False)
    assert mat_low.level in ("Prototype", "Learning Project")
