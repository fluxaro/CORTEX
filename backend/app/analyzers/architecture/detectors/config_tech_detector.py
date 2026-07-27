"""Configuration, Technology Stack, and API Surface detector."""

import re

from app.analyzers.architecture.models import TechStackResult
from app.analyzers.shared.models import FileAnalysisResult


class ConfigTechDetector:
    """Detects infrastructure configurations, tech stack tools, and exposed API surfaces."""

    CONFIG_RULES = [
        ("Docker", "containers", r"(?i)dockerfile"),
        ("Docker Compose", "containers", r"(?i)docker-compose\.yml|compose\.yaml"),
        ("Kubernetes", "cloud", r"(?i)k8s|deployment\.yaml|helm"),
        ("GitHub Actions", "ci_cd", r"\.github/workflows"),
        ("GitLab CI", "ci_cd", r"\.gitlab-ci\.yml"),
        ("Azure Pipelines", "ci_cd", r"azure-pipelines\.yml"),
        ("Terraform", "cloud", r"\.tf$"),
        ("Ansible", "cloud", r"playbook\.yml|ansible"),
        ("Nginx", "cloud", r"nginx\.conf"),
        ("Redis", "caching", r"redis"),
        ("PostgreSQL", "databases", r"postgres|psycopg|asyncpg"),
        ("MongoDB", "databases", r"mongo|mongoose"),
        ("SQLite", "databases", r"sqlite"),
        ("Prisma", "orms", r"schema\.prisma"),
        ("Alembic", "orms", r"alembic\.ini|alembic/versions"),
    ]

    API_SURFACE_RULES = [
        (
            "REST APIs",
            r"(?i)(GET|POST|PUT|DELETE|APIRouter|fastapi|express\(\)|@app\.)",
        ),
        ("GraphQL", r"(?i)(graphql|type Query|gql)"),
        ("gRPC", r"(?i)(\.proto|grpc)"),
        ("WebSocket", r"(?i)(websocket|ws://|wss://|@WebSocket)"),
        ("Server Sent Events", r"(?i)(EventSource|text/event-stream)"),
        ("Background Workers", r"(?i)(celery|rq|bull|sidekiq)"),
        ("Cron Jobs", r"(?i)(@periodic_task|cron|schedule)"),
    ]

    @classmethod
    def analyze_tech_stack(  # noqa: C901
        cls,
        all_file_paths: list[str],
        file_results: list[FileAnalysisResult],
    ) -> TechStackResult:
        """Extract structured technology stack metadata and API surfaces."""
        tech = TechStackResult()

        all_paths_str = " ".join(all_file_paths)
        all_imports_str = (
            " ".join(imp for f in file_results for imp in f.imports)
            + " "
            + all_paths_str
        )

        # Languages
        languages = list({f.language for f in file_results if f.language != "Text"})
        tech.languages = languages if languages else ["Python"]

        # Config Rules Lookup
        for name, category, pattern in cls.CONFIG_RULES:
            if re.search(pattern, all_imports_str):
                attr = getattr(tech, category, None)
                if isinstance(attr, list) and name not in attr:
                    attr.append(name)

        # Build tools / Linters / Formatters
        if "pyproject.toml" in all_paths_str or "setup.py" in all_paths_str:
            tech.package_managers.append("pip/setuptools")
            tech.build_tools.append("flit/poetry/hatch")
        if "package.json" in all_paths_str:
            tech.package_managers.append("npm/yarn/pnpm")
        if "go.mod" in all_paths_str:
            tech.package_managers.append("go modules")
        if "Cargo.toml" in all_paths_str:
            tech.package_managers.append("cargo")

        if (
            "ruff" in all_imports_str
            or "flake8" in all_imports_str
            or "eslint" in all_imports_str
        ):
            tech.linters.extend(["Ruff/ESLint"])
        if "black" in all_imports_str or "prettier" in all_imports_str:
            tech.formatters.extend(["Black/Prettier"])
        if "pytest" in all_imports_str or "jest" in all_imports_str:
            tech.testing_frameworks.extend(["Pytest/Jest"])

        # API Surfaces
        for api_name, pattern in cls.API_SURFACE_RULES:
            if re.search(pattern, all_imports_str):
                if api_name not in tech.api_surfaces:
                    tech.api_surfaces.append(api_name)

        return tech
