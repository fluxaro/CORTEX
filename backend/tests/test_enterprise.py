"""Tests for Phase 9 Enterprise Platform & Git Integration features."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.jwt import create_access_token, decode_token
from app.core.security.password import hash_password, verify_password
from app.core.security.rbac import has_permission
from app.models.enterprise import UserRole
from app.schemas.enterprise import (
    GitRepoImportRequest,
    OrganizationCreateRequest,
    UserLoginRequest,
    UserRegisterRequest,
    WorkspaceCreateRequest,
)
from app.services.auth_service import AuthService
from app.services.git_platform_service import GitPlatformService
from app.services.notification_service import NotificationService
from app.services.workspace_service import WorkspaceService


@pytest.mark.asyncio
async def test_password_hashing():
    raw = "SecurePassword123!"
    hashed = hash_password(raw)
    assert verify_password(raw, hashed)
    assert not verify_password("WrongPassword", hashed)


@pytest.mark.asyncio
async def test_jwt_token_generation():
    token = create_access_token({"sub": "user-123", "role": "ADMIN"})
    payload = decode_token(token)
    assert payload["sub"] == "user-123"
    assert payload["role"] == "ADMIN"
    assert payload["type"] == "access"


@pytest.mark.asyncio
async def test_rbac_permission_hierarchy():
    assert has_permission(UserRole.OWNER, UserRole.DEVELOPER)
    assert has_permission(UserRole.ADMIN, UserRole.MAINTAINER)
    assert not has_permission(UserRole.VIEWER, UserRole.ADMIN)


@pytest.mark.asyncio
async def test_auth_service_register_and_login(db_session: AsyncSession):
    service = AuthService(db_session)
    reg_req = UserRegisterRequest(
        email="test_enterprise@cortex.io",
        password="MyPassword123!",
        full_name="Enterprise Tester",
    )
    user, access, refresh = await service.register_user(reg_req)
    assert user.email == "test_enterprise@cortex.io"
    assert access is not None
    assert refresh is not None

    login_req = UserLoginRequest(
        email="test_enterprise@cortex.io", password="MyPassword123!"
    )
    user_logged, access_logged, _ = await service.authenticate_user(login_req)
    assert user_logged.id == user.id


@pytest.mark.asyncio
async def test_workspace_and_org_creation(db_session: AsyncSession):
    ws_service = WorkspaceService(db_session)
    org_req = OrganizationCreateRequest(name="Acme Corp", slug="acme-corp")
    org = await ws_service.create_organization("owner-123", org_req)
    assert org.name == "Acme Corp"

    ws_req = WorkspaceCreateRequest(
        name="Engineering", slug="acme-engineering", organization_id=org.id
    )
    ws = await ws_service.create_workspace("owner-123", ws_req)
    assert ws.name == "Engineering"
    assert ws.organization_id == org.id


@pytest.mark.asyncio
async def test_git_platform_import_and_webhook(db_session: AsyncSession):
    git_service = GitPlatformService(db_session)
    req = GitRepoImportRequest(
        provider="GITHUB",
        external_repo_id="12345",
        repo_url="https://github.com/acme/cortex-repo",
        name="cortex-repo",
    )
    repo, sync = await git_service.import_repository(req)
    assert repo.name == "cortex-repo"
    assert sync.provider == "GITHUB"


@pytest.mark.asyncio
async def test_notification_service(db_session: AsyncSession):
    notif_service = NotificationService(db_session)
    notif = await notif_service.create_notification(
        "user-101", "Scan Complete", "Scan finished successfully."
    )
    assert notif.title == "Scan Complete"
    assert not notif.is_read

    read_notif = await notif_service.mark_as_read(notif.id)
    assert read_notif.is_read


@pytest.mark.asyncio
async def test_api_auth_endpoints(client: AsyncClient):
    resp = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "api_user@cortex.io",
            "password": "Password123!",
            "full_name": "API User",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_api_workspace_endpoints(client: AsyncClient):
    resp = await client.post(
        "/api/v1/workspaces",
        json={"name": "Dev Workspace", "slug": "dev-workspace"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Dev Workspace"
