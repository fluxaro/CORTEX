"""Version information endpoint."""

from fastapi import APIRouter, status

from app.core.config.settings import settings
from app.schemas.version import VersionResponse

router = APIRouter()


@router.get(
    "/version",
    response_model=VersionResponse,
    status_code=status.HTTP_200_OK,
    summary="Application version",
    description="Retrieve the application name and version.",
)
async def get_version() -> VersionResponse:
    """Return application name and version."""
    return VersionResponse(
        app=settings.APP_NAME,
        version=settings.APP_VERSION,
    )
