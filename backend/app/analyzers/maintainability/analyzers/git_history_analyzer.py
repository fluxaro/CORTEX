"""Git history, commit quality, and release cadence analyzer."""

import re
from datetime import UTC, datetime

import git

from app.analyzers.maintainability.models import (
    CommitResult,
    GitHistoryResult,
    ReleaseResult,
)


class GitHistoryAnalyzer:
    """Analyzes Git history, contributor count, Conventional Commits, and release cadence using GitPython."""

    CONVENTIONAL_PREFIXES = (
        "feat:",
        "fix:",
        "docs:",
        "style:",
        "refactor:",
        "perf:",
        "test:",
        "build:",
        "ci:",
        "chore:",
        "revert:",
    )
    GENERIC_MESSAGES = {
        "fix",
        "update",
        "wip",
        "change",
        "temp",
        "test",
        "commit",
        "changes",
        "stuff",
        "add",
    }

    @classmethod
    def analyze(  # noqa: C901
        cls, target_path: str
    ) -> tuple[GitHistoryResult, CommitResult, ReleaseResult]:
        """Analyze repository Git log and release tags."""
        try:
            repo = git.Repo(target_path, search_parent_directories=True)
        except (git.InvalidGitRepositoryError, git.NoSuchPathError):
            return (
                GitHistoryResult(),
                CommitResult(commit_quality_score=50.0),
                ReleaseResult(),
            )

        commits = list(repo.iter_commits(max_count=500))
        if not commits:
            return (
                GitHistoryResult(),
                CommitResult(commit_quality_score=50.0),
                ReleaseResult(),
            )

        total_commits = len(commits)
        authors = {c.author.email for c in commits if c.author and c.author.email}
        contributor_count = len(authors)

        try:
            branch_count = len(list(repo.branches))
        except Exception:
            branch_count = 1

        try:
            tags = list(repo.tags)
            tag_count = len(tags)
        except Exception:
            tags = []
            tag_count = 0

        first_commit_time = datetime.fromtimestamp(commits[-1].committed_date, tz=UTC)
        latest_commit_time = datetime.fromtimestamp(commits[0].committed_date, tz=UTC)
        now_time = datetime.now(UTC)

        repo_age_days = max((now_time - first_commit_time).days, 1)
        weeks = max(repo_age_days / 7.0, 1.0)
        commits_per_week = round(total_commits / weeks, 2)

        # Inactive periods (> 30 days gap between adjacent commits)
        inactive_periods = 0
        for i in range(len(commits) - 1):
            t1 = datetime.fromtimestamp(commits[i].committed_date, tz=UTC)
            t2 = datetime.fromtimestamp(commits[i + 1].committed_date, tz=UTC)
            if (t1 - t2).days > 30:
                inactive_periods += 1

        # Commit Quality & Conventional Commits Analysis
        conventional_count = 0
        generic_count = 0
        types_breakdown: dict[str, int] = {}

        for c in commits:
            raw_msg = c.message
            msg_str = (
                raw_msg.decode("utf-8", errors="ignore")
                if isinstance(raw_msg, bytes)
                else str(raw_msg)
            )
            msg_lower = msg_str.strip().lower()

            if msg_lower.startswith(cls.CONVENTIONAL_PREFIXES):
                conventional_count += 1
                prefix = msg_lower.split(":", 1)[0]
                types_breakdown[prefix] = types_breakdown.get(prefix, 0) + 1

            if msg_lower in cls.GENERIC_MESSAGES or len(msg_lower) < 5:
                generic_count += 1

        conv_pct = round((conventional_count / total_commits) * 100.0, 1)
        gen_pct = round((generic_count / total_commits) * 100.0, 1)

        quality_score = 50.0 + (conv_pct * 0.4) - (gen_pct * 0.5)
        quality_score = round(max(min(quality_score, 100.0), 0.0), 1)

        # Velocity score (0-100)
        velocity_score = round(
            min((commits_per_week * 10.0) + (contributor_count * 5.0), 100.0), 1
        )

        git_res = GitHistoryResult(
            commit_count=total_commits,
            contributor_count=contributor_count,
            branch_count=branch_count,
            tag_count=tag_count,
            repo_age_days=repo_age_days,
            commits_per_week=commits_per_week,
            inactive_periods_count=inactive_periods,
            development_velocity_score=velocity_score,
        )

        commit_res = CommitResult(
            commit_quality_score=quality_score,
            conventional_commits_percentage=conv_pct,
            generic_commits_percentage=gen_pct,
            commit_types_breakdown=types_breakdown,
        )

        # Release Analysis
        days_since_latest = (now_time - latest_commit_time).days
        latest_tag_name = tags[-1].name if tags else None

        release_score = 0.0
        if tag_count > 0:
            release_score += min(tag_count * 10.0, 50.0)
        if days_since_latest < 30:
            release_score += 30.0
        elif days_since_latest < 90:
            release_score += 15.0

        release_res = ReleaseResult(
            release_score=round(min(release_score, 100.0), 1),
            release_count=tag_count,
            has_changelog=False,  # Updated by caller
            uses_semver=bool(
                latest_tag_name and re.match(r"^v?\d+\.\d+\.\d+", latest_tag_name)
            ),
            latest_release_tag=latest_tag_name,
            days_since_last_release=days_since_latest,
        )

        return git_res, commit_res, release_res
