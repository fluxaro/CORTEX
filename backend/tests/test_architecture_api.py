"""Tests for Architecture Intelligence REST API endpoints."""

import uuid
from pathlib import Path
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository
from app.tasks.architecture_tasks import _async_run_architecture_analysis


@pytest.mark.asyncio
async def test_architecture_pipeline_and_api(
    client: AsyncClient,
    db_session: AsyncSession,
    tmp_path: Path,
) -> None:
    """Test full Architecture Intelligence analysis pipeline and REST API retrieval endpoints."""
    # Create sample repository directory on disk
    repo_dir = tmp_path / "arch_repo"
    repo_dir.mkdir()

    controllers_dir = repo_dir / "controllers"
    controllers_dir.mkdir()
    ctrl_file = controllers_dir / "user_controller.py"
    ctrl_file.write_text(
        "import fastapi\nfrom services.user_service import UserService\n",
        encoding="utf-8",
    )

    services_dir = repo_dir / "services"
    services_dir.mkdir()
    srv_file = services_dir / "user_service.py"
    srv_file.write_text(
        "from repositories.user_repository import UserRepository\n", encoding="utf-8"
    )

    repos_dir = repo_dir / "repositories"
    repos_dir.mkdir()
    repo_file = repos_dir / "user_repository.py"
    repo_file.write_text("class UserRepository:\n    pass\n", encoding="utf-8")

    mock_metadata = {
        "name": "arch_repo",
        "owner": "me-hv",
        "full_name": "me-hv/arch_repo",
        "description": "Sample Repo for arch analysis test",
        "default_branch": "main",
        "stars": 10,
        "forks": 2,
        "language": "Python",
        "license": "MIT",
        "clone_url": "https://github.com/me-hv/arch_repo.git",
        "html_url": "https://github.com/me-hv/arch_repo",
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
                json={"url": "https://github.com/me-hv/arch_repo"},
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

    # Trigger architecture analysis API endpoint
    with patch("app.tasks.architecture_tasks.architecture_analysis_task.delay"):
        trigger_res = await client.post(f"/api/v1/repositories/{repo_id}/architecture")
        assert trigger_res.status_code == 202

    # Mock AsyncSessionLocal to yield test db_session for task
    class MockSessionContext:
        async def __aenter__(self):
            return db_session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

    with patch(
        "app.tasks.architecture_tasks.AsyncSessionLocal",
        return_value=MockSessionContext(),
    ):
        with patch(
            "app.tasks.analysis_tasks.AsyncSessionLocal",
            return_value=MockSessionContext(),
        ):
            await _async_run_architecture_analysis(repo_id)

    # 2. GET /repositories/{id}/architecture
    get_arch = await client.get(f"/api/v1/repositories/{repo_id}/architecture")
    assert get_arch.status_code == 200
    a_data = get_arch.json()
    assert "arch_style" in a_data
    assert "layer_separation_score" in a_data

    # 3. GET /repositories/{id}/patterns
    patterns_res = await client.get(f"/api/v1/repositories/{repo_id}/patterns")
    assert patterns_res.status_code == 200
    p_data = patterns_res.json()
    assert p_data["total"] >= 1

    # 4. GET /repositories/{id}/layers
    layers_res = await client.get(f"/api/v1/repositories/{repo_id}/layers")
    assert layers_res.status_code == 200
    assert len(layers_res.json()) >= 1

    # 5. GET /repositories/{id}/dependency-graph
    graph_res = await client.get(f"/api/v1/repositories/{repo_id}/dependency-graph")
    assert graph_res.status_code == 200
    g_data = graph_res.json()
    assert g_data["total_nodes"] >= 1

    # 6. GET /repositories/{id}/frameworks
    fw_res = await client.get(f"/api/v1/repositories/{repo_id}/frameworks")
    assert fw_res.status_code == 200
    assert len(fw_res.json()) >= 1

    # 7. GET /repositories/{id}/technologies
    tech_res = await client.get(f"/api/v1/repositories/{repo_id}/technologies")
    assert tech_res.status_code == 200
    assert "Python" in tech_res.json()["languages"]
