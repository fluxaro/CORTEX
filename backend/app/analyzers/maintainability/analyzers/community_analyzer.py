"""Community standards and governance analyzer."""

from app.analyzers.maintainability.models import CommunityResult


class CommunityAnalyzer:
    """Scans community files, security policies, and issue templates."""

    @classmethod
    def analyze(cls, file_paths: list[str]) -> CommunityResult:
        """Analyze open source community readiness."""
        paths_lower = [p.lower() for p in file_paths]

        has_contrib = any("contributing" in p for p in paths_lower)
        has_coc = any("code_of_conduct" in p for p in paths_lower)
        has_sec = any("security" in p for p in paths_lower)
        has_issue_tmpl = any("issue_template" in p for p in paths_lower)
        has_pr_tmpl = any("pull_request_template" in p for p in paths_lower)
        has_disc = any("discussion" in p for p in paths_lower)

        # Community score calculation (0-100)
        score = 0.0
        if has_contrib:
            score += 25.0
        if has_coc:
            score += 20.0
        if has_sec:
            score += 20.0
        if has_issue_tmpl:
            score += 15.0
        if has_pr_tmpl:
            score += 15.0
        if has_disc:
            score += 5.0

        return CommunityResult(
            community_score=round(min(score, 100.0), 1),
            has_contributing=has_contrib,
            has_code_of_conduct=has_coc,
            has_security_policy=has_sec,
            has_issue_templates=has_issue_tmpl,
            has_pr_templates=has_pr_tmpl,
            has_discussions=has_disc,
        )
