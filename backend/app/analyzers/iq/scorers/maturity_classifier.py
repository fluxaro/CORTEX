"""Engineering Maturity Model classifier."""

from app.analyzers.iq.models import MaturityClassification, SubsystemScores


class MaturityClassifier:
    """Classifies software repositories into engineering maturity levels."""

    @classmethod
    def classify(
        cls, subsystems: SubsystemScores, has_ci: bool = False, has_license: bool = True
    ) -> MaturityClassification:
        """Classify repository based on subsystem metrics."""
        reasons = []

        score = (
            subsystems.static_analysis_score * 0.2
            + subsystems.security_score * 0.3
            + subsystems.testing_score * 0.25
            + subsystems.documentation_score * 0.15
            + subsystems.ci_score * 0.1
        )

        if score >= 80.0 and has_ci and subsystems.security_score >= 75.0:
            reasons.append(
                "High security posture, strong test suite, and CI/CD automation configured."
            )
            return MaturityClassification(level="Enterprise Ready", reasons=reasons)

        if score >= 70.0 and (has_ci or subsystems.testing_score >= 50.0):
            reasons.append(
                "Solid maintainability, testing suite present, and documentation in place."
            )
            return MaturityClassification(level="Production Ready", reasons=reasons)

        if (
            subsystems.community_score >= 60.0
            and has_license
            and subsystems.documentation_score >= 50.0
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
