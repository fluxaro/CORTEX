"""Engineering Maturity Model classifier."""

from typing import Any
from app.analyzers.grading.models import CategoryScores, MaturityClassification, SubsystemScores


class MaturityClassifier:
    """Classifies software repositories into engineering maturity levels."""

    @classmethod
    def classify(
        cls, subsystems: Any, has_ci: bool = False, has_license: bool = True
    ) -> MaturityClassification:
        """Classify repository based on category metrics."""
        reasons = []

        sec_score = getattr(subsystems, "security_score", 50.0)
        code_score = getattr(subsystems, "code_quality_score", getattr(subsystems, "static_analysis_score", 50.0))
        maint_score = getattr(subsystems, "maintainability_score", getattr(subsystems, "testing_score", 50.0))

        score = (sec_score * 0.40) + (code_score * 0.30) + (maint_score * 0.30)

        if score >= 80.0 and has_ci and sec_score >= 75.0:
            reasons.append(
                "High security posture, strong test suite, and CI/CD automation configured."
            )
            return MaturityClassification(level="Enterprise Ready", reasons=reasons)

        if score >= 70.0 and (has_ci or maint_score >= 50.0):
            reasons.append(
                "Solid maintainability, testing suite present, and documentation in place."
            )
            return MaturityClassification(level="Production Ready", reasons=reasons)

        if (
            score >= 60.0
            and has_license
        ):
            reasons.append(
                "Well-documented open source standards, community files, and clear licensing."
            )
            return MaturityClassification(level="Open Source Mature", reasons=reasons)

        if score >= 45.0:
            reasons.append(
                "Active development structure with baseline documentation and testing."
            )
            return MaturityClassification(level="Personal Project", reasons=reasons)

        if score >= 25.0:
            reasons.append(
                "Initial code structure present but missing tests, CI/CD, and security controls."
            )
            return MaturityClassification(level="Learning Project", reasons=reasons)

        reasons.append(
            "Early stage prototype codebase with minimal testing and infrastructure."
        )
        return MaturityClassification(level="Prototype", reasons=reasons)
