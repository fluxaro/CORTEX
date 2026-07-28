"""Main Maintainability & Repository Intelligence Engine orchestrator."""

import os

from app.analyzers.detector import RepositoryFileDetector
from app.analyzers.maintainability.analyzers.ci_analyzer import CiAnalyzer
from app.analyzers.maintainability.analyzers.community_analyzer import CommunityAnalyzer
from app.analyzers.maintainability.analyzers.docs_analyzer import DocsAnalyzer
from app.analyzers.maintainability.analyzers.git_history_analyzer import (
    GitHistoryAnalyzer,
)
from app.analyzers.maintainability.analyzers.license_changelog_analyzer import (
    LicenseChangelogAnalyzer,
)
from app.analyzers.maintainability.analyzers.package_quality_analyzer import (
    PackageQualityAnalyzer,
)
from app.analyzers.maintainability.analyzers.testing_analyzer import TestingAnalyzer
from app.analyzers.maintainability.models import MaintainabilityAnalysisResult


class MaintainabilityEngine:
    """Orchestrates deterministic maintainability, documentation, testing, CI, Git, and community analysis."""

    def __init__(self, target_path: str) -> None:
        self.target_path = os.path.abspath(target_path)

    def run(self) -> MaintainabilityAnalysisResult:
        """Run complete maintainability analysis pipeline."""
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

        # 1. Documentation & README
        doc_res = DocsAnalyzer.analyze(discovered.all_files, file_contents)

        # 2. License & CHANGELOG
        lic_res = LicenseChangelogAnalyzer.analyze_license(file_contents)
        has_changelog, uses_semver = LicenseChangelogAnalyzer.analyze_changelog(
            file_contents
        )

        # 3. Community Standards
        comm_res = CommunityAnalyzer.analyze(discovered.all_files)

        # 4. Testing Maturity
        test_res = TestingAnalyzer.analyze(discovered.all_files, file_contents)

        # 5. CI/CD Pipeline
        ci_res = CiAnalyzer.analyze(discovered.all_files, file_contents)

        # 6. Git History & Commits & Releases
        git_res, commit_res, rel_res = GitHistoryAnalyzer.analyze(self.target_path)
        rel_res.has_changelog = has_changelog
        if not rel_res.uses_semver:
            rel_res.uses_semver = uses_semver

        # 7. Package Quality
        pkg_res = PackageQualityAnalyzer.analyze(file_contents)

        # Calculate Repository Health Score (0-100)
        repo_health_score = 40.0
        if git_res.commits_per_week > 0.5:
            repo_health_score += 20.0
        if git_res.inactive_periods_count == 0:
            repo_health_score += 15.0
        if doc_res.documentation_score > 50.0:
            repo_health_score += 15.0
        if comm_res.has_contributing:
            repo_health_score += 10.0
        repo_health_score = round(min(repo_health_score, 100.0), 1)

        return MaintainabilityAnalysisResult(
            documentation_score=doc_res.documentation_score,
            testing_score=test_res.testing_score,
            ci_score=ci_res.ci_score,
            release_score=rel_res.release_score,
            repository_health_score=repo_health_score,
            community_score=comm_res.community_score,
            documentation=doc_res,
            testing=test_res,
            ci=ci_res,
            git_history=git_res,
            commit_analysis=commit_res,
            release_analysis=rel_res,
            community=comm_res,
            license_analysis=lic_res,
            package_quality=pkg_res,
        )
