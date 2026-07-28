"""Strengths, weaknesses, and improvement recommendations analyzer."""

from app.analyzers.iq.models import (
    RecommendationItem,
    StrengthsWeaknessesResult,
    SubsystemScores,
)


class StrengthsWeaknessesAnalyzer:
    """Identifies repository strengths, weaknesses, and prioritized improvement recommendations."""

    @classmethod
    def analyze(  # noqa: C901
        cls,
        subsystems: SubsystemScores,
        has_secrets: bool = False,
        has_vulns: bool = False,
        has_ci: bool = False,
    ) -> StrengthsWeaknessesResult:
        """Extract strengths, weaknesses, and actionable recommendations."""
        strengths: list[str] = []
        weaknesses: list[str] = []
        recommendations: list[RecommendationItem] = []

        # Strengths
        if subsystems.architecture_score >= 70.0:
            strengths.append(
                "Well-structured architectural design with clear layer separation."
            )
        if subsystems.testing_score >= 60.0:
            strengths.append(
                "Strong testing maturity with established test runner setup."
            )
        if subsystems.documentation_score >= 60.0:
            strengths.append("Comprehensive README and documentation coverage.")
        if subsystems.security_score >= 75.0 and not has_secrets:
            strengths.append(
                "Secure coding practices with no committed secrets detected."
            )
        if subsystems.ci_score >= 50.0:
            strengths.append(
                "CI/CD automation pipelines configured for testing and build verification."
            )

        # Weaknesses
        if has_secrets or subsystems.security_score < 60.0:
            weaknesses.append(
                "Security risk: exposed secrets or unhandled static security vulnerabilities."
            )
        if has_vulns:
            weaknesses.append(
                "Dependency risk: vulnerable third-party package dependencies detected."
            )
        if subsystems.testing_score < 40.0:
            weaknesses.append(
                "Testing gap: insufficient test coverage and test suite maturity."
            )
        if subsystems.documentation_score < 40.0:
            weaknesses.append(
                "Documentation gap: missing key README sections or developer onboarding guides."
            )
        if not has_ci:
            weaknesses.append(
                "CI/CD gap: automated testing and linting pipelines missing."
            )

        # Recommendations
        if has_secrets:
            recommendations.append(
                RecommendationItem(
                    category="Security",
                    title="Remediate Exposed Hardcoded Credentials",
                    description="Revoke committed API keys/tokens and migrate configuration to environment secrets.",
                    timeframe="Immediate",
                    priority="Critical",
                    difficulty="Easy",
                    estimated_hours=4.0,
                )
            )

        if has_vulns:
            recommendations.append(
                RecommendationItem(
                    category="Security",
                    title="Upgrade Vulnerable Third-Party Dependencies",
                    description="Update vulnerable packages in manifest files to patched non-vulnerable versions.",
                    timeframe="Short-term",
                    priority="High",
                    difficulty="Medium",
                    estimated_hours=8.0,
                )
            )

        if subsystems.testing_score < 50.0:
            recommendations.append(
                RecommendationItem(
                    category="Testing",
                    title="Implement Automated Test Suite",
                    description="Add unit tests and integration testing for key business logic modules.",
                    timeframe="Short-term",
                    priority="High",
                    difficulty="Medium",
                    estimated_hours=16.0,
                )
            )

        if subsystems.documentation_score < 50.0:
            recommendations.append(
                RecommendationItem(
                    category="Documentation",
                    title="Complete README & Developer Onboarding Docs",
                    description="Add Quick Start, Installation, Architecture overview, and API references to README.",
                    timeframe="Medium-term",
                    priority="Medium",
                    difficulty="Easy",
                    estimated_hours=8.0,
                )
            )

        if not has_ci:
            recommendations.append(
                RecommendationItem(
                    category="CI/CD",
                    title="Setup Continuous Integration Pipeline",
                    description="Configure GitHub Actions or equivalent CI workflow for automated testing and linting on push.",
                    timeframe="Medium-term",
                    priority="Medium",
                    difficulty="Medium",
                    estimated_hours=6.0,
                )
            )

        return StrengthsWeaknessesResult(
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
        )
