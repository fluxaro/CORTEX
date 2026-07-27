"""Tests for PythonAST static analyzer."""

from app.analyzers.python.python_analyzer import PythonAnalyzer


def test_python_analyzer_parse_functions_and_classes() -> None:
    """Test analyzing Python source code with functions and classes."""
    code = """
import os
import sys

class Calculator:
    def add(self, a: int, b: int) -> int:
        if a > 0 and b > 0:
            return a + b
        return 0

    def _internal(self):
        pass

def top_level_function(x):
    for i in range(x):
        while True:
            break
    return x
"""
    analyzer = PythonAnalyzer()
    res = analyzer.analyze_file("sample.py", code, file_size=len(code))

    assert res.language == "Python"
    assert res.loc > 0
    assert res.class_count == 1
    assert res.function_count == 3  # top_level_function, add, _internal
    assert len(res.imports) == 2
    assert "os" in res.imports

    # Class verification
    cls = res.classes[0]
    assert cls.name == "Calculator"
    assert cls.methods_count == 2
    assert cls.public_methods == 1
    assert cls.private_methods == 1
