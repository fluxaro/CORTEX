"""Custom application exceptions."""

from typing import Any


class ProjectIQError(Exception):
    """Base class for all ProjectIQ exceptions."""

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details


class InvalidGitHubURLError(ProjectIQError):
    """Raised when a provided GitHub URL is invalid or malformed."""

    def __init__(self, message: str = "Invalid GitHub repository URL.") -> None:
        super().__init__(message=message, status_code=400)


class RepositoryAlreadyExistsError(ProjectIQError):
    """Raised when attempting to add a repository that has already been ingested."""

    def __init__(self, full_name: str) -> None:
        super().__init__(
            message=f"Repository '{full_name}' has already been added.",
            status_code=409,
        )


class RepositoryNotFoundError(ProjectIQError):
    """Raised when a requested repository is not found."""

    def __init__(self, identifier: str) -> None:
        super().__init__(
            message=f"Repository '{identifier}' was not found.",
            status_code=404,
        )


class GitHubAPIError(ProjectIQError):
    """Raised when an error occurs during GitHub API communication."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message=message, status_code=status_code)


class GitCloneError(ProjectIQError):
    """Raised when a Git clone operation fails."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=500)
