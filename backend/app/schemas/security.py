"""Pydantic v2 schemas for Security Intelligence endpoints."""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SecurityFindingResponse(BaseModel):
    """Schema for SAST security rule finding."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    rule_id: str
    rule_name: str
    category: str
    severity: str
    confidence: float
    language: str
    file_path: str
    line_number: int
    column_number: int
    description: str
    remediation_placeholder: str
    reference_url: str | None = None
    cvss_score: float | None = None


class SecurityFindingListResponse(BaseModel):
    """Paginated list response for SAST security findings."""

    items: list[SecurityFindingResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class SecretFindingResponse(BaseModel):
    """Schema for secret or token finding."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    secret_type: str
    severity: str
    line_number: int
    file_path: str
    entropy: float
    masked_value: str
    description: str


class SecretFindingListResponse(BaseModel):
    """Paginated list response for secret findings."""

    items: list[SecretFindingResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class DependencyFindingResponse(BaseModel):
    """Schema for dependency vulnerability finding."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    package_name: str
    version: str
    cve_id: str | None = None
    cvss_score: float | None = None
    severity: str
    license: str | None = None
    description: str
    references: list[str]


class DependencyFindingListResponse(BaseModel):
    """Paginated list response for dependency findings."""

    items: list[DependencyFindingResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ConfigurationFindingResponse(BaseModel):
    """Schema for configuration misconfiguration finding."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    file_path: str
    rule_name: str
    severity: str
    line_number: int
    description: str


class ConfigurationFindingListResponse(BaseModel):
    """Paginated list response for configuration findings."""

    items: list[ConfigurationFindingResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AuthenticationFindingResponse(BaseModel):
    """Schema for authentication weakness finding."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    auth_type: str
    severity: str
    file_path: str
    line_number: int
    description: str


class AuthenticationFindingListResponse(BaseModel):
    """Paginated list response for authentication findings."""

    items: list[AuthenticationFindingResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class AuthorizationFindingResponse(BaseModel):
    """Schema for authorization weakness finding."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    authz_type: str
    severity: str
    file_path: str
    line_number: int
    description: str


class AuthorizationFindingListResponse(BaseModel):
    """Paginated list response for authorization findings."""

    items: list[AuthorizationFindingResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class SecurityAnalysisResponse(BaseModel):
    """Schema for overall Security Intelligence analysis report."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    repository_id: uuid.UUID
    analysis_run_id: uuid.UUID

    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    info_count: int

    secret_count: int
    dependency_vuln_count: int
    config_issues_count: int
    auth_issues_count: int

    created_at: datetime
    updated_at: datetime
