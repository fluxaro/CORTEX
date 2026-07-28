"""Tests for Maintainability & Repository Intelligence REST API endpoints."""

import uuid
from pathlib import Path
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository
from app.tasks.repository_intelligence_tasks import _async_run_repository_intelligence


@pytest.mark.asyncio
async def test_maintainability_pipeline_and_api(
    client: AsyncClient,
    db_session: AsyncSession,
    tmp_path: Path,
) -> None:
    """Test full Maintainability analysis pipeline and REST API endpoints."""
    repo_dir = tmp_path / "maint_repo"
    repo_dir.mkdir()

    readme_file = repo_dir / "README.md"
    readme_file.write_text(
        "# Maint Repo\n\n## Installation\npip install maint\n\n## Usage\npython run.py\n\n## License\nMIT\n",
        encoding="utf-8",
    )

    test_file = repo_dir / "test_app.py"
    test_file.write_text(
        "import pytest\ndef test_dummy(): assert True\n", encoding="utf-8"
    )

    mock_metadata = {
        "name": "maint_repo",
        "owner": "me-hv",
        "full_name": "me-hv/maint_repo",
        "description": "Sample Repo for maintainability test",
        "default_branch": "main",
        "stars": 20,
        "forks": 5,
        "language": "Python",
        "license": "MIT",
        "clone_url": "https://github.com/me-hv/maint_repo.git",
        "html_url": "https://github.com/me-hv/maint_repo",
        "visibility": "public",
        "size": 25,
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
                json={"url": "https://github.com/me-hv/maint_repo"},
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

    # Trigger maintainability analysis API endpoint
    with patch(
        "app.tasks.repository_intelligence_tasks.repository_intelligence_task.delay"
    ):
        trigger_res = await client.post(
            f"/api/v1/repositories/{repo_id}/maintainability"
        )
        assert trigger_res.status_code == 202

    # Mock AsyncSessionLocal to yield test db_session for task
    class MockSessionContext:
        async def __aenter__(self):
            return db_session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch(
        "app.tasks.repository_intelligence_tasks.AsyncSessionLocal",
        return_value=MockSessionContext(),
    ):
        await _async_run_repository_intelligence(repo_id)

    # 2. GET /repositories/{id}/maintainability
    get_maint = await client.get(f"/api/v1/repositories/{repo_id}/maintainability")
    assert get_maint.status_code == 200
    m_data = get_maint.json()
    assert m_data["documentation_score"] > 0.0

    # 3. GET /repositories/{id}/documentation
    doc_res = await client.get(f"/api/v1/repositories/{repo_id}/documentation")
    assert doc_res.status_code == 200

    # 4. GET /repositories/{id}/testing
    test_res = await client.get(f"/api/v1/repositories/{repo_id}/testing")
    assert test_res.status_code == 200
    assert test_res.json()["test_file_count"] >= 1

    # 5. GET /repositories/{id}/git-history
    gh_res = await client.get(f"/api/v1/repositories/{repo_id}/git-history")
    assert gh_res.status_code == 200

    # 6. GET /repositories/{id}/commits
    ca_res = await client.get(f"/api/v1/repositories/{repo_id}/commits")
    assert ca_res.status_code == 200

    # 7. GET /repositories/{id}/releases
    rel_res = await client.get(f"/api/v1/repositories/{repo_id}/releases")
    assert rel_res.status_code == 200

    # 8. GET /repositories/{id}/ci
    ci_res = await client.get(f"/api/v1/repositories/{repo_id}/ci")
    assert ci_res.status_code == 200

    # 9. GET /repositories/{id}/community
    comm_res = await client.get(f"/api/v1/repositories/{repo_id}/community")
    assert comm_res.status_code == 200

    # 10. GET /repositories/{id}/repository-health
    rh_res = await client.get(f"/api/v1/repositories/{repo_id}/repository-health")
    assert rh_res.status_code == 200
