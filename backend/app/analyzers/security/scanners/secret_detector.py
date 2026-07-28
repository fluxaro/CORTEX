"""Secret and credentials scanner."""

import math
import re
from typing import Any

from app.analyzers.security.base_scanner import BaseSecurityScanner
from app.analyzers.security.models import SecretFindingResult, SecurityAnalysisResult


class SecretDetector(BaseSecurityScanner):
    """Scans repository files for committed API keys, tokens, passwords, and private keys."""

    SECRET_PATTERNS = [
        ("AWS Access Key", r"AKIA[0-9A-Z]{16}", "CRITICAL"),
        ("GCP API Key", r"AIza[0-9A-Za-z-_]{35}", "CRITICAL"),
        (
            "GitHub Personal Access Token",
            r"ghp_[0-9a-zA-Z]{36}|github_pat_[0-9a-zA-Z_]{80,}",
            "CRITICAL",
        ),
        ("GitLab Access Token", r"glpat-[0-9a-zA-Z\-]{20}", "CRITICAL"),
        ("OpenAI API Key", r"sk-[a-zA-Z0-9]{32,}", "CRITICAL"),
        ("Stripe Secret Key", r"sk_live_[0-9a-zA-Z]{24,}", "CRITICAL"),
        ("Twilio API Key", r"SK[0-9a-fA-F]{32}", "HIGH"),
        ("Slack Bot Token", r"xoxb-[0-9]{11}-[0-9]{11}-[a-zA-Z0-9]{24}", "CRITICAL"),
        ("Telegram Bot Token", r"[0-9]{9}:[a-zA-Z0-9_-]{35}", "HIGH"),
        (
            "PostgreSQL Connection URL",
            r"postgres(?:ql)?://\w+:\w+@[\w\.-]+:\d+/\w+",
            "CRITICAL",
        ),
        ("MongoDB Connection URL", r"mongodb(?:\+srv)?://\w+:\w+@[\w\.-]+", "CRITICAL"),
        ("Redis Connection URL", r"redis://:\w+@[\w\.-]+:\d+", "HIGH"),
        ("RSA Private Key", r"-----BEGIN RSA PRIVATE KEY-----", "CRITICAL"),
        (
            "PEM Private Key",
            r"-----BEGIN (?:EC|OPENSSH|ANY)? PRIVATE KEY-----",
            "CRITICAL",
        ),
        (
            "JWT Secret Token",
            r"eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]*",
            "HIGH",
        ),
        (
            "Slack Webhook URL",
            r"https://hooks\.slack\.com/services/T[a-zA-Z0-9_]+/B[a-zA-Z0-9_]+/[a-zA-Z0-9_]+",
            "HIGH",
        ),
        (
            "Discord Webhook URL",
            r"https://discord(?:app)?\.com/api/webhooks/\d+/[a-zA-Z0-9_-]+",
            "HIGH",
        ),
        (
            "Hardcoded Password Variable",
            r"(?i)(password|passwd|secret_key)\s*=\s*['\"][^'\"]{6,}['\"]",
            "HIGH",
        ),
    ]

    @property
    def scanner_name(self) -> str:
        return "SecretDetector"

    def scan(
        self,
        target_path: str,
        file_contents: dict[str, str],
        extra_context: dict[str, Any] | None = None,
    ) -> SecurityAnalysisResult:
        result = SecurityAnalysisResult()
        secrets: list[SecretFindingResult] = []

        for rel_path, content in file_contents.items():
            lines = content.splitlines()

            for line_no, line in enumerate(lines, start=1):
                # Pattern Matching
                for secret_type, regex_pat, severity in self.SECRET_PATTERNS:
                    matches = re.findall(regex_pat, line)
                    for raw_val in matches:
                        entropy = self.calculate_shannon_entropy(raw_val)
                        secrets.append(
                            SecretFindingResult(
                                secret_type=secret_type,
                                severity=severity,
                                line_number=line_no,
                                file_path=rel_path,
                                entropy=round(entropy, 2),
                                masked_value=self.mask_value(raw_val),
                                description=f"Potential hardcoded {secret_type} exposed in '{rel_path}' line {line_no}.",
                            )
                        )

        result.secrets = secrets
        result.secret_count = len(secrets)
        result.critical_count = sum(1 for s in secrets if s.severity == "CRITICAL")
        result.high_count = sum(1 for s in secrets if s.severity == "HIGH")

        return result

    @staticmethod
    def calculate_shannon_entropy(data: str) -> float:
        """Calculate Shannon entropy for a string to assess randomness."""
        if not data:
            return 0.0
        entropy = 0.0
        length = len(data)
        frequencies = {c: data.count(c) for c in set(data)}
        for count in frequencies.values():
            p = count / length
            entropy -= p * math.log2(p)
        return entropy

    @staticmethod
    def mask_value(val: str) -> str:
        """Mask sensitive value showing only prefix and suffix."""
        if len(val) <= 6:
            return "******"
        return f"{val[:3]}...{val[-3:]}"
