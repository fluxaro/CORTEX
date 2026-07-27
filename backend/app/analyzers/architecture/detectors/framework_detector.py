"""Framework detection and convention validator."""

import re
from typing import Any

from app.analyzers.architecture.models import FrameworkDetectionResult
from app.analyzers.shared.models import FileAnalysisResult


class FrameworkDetector:
    """Detects web/backend frameworks and validates framework conventions."""

    FRAMEWORK_INDICATORS = [
        ("FastAPI", "Web Framework", r"(?i)\bfastapi\b|\bAPIRouter\b", "Python"),
        ("Django", "Web Framework", r"(?i)\bdjango\b|\bmodels\.Model\b", "Python"),
        ("Flask", "Web Framework", r"(?i)\bflask\b|\bFlask\(__name__\)", "Python"),
        (
            "Next.js",
            "Fullstack Framework",
            r"(?i)\bnext\b|pages/|app/page\.",
            "TypeScript",
        ),
        (
            "React",
            "Frontend Library",
            r"(?i)\breact\b|use(State|Effect|Context)",
            "TypeScript",
        ),
        ("Express", "Web Framework", r"(?i)\bexpress\b|express\(\)", "JavaScript"),
        ("NestJS", "Backend Framework", r"(?i)@nestjs/|@Controller\(", "TypeScript"),
        (
            "Spring Boot",
            "Enterprise Framework",
            r"(?i)org\.springframework\.boot|@SpringBootApplication",
            "Java",
        ),
        ("Gin", "Web Framework", r"(?i)github\.com/gin-gonic/gin", "Go"),
        ("Echo", "Web Framework", r"(?i)github\.com/labstack/echo", "Go"),
        ("Fiber", "Web Framework", r"(?i)github\.com/gofiber/fiber", "Go"),
        ("Actix", "Web Framework", r"(?i)actix-web", "Rust"),
        ("Rocket", "Web Framework", r"(?i)rocket::", "Rust"),
        ("Axum", "Web Framework", r"(?i)axum::", "Rust"),
    ]

    @classmethod
    def detect_frameworks(
        cls,
        file_results: list[FileAnalysisResult],
    ) -> list[FrameworkDetectionResult]:
        """Detect installed frameworks and validate framework conventions."""
        detected: dict[str, FrameworkDetectionResult] = {}
        all_imports = set()
        all_paths = [f.path for f in file_results]

        for f in file_results:
            all_imports.update(f.imports)

        full_import_str = " ".join(all_imports) + " " + " ".join(all_paths)

        for name, category, pattern, _lang in cls.FRAMEWORK_INDICATORS:
            if re.search(pattern, full_import_str):
                findings: list[dict[str, Any]] = []
                is_compliant = True

                if name == "FastAPI":
                    has_router = any(
                        "APIRouter" in " ".join(f.imports) or "router" in f.path
                        for f in file_results
                    )
                    has_schemas = any(
                        "schemas" in f.path or "pydantic" in " ".join(f.imports)
                        for f in file_results
                    )

                    findings.append(
                        {"convention": "Router Separation", "compliant": has_router}
                    )
                    findings.append(
                        {"convention": "Pydantic Schemas", "compliant": has_schemas}
                    )
                    is_compliant = has_router and has_schemas

                elif name == "React":
                    has_hooks = any(
                        "use" in f.path or "useState" in " ".join(f.imports)
                        for f in file_results
                    )
                    has_components = any("components" in f.path for f in file_results)
                    findings.append(
                        {"convention": "Hooks Usage", "compliant": has_hooks}
                    )
                    findings.append(
                        {
                            "convention": "Component Separation",
                            "compliant": has_components,
                        }
                    )
                    is_compliant = has_components

                elif name == "Express":
                    has_routes = any("routes" in f.path for f in file_results)
                    has_controllers = any("controllers" in f.path for f in file_results)
                    findings.append(
                        {"convention": "Routes Separation", "compliant": has_routes}
                    )
                    findings.append(
                        {
                            "convention": "Controllers Separation",
                            "compliant": has_controllers,
                        }
                    )
                    is_compliant = has_routes and has_controllers

                detected[name] = FrameworkDetectionResult(
                    name=name,
                    category=category,
                    detected_version="Latest",
                    is_convention_compliant=is_compliant,
                    convention_findings=findings,
                )

        return list(detected.values())
