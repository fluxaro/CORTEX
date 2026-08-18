"""API v1 router composition."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    analysis,
    architecture,
    audit_logs,
    auth,
    comparison,
    git_platforms,
    grading,
    health,
    maintainability,
    notifications,
    organizations,
    repositories,
    security,
    trends,
    version,
    webhooks,
    workspaces,
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(version.router, tags=["Version"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["Workspaces"])
api_router.include_router(
    organizations.router, prefix="/organizations", tags=["Organizations"]
)
api_router.include_router(
    git_platforms.router, prefix="/git-platforms", tags=["Git Platforms"]
)
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
api_router.include_router(
    notifications.router, prefix="/notifications", tags=["Notifications"]
)
api_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["Audit Logs"])
api_router.include_router(trends.router, tags=["Trend Metrics"])
api_router.include_router(
    comparison.router, prefix="/comparison", tags=["Repository Comparison"]
)
api_router.include_router(
    repositories.router, prefix="/repositories", tags=["Repositories"]
)
api_router.include_router(
    analysis.router, prefix="/repositories", tags=["Static Analysis"]
)
api_router.include_router(
    architecture.router, prefix="/repositories", tags=["Architecture Intelligence"]
)
api_router.include_router(
    security.router, prefix="/repositories", tags=["Security Intelligence (SAST)"]
)
api_router.include_router(
    maintainability.router,
    prefix="/repositories",
    tags=["Maintainability Intelligence"],
)
api_router.include_router(
    grading.router, prefix="/repositories", tags=["Repository Grading Engine & AI Intelligence"]
)
