"""High-level software architecture detector."""

from app.analyzers.architecture.models import LayerResult


class ArchDetector:
    """Detects software architecture style based on layer structure and file organization."""

    @classmethod
    def detect_architecture_style(
        cls,
        layers: list[LayerResult],
        all_file_paths: list[str],
    ) -> tuple[str, float]:
        """Classify high-level architecture style and assign confidence score."""
        layer_names = {layer.name for layer in layers}
        paths_str = " ".join(all_file_paths).lower()

        has_domain = any(k in paths_str for k in ("domain/", "entities/"))
        has_infra = any(k in paths_str for k in ("infrastructure/", "repositories/"))
        has_app = any(
            k in paths_str for k in ("application/", "use_cases/", "services/")
        )

        if has_domain and has_infra and has_app:
            if "adapters/" in paths_str or "ports/" in paths_str:
                return "Hexagonal Architecture", 0.95
            elif "use_cases/" in paths_str or "entities/" in paths_str:
                return "Clean Architecture", 0.90
            return "Onion Architecture", 0.85

        if "commands/" in paths_str and "queries/" in paths_str:
            return "CQRS Architecture", 0.85

        if "features/" in paths_str or "modules/" in paths_str:
            return "Feature-Based Architecture", 0.85

        if (
            "controllers/" in paths_str
            and ("views/" in paths_str or "templates/" in paths_str)
            and "models/" in paths_str
        ):
            return "MVC Architecture", 0.90

        if len(layer_names) >= 3:
            return "Layered Architecture", 0.85

        if "docker-compose" in paths_str and (
            "services/" in paths_str or "microservices/" in paths_str
        ):
            return "Microservices", 0.75

        return "Monolith", 0.80
