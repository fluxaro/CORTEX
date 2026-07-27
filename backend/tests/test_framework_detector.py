"""Tests for FrameworkDetector and convention checks."""

from app.analyzers.architecture.detectors.framework_detector import FrameworkDetector
from app.analyzers.shared.models import FileAnalysisResult


def test_fastapi_framework_detection() -> None:
    """Test detecting FastAPI framework and checking conventions."""
    file_res = FileAnalysisResult(
        path="app/api/endpoints/users.py",
        language="Python",
        imports=["fastapi", "APIRouter", "pydantic"],
    )

    frameworks = FrameworkDetector.detect_frameworks([file_res])

    assert len(frameworks) >= 1
    fastapi_fw = next(f for f in frameworks if f.name == "FastAPI")
    assert fastapi_fw.category == "Web Framework"
    assert fastapi_fw.is_convention_compliant is True
