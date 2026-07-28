"""Technical Debt estimation and category breakdown calculator."""

from app.analyzers.iq.models import TechnicalDebtItem, TechnicalDebtResult


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
            "Dependency": 0.0,
            "Configuration": 0.0,
        }

        # Maintainability Debt
        if code_smells_count > 0:
            hours = code_smells_count * 2.0
            breakdown["Maintainability"] += hours
            items.append(
                TechnicalDebtItem(
                    category="Maintainability",
                    description=f"Refactor {code_smells_count} code smells (long methods, god classes, deep nesting).",
                    estimated_hours=hours,
                )
            )

        # Security Debt
        if security_secrets_count > 0:
            hours = security_secrets_count * 4.0
            breakdown["Security"] += hours
            items.append(
                TechnicalDebtItem(
                    category="Security",
                    description=f"Revoke and migrate {security_secrets_count} hardcoded credentials to secret store.",
                    estimated_hours=hours,
                )
            )

        # Dependency Debt
        if dependency_vulns_count > 0:
            hours = dependency_vulns_count * 3.0
            breakdown["Dependency"] += hours
            items.append(
                TechnicalDebtItem(
                    category="Dependency",
                    description=f"Upgrade {dependency_vulns_count} vulnerable third-party dependencies.",
                    estimated_hours=hours,
                )
            )

        # Configuration Debt
        if config_issues_count > 0:
            hours = config_issues_count * 2.0
            breakdown["Configuration"] += hours
            items.append(
                TechnicalDebtItem(
                    category="Configuration",
                    description=f"Fix {config_issues_count} infrastructure configuration issues in Dockerfiles/env files.",
                    estimated_hours=hours,
                )
            )

        # Architecture Debt
        if architecture_violations_count > 0:
            hours = architecture_violations_count * 4.0
            breakdown["Architecture"] += hours
            items.append(
                TechnicalDebtItem(
                    category="Architecture",
                    description=f"Fix {architecture_violations_count} architectural layer violations and circular dependencies.",
                    estimated_hours=hours,
                )
            )

        # Testing Debt
        if testing_score < 50.0:
            hours = round((50.0 - testing_score) * 0.4, 1)
            breakdown["Testing"] += hours
            items.append(
                TechnicalDebtItem(
                    category="Testing",
                    description="Increase test suite coverage and implement missing unit/integration tests.",
                    estimated_hours=hours,
                )
            )

        # Documentation Debt
        if documentation_score < 50.0:
            hours = round((50.0 - documentation_score) * 0.2, 1)
            breakdown["Documentation"] += hours
            items.append(
                TechnicalDebtItem(
                    category="Documentation",
                    description="Improve README sections, API reference, and developer onboarding guides.",
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
