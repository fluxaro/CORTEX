"""README section and completeness analyzer."""

import re

from app.analyzers.maintainability.models import ReadmeResult


class ReadmeAnalyzer:
    """Analyzes README file structure, standard engineering sections, and quality badges."""

    SECTION_PATTERNS = [
        ("Title", r"^#\s+.+"),
        ("Description", r"(?i)#+\s*(about|description|overview|introduction)\b"),
        ("Installation", r"(?i)#+\s*(installation|install|getting started|setup)\b"),
        ("Quick Start", r"(?i)#+\s*(quick\s*start|quickstart)\b"),
        ("Usage", r"(?i)#+\s*(usage|how to use|running)\b"),
        ("Configuration", r"(?i)#+\s*(configuration|config|settings)\b"),
        ("Environment Variables", r"(?i)#+\s*(environment|env vars|variables)\b"),
        ("Examples", r"(?i)#+\s*(examples|demo|sample)\b"),
        ("Screenshots", r"(?i)#+\s*(screenshots|preview|ui)\b"),
        ("Architecture", r"(?i)#+\s*(architecture|design|design patterns)\b"),
        ("Features", r"(?i)#+\s*(features|key features|capabilities)\b"),
        ("API Documentation", r"(?i)#+\s*(api|endpoints|api documentation|routes)\b"),
        ("Contributing", r"(?i)#+\s*(contributing|contribution|development)\b"),
        ("License", r"(?i)#+\s*(license|licence)\b"),
        ("FAQ", r"(?i)#+\s*(faq|frequently asked questions)\b"),
        ("Badges", r"(?i)(shields\.io|badge|build status|codecov)\b"),
        ("Roadmap", r"(?i)#+\s*(roadmap|future work)\b"),
        ("Changelog Reference", r"(?i)#+\s*(changelog|release notes)\b"),
        ("Contact Information", r"(?i)#+\s*(contact|author|support)\b"),
    ]

    @classmethod
    def analyze(cls, file_contents: dict[str, str]) -> ReadmeResult:
        """Analyze README markdown content."""
        readme_content = ""
        for path, content in file_contents.items():
            if path.lower().startswith("readme"):
                readme_content = content
                break

        if not readme_content:
            all_sections = [s[0] for s in cls.SECTION_PATTERNS]
            return ReadmeResult(
                completeness_percentage=0.0,
                detected_sections=[],
                missing_sections=all_sections,
                has_badges=False,
                has_screenshots=False,
            )

        detected = []
        missing = []

        for name, pattern in cls.SECTION_PATTERNS:
            if re.search(pattern, readme_content, re.MULTILINE):
                detected.append(name)
            else:
                missing.append(name)

        has_badges = bool(
            re.search(r"shields\.io|badge|img\.shields", readme_content, re.IGNORECASE)
        )
        has_screenshots = bool(
            re.search(
                r"!\[.*\]\(.*\.(png|jpg|jpeg|gif|svg)\)|<img\s+src=",
                readme_content,
                re.IGNORECASE,
            )
        )

        total_sections = len(cls.SECTION_PATTERNS)
        completeness = round((len(detected) / total_sections) * 100.0, 1)

        return ReadmeResult(
            completeness_percentage=completeness,
            detected_sections=detected,
            missing_sections=missing,
            has_badges=has_badges,
            has_screenshots=has_screenshots,
        )
