"""Tests for CORTEX Category Grade Calculator and weighting."""

from app.analyzers.grading.models import CategoryScores
from app.analyzers.grading.scorers.grade_calculator import GradeCalculator
from app.analyzers.grading.weights import CategoryWeights


def test_category_grade_calculation() -> None:
    """Test calculating weighted Category Grade report."""
    categories = CategoryScores(
        security_score=85.0,
        architecture_score=90.0,
        code_quality_score=80.0,
        maintainability_score=85.0,
        community_velocity_score=80.0,
    )

    weights = CategoryWeights(
        security=0.30,
        architecture=0.20,
        code_quality=0.20,
        maintainability=0.20,
        community_velocity=0.10,
    )

    score, grade, capped, reason = GradeCalculator.calculate_grade(categories, weights)
    assert 80.0 <= score <= 90.0
    assert grade in ["A-", "A", "B+"]
    assert capped is False
