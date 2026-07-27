"""Tests for GitService cloning abstraction."""

from unittest.mock import MagicMock, patch

import git
import pytest

from app.exceptions.custom_exceptions import GitCloneError
from app.services.git_service import GitService


def test_clone_repository_success(tmp_path: any) -> None:
    """Test GitService.clone_repository calls git.Repo.clone_from."""
    target_dir = str(tmp_path / "test_repo")

    mock_repo = MagicMock()
    mock_repo.bare = False

    with patch("git.Repo.clone_from", return_value=mock_repo) as mock_clone:
        result = GitService.clone_repository(
            clone_url="https://github.com/owner/repo.git",
            target_path=target_dir,
            branch="main",
        )

        mock_clone.assert_called_once()
        assert (
            "repo.git" in mock_clone.call_args.kwargs["url"]
            or mock_clone.call_args.kwargs.get("url")
            == "https://github.com/owner/repo.git"
        )
        assert result.endswith("test_repo")


def test_clone_repository_failure(tmp_path: any) -> None:
    """Test GitService.clone_repository handles GitCommandError properly."""
    target_dir = str(tmp_path / "failed_repo")

    with patch(
        "git.Repo.clone_from",
        side_effect=git.GitCommandError("clone", "Authentication failed"),
    ):
        with pytest.raises(GitCloneError):
            GitService.clone_repository(
                clone_url="https://github.com/owner/private.git",
                target_path=target_dir,
            )
