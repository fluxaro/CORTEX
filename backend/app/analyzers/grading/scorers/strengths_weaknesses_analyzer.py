"""Strengths, weaknesses, and improvement recommendations analyzer."""

from typing import Any
from app.analyzers.grading.models import (
    RecommendationItem,
    StrengthsWeaknessesResult,
)


class StrengthsWeaknessesAnalyzer:
    """Identifies repository strengths, weaknesses, and prioritized improvement recommendations."""

    @classmethod
    def analyze(  # noqa: C901
        cls,
        subsystems: Any,
        has_secrets: bool = False,
        has_vulns: bool = False,
        has_ci: bool = False,
    ) -> StrengthsWeaknessesResult:
        """Extract strengths, weaknesses, and actionable recommendations."""
        strengths: list[str] = []
        weaknesses: list[str] = []
        recommendations: list[RecommendationItem] = []

        arch_score = getattr(subsystems, "architecture_score", 50.0)
        sec_score = getattr(subsystems, "security_score", 50.0)
        code_score = getattr(subsystems, "code_quality_score", getattr(subsystems, "static_analysis_score", 50.0))
        maint_score = getattr(subsystems, "maintainability_score", getattr(subsystems, "testing_score", 50.0))

        # Strengths
        if arch_score >= 70.0:
            strengths.append(
                "Well-structured architectural design with clear layer separation."
            )
        if sec_score >= 75.0 and not has_secrets:
            strengths.append(
                "Strong security posture with zero hardcoded API keys or high-entropy secrets."
            )
        if code_score >= 70.0:
            strengths.append(
                "High maintainability index with low function cyclomatic complexity."
            )
        if maint_score >= 70.0:
            strengths.append(
                "Robust test suite and documentation coverage."
            )

        if not strengths:
            strengths.append("Modular code structure and clean source directory organization.")

        # Weaknesses
        if has_secrets:
            weaknesses.append("Detected exposed hardcoded secrets or API tokens in source code.")
            recommendations.append(
                RecommendationItem(
                    category="Security",
                    title="Remediate Exposed Secrets",
                    description="Revoke exposed credentials immediately and migrate to environment variables.",
                    timeframe="Immediate",
                    priority="Critical",
                    difficulty="Easy",
                    estimated_hours=2.0,
                )
            )

        if has_vulns:
            weaknesses.append("Package dependencies contain known CVE vulnerabilities.")
            recommendations.append(
                RecommendationItem(
                    category="Security",
                    title="Update Vulnerable Dependencies",
                    description="Upgrade third-party packages to safe, patched versions.",
                    timeframe="Short-term",
                    priority="High",
                    difficulty="Medium",
                    estimated_hours=4.0,
                )
            )

        if maint_score < 50.0:
            weaknesses.append("Low testing maturity or documentation coverage.")
            recommendations.append(
                RecommendationItem(
                    category="Testing",
                    title="Increase Automated Test Coverage",
                    description="Add unit and integration tests covering critical execution paths.",
                    timeframe="Medium-term",
                    priority="High",
                    difficulty="Medium",
                    estimated_hours=12.0,
                )
            )

        if not weaknesses:
            weaknesses.append("Minor maintenance and dependency documentation polish required.")

        return StrengthsWeaknessesResult(
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
        )
