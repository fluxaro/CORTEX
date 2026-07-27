"""Tests for ArchDetector architecture style classification."""

from app.analyzers.architecture.detectors.arch_detector import ArchDetector
from app.analyzers.architecture.detectors.layer_detector import LayerDetector


def test_clean_architecture_detection() -> None:
    """Test detecting Clean Architecture style."""
    paths = [
        "domain/entities/user.py",
        "use_cases/create_user.py",
        "infrastructure/repositories/user_repo.py",
        "controllers/user_controller.py",
    ]
    layers = LayerDetector.detect_layers(paths)
    style, confidence = ArchDetector.detect_architecture_style(layers, paths)

    assert style in (
        "Clean Architecture",
        "Hexagonal Architecture",
        "Onion Architecture",
    )
    assert confidence >= 0.85


def test_mvc_architecture_detection() -> None:
    """Test detecting MVC Architecture style."""
    paths = [
        "app/models/user.py",
        "app/views/user_view.py",
        "app/controllers/user_controller.py",
    ]
    layers = LayerDetector.detect_layers(paths)
    style, confidence = ArchDetector.detect_architecture_style(layers, paths)

    assert style == "MVC Architecture"
    assert confidence >= 0.85
