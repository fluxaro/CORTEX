"""Tests for GitHubClient service."""

import httpx
import pytest

from app.exceptions.custom_exceptions import GitHubAPIError, InvalidGitHubURLError
from app.services.github_client import GitHubClient


def test_parse_github_url_valid() -> None:
    """Test URL parsing for valid GitHub repository URLs."""
    owner, repo = GitHubClient.parse_github_url("https://github.com/me-hv/Cortex")
    assert owner == "me-hv"
    assert repo == "Cortex"

    owner2, repo2 = GitHubClient.parse_github_url(
        "https://github.com/me-hv/ShortLink.git"
    )
    assert owner2 == "me-hv"
    assert repo2 == "ShortLink"

    owner3, repo3 = GitHubClient.parse_github_url("github.com/fastapi/fastapi")
    assert owner3 == "fastapi"
    assert repo3 == "fastapi"


def test_parse_github_url_invalid() -> None:
    """Test URL parsing raises InvalidGitHubURLError on invalid URLs."""
    with pytest.raises(InvalidGitHubURLError):
        GitHubClient.parse_github_url("https://gitlab.com/owner/repo")

    with pytest.raises(InvalidGitHubURLError):
        GitHubClient.parse_github_url("not_a_url")


@pytest.mark.asyncio
async def test_get_repository_metadata_success() -> None:
    """Test fetching repository metadata with mocked HTTP response."""
    mock_payload = {
        "name": "ShortLink",
        "full_name": "me-hv/ShortLink",
        "owner": {"login": "me-hv"},
        "description": "URL Shortener Service",
        "default_branch": "main",
        "stargazers_count": 42,
        "forks_count": 5,
        "language": "Python",
        "license": {"spdx_id": "MIT"},
        "clone_url": "https://github.com/me-hv/ShortLink.git",
        "html_url": "https://github.com/me-hv/ShortLink",
        "visibility": "public",
        "private": False,
        "size": 1024,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-02T00:00:00Z",
        "pushed_at": "2026-01-03T00:00:00Z",
    }

    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json=mock_payload)
    )

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = GitHubClient(http_client=http_client)
        metadata = await client.get_repository_metadata("me-hv", "ShortLink")

    assert metadata["name"] == "ShortLink"
    assert metadata["owner"] == "me-hv"
    assert metadata["full_name"] == "me-hv/ShortLink"
    assert metadata["stars"] == 42
    assert metadata["forks"] == 5
    assert metadata["language"] == "Python"
    assert metadata["license"] == "MIT"
    assert metadata["visibility"] == "public"


@pytest.mark.asyncio
async def test_get_repository_metadata_not_found() -> None:
    """Test 404 response raising GitHubAPIError."""
    transport = httpx.MockTransport(
        lambda request: httpx.Response(404, json={"message": "Not Found"})
    )

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = GitHubClient(http_client=http_client)
        with pytest.raises(GitHubAPIError) as exc_info:
            await client.get_repository_metadata("nonexistent", "repo")

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_get_repository_metadata_private_repo_rejected() -> None:
    """Test private repository payload raising InvalidGitHubURLError."""
    mock_payload = {
        "name": "PrivateRepo",
        "full_name": "me-hv/PrivateRepo",
        "owner": {"login": "me-hv"},
        "private": True,
        "visibility": "private",
    }

    transport = httpx.MockTransport(
        lambda request: httpx.Response(200, json=mock_payload)
    )

    async with httpx.AsyncClient(transport=transport) as http_client:
        client = GitHubClient(http_client=http_client)
        with pytest.raises(InvalidGitHubURLError):
            await client.get_repository_metadata("me-hv", "PrivateRepo")
