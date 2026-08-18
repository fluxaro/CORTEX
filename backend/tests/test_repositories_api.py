"""Tests for Repository REST API endpoints."""

from unittest.mock import patch

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_repository_success(client: AsyncClient) -> None:
    """Test POST /api/v1/repositories adds a public repository."""
    mock_metadata = {
        "name": "ShortLink",
        "owner": "me-hv",
        "full_name": "me-hv/ShortLink",
        "description": "URL Shortener Service",
        "default_branch": "main",
        "stars": 100,
        "forks": 15,
        "language": "Python",
        "license": "MIT",
        "clone_url": "https://github.com/me-hv/ShortLink.git",
        "html_url": "https://github.com/me-hv/ShortLink",
        "visibility": "public",
        "size": 2048,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-02T00:00:00Z",
        "last_pushed_at": "2026-01-03T00:00:00Z",
    }

    with patch(
        "app.services.github_client.GitHubClient.get_repository_metadata",
        return_value=mock_metadata,
    ):
        with patch("app.tasks.repository_tasks.clone_repository_task.delay"):
            response = await client.post(
                "/api/v1/repositories",
                json={"url": "https://github.com/me-hv/ShortLink"},
            )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "ShortLink"
    assert data["owner"] == "me-hv"
    assert data["full_name"] == "me-hv/ShortLink"
    assert data["status"] == "PENDING"
    assert data["stars"] == 100


@pytest.mark.asyncio
async def test_create_repository_duplicate(client: AsyncClient) -> None:
    """Test duplicate repository creation returns 409 Conflict."""
    mock_metadata = {
        "name": "ShortLink",
        "owner": "me-hv",
        "full_name": "me-hv/ShortLink",
        "description": "URL Shortener Service",
        "default_branch": "main",
        "stars": 100,
        "forks": 15,
        "language": "Python",
        "license": "MIT",
        "clone_url": "https://github.com/me-hv/ShortLink.git",
        "html_url": "https://github.com/me-hv/ShortLink",
        "visibility": "public",
        "size": 2048,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-02T00:00:00Z",
        "last_pushed_at": "2026-01-03T00:00:00Z",
    }

    with patch(
        "app.services.github_client.GitHubClient.get_repository_metadata",
        return_value=mock_metadata,
    ):
        with patch("app.tasks.repository_tasks.clone_repository_task.delay"):
            # First creation
            res1 = await client.post(
                "/api/v1/repositories",
                json={"url": "https://github.com/me-hv/ShortLink"},
            )
            assert res1.status_code == 201

            # Second creation (duplicate)
            res2 = await client.post(
                "/api/v1/repositories",
                json={"url": "https://github.com/me-hv/ShortLink"},
            )
            assert res2.status_code == 409
            assert "already been added" in res2.json()["error"]["message"]


@pytest.mark.asyncio
async def test_create_repository_invalid_url(client: AsyncClient) -> None:
    """Test POST /api/v1/repositories with invalid URL returns 400 Bad Request."""
    response = await client.post(
        "/api/v1/repositories",
        json={"url": "https://gitlab.com/invalid/repo"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_repositories_pagination_and_filtering(client: AsyncClient) -> None:
    """Test GET /api/v1/repositories with pagination and filtering."""
    mock_metadata = {
        "name": "Cortex",
        "owner": "me-hv",
        "full_name": "me-hv/Cortex",
        "description": "Repo Intelligence",
        "default_branch": "main",
        "stars": 500,
        "forks": 50,
        "language": "Python",
        "license": "MIT",
        "clone_url": "https://github.com/me-hv/Cortex.git",
        "html_url": "https://github.com/me-hv/Cortex",
        "visibility": "public",
        "size": 5000,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-02T00:00:00Z",
        "last_pushed_at": "2026-01-03T00:00:00Z",
    }

    with patch(
        "app.services.github_client.GitHubClient.get_repository_metadata",
        return_value=mock_metadata,
    ):
        with patch("app.tasks.repository_tasks.clone_repository_task.delay"):
            await client.post(
                "/api/v1/repositories",
                json={"url": "https://github.com/me-hv/Cortex"},
            )

    response = await client.get("/api/v1/repositories?owner=me-hv&language=Python")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["page"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["full_name"] == "me-hv/Cortex"


@pytest.mark.asyncio
async def test_get_and_delete_repository(client: AsyncClient) -> None:
    """Test GET /api/v1/repositories/{id} and DELETE /api/v1/repositories/{id}."""
    mock_metadata = {
        "name": "TestRepo",
        "owner": "me-hv",
        "full_name": "me-hv/TestRepo",
        "description": "Test Repo",
        "default_branch": "main",
        "stars": 10,
        "forks": 1,
        "language": "TypeScript",
        "license": "MIT",
        "clone_url": "https://github.com/me-hv/TestRepo.git",
        "html_url": "https://github.com/me-hv/TestRepo",
        "visibility": "public",
        "size": 100,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-02T00:00:00Z",
        "last_pushed_at": "2026-01-03T00:00:00Z",
    }

    with patch(
        "app.services.github_client.GitHubClient.get_repository_metadata",
        return_value=mock_metadata,
    ):
        with patch("app.tasks.repository_tasks.clone_repository_task.delay"):
            post_res = await client.post(
                "/api/v1/repositories",
                json={"url": "https://github.com/me-hv/TestRepo"},
            )
            assert post_res.status_code == 201
            repo_id = post_res.json()["id"]

    # GET /repositories/{id}
    get_res = await client.get(f"/api/v1/repositories/{repo_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == repo_id

    # DELETE /repositories/{id}
    del_res = await client.delete(f"/api/v1/repositories/{repo_id}")
    assert del_res.status_code == 204

    # Verify 404 after deletion
    get_res_404 = await client.get(f"/api/v1/repositories/{repo_id}")
    assert get_res_404.status_code == 404
