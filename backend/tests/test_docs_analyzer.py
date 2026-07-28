"""Tests for DocsAnalyzer documentation coverage."""

from app.analyzers.maintainability.analyzers.docs_analyzer import DocsAnalyzer


def test_docs_analyzer() -> None:
    """Test detecting documentation files and generator configs."""
    file_paths = ["README.md", "docs/architecture.md", "mkdocs.yml", "docs/api.md"]
    file_contents = {"README.md": "# Title\n## API Documentation\n"}

    res = DocsAnalyzer.analyze(file_paths, file_contents)

    assert res.has_architecture_docs is True
    assert res.has_api_docs is True
    assert "MkDocs" in res.doc_frameworks
    assert res.documentation_score > 30.0
