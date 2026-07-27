"""Pydantic v2 schemas for repository endpoints."""

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RepositoryCreate(BaseModel):
    """Schema for repository creation request."""

    url: str = Field(
        ...,
        description="Public GitHub repository URL (e.g. https://github.com/owner/repo)",
        examples=["https://github.com/me-hv/ShortLink"],
    )


class FileIndexResponse(BaseModel):
    """Schema for file system index details."""

    model_config = ConfigDict(from_attributes=True)

    folder_count: int
    file_count: int
    max_depth: int
    total_size_bytes: int
    largest_files: list[dict[str, Any]]
    file_extensions: dict[str, int]
    language_distribution: dict[str, Any]


class RepositoryResponse(BaseModel):
    """Schema for repository details response."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    owner: str
    full_name: str
    description: str | None = None
    default_branch: str
    stars: int
    forks: int
    language: str | None = None
    license: str | None = None
    clone_url: str
    html_url: str
    visibility: str
    size: int
    created_at: datetime
    updated_at: datetime
    last_pushed_at: datetime | None = None
    status: str
    analysis_status: str
    local_path: str | None = None
    created_on: datetime
    updated_on: datetime
    file_index: FileIndexResponse | None = None


class RepositoryListResponse(BaseModel):
    """Paginated schema for listing repositories."""

    items: list[RepositoryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
