"""Version endpoint response schema."""

from pydantic import BaseModel, ConfigDict


class VersionResponse(BaseModel):
    """Schema for version response."""

    model_config = ConfigDict(frozen=True)

    app: str = "ProjectIQ"
    version: str = "0.1.0"
