"""Tests for Prompt Template Engine."""

from app.core.ai.prompts.templates import EXECUTIVE_SUMMARY_TEMPLATE, SYSTEM_PROMPT


def test_prompt_template_rendering() -> None:
    """Test formatting prompt template with context variables."""
    rendered = EXECUTIVE_SUMMARY_TEMPLATE.format(
        repo_name="ProjectIQ",
        static_score=85.0,
        arch_score=90.0,
        security_score=80.0,
        doc_score=75.0,
        test_score=80.0,
        ci_score=100.0,
        health_score=85.0,
        community_score=90.0,
        overall_iq=83.5,
        maturity_level="Enterprise Ready",
        critical_secrets=0,
        critical_vulns=0,
        smells_count=2,
        avg_complexity=2.5,
        debt_hours=12.0,
        debt_days=1.5,
    )

    assert "ProjectIQ" in rendered
    assert "83.5/100" in rendered
    assert "Enterprise Ready" in rendered
    assert "Lead Technical Architect" in SYSTEM_PROMPT
