"""Tests for Security Intelligence REST API endpoints."""

import uuid
from pathlib import Path
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository
from app.tasks.security_tasks import _async_run_security_analysis


@pytest.mark.asyncio
async def test_security_pipeline_and_api(
    client: AsyncClient,
    db_session: AsyncSession,
    tmp_path: Path,
) -> None:
    """Test full Security Intelligence analysis pipeline and REST API endpoints."""
    repo_dir = tmp_path / "sec_repo"
    repo_dir.mkdir()

    app_file = repo_dir / "app.py"
    app_file.write_text(
        "AWS_KEY = 'AKIAIOSFODNN7EXAMPLE'\neval('print(1)')\n",
        encoding="utf-8",
    )

    req_file = repo_dir / "requirements.txt"
    req_file.write_text("requests==2.20.0\n", encoding="utf-8")

    mock_metadata = {
        "name": "sec_repo",
        "owner": "me-hv",
        "full_name": "me-hv/sec_repo",
        "description": "Sample Repo for security analysis test",
        "default_branch": "main",
        "stars": 10,
        "forks": 2,
        "language": "Python",
        "license": "MIT",
        "clone_url": "https://github.com/me-hv/sec_repo.git",
        "html_url": "https://github.com/me-hv/sec_repo",
        "visibility": "public",
        "size": 15,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-02T00:00:00Z",
        "last_pushed_at": "2026-01-03T00:00:00Z",
    }

    # 1. Create Repository
    with patch(
        "app.services.github_client.GitHubClient.get_repository_metadata",
        return_value=mock_metadata,
    ):
        with patch("app.tasks.repository_tasks.clone_repository_task.delay"):
            res = await client.post(
                "/api/v1/repositories",
                json={"url": "https://github.com/me-hv/sec_repo"},
            )
            assert res.status_code == 201
            repo_id = res.json()["id"]

    # Set local_path on repo using test db_session
    r_result = await db_session.execute(
        select(Repository).where(Repository.id == uuid.UUID(repo_id))
    )
    repo_obj = r_result.scalar_one()
    repo_obj.local_path = str(repo_dir)
    await db_session.commit()

    # Trigger security analysis API endpoint
    with patch("app.tasks.security_tasks.security_analysis_task.delay"):
        trigger_res = await client.post(f"/api/v1/repositories/{repo_id}/security")
        assert trigger_res.status_code == 202

    # Mock AsyncSessionLocal to yield test db_session for task
    class MockSessionContext:
        async def __aenter__(self):
            return db_session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch(
        "app.tasks.security_tasks.AsyncSessionLocal", return_value=MockSessionContext()
    ):
        await _async_run_security_analysis(repo_id)

    # 2. GET /repositories/{id}/security
    get_sec = await client.get(f"/api/v1/repositories/{repo_id}/security")
    assert get_sec.status_code == 200
    s_data = get_sec.json()
    assert s_data["secret_count"] >= 1
    assert s_data["dependency_vuln_count"] >= 1

    # 3. GET /repositories/{id}/security/findings
    findings_res = await client.get(f"/api/v1/repositories/{repo_id}/security/findings")
    assert findings_res.status_code == 200
    assert findings_res.json()["total"] >= 1

    # 4. GET /repositories/{id}/security/secrets
    secrets_res = await client.get(f"/api/v1/repositories/{repo_id}/security/secrets")
    assert secrets_res.status_code == 200
    assert secrets_res.json()["total"] >= 1

    # 5. GET /repositories/{id}/security/dependencies
    deps_res = await client.get(f"/api/v1/repositories/{repo_id}/security/dependencies")
    assert deps_res.status_code == 200
    assert deps_res.json()["total"] >= 1

    # 6. GET /repositories/{id}/security/configuration
    config_res = await client.get(
        f"/api/v1/repositories/{repo_id}/security/configuration"
    )
    assert config_res.status_code == 200

    # 7. GET /repositories/{id}/security/authentication
    auth_res = await client.get(
        f"/api/v1/repositories/{repo_id}/security/authentication"
    )
    assert auth_res.status_code == 200

    # 8. GET /repositories/{id}/security/authorization
    authz_res = await client.get(
        f"/api/v1/repositories/{repo_id}/security/authorization"
    )
    assert authz_res.status_code == 200
