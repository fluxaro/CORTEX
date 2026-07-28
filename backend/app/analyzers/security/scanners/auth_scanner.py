"""Authentication and Web Security scanner."""

import re
from typing import Any

from app.analyzers.security.base_scanner import BaseSecurityScanner
from app.analyzers.security.models import AuthFindingResult, SecurityAnalysisResult


class AuthScanner(BaseSecurityScanner):
    """Scans authentication mechanisms, password hashing algorithms, and web security controls."""

    AUTH_RULES = [
        (
            "Weak MD5 Password Hashing",
            r"(?i)md5\(.*password",
            "HIGH",
            "Passwords hashed using broken MD5 algorithm.",
        ),
        (
            "Weak SHA1 Password Hashing",
            r"(?i)sha1\(.*password",
            "HIGH",
            "Passwords hashed using vulnerable SHA1 algorithm.",
        ),
        (
            "Missing Password Hashing",
            r"(?i)save\(.*password\b(?!.*hash)",
            "CRITICAL",
            "Plaintext password saved without password hashing.",
        ),
        (
            "JWT Secret Hardcoded",
            r"(?i)jwt\.encode\(.*key\s*=\s*['\"][^'\"]+['\"]",
            "HIGH",
            "Hardcoded JWT secret key used for token encoding.",
        ),
        (
            "CORS Wildcard Origin",
            r"(?i)Access-Control-Allow-Origin\s*:\s*\*|allow_origins\s*=\s*\[[\"']\*[\"']\]",
            "MEDIUM",
            "CORS permits unrestricted wildcard '*' origins.",
        ),
        (
            "Cookie Missing HttpOnly Flag",
            r"(?i)set_cookie\(.*httponly\s*=\s*False",
            "MEDIUM",
            "Cookie set without HttpOnly flag, susceptible to XSS theft.",
        ),
        (
            "Cookie Missing Secure Flag",
            r"(?i)set_cookie\(.*secure\s*=\s*False",
            "MEDIUM",
            "Cookie set without Secure flag, transmitted over plaintext HTTP.",
        ),
    ]

    @property
    def scanner_name(self) -> str:
        return "AuthScanner"

    def scan(
        self,
        target_path: str,
        file_contents: dict[str, str],
        extra_context: dict[str, Any] | None = None,
    ) -> SecurityAnalysisResult:
        result = SecurityAnalysisResult()
        auth_findings: list[AuthFindingResult] = []

        for rel_path, content in file_contents.items():
            lines = content.splitlines()
            for line_no, line in enumerate(lines, start=1):
                for auth_type, pattern, severity, desc in self.AUTH_RULES:
                    if re.search(pattern, line):
                        auth_findings.append(
                            AuthFindingResult(
                                auth_type=auth_type,
                                severity=severity,
                                file_path=rel_path,
                                line_number=line_no,
                                description=f"Authentication issue '{auth_type}' in '{rel_path}' line {line_no}: {desc}",
                            )
                        )

        result.auth_findings = auth_findings
        result.auth_issues_count = len(auth_findings)
        result.critical_count += sum(
            1 for a in auth_findings if a.severity == "CRITICAL"
        )
        result.high_count += sum(1 for a in auth_findings if a.severity == "HIGH")

        return result
