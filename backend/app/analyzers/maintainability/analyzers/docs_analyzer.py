"""Documentation structure and frameworks analyzer."""

from app.analyzers.maintainability.analyzers.readme_analyzer import ReadmeAnalyzer
from app.analyzers.maintainability.models import DocumentationResult


class DocsAnalyzer:
    """Scans repository documentation structure, wikis, and generator configs."""

    @classmethod
    def analyze(
        cls, file_paths: list[str], file_contents: dict[str, str]
    ) -> DocumentationResult:
        """Analyze documentation coverage and generator frameworks."""
        paths_lower = [p.lower() for p in file_paths]
        readme_res = ReadmeAnalyzer.analyze(file_contents)

        doc_frameworks = []
        if any("mkdocs.yml" in p for p in paths_lower):
            doc_frameworks.append("MkDocs")
        if any("docusaurus.config" in p for p in paths_lower):
            doc_frameworks.append("Docusaurus")
        if any("swagger" in p or "openapi" in p for p in paths_lower):
            doc_frameworks.append("Swagger/OpenAPI")
        if any("typedoc" in p for p in paths_lower):
            doc_frameworks.append("TypeDoc")
        if any("javadoc" in p for p in paths_lower):
            doc_frameworks.append("Javadoc")

        has_arch = (
            any("architecture" in p or "design" in p for p in paths_lower)
            or "Architecture" in readme_res.detected_sections
        )
        has_api = (
            any("api" in p or "openapi" in p or "swagger" in p for p in paths_lower)
            or "API Documentation" in readme_res.detected_sections
        )
        has_deploy = any("deploy" in p or "docker" in p for p in paths_lower)
        has_dev = (
            any(
                "contributing" in p or "dev" in p or "developer" in p
                for p in paths_lower
            )
            or "Contributing" in readme_res.detected_sections
        )

        # Calculate documentation score (0-100)
        score = readme_res.completeness_percentage * 0.5
        if has_arch:
            score += 15.0
        if has_api:
            score += 15.0
        if has_deploy:
            score += 10.0
        if has_dev:
            score += 10.0

        return DocumentationResult(
            documentation_score=round(min(score, 100.0), 1),
            has_architecture_docs=has_arch,
            has_api_docs=has_api,
            has_deployment_guide=has_deploy,
            has_dev_guide=has_dev,
            doc_frameworks=doc_frameworks,
            readme=readme_res,
        )
