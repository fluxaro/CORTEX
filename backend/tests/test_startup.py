"""Tests for application factory and startup lifecycle."""

from app.main import create_app


def test_create_app() -> None:
    """Test that create_app instantiates a valid FastAPI instance."""
    app_instance = create_app()
    assert app_instance.title == "ProjectIQ"
    assert app_instance.version == "0.1.0"
