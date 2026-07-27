"""Tests for complexity calculations, maintainability index, and grading."""

from app.analyzers.shared.metrics import (
    calculate_complexity_grade,
    calculate_maintainability_index,
)


def test_maintainability_index_calculation() -> None:
    """Test maintainability index returns value in valid 0.0 to 100.0 range."""
    mi_simple = calculate_maintainability_index(loc=20, complexity=2, comment_lines=5)
    assert 0.0 <= mi_simple <= 100.0
    assert mi_simple > 50.0

    mi_complex = calculate_maintainability_index(
        loc=500, complexity=45, comment_lines=0
    )
    assert 0.0 <= mi_complex <= 100.0
    assert mi_complex < mi_simple


def test_complexity_grading() -> None:
    """Test letter grade assignment for cyclomatic complexity."""
    assert calculate_complexity_grade(3.0) == "A"
    assert calculate_complexity_grade(8.5) == "B"
    assert calculate_complexity_grade(15.0) == "C"
    assert calculate_complexity_grade(25.0) == "D"
    assert calculate_complexity_grade(35.0) == "E"
    assert calculate_complexity_grade(50.0) == "F"
