"""Tests for TestingAnalyzer framework and test suite detector."""

from app.analyzers.maintainability.analyzers.testing_analyzer import TestingAnalyzer


def test_testing_analyzer() -> None:
    """Test detecting Pytest runner and test file counts."""
    file_paths = ["tests/test_main.py", "tests/test_api.py"]
    file_contents = {
        "tests/test_main.py": "import pytest\ndef test_feature():\n    assert True\n",
        "tests/test_api.py": "def test_endpoint():\n    pass\n",
    }

    res = TestingAnalyzer.analyze(file_paths, file_contents)

    assert "Pytest" in res.frameworks
    assert res.test_file_count == 2
    assert res.estimated_test_count >= 2
    assert res.has_unit_tests is True
    assert res.testing_score > 30.0
