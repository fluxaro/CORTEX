"""Tests for SecretDetector API key and credential scanner."""

from app.analyzers.security.scanners.secret_detector import SecretDetector


def test_secret_detector_findings() -> None:
    """Test detecting hardcoded AWS keys, GitHub tokens, and private keys."""
    file_map = {
        "config.py": "AWS_KEY = 'AKIAIOSFODNN7EXAMPLE'\nGITHUB_TOKEN = 'ghp_1234567890abcdefghijklmnopqrstuvwxyz'\n",
        "keys.pem": "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA...\n-----END RSA PRIVATE KEY-----\n",
    }

    detector = SecretDetector()
    res = detector.scan("/tmp", file_map)

    assert res.secret_count >= 3
    assert res.critical_count >= 2

    types = {s.secret_type for s in res.secrets}
    assert "AWS Access Key" in types
    assert "GitHub Personal Access Token" in types
    assert "RSA Private Key" in types
