"""Data transfer objects for Security Intelligence analysis."""

from dataclasses import dataclass, field


@dataclass
class SecretFindingResult:
    """Hardcoded secret or token finding."""

    secret_type: str
    severity: str
    line_number: int
    file_path: str
    entropy: float = 0.0
    masked_value: str = "********"
    description: str = ""


@dataclass
class DependencyFindingResult:
    """Dependency vulnerability or license finding."""

    package_name: str
    version: str
    cve_id: str | None = None
    cvss_score: float | None = None
    severity: str = "HIGH"
    license: str | None = None
    description: str = ""
    references: list[str] = field(default_factory=list)


@dataclass
class ConfigFindingResult:
    """Configuration misconfiguration finding."""

    file_path: str
    rule_name: str
    severity: str
    line_number: int = 1
    description: str = ""


@dataclass
class AuthFindingResult:
    """Authentication weakness finding."""

    auth_type: str
    severity: str
    file_path: str
    line_number: int = 1
    description: str = ""


@dataclass
class AuthzFindingResult:
    """Authorization weakness finding."""

    authz_type: str
    severity: str
    file_path: str
    line_number: int = 1
    description: str = ""


@dataclass
class SecurityFindingResult:
    """General SAST security rule finding."""

    rule_id: str
    rule_name: str
    category: str
    severity: str
    confidence: float
    language: str
    file_path: str
    line_number: int = 1
    column_number: int = 1
    description: str = ""
    remediation_placeholder: str = "Upgrade dependency or sanitize user input."
    reference_url: str | None = None
    cvss_score: float | None = None


@dataclass
class SecurityAnalysisResult:
    """Aggregated security intelligence analysis report."""

    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    info_count: int = 0

    secret_count: int = 0
    dependency_vuln_count: int = 0
    config_issues_count: int = 0
    auth_issues_count: int = 0

    findings: list[SecurityFindingResult] = field(default_factory=list)
    secrets: list[SecretFindingResult] = field(default_factory=list)
    dependencies: list[DependencyFindingResult] = field(default_factory=list)
    configs: list[ConfigFindingResult] = field(default_factory=list)
    auth_findings: list[AuthFindingResult] = field(default_factory=list)
    authz_findings: list[AuthzFindingResult] = field(default_factory=list)
