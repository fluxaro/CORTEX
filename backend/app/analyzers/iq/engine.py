"""Repository IQ Engine orchestrator."""

from typing import Any

from app.analyzers.iq.models import (
    RepositoryIQResult,
    SubsystemScores,
)
from app.analyzers.iq.scorers.benchmarker import Benchmarker
from app.analyzers.iq.scorers.iq_scorer import IQScorer
from app.analyzers.iq.scorers.maturity_classifier import MaturityClassifier
from app.analyzers.iq.scorers.strengths_weaknesses_analyzer import (
    StrengthsWeaknessesAnalyzer,
)
from app.analyzers.iq.scorers.technical_debt_calculator import TechnicalDebtCalculator
from app.core.ai.factory import AIProviderFactory
from app.core.ai.prompts.templates import (
    EXECUTIVE_SUMMARY_TEMPLATE,
    SYSTEM_PROMPT,
    TECHNICAL_SUMMARY_TEMPLATE,
)


class RepositoryIQEngine:
    """Main Repository IQ Engine orchestrator combining database metrics, scoring models, and AI prompts."""

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
    ) -> RepositoryIQResult:
        """Execute Repository IQ calculation and AI prompt generation."""
        # 1. Extract Subsystem Scores
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
        health_score = maint_metrics.repository_health_score if maint_metrics else 50.0
        comm_score = maint_metrics.community_score if maint_metrics else 50.0

        subsystems = SubsystemScores(
            static_analysis_score=static_score,
            architecture_score=arch_score,
            security_score=sec_score,
            documentation_score=doc_score,
            testing_score=test_score,
            ci_score=ci_score,
            git_practices_score=git_score,
            repository_health_score=health_score,
            community_score=comm_score,
        )

        # 2. Compute Overall Repository IQ Score
        overall_score = IQScorer.calculate_score(subsystems)

        # 3. Compute Maturity Classification
        has_ci = bool(ci_analysis and len(getattr(ci_analysis, "providers", [])) > 0)
        maturity = MaturityClassifier.classify(subsystems, has_ci=has_ci)

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
        benchmark = Benchmarker.calculate_percentiles(overall_score, subsystems)

        # 6. Strengths & Weaknesses
        insights = StrengthsWeaknessesAnalyzer.analyze(
            subsystems=subsystems,
            has_secrets=sec_secrets > 0,
            has_vulns=dep_vulns > 0,
            has_ci=has_ci,
        )

        # 7. AI Prompt Summaries (without scanning source code directly!)
        ai_provider = AIProviderFactory.get_provider(provider_type)

        exec_prompt = EXECUTIVE_SUMMARY_TEMPLATE.format(
            repo_name=repo_name,
            static_score=static_score,
            arch_score=arch_score,
            security_score=sec_score,
            doc_score=doc_score,
            test_score=test_score,
            ci_score=ci_score,
            health_score=health_score,
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

        return RepositoryIQResult(
            overall_score=overall_score,
            subsystem_scores=subsystems,
            maturity=maturity,
            debt=debt,
            insights=insights,
            benchmark=benchmark,
            executive_summary=exec_summary,
            technical_summary=tech_summary,
            architecture_summary=f"Architecture Style: {getattr(arch_analysis, 'architecture_style', 'Modular')}. Modularity: {arch_score}/100.",
            security_summary=f"Security Posture: {sec_score}/100. Critical Secrets: {sec_secrets}, Vulnerabilities: {dep_vulns}.",
            maintainability_summary=f"Maintainability Index: {static_score}/100. Testing Score: {test_score}/100.",
            recruiter_summary=f"Engineering Maturity: {maturity.level}. Repository IQ: {overall_score}/100.",
            engineering_manager_summary=f"Total Technical Debt: {debt.total_hours}h ({debt.total_days} days). Key Focus: {debt.items[0].description if debt.items else 'Routine maintenance'}.",
        )
