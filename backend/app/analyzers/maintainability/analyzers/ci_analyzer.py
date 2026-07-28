"""CI/CD pipeline and automation job analyzer."""

import re

from app.analyzers.maintainability.models import CiResult


class CiAnalyzer:
    """Detects CI/CD automation providers, workflow jobs, security scans, and deployment steps."""

    @classmethod
    def analyze(  # noqa: C901
        cls, file_paths: list[str], file_contents: dict[str, str]
    ) -> CiResult:
        """Analyze CI/CD configs and job types."""
        paths_lower = [p.lower() for p in file_paths]

        providers = []
        if any(".github/workflows" in p for p in paths_lower):
            providers.append("GitHub Actions")
        if any(".gitlab-ci" in p for p in paths_lower):
            providers.append("GitLab CI")
        if any("azure-pipelines" in p for p in paths_lower):
            providers.append("Azure Pipelines")
        if any(".circleci" in p for p in paths_lower):
            providers.append("CircleCI")
        if any("jenkinsfile" in p for p in paths_lower):
            providers.append("Jenkins")
        if any(".travis" in p for p in paths_lower):
            providers.append("Travis CI")

        has_test = False
        has_lint = False
        has_sec = False
        has_build = False
        has_deploy = False

        for path, content in file_contents.items():
            path_lower = path.lower()
            if not any(
                provider_path in path_lower
                for provider_path in (
                    ".github/workflows",
                    ".gitlab-ci",
                    "circleci",
                    "jenkins",
                    "azure-pipelines",
                    "travis",
                )
            ):
                continue

            if re.search(r"(?i)\b(pytest|jest|test|npm test|go test)\b", content):
                has_test = True
            if re.search(r"(?i)\b(lint|flake8|eslint|ruff|black|fmt)\b", content):
                has_lint = True
            if re.search(r"(?i)\b(snyk|trivy|codeql|bandit|security|audit)\b", content):
                has_sec = True
            if re.search(r"(?i)\b(build|docker build|compile|mvn package)\b", content):
                has_build = True
            if re.search(
                r"(?i)\b(deploy|release|kubectl|docker push|aws s3|cloud run)\b",
                content,
            ):
                has_deploy = True

        score = 0.0
        if len(providers) > 0:
            score += 30.0
        if has_test:
            score += 25.0
        if has_lint:
            score += 15.0
        if has_sec:
            score += 15.0
        if has_build:
            score += 10.0
        if has_deploy:
            score += 5.0

        return CiResult(
            ci_score=round(min(score, 100.0), 1),
            providers=providers,
            has_test_jobs=has_test,
            has_lint_jobs=has_lint,
            has_security_scans=has_sec,
            has_build_jobs=has_build,
            has_deploy_jobs=has_deploy,
        )
