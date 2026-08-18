"""Tests for Technical Debt calculator."""

from app.analyzers.grading.scorers.technical_debt_calculator import TechnicalDebtCalculator


def test_technical_debt_calculator() -> None:
    """Test calculating technical debt hours and breakdown."""
    res = TechnicalDebtCalculator.calculate(
        code_smells_count=4,
        security_secrets_count=1,
        dependency_vulns_count=2,
        config_issues_count=1,
        architecture_violations_count=1,
        testing_score=50.0,
        documentation_score=60.0,
    )
    assert res.total_hours > 0.0
    assert res.total_days > 0.0
    assert "Security" in res.category_breakdown
    assert len(res.items) >= 4
