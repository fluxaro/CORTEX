"""Architectural layer detector."""

from app.analyzers.architecture.models import LayerResult


class LayerDetector:
    """Classifies repository paths and files into architectural layers."""

    LAYER_PATTERNS = {
        "Presentation": [
            "controllers/",
            "routes/",
            "api/",
            "endpoints/",
            "views/",
            "components/",
            "pages/",
            "web/",
            "ui/",
        ],
        "Application": [
            "services/",
            "use_cases/",
            "commands/",
            "queries/",
            "handlers/",
            "app/",
            "application/",
        ],
        "Domain": [
            "domain/",
            "entities/",
            "models/",
            "aggregates/",
            "core/",
            "types/",
        ],
        "Infrastructure": [
            "infrastructure/",
            "repositories/",
            "persistence/",
            "database/",
            "db/",
            "external/",
            "client/",
            "integrations/",
        ],
        "Utilities/Shared": [
            "utils/",
            "helpers/",
            "common/",
            "shared/",
            "middleware/",
            "config/",
        ],
    }

    @classmethod
    def detect_layers(cls, file_paths: list[str]) -> list[LayerResult]:
        """Categorize file paths into architectural layers."""
        layer_files: dict[str, list[str]] = {
            "Presentation": [],
            "Application": [],
            "Domain": [],
            "Infrastructure": [],
            "Utilities/Shared": [],
        }

        for path in file_paths:
            path_lower = path.lower()
            assigned = False

            for layer_name, patterns in cls.LAYER_PATTERNS.items():
                if any(p in path_lower for p in patterns):
                    layer_files[layer_name].append(path)
                    assigned = True
                    break

            if not assigned:
                layer_files["Domain"].append(path)

        results: list[LayerResult] = []
        descriptions = {
            "Presentation": "UI components, controllers, HTTP routes, and API endpoints",
            "Application": "Business use-cases, orchestration services, and command handlers",
            "Domain": "Core domain models, entities, and business rules",
            "Infrastructure": "Database persistence, external API clients, and repositories",
            "Utilities/Shared": "Shared utilities, middlewares, and configuration helpers",
        }

        for name, files in layer_files.items():
            if files:
                results.append(
                    LayerResult(
                        name=name,
                        category=name.lower(),
                        file_paths=files,
                        description=descriptions.get(name, ""),
                    )
                )

        return results
