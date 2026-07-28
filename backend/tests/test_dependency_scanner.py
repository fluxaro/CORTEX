"""Tests for DependencyScanner vulnerability inspector."""

from app.analyzers.security.scanners.dependency_scanner import DependencyScanner


def test_dependency_scanner_findings() -> None:
    """Test detecting vulnerable dependencies in requirements.txt and package.json."""
    file_map = {
        "requirements.txt": "requests==2.20.0\nPyYAML==5.1\n",
        "package.json": '{"dependencies": {"express": "4.15.0"}}\n',
    }

    scanner = DependencyScanner()
    res = scanner.scan("/tmp", file_map)

    assert res.dependency_vuln_count >= 3
    pkgs = {d.package_name for d in res.dependencies}
    assert "requests" in pkgs
    assert "PyYAML" in pkgs
    assert "express" in pkgs
