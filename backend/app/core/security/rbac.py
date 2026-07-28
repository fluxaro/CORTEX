"""Role-Based Access Control (RBAC) permission logic."""

from app.models.enterprise import UserRole

ROLE_HIERARCHY: dict[str, int] = {
    UserRole.OWNER: 5,
    UserRole.ADMIN: 4,
    UserRole.MAINTAINER: 3,
    UserRole.DEVELOPER: 2,
    UserRole.VIEWER: 1,
}


def has_permission(user_role: str, required_role: str) -> bool:
    """Check whether user_role meets or exceeds required_role hierarchy level."""
    user_level = ROLE_HIERARCHY.get(user_role.upper(), 1)
    required_level = ROLE_HIERARCHY.get(required_role.upper(), 1)
    return user_level >= required_level


def check_permission_or_raise(user_role: str, required_role: str) -> None:
    """Validate permission or raise ValueError/PermissionError."""
    if not has_permission(user_role, required_role):
        raise PermissionError(
            f"Role '{user_role}' lacks required permission level '{required_role}'."
        )
