"""Tests for PatternDetector design pattern identification."""

from app.analyzers.architecture.detectors.pattern_detector import PatternDetector
from app.analyzers.shared.models import ClassAnalysisResult, FileAnalysisResult


def test_repository_pattern_detection() -> None:
    """Test detecting Repository Pattern and DTO pattern."""
    file_res = FileAnalysisResult(
        path="app/repositories/user_repository.py",
        language="Python",
        classes=[ClassAnalysisResult(name="UserRepository")],
    )

    patterns = PatternDetector.detect_patterns([file_res])

    assert len(patterns) >= 1
    repo_pat = next(p for p in patterns if p.pattern_name == "Repository Pattern")
    assert repo_pat.category == "Architectural"
    assert repo_pat.confidence_score >= 0.8
