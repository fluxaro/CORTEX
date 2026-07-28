"""Pydantic v2 schemas for Maintainability & Repository Intelligence endpoints."""

import uuid

from pydantic import BaseModel, ConfigDict


class ReadmeAnalysisResponse(BaseModel):
    """Schema for README section completeness."""

    model_config = ConfigDict(from_attributes=True)

    completeness_percentage: float
    detected_sections: list[str]
    missing_sections: list[str]
    has_badges: bool
    has_screenshots: bool


class DocumentationAnalysisResponse(BaseModel):
    """Schema for documentation coverage."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    documentation_score: float
    has_architecture_docs: bool
    has_api_docs: bool
    has_deployment_guide: bool
    has_dev_guide: bool
    doc_frameworks: list[str]
    readme_analysis: ReadmeAnalysisResponse | None = None


class TestingAnalysisResponse(BaseModel):
    """Schema for testing suite maturity."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    testing_score: float
    frameworks: list[str]
    test_file_count: int
    estimated_test_count: int
    has_unit_tests: bool
    has_integration_tests: bool
    has_e2e_tests: bool
    has_mocks: bool


class GitHistoryAnalysisResponse(BaseModel):
    """Schema for Git history and commit frequency."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    commit_count: int
    contributor_count: int
    branch_count: int
    tag_count: int
    repo_age_days: int
    commits_per_week: float
    inactive_periods_count: int
    development_velocity_score: float


class CommitAnalysisResponse(BaseModel):
    """Schema for commit quality and Conventional Commits."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    commit_quality_score: float
    conventional_commits_percentage: float
    generic_commits_percentage: float
    commit_types_breakdown: dict[str, int]


class ReleaseAnalysisResponse(BaseModel):
    """Schema for Git release history and SemVer."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    release_score: float
    release_count: int
    has_changelog: bool
    uses_semver: bool
    latest_release_tag: str | None = None
    days_since_last_release: int | None = None


class CommunityAnalysisResponse(BaseModel):
    """Schema for open source community standards."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    community_score: float
    has_contributing: bool
    has_code_of_conduct: bool
    has_security_policy: bool
    has_issue_templates: bool
    has_pr_templates: bool
    has_discussions: bool


class CiAnalysisResponse(BaseModel):
    """Schema for CI/CD automation pipelines."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    ci_score: float
    providers: list[str]
    has_test_jobs: bool
    has_lint_jobs: bool
    has_security_scans: bool
    has_build_jobs: bool
    has_deploy_jobs: bool


class MaintainabilityMetricsResponse(BaseModel):
    """Schema for raw subsystem scores."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    repository_id: uuid.UUID
    analysis_run_id: uuid.UUID

    documentation_score: float
    testing_score: float
    ci_score: float
    release_score: float
    repository_health_score: float
    community_score: float


class RepositoryHealthResponse(BaseModel):
    """Schema for repository health breakdown."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    repository_health_score: float
    maintenance_frequency_score: float
    community_readiness_score: float
    contribution_readiness_score: float
