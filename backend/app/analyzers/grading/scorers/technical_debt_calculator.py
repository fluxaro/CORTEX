"""Technical Debt estimation and category breakdown calculator."""

from app.analyzers.grading.models import TechnicalDebtItem, TechnicalDebtResult


class TechnicalDebtCalculator:
    """Estimates technical debt hours, days, and categories by referencing stored findings."""

    @classmethod
    def calculate(  # noqa: C901
        cls,
        code_smells_count: int = 0,
        security_secrets_count: int = 0,
        dependency_vulns_count: int = 0,
        config_issues_count: int = 0,
        architecture_violations_count: int = 0,
        testing_score: float = 0.0,
        documentation_score: float = 0.0,
    ) -> TechnicalDebtResult:
        """Calculate technical debt hours and itemized categories."""
        items: list[TechnicalDebtItem] = []
        breakdown: dict[str, float] = {
            "Architecture": 0.0,
            "Security": 0.0,
            "Testing": 0.0,
            "Documentation": 0.0,
            "Maintainability": 0.0,
        }

        if architecture_violations_count > 0:
            hours = architecture_violations_count * 4.0
            breakdown["Architecture"] += hours
            items.append(
                TechnicalDebtItem(
                    category="Architecture",
                    description=f"{architecture_violations_count} architecture boundary violations detected.",
                    estimated_hours=hours,
                )
            )

        if security_secrets_count > 0:
            hours = security_secrets_count * 2.0
            breakdown["Security"] += hours
            items.append(
                TechnicalDebtItem(
                    category="Security",
                    description=f"{security_secrets_count} exposed secrets require remediation.",
                    estimated_hours=hours,
                )
            )

        if dependency_vulns_count > 0:
            hours = dependency_vulns_count * 3.0
            breakdown["Security"] += hours
            items.append(
                TechnicalDebtItem(
                    category="Security",
                    description=f"{dependency_vulns_count} dependency CVE vulnerabilities require upgrade.",
                    estimated_hours=hours,
                )
            )

        if code_smells_count > 0:
            hours = code_smells_count * 1.5
            breakdown["Maintainability"] += hours
            items.append(
                TechnicalDebtItem(
                    category="Maintainability",
                    description=f"{code_smells_count} code smells detected across functions/classes.",
                    estimated_hours=hours,
                )
            )

        if testing_score < 70.0:
            hours = round((70.0 - testing_score) * 0.2, 1)
            breakdown["Testing"] += hours
            items.append(
                TechnicalDebtItem(
                    category="Testing",
                    description="Test coverage below 70% threshold.",
                    estimated_hours=hours,
                )
            )

        total_hours = sum(breakdown.values())
        total_days = round(total_hours / 8.0, 1)

        return TechnicalDebtResult(
            total_hours=round(total_hours, 1),
            total_days=total_days,
            category_breakdown=breakdown,
            items=items,
        )
