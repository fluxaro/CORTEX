"""Tests for CORTEX Repository Grade REST API endpoints and Celery execution pipeline."""

import uuid
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.repository import Repository
from app.tasks.repository_grading_tasks import _async_run_repository_grading


@pytest.mark.asyncio
async def test_grading_pipeline_and_api(
    client: AsyncClient,
    db_session: AsyncSession,
    tmp_path,
) -> None:
    """Test full Repository Grading pipeline, REST API endpoints, and deprecated /iq route."""
    repo_dir = tmp_path / "cortex_test_repo"
    repo_dir.mkdir()
    (repo_dir / "README.md").write_text(
        "# CORTEX Test Repo\n\n## Installation\npip install cortex\n\n## License\nMIT\n",
        encoding="utf-8",
    )

    mock_metadata = {
        "name": "cortex_test_repo",
        "owner": "me-hv",
        "full_name": "me-hv/cortex_test_repo",
        "description": "Sample Repo for CORTEX test",
        "default_branch": "main",
        "stars": 10,
        "forks": 2,
        "language": "Python",
        "license": "MIT",
        "clone_url": "https://github.com/me-hv/cortex_test_repo.git",
        "html_url": "https://github.com/me-hv/cortex_test_repo",
        "visibility": "public",
        "size": 1024,
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-02T00:00:00Z",
        "last_pushed_at": "2026-01-03T00:00:00Z",
    }

    with patch(
        "app.services.github_client.GitHubClient.get_repository_metadata",
        return_value=mock_metadata,
    ), patch("app.tasks.repository_tasks.clone_repository_task.delay"):
        create_res = await client.post(
            "/api/v1/repositories",
            json={"url": "https://github.com/me-hv/cortex_test_repo"},
        )
    assert create_res.status_code == 201
    repo_id_str = create_res.json()["id"]
    repo_uuid = uuid.UUID(repo_id_str)

    # Manually assign local_path for scanner testing
    res = await db_session.execute(select(Repository).where(Repository.id == repo_uuid))
    repo_obj = res.scalar_one()
    repo_obj.local_path = str(repo_dir)
    await db_session.commit()

    # 1. Trigger Grade API endpoint POST /repositories/{id}/grade
    with patch("app.tasks.repository_grading_tasks.repository_grading_task.delay"):
        trigger_res = await client.post(f"/api/v1/repositories/{repo_id_str}/grade")
        assert trigger_res.status_code == 202
        assert trigger_res.json()["repository_id"] == repo_id_str

    # Execute async task logic synchronously
    with patch(
        "app.tasks.repository_grading_tasks.AsyncSessionLocal",
        return_value=db_session,
    ):
        await _async_run_repository_grading(repo_id_str)

    # 2. GET /repositories/{id}/grade
    get_grade = await client.get(f"/api/v1/repositories/{repo_id_str}/grade")
    assert get_grade.status_code == 200
    grade_data = get_grade.json()
    assert grade_data["overall_score"] >= 0.0
    assert "overall_grade" in grade_data
    assert "category_scores" in grade_data

    # 3. GET /repositories/{id}/persona-summary?persona=executive
    persona_res = await client.get(
        f"/api/v1/repositories/{repo_id_str}/persona-summary?persona=executive"
    )
    assert persona_res.status_code == 200
    p_data = persona_res.json()
    assert p_data["persona"] == "executive"
    assert "summary_text" in p_data

    # 4. GET /repositories/{id}/iq (deprecated contract verification)
    deprecated_res = await client.get(f"/api/v1/repositories/{repo_id_str}/iq")
    assert deprecated_res.status_code == 200
    assert deprecated_res.headers.get("Deprecation") == "true"
    assert "/api/v1/repositories/" in deprecated_res.headers.get("Link", "")
