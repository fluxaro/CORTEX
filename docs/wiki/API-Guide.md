# ProjectIQ API Guide

The ProjectIQ REST API provides comprehensive endpoints for managing repositories, running static analysis, extracting architecture graphs, auditing security findings, fetching Repository IQ summaries, and managing enterprise workspaces.

Interactive Swagger documentation is available at `http://localhost:8000/docs`.

## Authentication
ProjectIQ uses Bearer JWT Access Tokens:
```http
Authorization: Bearer <access_token>
```

## Key API Resources
- **`/api/v1/auth`**: User registration, login, refresh tokens, and OAuth flow.
- **`/api/v1/workspaces`**: Workspace boundaries, memberships, and invitations.
- **`/api/v1/repositories`**: Ingestion, status tracking, and file index.
- **`/api/v1/repositories/{id}/iq`**: Repository IQ 0-100 overall score and maturity classification.
- **`/api/v1/repositories/{id}/architecture`**: Architecture style, design patterns, and dependency graph.
- **`/api/v1/repositories/{id}/security`**: SAST findings, secret scans, dependency CVEs.
- **`/api/v1/repositories/{id}/trends`**: Time-series historical metric snapshots.
- **`/api/v1/comparison/compare`**: Cross-repository benchmark matrix.
