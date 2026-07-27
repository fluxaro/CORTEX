"""Tests for DependencyGraphBuilder and architectural rule validation."""

from app.analyzers.architecture.detectors.dependency_graph import DependencyGraphBuilder
from app.analyzers.shared.models import FileAnalysisResult


def test_dependency_graph_and_cross_layer_violation() -> None:
    """Test graph generation and cross-layer violation detection."""
    f1 = FileAnalysisResult(
        path="app/controllers/user_controller.py",
        language="Python",
        imports=["app.infrastructure.database"],
    )
    f2 = FileAnalysisResult(
        path="app/infrastructure/database.py",
        language="Python",
        imports=[],
    )

    graph_data, violations, scores = DependencyGraphBuilder.build_graph([f1, f2])

    assert len(graph_data.nodes) >= 2
    assert len(graph_data.edges) >= 1
    assert len(violations) >= 1

    v = violations[0]
    assert v.violation_type == "Cross-Layer Violation"
    assert "layer_separation_score" in scores
