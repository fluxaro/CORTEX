# API Reference

ProjectIQ exposes a fully documented REST API following OpenAPI 3.1 standards.

**Interactive documentation:** `http://localhost:8000/docs` (Swagger UI)

---

## Authentication

ProjectIQ uses **JWT Bearer tokens** for authentication.

### Register
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "engineer@example.com",
  "password": "SecurePassword123!",
  "full_name": "Jane Engineer"
}
```
**Response 201:**
```json
{
  "access_token": "eyJhbGci...",
  "refresh_token": "eyJhbGci...",
  "token_type": "bearer"
}
```

### Login
```http
POST /api/v1/auth/login
Content-Type: application/json

{ "email": "engineer@example.com", "password": "SecurePassword123!" }
```

### Using Bearer Tokens
```http
GET /api/v1/workspaces
Authorization: Bearer eyJhbGci...
```

---

## Repository Management

### Ingest Repository
```http
POST /api/v1/repositories
Content-Type: application/json

{ "url": "https://github.com/tiangolo/fastapi" }
```
**Response 201:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "fastapi",
  "owner": "tiangolo",
  "provider": "GITHUB",
  "status": "PENDING",
  "created_at": "2026-07-28T09:00:00Z"
}
```

### List Repositories
```http
GET /api/v1/repositories?page=1&page_size=20&sort=created_at&order=desc&q=fastapi
```
**Response 200:**
```json
{
  "items": [...],
  "total": 42,
  "page": 1,
  "page_size": 20,
  "pages": 3
}
```

---

## Analysis Endpoints

### Trigger Analysis
```http
POST /api/v1/repositories/{id}/analyze
```
**Response 202:** Analysis queued. Poll `/api/v1/repositories/{id}/analysis` for status.

### Get Repository IQ Score
```http
GET /api/v1/repositories/{id}/iq
```
**Response 200:**
```json
{
  "overall_score": 87.4,
  "maturity_level": "Production Ready",
  "subsystem_scores": {
    "static_analysis": 82.0,
    "architecture": 91.5,
    "security": 88.0,
    "documentation": 75.0,
    "testing": 90.0,
    "ci_cd": 95.0,
    "git_practices": 88.0,
    "community": 70.0
  }
}
```

### Get Security Findings
```http
GET /api/v1/repositories/{id}/security/findings?severity=HIGH&page=1&page_size=50
```
**Response 200:**
```json
{
  "items": [
    {
      "id": "...",
      "category": "INJECTION",
      "severity": "HIGH",
      "title": "SQL Injection via string concatenation",
      "file_path": "app/api/users.py",
      "line_number": 42,
      "code_snippet": "query = 'SELECT * FROM users WHERE id=' + user_id",
      "recommendation": "Use parameterized queries or ORM filters."
    }
  ],
  "total": 3
}
```

---

## Error Responses

All errors follow a consistent format:

```json
{
  "detail": "Repository with URL already exists.",
  "code": "REPOSITORY_EXISTS",
  "request_id": "a3f9c2d1-..."
}
```

| HTTP Status | Meaning |
| :--- | :--- |
| `400 Bad Request` | Validation error, malformed request |
| `401 Unauthorized` | Missing or invalid JWT token |
| `403 Forbidden` | Insufficient RBAC role |
| `404 Not Found` | Resource does not exist |
| `409 Conflict` | Duplicate resource |
| `422 Unprocessable Entity` | Pydantic validation failure |
| `429 Too Many Requests` | Rate limit exceeded |
| `500 Internal Server Error` | Unexpected server error |

---

## Pagination

All list endpoints support:

| Parameter | Default | Description |
| :--- | :--- | :--- |
| `page` | `1` | Page number (1-indexed) |
| `page_size` | `20` | Results per page (max 100) |
| `sort` | `created_at` | Sort field |
| `order` | `desc` | `asc` or `desc` |
| `q` | — | Search/filter query |
