"""Unit tests for GradeCalculator 5-category evaluation, guardrail caps, and determinism."""

import pytest

from app.analyzers.grading.models import CategoryScores
from app.analyzers.grading.scorers.grade_calculator import GradeCalculator


def test_score_to_letter_grade_mapping():
    """Verify exact score to letter grade mapping thresholds."""
    assert GradeCalculator.score_to_grade(95.0) == "A+"
    assert GradeCalculator.score_to_grade(90.0) == "A"
    assert GradeCalculator.score_to_grade(83.0) == "A-"
    assert GradeCalculator.score_to_grade(75.0) == "B+"
    assert GradeCalculator.score_to_grade(68.0) == "B"
    assert GradeCalculator.score_to_grade(62.0) == "B-"
    assert GradeCalculator.score_to_grade(55.0) == "C+"
    assert GradeCalculator.score_to_grade(48.0) == "C"
    assert GradeCalculator.score_to_grade(42.0) == "C-"
    assert GradeCalculator.score_to_grade(35.0) == "D"
    assert GradeCalculator.score_to_grade(15.0) == "F"


def test_guardrail_cap_security_f():
    """Verify overall grade capped at C max when Security is F (< 30)."""
    cats = CategoryScores(
        security_score=20.0,  # F
        architecture_score=100.0,
        code_quality_score=100.0,
        maintainability_score=100.0,
        community_velocity_score=100.0,
    )
    score, grade, capped, reason = GradeCalculator.calculate_grade(cats)

    # Uncapped score would be (20*0.3)+(100*0.7) = 76.0 (B+), but capped at C (52.0 max)
    assert capped is True
    assert grade in ["C+", "C", "C-"]
    assert score <= 59.0
    assert "critical security findings" in (reason or "")


def test_guardrail_cap_security_d():
    """Verify overall grade capped at B max when Security is D (30-39)."""
    cats = CategoryScores(
        security_score=35.0,  # D
        architecture_score=100.0,
        code_quality_score=100.0,
        maintainability_score=100.0,
        community_velocity_score=100.0,
    )
    score, grade, capped, reason = GradeCalculator.calculate_grade(cats)

    # Uncapped score would be (35*0.3)+(100*0.7) = 80.5 (A-), but capped at B (72.0 max)
    assert capped is True
    assert grade in ["B+", "B", "B-"]
    assert score <= 72.0
    assert "moderate security risks" in (reason or "")


def test_no_guardrail_cap_when_security_passes():
    """Verify no cap applied when Security is C- or higher."""
    cats = CategoryScores(
        security_score=85.0,  # A-
        architecture_score=90.0,
        code_quality_score=88.0,
        maintainability_score=85.0,
        community_velocity_score=80.0,
    )
    score, grade, capped, reason = GradeCalculator.calculate_grade(cats)

    assert capped is False
    assert reason is None
    assert grade == "A-"


def test_grade_stability_determinism():
    """100-run grade stability determinism test: same inputs must produce identical grades."""
    cats = CategoryScores(
        security_score=78.5,
        architecture_score=84.2,
        code_quality_score=91.0,
        maintainability_score=88.7,
        community_velocity_score=75.0,
    )

    first_score, first_grade, first_capped, first_reason = GradeCalculator.calculate_grade(cats)

    for _ in range(100):
        s, g, c, r = GradeCalculator.calculate_grade(cats)
        assert s == first_score
        assert g == first_grade
        assert c == first_capped
        assert r == first_reason
