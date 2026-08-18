"""CORTEX Repository Grading Engine orchestrator."""

from typing import Any

from app.analyzers.grading.models import (
    CategoryScores,
    RepositoryGradeReportDTO,
)
from app.analyzers.grading.scorers.benchmarker import Benchmarker
from app.analyzers.grading.scorers.grade_calculator import GradeCalculator
from app.analyzers.grading.scorers.maturity_classifier import MaturityClassifier
from app.analyzers.grading.scorers.strengths_weaknesses_analyzer import (
    StrengthsWeaknessesAnalyzer,
)
from app.analyzers.grading.scorers.technical_debt_calculator import TechnicalDebtCalculator
from app.core.ai.factory import AIProviderFactory
from app.core.ai.prompts.templates import (
    EXECUTIVE_SUMMARY_TEMPLATE,
    SYSTEM_PROMPT,
    TECHNICAL_SUMMARY_TEMPLATE,
)


class RepositoryGradingEngine:
    """Main CORTEX Repository Grading Engine orchestrator combining database metrics, scoring models, and AI prompts."""

    @classmethod
    def run(  # noqa: C901
        cls,
        repo_name: str,
        static_metrics: Any | None = None,
        arch_analysis: Any | None = None,
        sec_analysis: Any | None = None,
        maint_metrics: Any | None = None,
        doc_analysis: Any | None = None,
        test_analysis: Any | None = None,
        ci_analysis: Any | None = None,
        git_history: Any | None = None,
        community_analysis: Any | None = None,
        provider_type: str = "mock",
    ) -> RepositoryGradeReportDTO:
        """Execute Repository Grade calculation and narrative prompt generation."""
        # 1. Extract 5 Consolidated Category Scores
        static_score = static_metrics.maintainability_index if static_metrics else 50.0
        arch_score = arch_analysis.architecture_score if arch_analysis else 50.0

        if sec_analysis:
            sec_score = max(
                100.0
                - (sec_analysis.critical_count * 25.0 + sec_analysis.high_count * 10.0),
                0.0,
            )
        else:
            sec_score = 50.0

        doc_score = maint_metrics.documentation_score if maint_metrics else 50.0
        test_score = maint_metrics.testing_score if maint_metrics else 50.0
        ci_score = maint_metrics.ci_score if maint_metrics else 50.0
        git_score = git_history.development_velocity_score if git_history else 50.0
        comm_score = maint_metrics.community_score if maint_metrics else 50.0

        maintainability_cat_score = round(
            (doc_score * 0.35) + (test_score * 0.45) + (ci_score * 0.20), 1
        )
        community_cat_score = round((git_score * 0.50) + (comm_score * 0.50), 1)

        categories = CategoryScores(
            security_score=sec_score,
            architecture_score=arch_score,
            code_quality_score=static_score,
            maintainability_score=maintainability_cat_score,
            community_velocity_score=community_cat_score,
        )

        # 2. Compute Overall Score, Letter Grade, and Security Guardrail Caps
        overall_score, overall_grade, is_capped, cap_reason = (
            GradeCalculator.calculate_grade(categories)
        )

        # 3. Compute Maturity Classification
        has_ci = bool(ci_analysis and len(getattr(ci_analysis, "providers", [])) > 0)
        maturity = MaturityClassifier.classify(categories, has_ci=has_ci)

        # 4. Technical Debt Estimation
        smells_count = (
            len(getattr(static_metrics, "smells", [])) if static_metrics else 0
        )
        sec_secrets = getattr(sec_analysis, "secret_count", 0) if sec_analysis else 0
        dep_vulns = (
            getattr(sec_analysis, "dependency_vuln_count", 0) if sec_analysis else 0
        )
        cfg_issues = (
            getattr(sec_analysis, "config_issues_count", 0) if sec_analysis else 0
        )
        arch_violations = (
            len(getattr(arch_analysis, "violations", [])) if arch_analysis else 0
        )

        debt = TechnicalDebtCalculator.calculate(
            code_smells_count=smells_count,
            security_secrets_count=sec_secrets,
            dependency_vulns_count=dep_vulns,
            config_issues_count=cfg_issues,
            architecture_violations_count=arch_violations,
            testing_score=test_score,
            documentation_score=doc_score,
        )

        # 5. Benchmarking & Percentiles
        benchmark = Benchmarker.calculate_percentiles(overall_score, categories)

        # 6. Strengths & Weaknesses
        insights = StrengthsWeaknessesAnalyzer.analyze(
            subsystems=categories,
            has_secrets=sec_secrets > 0,
            has_vulns=dep_vulns > 0,
            has_ci=has_ci,
        )

        # 7. AI Persona Summaries & Narrative Generation
        ai_provider = AIProviderFactory.get_provider(provider_type)

        top_strength = insights.strengths[0] if insights.strengths else "Clean modular structure"
        top_risk = insights.weaknesses[0] if insights.weaknesses else "Routine maintenance debt"

        narrative = (
            f"{repo_name} is a software project demonstrating a Grade {overall_grade} ({overall_score}/100) engineering posture. "
            f"Its primary architectural strength is {top_strength.lower()}. "
            f"The main operational risk is {top_risk.lower()}. "
            f"It is a strong fit for teams requiring structured standards, but requires attention prior to enterprise deployment."
        )

        exec_prompt = EXECUTIVE_SUMMARY_TEMPLATE.format(
            repo_name=repo_name,
            static_score=static_score,
            arch_score=arch_score,
            security_score=sec_score,
            doc_score=doc_score,
            test_score=test_score,
            ci_score=ci_score,
            health_score=community_cat_score,
            community_score=comm_score,
            overall_iq=overall_score,
            maturity_level=maturity.level,
            critical_secrets=sec_secrets,
            critical_vulns=dep_vulns,
            smells_count=smells_count,
            avg_complexity=(
                getattr(static_metrics, "average_cyclomatic_complexity", 1.0)
                if static_metrics
                else 1.0
            ),
            debt_hours=debt.total_hours,
            debt_days=debt.total_days,
        )
        exec_summary = ai_provider.generate(exec_prompt, SYSTEM_PROMPT)

        tech_prompt = TECHNICAL_SUMMARY_TEMPLATE.format(
            repo_name=repo_name,
            arch_style=(
                getattr(arch_analysis, "architecture_style", "Layered Architecture")
                if arch_analysis
                else "Layered Architecture"
            ),
            arch_confidence=(
                getattr(arch_analysis, "confidence_score", 0.85)
                if arch_analysis
                else 0.85
            ),
            frameworks=(
                getattr(arch_analysis, "frameworks", []) if arch_analysis else []
            ),
            languages=(
                getattr(arch_analysis, "languages", ["Python"])
                if arch_analysis
                else ["Python"]
            ),
            maintainability_index=static_score,
            duplication_pct=(
                getattr(static_metrics, "duplication_percentage", 0.0)
                if static_metrics
                else 0.0
            ),
            conventional_commits_pct=(
                getattr(git_history, "conventional_commits_percentage", 0.0)
                if git_history
                else 0.0
            ),
            test_frameworks=(
                getattr(test_analysis, "frameworks", []) if test_analysis else []
            ),
            test_file_count=(
                getattr(test_analysis, "test_file_count", 0) if test_analysis else 0
            ),
        )
        tech_summary = ai_provider.generate(tech_prompt, SYSTEM_PROMPT)

        return RepositoryGradeReportDTO(
            overall_score=overall_score,
            overall_grade=overall_grade,
            capped=is_capped,
            cap_reason=cap_reason,
            category_scores=categories,
            maturity=maturity,
            debt=debt,
            insights=insights,
            benchmark=benchmark,
            narrative_summary=narrative,
            executive_summary=exec_summary,
            technical_summary=tech_summary,
            architecture_summary=f"Architecture Style: {getattr(arch_analysis, 'architecture_style', 'Modular')}. Modularity: {arch_score}/100.",
            security_summary=f"Security Posture: {sec_score}/100. Critical Secrets: {sec_secrets}, Vulnerabilities: {dep_vulns}.",
            maintainability_summary=f"Maintainability Index: {static_score}/100. Testing Score: {test_score}/100.",
            recruiter_summary=f"Engineering Maturity: {maturity.level}. Grade: {overall_grade} ({overall_score}/100).",
            engineering_manager_summary=f"Total Technical Debt: {debt.total_hours}h ({debt.total_days} days). Key Focus: {debt.items[0].description if debt.items else 'Routine maintenance'}.",
        )


# Backward compatibility class alias
RepositoryIQEngine = RepositoryGradingEngine
