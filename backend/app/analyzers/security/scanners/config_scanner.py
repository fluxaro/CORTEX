"""Infrastructure configuration security scanner."""

import re
from typing import Any

from app.analyzers.security.base_scanner import BaseSecurityScanner
from app.analyzers.security.models import ConfigFindingResult, SecurityAnalysisResult


class ConfigScanner(BaseSecurityScanner):
    """Scans Dockerfiles, compose files, environment files, K8s, and web server configs."""

    CONFIG_RULES = [
        (
            "Debug Mode Enabled",
            r"(?i)\bDEBUG\s*=\s*(true|1|yes)\b",
            "HIGH",
            "Debug mode enabled in environment configuration.",
        ),
        (
            "Root User Container",
            r"(?i)USER\s+root",
            "HIGH",
            "Container configured to run as root superuser.",
        ),
        (
            "Privileged Container",
            r"(?i)privileged:\s*true",
            "CRITICAL",
            "Container executed with host root privileges.",
        ),
        (
            "Unsafe Curl Execution",
            r"(?i)curl\s+.*\|\s*(bash|sh)",
            "HIGH",
            "Piping unverified curl script execution into shell.",
        ),
        (
            "Default Credentials",
            r"(?i)(postgres:postgres|admin:admin|root:root)",
            "HIGH",
            "Default default credentials detected in config.",
        ),
        (
            "Open Insecure Port 80",
            r"(?i)ports:\s*-\s*[\"']?80:80",
            "MEDIUM",
            "HTTP port 80 exposed without TLS encryption.",
        ),
        (
            "Missing Security Headers",
            r"(?i)add_header\s+X-Frame-Options",
            "LOW",
            "Missing web server security header.",
        ),
    ]

    @property
    def scanner_name(self) -> str:
        return "ConfigScanner"

    def scan(
        self,
        target_path: str,
        file_contents: dict[str, str],
        extra_context: dict[str, Any] | None = None,
    ) -> SecurityAnalysisResult:
        result = SecurityAnalysisResult()
        configs: list[ConfigFindingResult] = []

        config_extensions = (
            ".env",
            ".dockerfile",
            "dockerfile",
            ".yml",
            ".yaml",
            ".tf",
            ".conf",
        )

        for rel_path, content in file_contents.items():
            path_lower = rel_path.lower()
            if not any(
                path_lower.endswith(ext) or ext in path_lower
                for ext in config_extensions
            ):
                continue

            lines = content.splitlines()
            for line_no, line in enumerate(lines, start=1):
                for rule_name, pattern, severity, desc in self.CONFIG_RULES:
                    if re.search(pattern, line):
                        configs.append(
                            ConfigFindingResult(
                                file_path=rel_path,
                                rule_name=rule_name,
                                severity=severity,
                                line_number=line_no,
                                description=f"Configuration issue '{rule_name}' found in '{rel_path}' line {line_no}: {desc}",
                            )
                        )

        result.configs = configs
        result.config_issues_count = len(configs)
        result.high_count += sum(1 for c in configs if c.severity == "HIGH")
        result.critical_count += sum(1 for c in configs if c.severity == "CRITICAL")
        result.medium_count += sum(1 for c in configs if c.severity == "MEDIUM")

        return result
