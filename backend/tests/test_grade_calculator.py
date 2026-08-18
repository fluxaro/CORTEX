"""Unit tests for CORTEX GradeCalculator, Guardrail Caps, and Grade Stability."""

from app.analyzers.grading.models import CategoryScores
from app.analyzers.grading.scorers.grade_calculator import GradeCalculator
from app.analyzers.grading.weights import CategoryWeights


def test_score_to_grade_boundaries():
    """Verify exact 0-100 numeric to letter grade mappings."""
    assert GradeCalculator.score_to_grade(95.0) == "A+"
    assert GradeCalculator.score_to_grade(93.0) == "A+"
    assert GradeCalculator.score_to_grade(92.0) == "A"
    assert GradeCalculator.score_to_grade(87.0) == "A"
    assert GradeCalculator.score_to_grade(86.0) == "A-"
    assert GradeCalculator.score_to_grade(80.0) == "A-"
    assert GradeCalculator.score_to_grade(79.0) == "B+"
    assert GradeCalculator.score_to_grade(73.0) == "B+"
    assert GradeCalculator.score_to_grade(72.0) == "B"
    assert GradeCalculator.score_to_grade(67.0) == "B"
    assert GradeCalculator.score_to_grade(66.0) == "B-"
    assert GradeCalculator.score_to_grade(60.0) == "B-"
    assert GradeCalculator.score_to_grade(59.0) == "C+"
    assert GradeCalculator.score_to_grade(53.0) == "C+"
    assert GradeCalculator.score_to_grade(52.0) == "C"
    assert GradeCalculator.score_to_grade(47.0) == "C"
    assert GradeCalculator.score_to_grade(46.0) == "C-"
    assert GradeCalculator.score_to_grade(40.0) == "C-"
    assert GradeCalculator.score_to_grade(39.0) == "D"
    assert GradeCalculator.score_to_grade(30.0) == "D"
    assert GradeCalculator.score_to_grade(29.0) == "F"
    assert GradeCalculator.score_to_grade(0.0) == "F"


def test_guardrail_cap_security_f():
    """Verify Security F (0-29) caps overall grade at C max."""
    # Even if all other categories are 100%, Security F must cap grade at C
    cats = CategoryScores(
        security_score=20.0,  # F
        architecture_score=100.0,
        code_quality_score=100.0,
        maintainability_score=100.0,
        community_velocity_score=100.0,
    )
    score, grade, capped, reason = GradeCalculator.calculate_grade(cats)

    assert capped is True
    assert "capped at C" in reason
    assert grade in ["C", "C-", "D", "F"]
    assert score <= 52.0


def test_guardrail_cap_security_d():
    """Verify Security D (30-39) caps overall grade at B max."""
    # High scores elsewhere capped at B max
    cats = CategoryScores(
        security_score=35.0,  # D
        architecture_score=95.0,
        code_quality_score=95.0,
        maintainability_score=95.0,
        community_velocity_score=95.0,
    )
    score, grade, capped, reason = GradeCalculator.calculate_grade(cats)

    assert capped is True
    assert "capped at B" in reason
    assert grade in ["B", "B-", "C+", "C", "C-", "D", "F"]
    assert score <= 72.0


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
    assert grade == "A"
    assert score == 86.1


def test_grade_stability_and_determinism():
    """Verify analyzing identical metrics repeatedly produces 100% deterministic grades."""
    cats = CategoryScores(
        security_score=92.0,
        architecture_score=88.0,
        code_quality_score=85.0,
        maintainability_score=80.0,
        community_velocity_score=75.0,
    )
    w = CategoryWeights()

    first_score, first_grade, first_capped, first_reason = GradeCalculator.calculate_grade(cats, w)

    for _ in range(100):
        s, g, c, r = GradeCalculator.calculate_grade(cats, w)
        assert s == first_score
        assert g == first_grade
        assert c == first_capped
        assert r == first_reason
