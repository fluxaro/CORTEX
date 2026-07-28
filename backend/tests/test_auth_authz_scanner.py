"""Tests for AuthScanner and AuthzScanner."""

from app.analyzers.security.scanners.auth_scanner import AuthScanner
from app.analyzers.security.scanners.authz_scanner import AuthzScanner


def test_auth_authz_scanners() -> None:
    """Test detecting weak authentication hashing and unprotected admin endpoints."""
    file_map = {
        "auth.py": "import hashlib\nhashlib.md5(password.encode())\n",
        "routes.py": "@app.get('/admin/dashboard')\ndef admin_dashboard(): pass\n",
    }

    auth_res = AuthScanner().scan("/tmp", file_map)
    assert auth_res.auth_issues_count >= 1
    assert auth_res.auth_findings[0].auth_type == "Weak MD5 Password Hashing"

    authz_res = AuthzScanner().scan("/tmp", file_map)
    assert len(authz_res.authz_findings) >= 1
    assert authz_res.authz_findings[0].authz_type == "Unprotected Admin Endpoint"
