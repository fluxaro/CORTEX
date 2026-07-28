"""Tests for Technical Debt calculator."""

from app.analyzers.iq.scorers.technical_debt_calculator import TechnicalDebtCalculator


def test_technical_debt_calculator() -> None:
    """Test estimating technical debt hours and category breakdown."""
    debt = TechnicalDebtCalculator.calculate(
        code_smells_count=5,
        security_secrets_count=2,
        dependency_vulns_count=1,
        config_issues_count=1,
        architecture_violations_count=2,
        testing_score=30.0,
        documentation_score=40.0,
    )

    assert debt.total_hours > 0.0
    assert debt.total_days > 0.0
    assert "Maintainability" in debt.category_breakdown
    assert "Security" in debt.category_breakdown
    assert len(debt.items) >= 4
