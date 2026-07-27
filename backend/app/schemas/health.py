"""Health endpoint response schema."""

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """Schema for health status response."""

    model_config = ConfigDict(frozen=True)

    status: str = "healthy"
