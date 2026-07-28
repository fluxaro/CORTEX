"""Tests for GitHistoryAnalyzer."""

from app.analyzers.maintainability.analyzers.git_history_analyzer import (
    GitHistoryAnalyzer,
)


def test_git_history_analyzer(tmp_path) -> None:
    """Test analyzing Git log history."""
    import git

    repo_dir = tmp_path / "test_repo"
    repo_dir.mkdir()
    repo = git.Repo.init(repo_dir)

    dummy_file = repo_dir / "README.md"
    dummy_file.write_text("# Test Repo\n", encoding="utf-8")
    repo.index.add(["README.md"])
    repo.index.commit("feat: initial commit")

    git_res, commit_res, rel_res = GitHistoryAnalyzer.analyze(str(repo_dir))

    assert git_res.commit_count >= 1
    assert commit_res.conventional_commits_percentage == 100.0
    assert commit_res.commit_quality_score >= 50.0
