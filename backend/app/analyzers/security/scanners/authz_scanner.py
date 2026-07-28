"""Authorization and RBAC scanner."""

import re
from typing import Any

from app.analyzers.security.base_scanner import BaseSecurityScanner
from app.analyzers.security.models import AuthzFindingResult, SecurityAnalysisResult


class AuthzScanner(BaseSecurityScanner):
    """Scans role-based access controls, permission middleware, and protected endpoints."""

    AUTHZ_RULES = [
        (
            "Unprotected Admin Endpoint",
            r"(?i)/admin/.*(?!.*(Depends|permission|auth))",
            "HIGH",
            "Admin endpoint route missing explicit authentication or permission guard.",
        ),
        (
            "Bypassed Authorization Check",
            r"(?i)if\s+user\.is_admin\s*==\s*False\s*:\s*pass",
            "HIGH",
            "Admin authorization check explicitly bypassed.",
        ),
        (
            "Hardcoded Superuser Check",
            r"(?i)user\.username\s*==\s*['\"]admin['\"]",
            "MEDIUM",
            "Authorization logic hardcodes username 'admin' instead of role system.",
        ),
    ]

    @property
    def scanner_name(self) -> str:
        return "AuthzScanner"

    def scan(
        self,
        target_path: str,
        file_contents: dict[str, str],
        extra_context: dict[str, Any] | None = None,
    ) -> SecurityAnalysisResult:
        result = SecurityAnalysisResult()
        authz_findings: list[AuthzFindingResult] = []

        for rel_path, content in file_contents.items():
            lines = content.splitlines()
            for line_no, line in enumerate(lines, start=1):
                for authz_type, pattern, severity, desc in self.AUTHZ_RULES:
                    if re.search(pattern, line):
                        authz_findings.append(
                            AuthzFindingResult(
                                authz_type=authz_type,
                                severity=severity,
                                file_path=rel_path,
                                line_number=line_no,
                                description=f"Authorization issue '{authz_type}' in '{rel_path}' line {line_no}: {desc}",
                            )
                        )

        result.authz_findings = authz_findings
        result.high_count += sum(1 for a in authz_findings if a.severity == "HIGH")

        return result
