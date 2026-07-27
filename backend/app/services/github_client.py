"""GitHub REST API client abstraction."""

import re
from datetime import UTC, datetime
from typing import Any

import httpx

from app.core.config.settings import settings
from app.exceptions.custom_exceptions import GitHubAPIError, InvalidGitHubURLError


def _parse_date(val: Any) -> datetime | None:
    """Parse string or return datetime object in UTC."""
    if not val:
        return None
    if isinstance(val, datetime):
        return val
    if isinstance(val, str):
        cleaned = val.replace("Z", "+00:00")
        return datetime.fromisoformat(cleaned)
    return None


class GitHubClient:
    """Client for interacting with GitHub REST API."""

    GITHUB_URL_PATTERN = re.compile(
        r"^(?:https?://)?(?:www\.)?github\.com/([a-zA-Z0-9_.-]+)/([a-zA-Z0-9_.-]+?)(?:\.git)?/?$"
    )

    def __init__(
        self,
        token: str | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self.token = token or settings.GITHUB_TOKEN
        self.http_client = http_client

    @classmethod
    def parse_github_url(cls, url: str) -> tuple[str, str]:
        """Extract (owner, repo_name) from a GitHub URL string."""
        clean_url = url.strip()
        match = cls.GITHUB_URL_PATTERN.match(clean_url)
        if not match:
            raise InvalidGitHubURLError(
                f"'{url}' is not a valid GitHub repository URL."
            )
        owner, repo = match.groups()
        return owner, repo

    def _get_headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": f"{settings.APP_NAME}/{settings.APP_VERSION}",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def get_repository_metadata(self, owner: str, repo: str) -> dict[str, Any]:
        """Fetch repository metadata from GitHub REST API."""
        url = f"https://api.github.com/repos/{owner}/{repo}"
        headers = self._get_headers()

        async def _make_request(client: httpx.AsyncClient) -> httpx.Response:
            return await client.get(url, headers=headers, timeout=10.0)

        try:
            if self.http_client:
                response = await _make_request(self.http_client)
            else:
                async with httpx.AsyncClient() as client:
                    response = await _make_request(client)
        except httpx.TimeoutException as exc:
            raise GitHubAPIError("Timed out while connecting to GitHub API.") from exc
        except httpx.RequestError as exc:
            raise GitHubAPIError(
                f"Network error connecting to GitHub API: {exc}"
            ) from exc

        if response.status_code == 404:
            raise GitHubAPIError(
                f"Repository '{owner}/{repo}' was not found on GitHub.",
                status_code=404,
            )
        elif response.status_code in (401, 403):
            # Check rate limiting header
            remaining = response.headers.get("X-RateLimit-Remaining")
            if remaining == "0":
                raise GitHubAPIError(
                    "GitHub API rate limit exceeded. Please try again later or provide a GITHUB_TOKEN.",
                    status_code=429,
                )
            raise GitHubAPIError(
                f"Access denied to repository '{owner}/{repo}' (may be private or require authentication).",
                status_code=403,
            )
        elif response.status_code != 200:
            raise GitHubAPIError(
                f"GitHub API returned unexpected status {response.status_code}.",
                status_code=response.status_code,
            )

        data = response.json()

        # Reject private repositories
        if data.get("private", False) or data.get("visibility") == "private":
            raise InvalidGitHubURLError(
                f"Repository '{owner}/{repo}' is private. Only public repositories are supported."
            )

        license_info = data.get("license")
        license_name = (
            license_info.get("spdx_id") or license_info.get("name")
            if license_info
            else None
        )

        now = datetime.now(UTC)
        created_at = _parse_date(data.get("created_at")) or now
        updated_at = _parse_date(data.get("updated_at")) or now
        last_pushed_at = _parse_date(data.get("pushed_at"))

        return {
            "name": data["name"],
            "owner": data["owner"]["login"],
            "full_name": data["full_name"],
            "description": data.get("description"),
            "default_branch": data.get("default_branch", "main"),
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "language": data.get("language"),
            "license": license_name,
            "clone_url": data.get(
                "clone_url", f"https://github.com/{owner}/{repo}.git"
            ),
            "html_url": data.get("html_url", f"https://github.com/{owner}/{repo}"),
            "visibility": data.get("visibility", "public"),
            "size": data.get("size", 0),
            "created_at": created_at,
            "updated_at": updated_at,
            "last_pushed_at": last_pushed_at,
        }
