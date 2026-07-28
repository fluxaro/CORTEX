"""Dependency vulnerability scanner."""

import re
from typing import Any

from app.analyzers.security.base_scanner import BaseSecurityScanner
from app.analyzers.security.models import (
    DependencyFindingResult,
    SecurityAnalysisResult,
)


class DependencyScanner(BaseSecurityScanner):
    """Scans manifest files (requirements.txt, package.json, Cargo.toml, etc.) for vulnerable dependencies."""

    KNOWN_VULNERABILITIES = [
        (
            "requests",
            r"requests\s*==\s*2\.(?:[0-1]?\d|2[0-9])\.",
            "CVE-2023-32681",
            7.5,
            "HIGH",
            "Requests leakage of Authorization header on redirect.",
        ),
        (
            "urllib3",
            r"urllib3\s*==\s*1\.(?:2[0-5]|1\d)\.",
            "CVE-2023-43804",
            8.1,
            "HIGH",
            "Cookie leakage in redirected requests.",
        ),
        (
            "PyYAML",
            r"PyYAML\s*==\s*[1-5]\.",
            "CVE-2020-14343",
            9.8,
            "CRITICAL",
            "Arbitrary code execution through untrusted YAML load.",
        ),
        (
            "express",
            r"\"express\"\s*:\s*\"[~^]?4\.(?:1[0-7]|[0-9])\.",
            "CVE-2024-21508",
            7.5,
            "HIGH",
            "Express open redirect vulnerability.",
        ),
        (
            "lodash",
            r"\"lodash\"\s*:\s*\"[~^]?4\.17\.(?:1[0-9]|20)\"",
            "CVE-2021-23337",
            7.2,
            "HIGH",
            "Command injection via template function.",
        ),
        (
            "log4j",
            r"log4j-core",
            "CVE-2021-44228",
            10.0,
            "CRITICAL",
            "Remote Code Execution in Apache Log4j2.",
        ),
    ]

    @property
    def scanner_name(self) -> str:
        return "DependencyScanner"

    def scan(
        self,
        target_path: str,
        file_contents: dict[str, str],
        extra_context: dict[str, Any] | None = None,
    ) -> SecurityAnalysisResult:
        result = SecurityAnalysisResult()
        dependencies: list[DependencyFindingResult] = []

        manifest_files = (
            "requirements.txt",
            "package.json",
            "pom.xml",
            "cargo.toml",
            "go.mod",
        )

        for rel_path, content in file_contents.items():
            if not any(rel_path.lower().endswith(m) for m in manifest_files):
                continue

            for (
                pkg_name,
                pattern,
                cve,
                cvss,
                severity,
                desc,
            ) in self.KNOWN_VULNERABILITIES:
                if re.search(pattern, content):
                    dependencies.append(
                        DependencyFindingResult(
                            package_name=pkg_name,
                            version="Vulnerable Version",
                            cve_id=cve,
                            cvss_score=cvss,
                            severity=severity,
                            description=desc,
                            references=[f"https://nvd.nist.gov/vuln/detail/{cve}"],
                        )
                    )

        result.dependencies = dependencies
        result.dependency_vuln_count = len(dependencies)
        result.critical_count += sum(
            1 for d in dependencies if d.severity == "CRITICAL"
        )
        result.high_count += sum(1 for d in dependencies if d.severity == "HIGH")

        return result
