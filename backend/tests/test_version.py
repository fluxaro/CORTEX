"""Tests for version endpoint."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_version_endpoint(client: AsyncClient) -> None:
    """Test GET /version returns app name and version."""
    response = await client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"app": "ProjectIQ", "version": "0.1.0"}


@pytest.mark.asyncio
async def test_version_api_v1_endpoint(client: AsyncClient) -> None:
    """Test GET /api/v1/version returns app name and version."""
    response = await client.get("/api/v1/version")
    assert response.status_code == 200
    assert response.json() == {"app": "ProjectIQ", "version": "0.1.0"}
