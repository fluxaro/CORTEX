"""Package metadata quality and completeness analyzer."""

import json

from app.analyzers.maintainability.models import PackageQualityResult


class PackageQualityAnalyzer:
    """Inspects package manifest metadata (package.json, pyproject.toml, Cargo.toml) for missing fields."""

    @classmethod
    def analyze(cls, file_contents: dict[str, str]) -> PackageQualityResult:
        """Analyze manifest completeness."""
        missing = []
        has_manifest = False

        for path, content in file_contents.items():
            path_lower = path.lower()
            if path_lower.endswith("package.json"):
                has_manifest = True
                try:
                    data = json.loads(content)
                    for key in (
                        "description",
                        "repository",
                        "keywords",
                        "author",
                        "version",
                        "homepage",
                    ):
                        if key not in data or not data[key]:
                            missing.append(key)
                except Exception:
                    pass
                break
            elif path_lower.endswith("pyproject.toml") or path_lower.endswith(
                "cargo.toml"
            ):
                has_manifest = True
                for key in (
                    "description",
                    "repository",
                    "keywords",
                    "authors",
                    "version",
                    "homepage",
                ):
                    if f"{key} =" not in content.lower():
                        missing.append(key)
                break

        return PackageQualityResult(
            missing_metadata=list(set(missing)),
            has_package_manifest=has_manifest,
        )
