"""Tests for CORTEX Repository Grade REST API endpoints and Celery execution pipeline."""

from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

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

    create_payload = {
        "name": "cortex_test_repo",
        "full_name": "me-hv/cortex_test_repo",
        "description": "Sample Repo for CORTEX test",
        "primary_language": "Python",
        "is_private": False,
        "is_fork": False,
        "default_branch": "main",
        "clone_url": "https://github.com/me-hv/cortex_test_repo.git",
        "html_url": "https://github.com/me-hv/cortex_test_repo",
        "local_path": str(repo_dir),
    }
    create_res = await client.post("/api/v1/repositories/", json=create_payload)
    assert create_res.status_code == 201
    repo_id = create_res.json()["id"]

    # 1. Trigger Grade API endpoint POST /repositories/{id}/grade
    with patch("app.tasks.repository_grading_tasks.repository_grading_task.delay"):
        trigger_res = await client.post(f"/api/v1/repositories/{repo_id}/grade")
        assert trigger_res.status_code == 202
        assert trigger_res.json()["repository_id"] == repo_id

    # Execute async task logic synchronously
    with patch(
        "app.tasks.repository_grading_tasks.AsyncSessionLocal",
        return_value=db_session,
    ):
        await _async_run_repository_grading(repo_id)

    # 2. GET /repositories/{id}/grade
    get_grade = await client.get(f"/api/v1/repositories/{repo_id}/grade")
    assert get_grade.status_code == 200
    grade_data = get_grade.json()
    assert grade_data["overall_score"] >= 0.0
    assert "overall_grade" in grade_data
    assert "category_scores" in grade_data
    assert "capped" in grade_data

    # 3. GET /repositories/{id}/persona-summary?persona=executive
    get_persona = await client.get(f"/api/v1/repositories/{repo_id}/persona-summary?persona=executive")
    assert get_persona.status_code == 200
    persona_data = get_persona.json()
    assert persona_data["persona"] == "executive"
    assert "summary_text" in persona_data

    # 4. Deprecated GET /repositories/{id}/iq route
    get_iq = await client.get(f"/api/v1/repositories/{repo_id}/iq")
    assert get_iq.status_code == 200
    assert get_iq.headers.get("Deprecation") == "true"
    assert "grade" in get_iq.headers.get("Link", "")

    # 5. GET /repositories/{id}/strengths & /weaknesses
    strengths_res = await client.get(f"/api/v1/repositories/{repo_id}/strengths")
    assert strengths_res.status_code == 200
    assert isinstance(strengths_res.json(), list)

    weaknesses_res = await client.get(f"/api/v1/repositories/{repo_id}/weaknesses")
    assert weaknesses_res.status_code == 200
    assert isinstance(weaknesses_res.json(), list)
