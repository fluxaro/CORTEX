"""Health check endpoint."""

from fastapi import APIRouter, status

from app.schemas.health import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check the operational status of the service.",
)
async def get_health() -> HealthResponse:
    """Return health status."""
    return HealthResponse(status="healthy")
