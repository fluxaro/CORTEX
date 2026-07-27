"""Git repository cloning service abstraction."""

import logging
import os
import shutil

import git

from app.exceptions.custom_exceptions import GitCloneError

logger = logging.getLogger(__name__)


class GitService:
    """Service for handling Git operations such as repository cloning."""

    @staticmethod
    def clone_repository(
        clone_url: str,
        target_path: str,
        branch: str | None = None,
        depth: int = 1,
    ) -> str:
        """Clone a remote git repository to target_path.

        If target_path already exists and contains a valid git repository, re-uses it.
        Returns absolute path to cloned repository.
        """
        abs_target_path = os.path.abspath(target_path)

        # Check if already cloned
        if os.path.exists(abs_target_path) and os.path.isdir(abs_target_path):
            try:
                repo = git.Repo(abs_target_path)
                if not repo.bare:
                    logger.info(
                        f"Repository already cloned at {abs_target_path}. Reusing existing clone."
                    )
                    return abs_target_path
            except git.InvalidGitRepositoryError:
                logger.warning(
                    f"Directory {abs_target_path} exists but is not a valid git repository. Re-cloning."
                )
                shutil.rmtree(abs_target_path, ignore_errors=True)

        os.makedirs(os.path.dirname(abs_target_path), exist_ok=True)

        try:
            logger.info(f"Cloning {clone_url} to {abs_target_path}...")
            if branch:
                git.Repo.clone_from(
                    url=clone_url,
                    to_path=abs_target_path,
                    branch=branch,
                    depth=depth,
                )
            else:
                git.Repo.clone_from(
                    url=clone_url,
                    to_path=abs_target_path,
                    depth=depth,
                )
            logger.info(f"Successfully cloned repository to {abs_target_path}")
            return abs_target_path
        except git.GitCommandError as exc:
            # Clean up partial directory if clone failed
            if os.path.exists(abs_target_path):
                shutil.rmtree(abs_target_path, ignore_errors=True)
            logger.error(f"Git command failed during clone: {exc}")
            raise GitCloneError(
                f"Failed to clone repository from {clone_url}: {exc.stderr or str(exc)}"
            ) from exc
        except Exception as exc:
            if os.path.exists(abs_target_path):
                shutil.rmtree(abs_target_path, ignore_errors=True)
            logger.error(f"Unexpected error during git clone: {exc}")
            raise GitCloneError(
                f"Unexpected error while cloning repository: {exc}"
            ) from exc
