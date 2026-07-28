"""Data transfer objects for Maintainability & Repository Intelligence."""

from dataclasses import dataclass, field


@dataclass
class ReadmeResult:
    """README section and completeness analysis result."""

    completeness_percentage: float = 0.0
    detected_sections: list[str] = field(default_factory=list)
    missing_sections: list[str] = field(default_factory=list)
    has_badges: bool = False
    has_screenshots: bool = False


@dataclass
class DocumentationResult:
    """Documentation structure analysis result."""

    documentation_score: float = 0.0
    has_architecture_docs: bool = False
    has_api_docs: bool = False
    has_deployment_guide: bool = False
    has_dev_guide: bool = False
    doc_frameworks: list[str] = field(default_factory=list)
    readme: ReadmeResult = field(default_factory=ReadmeResult)


@dataclass
class LicenseResult:
    """License identification and compliance result."""

    spdx_identifier: str = "NOASSERTION"
    is_osi_approved: bool = False
    has_license_file: bool = False
    is_consistent: bool = True


@dataclass
class TestingResult:
    """Testing maturity analysis result."""

    testing_score: float = 0.0
    frameworks: list[str] = field(default_factory=list)
    test_file_count: int = 0
    estimated_test_count: int = 0
    has_unit_tests: bool = False
    has_integration_tests: bool = False
    has_e2e_tests: bool = False
    has_mocks: bool = False


@dataclass
class CiResult:
    """CI/CD automation analysis result."""

    ci_score: float = 0.0
    providers: list[str] = field(default_factory=list)
    has_test_jobs: bool = False
    has_lint_jobs: bool = False
    has_security_scans: bool = False
    has_build_jobs: bool = False
    has_deploy_jobs: bool = False


@dataclass
class GitHistoryResult:
    """Git repository history analytics."""

    commit_count: int = 0
    contributor_count: int = 0
    branch_count: int = 0
    tag_count: int = 0
    repo_age_days: int = 0
    commits_per_week: float = 0.0
    inactive_periods_count: int = 0
    development_velocity_score: float = 0.0


@dataclass
class CommitResult:
    """Commit quality and Conventional Commits analytics."""

    commit_quality_score: float = 0.0
    conventional_commits_percentage: float = 0.0
    generic_commits_percentage: float = 0.0
    commit_types_breakdown: dict[str, int] = field(default_factory=dict)


@dataclass
class ReleaseResult:
    """Git releases and SemVer compliance analysis."""

    release_score: float = 0.0
    release_count: int = 0
    has_changelog: bool = False
    uses_semver: bool = False
    latest_release_tag: str | None = None
    days_since_last_release: int | None = None


@dataclass
class CommunityResult:
    """Open source community standards compliance."""

    community_score: float = 0.0
    has_contributing: bool = False
    has_code_of_conduct: bool = False
    has_security_policy: bool = False
    has_issue_templates: bool = False
    has_pr_templates: bool = False
    has_discussions: bool = False


@dataclass
class PackageQualityResult:
    """Package manifest metadata completeness."""

    missing_metadata: list[str] = field(default_factory=list)
    has_package_manifest: bool = False


@dataclass
class MaintainabilityAnalysisResult:
    """Aggregated Maintainability & Repository Intelligence report."""

    documentation_score: float = 0.0
    testing_score: float = 0.0
    ci_score: float = 0.0
    release_score: float = 0.0
    repository_health_score: float = 0.0
    community_score: float = 0.0

    documentation: DocumentationResult = field(default_factory=DocumentationResult)
    testing: TestingResult = field(default_factory=TestingResult)
    ci: CiResult = field(default_factory=CiResult)
    git_history: GitHistoryResult = field(default_factory=GitHistoryResult)
    commit_analysis: CommitResult = field(default_factory=CommitResult)
    release_analysis: ReleaseResult = field(default_factory=ReleaseResult)
    community: CommunityResult = field(default_factory=CommunityResult)
    license_analysis: LicenseResult = field(default_factory=LicenseResult)
    package_quality: PackageQualityResult = field(default_factory=PackageQualityResult)
