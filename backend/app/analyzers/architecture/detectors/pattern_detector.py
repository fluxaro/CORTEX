"""Design pattern detector."""

import re

from app.analyzers.architecture.models import DetectedPatternResult
from app.analyzers.shared.models import FileAnalysisResult


class PatternDetector:
    """Detects Creational, Structural, Behavioral, and Architectural design patterns."""

    PATTERN_RULES = [
        (
            "Repository Pattern",
            "Architectural",
            r"(?i)\b\w+Repository\b",
            "Encapsulates data access and persistence logic",
        ),
        (
            "Factory Pattern",
            "Creational",
            r"(?i)\b\w+Factory\b|\bcreate_\w+\b",
            "Creates objects without specifying exact class",
        ),
        (
            "Singleton Pattern",
            "Creational",
            r"(?i)\b_instance\b|\bgetInstance\b",
            "Ensures a class has only one instance",
        ),
        (
            "Builder Pattern",
            "Creational",
            r"(?i)\b\w+Builder\b",
            "Separates construction of complex objects",
        ),
        (
            "Strategy Pattern",
            "Behavioral",
            r"(?i)\b\w+Strategy\b",
            "Enables selecting algorithms at runtime",
        ),
        (
            "Observer Pattern",
            "Behavioral",
            r"(?i)\b(subscribe|unsubscribe|notify|Listener|Observer)\b",
            "Defines one-to-many event notification dependency",
        ),
        (
            "Decorator Pattern",
            "Structural",
            r"(?i)@\w+\b|\b\w+Decorator\b",
            "Attaches additional responsibilities dynamically",
        ),
        (
            "Facade Pattern",
            "Structural",
            r"(?i)\b\w+Facade\b",
            "Provides simplified interface to complex subsystem",
        ),
        (
            "Adapter Pattern",
            "Structural",
            r"(?i)\b\w+Adapter\b",
            "Converts interface of a class into another expected interface",
        ),
        (
            "Proxy Pattern",
            "Structural",
            r"(?i)\b\w+Proxy\b",
            "Provides surrogate or placeholder to control access",
        ),
        (
            "Dependency Injection",
            "Architectural",
            r"(?i)(Depends\(|@Inject|@Autowired|\b__init__\(.*self,.*\b\w+:\s*([A-Z]\w+))",
            "Injects object dependencies into consumers",
        ),
        (
            "Command Pattern",
            "Behavioral",
            r"(?i)\b\w+Command\b",
            "Encapsulates a request as an object",
        ),
        (
            "State Pattern",
            "Behavioral",
            r"(?i)\b\w+State\b",
            "Allows object to alter behavior when internal state changes",
        ),
        (
            "Chain of Responsibility",
            "Behavioral",
            r"(?i)\bset_next\b|\bHandler\b",
            "Passes request along chain of handlers",
        ),
        (
            "Template Method",
            "Behavioral",
            r"(?i)\b\w+Template\b",
            "Defines algorithm skeleton in method",
        ),
        (
            "Specification Pattern",
            "Behavioral",
            r"(?i)\b\w+Specification\b|\bis_satisfied_by\b",
            "Recombines business rules using boolean logic",
        ),
        (
            "Unit of Work",
            "Architectural",
            r"(?i)\bUnitOfWork\b|\bcommit\(\)\b",
            "Maintains list of business transaction changes",
        ),
        (
            "DTO",
            "Architectural",
            r"(?i)\b\w+DTO\b|\b\w+Schema\b|\b\w+Request\b|\b\w+Response\b",
            "Transfers data between software subsystems",
        ),
        (
            "Mapper",
            "Architectural",
            r"(?i)\b\w+Mapper\b|\bmap_to_\w+\b",
            "Maps data between disparate object schemas",
        ),
        (
            "Service Locator",
            "Architectural",
            r"(?i)\bServiceLocator\b|\bget_service\b",
            "Encapsulates service resolution logic",
        ),
    ]

    @classmethod
    def detect_patterns(
        cls, file_results: list[FileAnalysisResult]
    ) -> list[DetectedPatternResult]:
        """Inspect file analysis results and identify design patterns."""
        patterns: list[DetectedPatternResult] = []
        seen: set[tuple[str, str]] = set()

        for file_res in file_results:
            content_repr = f"{file_res.path}\n" + "\n".join(
                [c.name for c in file_res.classes]
                + [f.name for f in file_res.functions]
            )

            for pattern_name, category, regex_pat, desc in cls.PATTERN_RULES:
                match = re.search(regex_pat, content_repr)
                if match:
                    key = (pattern_name, file_res.path)
                    if key not in seen:
                        seen.add(key)
                        confidence = (
                            0.9
                            if pattern_name
                            in ("Repository Pattern", "DTO", "Dependency Injection")
                            else 0.75
                        )
                        patterns.append(
                            DetectedPatternResult(
                                pattern_name=pattern_name,
                                category=category,
                                confidence_score=confidence,
                                location=file_res.path,
                                description=desc,
                            )
                        )

        return patterns
