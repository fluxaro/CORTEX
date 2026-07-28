"""Static application security testing (SAST) rules scanner."""

import re
from typing import Any

from app.analyzers.security.base_scanner import BaseSecurityScanner
from app.analyzers.security.models import SecurityAnalysisResult, SecurityFindingResult


class SASTRules(BaseSecurityScanner):
    """Scans code for dangerous functions, SQL injection, XSS, and weak cryptography."""

    SAST_RULES = [
        (
            "SEC-001",
            "Dangerous Eval Execution",
            "Code Execution",
            r"\beval\s*\(",
            "CRITICAL",
            "Python/JS",
            "Use of eval() permits arbitrary code execution.",
        ),
        (
            "SEC-002",
            "Dangerous Exec Execution",
            "Code Execution",
            r"\bexec\s*\(",
            "CRITICAL",
            "Python",
            "Use of exec() permits dynamic arbitrary code execution.",
        ),
        (
            "SEC-003",
            "Unsafe Pickle Deserialization",
            "Deserialization",
            r"pickle\.loads\s*\(",
            "CRITICAL",
            "Python",
            "Unsafe pickle deserialization allows remote code execution.",
        ),
        (
            "SEC-004",
            "Command Injection Shell=True",
            "Command Injection",
            r"subprocess\.\w+\(.*shell\s*=\s*True",
            "HIGH",
            "Python",
            "Subprocess with shell=True enables shell command injection.",
        ),
        (
            "SEC-005",
            "Unsafe OS System Call",
            "Command Injection",
            r"os\.system\s*\(",
            "HIGH",
            "Python",
            "Use of os.system() is vulnerable to command injection.",
        ),
        (
            "SEC-006",
            "Java Runtime Exec",
            "Command Injection",
            r"Runtime\.getRuntime\(\)\.exec\(",
            "HIGH",
            "Java",
            "Direct Runtime.exec execution of unsanitized commands.",
        ),
        (
            "SEC-007",
            "React DangerouslySetInnerHTML",
            "Cross-Site Scripting",
            r"dangerouslySetInnerHTML",
            "HIGH",
            "TypeScript",
            "Bypasses React XSS sanitization protections.",
        ),
        (
            "SEC-008",
            "Direct innerHTML Assignment",
            "Cross-Site Scripting",
            r"\.innerHTML\s*=",
            "MEDIUM",
            "JavaScript",
            "Direct innerHTML assignment introduces XSS vulnerability.",
        ),
        (
            "SEC-009",
            "Weak MD5 Hashing",
            "Weak Cryptography",
            r"hashlib\.md5\(|MD5\.create\(",
            "MEDIUM",
            "Python",
            "MD5 hashing algorithm is cryptographically broken.",
        ),
        (
            "SEC-010",
            "Weak SHA1 Hashing",
            "Weak Cryptography",
            r"hashlib\.sha1\(|SHA1\.create\(",
            "MEDIUM",
            "Python",
            "SHA1 hashing algorithm is vulnerable to collision attacks.",
        ),
        (
            "SEC-011",
            "Insecure Pseudo-Randomness",
            "Insecure Randomness",
            r"\brandom\.random\(|Math\.random\(",
            "LOW",
            "Multi",
            "Standard pseudo-random generators are not cryptographically secure.",
        ),
        (
            "SEC-012",
            "SQL Injection Concatenation",
            "SQL Injection",
            r"(?i)(SELECT|INSERT|UPDATE|DELETE).*\+.*|\".*SELECT.*%s\"",
            "HIGH",
            "Multi",
            "SQL query created using string concatenation instead of parameterized binding.",
        ),
        (
            "SEC-013",
            "Unsafe YAML Load",
            "Deserialization",
            r"yaml\.load\s*\([^,)]*\)",
            "HIGH",
            "Python",
            "yaml.load() without SafeLoader executes arbitrary Python code.",
        ),
    ]

    @property
    def scanner_name(self) -> str:
        return "SASTRules"

    def scan(
        self,
        target_path: str,
        file_contents: dict[str, str],
        extra_context: dict[str, Any] | None = None,
    ) -> SecurityAnalysisResult:
        result = SecurityAnalysisResult()
        findings: list[SecurityFindingResult] = []

        code_extensions = (".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".java", ".rs")

        for rel_path, content in file_contents.items():
            if not rel_path.lower().endswith(code_extensions):
                continue

            lines = content.splitlines()
            for line_no, line in enumerate(lines, start=1):
                for (
                    rule_id,
                    rule_name,
                    category,
                    pattern,
                    severity,
                    lang,
                    desc,
                ) in self.SAST_RULES:
                    if re.search(pattern, line):
                        findings.append(
                            SecurityFindingResult(
                                rule_id=rule_id,
                                rule_name=rule_name,
                                category=category,
                                severity=severity,
                                confidence=0.85,
                                language=lang,
                                file_path=rel_path,
                                line_number=line_no,
                                description=f"Security issue [{rule_id}] {rule_name}: {desc}",
                                reference_url=f"https://owasp.org/www-community/vulnerabilities/{category.replace(' ', '_')}",
                            )
                        )

        result.findings = findings
        result.critical_count += sum(1 for f in findings if f.severity == "CRITICAL")
        result.high_count += sum(1 for f in findings if f.severity == "HIGH")
        result.medium_count += sum(1 for f in findings if f.severity == "MEDIUM")
        result.low_count += sum(1 for f in findings if f.severity == "LOW")

        return result
