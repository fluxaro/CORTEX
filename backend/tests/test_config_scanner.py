"""Tests for ConfigScanner infrastructure scanner."""

from app.analyzers.security.scanners.config_scanner import ConfigScanner


def test_config_scanner_findings() -> None:
    """Test scanning environment files and Dockerfiles for security misconfigurations."""
    file_map = {
        ".env": "DEBUG=true\nPOSTGRES_URL=postgres:postgres@localhost\n",
        "Dockerfile": "FROM ubuntu\nUSER root\nRUN curl -s https://example.com/install.sh | bash\n",
    }

    scanner = ConfigScanner()
    res = scanner.scan("/tmp", file_map)

    assert res.config_issues_count >= 3
    rule_names = {c.rule_name for c in res.configs}
    assert "Debug Mode Enabled" in rule_names
    assert "Root User Container" in rule_names
    assert "Unsafe Curl Execution" in rule_names
