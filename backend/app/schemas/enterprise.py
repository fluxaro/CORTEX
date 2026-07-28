"""Pydantic v2 schemas for Phase 9 Enterprise Platform features."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


# Auth Schemas
class UserRegisterRequest(BaseModel):
    email: str
    password: str = Field(..., min_length=6)
    full_name: str | None = None


class UserLoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    full_name: str | None = None
    avatar_url: str | None = None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime


class UserPreferenceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    theme: str = "dark"
    email_notifications: bool = True
    in_app_notifications: bool = True
    default_workspace_id: str | None = None


# Workspace & Organization Schemas
class OrganizationCreateRequest(BaseModel):
    name: str
    slug: str
    avatar_url: str | None = None


class OrganizationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    slug: str
    avatar_url: str | None = None
    owner_id: str
    created_at: datetime


class WorkspaceCreateRequest(BaseModel):
    name: str
    slug: str
    type: str = "PERSONAL"
    organization_id: str | None = None


class WorkspaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    slug: str
    type: str
    organization_id: str | None = None
    owner_id: str
    created_at: datetime


class MembershipResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    workspace_id: str | None = None
    organization_id: str | None = None
    role: str
    status: str
    created_at: datetime


class InvitationCreateRequest(BaseModel):
    email: str
    workspace_id: str | None = None
    organization_id: str | None = None
    role: str = "DEVELOPER"


class InvitationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    workspace_id: str | None = None
    organization_id: str | None = None
    role: str
    status: str
    expires_at: datetime
    created_at: datetime


# Git Platform & Webhook Schemas
class GitRepoImportRequest(BaseModel):
    provider: str
    external_repo_id: str
    repo_url: str
    name: str
    default_branch: str = "main"


class WebhookCreateRequest(BaseModel):
    repository_id: str
    provider: str = "GITHUB"
    url: str
    secret: str
    event_types: list[str] = ["push", "pull_request", "release"]


class WebhookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    repository_id: str
    provider: str
    url: str
    is_active: bool
    created_at: datetime


# Notification & Audit Log Schemas
class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime


class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str | None = None
    workspace_id: str | None = None
    action: str
    entity_type: str
    entity_id: str | None = None
    details_json: dict[str, Any] | None = None
    created_at: datetime


# Scan History, Trends & Comparison Schemas
class ScanHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    repository_id: str
    status: str
    duration_seconds: float
    commit_hash: str | None = None
    branch: str
    triggered_by: str
    created_at: datetime


class TrendMetricResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    repository_id: str
    recorded_at: datetime
    overall_iq: float
    security_score: float
    architecture_score: float
    complexity_score: float
    documentation_score: float
    debt_hours: float
    testing_score: float


class RepositoryComparisonRequest(BaseModel):
    title: str
    repository_ids: list[str]
    workspace_id: str | None = None


class RepositoryComparisonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    repo_ids_json: list[str]
    comparison_data_json: dict[str, Any] | None = None
    created_at: datetime
