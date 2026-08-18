# ADR 0003: Enterprise RBAC and Workspace Isolation

## Context
Collaborative engineering SaaS applications require multi-tenant isolation, organization hierarchies, and role permissions.

## Decision
Cortex implements a multi-tenant boundary model:
- **`Organization`**: Billing and domain boundary.
- **`Workspace`**: Repository and team member isolation boundary.
- **`Membership`**: Assigns roles (`OWNER`, `ADMIN`, `MAINTAINER`, `DEVELOPER`, `VIEWER`) per workspace.

## Consequences
- Every API endpoint validates membership and role level via `check_permission_or_raise`.
- Complete data segregation between organization and personal workspaces.
