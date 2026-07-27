"""Tests for static analysis REST API endpoints."""

import uuid
from pathlib import Path
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository
from app.tasks.analysis_tasks import _async_run_static_analysis


@pytest.mark.asyncio
async def test_static_analysis_pipeline_and_api(
    client: AsyncClient,
    db_session: AsyncSession,
    tmp_path: Path,
) -> None:
    """Test full static analysis pipeline and REST API retrieval endpoints."""
    # Create sample repository directory on disk
    repo_dir = tmp_path / "sample_repo"
    repo_dir.mkdir()

    py_file = repo_dir / "app.py"
    py_file.write_text(
        """
import os

class Helper:
    def compute(self, x: int) -> int:
        if x > 10:
            return x * 2
        return x

def main():
    h = Helper()
    print(h.compute(15))
""",
        encoding="utf-8",
    )

    mock_metadata = {
        "name": "sample_repo",
        "owner": "me-hv",
        "full_name": "me-hv/sample_repo",
        "description": "Sample Repo for static analysis test",
        "default_branch": "main",
        "stars": 5,
        "forks": 1,
        "language": "Python",
        "license": "MIT",
        "clone_url": "https://github.com/me-hv/sample_repo.git",
        "html_url": "https://github.com/me-hv/sample_repo",
        "visibility": "public",
        "size": 10,
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
                json={"url": "https://github.com/me-hv/sample_repo"},
            )
            assert res.status_code == 201
            repo_id = res.json()["id"]

    # Trigger analysis API endpoint
    with patch("app.tasks.analysis_tasks.static_analysis_task.delay"):
        trigger_res = await client.post(f"/api/v1/repositories/{repo_id}/analyze")
        assert trigger_res.status_code == 202
        run_id = trigger_res.json()["id"]

    # Set local_path on repo using test db_session
    r_result = await db_session.execute(
        select(Repository).where(Repository.id == uuid.UUID(repo_id))
    )
    repo_obj = r_result.scalar_one()
    repo_obj.local_path = str(repo_dir)
    await db_session.commit()

    # Mock AsyncSessionLocal to yield test db_session
    class MockSessionContext:
        async def __aenter__(self):
            return db_session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch(
        "app.tasks.analysis_tasks.AsyncSessionLocal", return_value=MockSessionContext()
    ):
        await _async_run_static_analysis(run_id)

    # 2. GET /repositories/{id}/analysis
    get_run = await client.get(f"/api/v1/repositories/{repo_id}/analysis")
    assert get_run.status_code == 200
    assert get_run.json()["status"] == "COMPLETED"

    # 3. GET /repositories/{id}/metrics
    metrics_res = await client.get(f"/api/v1/repositories/{repo_id}/metrics")
    assert metrics_res.status_code == 200
    m_data = metrics_res.json()
    assert m_data["total_files"] == 1
    assert m_data["complexity_rank"] in ("A", "B", "C", "D", "E", "F")

    # 4. GET /repositories/{id}/files
    files_res = await client.get(f"/api/v1/repositories/{repo_id}/files")
    assert files_res.status_code == 200
    f_data = files_res.json()
    assert f_data["total"] == 1
    assert f_data["items"][0]["language"] == "Python"

    # 5. GET /repositories/{id}/functions
    funcs_res = await client.get(f"/api/v1/repositories/{repo_id}/functions")
    assert funcs_res.status_code == 200
    fn_data = funcs_res.json()
    assert fn_data["total"] >= 1

    # 6. GET /repositories/{id}/classes
    cls_res = await client.get(f"/api/v1/repositories/{repo_id}/classes")
    assert cls_res.status_code == 200
    c_data = cls_res.json()
    assert c_data["total"] == 1
    assert c_data["items"][0]["name"] == "Helper"

    # 7. GET /repositories/{id}/smells
    smells_res = await client.get(f"/api/v1/repositories/{repo_id}/smells")
    assert smells_res.status_code == 200
