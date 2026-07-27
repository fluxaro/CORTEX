"""Tests for AnalyzerRegistry and base analyzer lookup."""

from app.analyzers.base.registry import AnalyzerRegistry
from app.analyzers.go.go_analyzer import GoAnalyzer
from app.analyzers.python.python_analyzer import PythonAnalyzer
from app.analyzers.typescript.typescript_analyzer import TypeScriptAnalyzer


def test_analyzer_registry_lookup() -> None:
    """Test registering and retrieving language analyzers."""
    py_analyzer = AnalyzerRegistry.get_analyzer_for_file("app/main.py")
    assert py_analyzer is not None
    assert isinstance(py_analyzer, PythonAnalyzer)
    assert py_analyzer.language_name == "Python"

    ts_analyzer = AnalyzerRegistry.get_analyzer_for_file("src/App.tsx")
    assert ts_analyzer is not None
    assert isinstance(ts_analyzer, TypeScriptAnalyzer)
    assert ts_analyzer.language_name == "TypeScript"

    go_analyzer = AnalyzerRegistry.get_analyzer_for_file("main.go")
    assert go_analyzer is not None
    assert isinstance(go_analyzer, GoAnalyzer)
    assert go_analyzer.language_name == "Go"


def test_analyzer_registry_unknown_extension() -> None:
    """Test unknown extension returns None."""
    analyzer = AnalyzerRegistry.get_analyzer_for_file("document.xyz")
    assert analyzer is None
