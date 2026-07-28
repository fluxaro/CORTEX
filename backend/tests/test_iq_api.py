"""Tests for Repository IQ REST API endpoints and Celery execution pipeline."""

import uuid
from pathlib import Path
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository
from app.tasks.repository_iq_tasks import _async_run_repository_iq


@pytest.mark.asyncio
async def test_iq_pipeline_and_api(
    client: AsyncClient,
    db_session: AsyncSession,
    tmp_path: Path,
) -> None:
    """Test full Repository IQ pipeline and REST API endpoints."""
    repo_dir = tmp_path / "iq_repo"
    repo_dir.mkdir()

    readme_file = repo_dir / "README.md"
    readme_file.write_text(
        "# IQ Repo\n\n## Installation\npip install iq\n\n## License\nMIT\n",
        encoding="utf-8",
    )

    mock_metadata = {
        "name": "iq_repo",
        "owner": "me-hv",
        "full_name": "me-hv/iq_repo",
        "description": "Sample Repo for IQ test",
        "default_branch": "main",
        "stars": 50,
        "forks": 10,
        "language": "Python",
        "license": "MIT",
        "clone_url": "https://github.com/me-hv/iq_repo.git",
        "html_url": "https://github.com/me-hv/iq_repo",
        "visibility": "public",
        "size": 30,
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
                json={"url": "https://github.com/me-hv/iq_repo"},
            )
            assert res.status_code == 201
            repo_id = res.json()["id"]

    r_result = await db_session.execute(
        select(Repository).where(Repository.id == uuid.UUID(repo_id))
    )
    repo_obj = r_result.scalar_one()
    repo_obj.local_path = str(repo_dir)
    await db_session.commit()

    # Trigger IQ API endpoint
    with patch("app.tasks.repository_iq_tasks.repository_iq_task.delay"):
        trigger_res = await client.post(f"/api/v1/repositories/{repo_id}/iq")
        assert trigger_res.status_code == 202

    class MockSessionContext:
        async def __aenter__(self):
            return db_session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch(
        "app.tasks.repository_iq_tasks.AsyncSessionLocal",
        return_value=MockSessionContext(),
    ):
        await _async_run_repository_iq(repo_id)

    # 2. GET /repositories/{id}/iq
    get_iq = await client.get(f"/api/v1/repositories/{repo_id}/iq")
    assert get_iq.status_code == 200
    iq_data = get_iq.json()
    assert iq_data["overall_score"] >= 0.0

    # 3. GET /repositories/{id}/executive-summary
    exec_res = await client.get(f"/api/v1/repositories/{repo_id}/executive-summary")
    assert exec_res.status_code == 200

    # 4. GET /repositories/{id}/technical-summary
    tech_res = await client.get(f"/api/v1/repositories/{repo_id}/technical-summary")
    assert tech_res.status_code == 200

    # 5. GET /repositories/{id}/strengths
    str_res = await client.get(f"/api/v1/repositories/{repo_id}/strengths")
    assert str_res.status_code == 200

    # 6. GET /repositories/{id}/weaknesses
    weak_res = await client.get(f"/api/v1/repositories/{repo_id}/weaknesses")
    assert weak_res.status_code == 200

    # 7. GET /repositories/{id}/technical-debt
    debt_res = await client.get(f"/api/v1/repositories/{repo_id}/technical-debt")
    assert debt_res.status_code == 200
    assert debt_res.json()["total_hours"] >= 0.0

    # 8. GET /repositories/{id}/recommendations
    rec_res = await client.get(f"/api/v1/repositories/{repo_id}/recommendations")
    assert rec_res.status_code == 200
    assert "items" in rec_res.json()

    # 9. GET /repositories/{id}/benchmark
    bench_res = await client.get(f"/api/v1/repositories/{repo_id}/benchmark")
    assert bench_res.status_code == 200
    assert bench_res.json()["overall_percentile"] > 0.0
