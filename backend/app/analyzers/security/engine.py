"""Main Security Intelligence Engine orchestrator."""

import os

from app.analyzers.detector import RepositoryFileDetector
from app.analyzers.security.models import SecurityAnalysisResult
from app.analyzers.security.registry import SecurityScannerRegistry
from app.analyzers.security.scanners.auth_scanner import AuthScanner
from app.analyzers.security.scanners.authz_scanner import AuthzScanner
from app.analyzers.security.scanners.config_scanner import ConfigScanner
from app.analyzers.security.scanners.dependency_scanner import DependencyScanner
from app.analyzers.security.scanners.sast_rules import SASTRules
from app.analyzers.security.scanners.secret_detector import SecretDetector


def _initialize_scanners() -> None:
    """Register standard security scanners."""
    SecurityScannerRegistry.register(SecretDetector())
    SecurityScannerRegistry.register(ConfigScanner())
    SecurityScannerRegistry.register(DependencyScanner())
    SecurityScannerRegistry.register(SASTRules())
    SecurityScannerRegistry.register(AuthScanner())
    SecurityScannerRegistry.register(AuthzScanner())


_initialize_scanners()


class SecurityIntelligenceEngine:
    """Orchestrates security scanners (SAST, Secrets, Configs, Dependencies, Auth/Authz)."""

    def __init__(self, target_path: str) -> None:
        self.target_path = os.path.abspath(target_path)

    def run(self) -> SecurityAnalysisResult:
        """Run complete security scanning pipeline."""
        if not os.path.exists(self.target_path) or not os.path.isdir(self.target_path):
            raise ValueError(
                f"Target repository path '{self.target_path}' does not exist or is not a directory."
            )

        discovered = RepositoryFileDetector.discover(self.target_path)

        file_contents: dict[str, str] = {}
        for rel_path in discovered.all_files:
            full_path = os.path.join(self.target_path, rel_path)
            try:
                with open(full_path, encoding="utf-8", errors="ignore") as f:
                    file_contents[rel_path] = f.read()
            except OSError:
                continue

        aggregated = SecurityAnalysisResult()

        for scanner in SecurityScannerRegistry.get_all_scanners():
            scan_res = scanner.scan(
                target_path=self.target_path,
                file_contents=file_contents,
            )

            aggregated.findings.extend(scan_res.findings)
            aggregated.secrets.extend(scan_res.secrets)
            aggregated.dependencies.extend(scan_res.dependencies)
            aggregated.configs.extend(scan_res.configs)
            aggregated.auth_findings.extend(scan_res.auth_findings)
            aggregated.authz_findings.extend(scan_res.authz_findings)

            aggregated.critical_count += scan_res.critical_count
            aggregated.high_count += scan_res.high_count
            aggregated.medium_count += scan_res.medium_count
            aggregated.low_count += scan_res.low_count
            aggregated.info_count += scan_res.info_count

            aggregated.secret_count += scan_res.secret_count
            aggregated.dependency_vuln_count += scan_res.dependency_vuln_count
            aggregated.config_issues_count += scan_res.config_issues_count
            aggregated.auth_issues_count += scan_res.auth_issues_count

        return aggregated
