# System Design — Authentication & Authorization Flow

## Authentication Flow

```
Client                     FastAPI                    DB
  │                           │                       │
  │  POST /auth/register       │                       │
  │  { email, password }      │                       │
  │──────────────────────────►│                       │
  │                           │  PBKDF2 hash password  │
  │                           │  INSERT users          │
  │                           │──────────────────────►│
  │                           │◄──────────────────────│
  │                           │  generate JWT tokens   │
  │◄──────────────────────────│                       │
  │  { access_token,          │                       │
  │    refresh_token }        │                       │
  │                           │                       │
  │  GET /workspaces           │                       │
  │  Authorization: Bearer <access_token>             │
  │──────────────────────────►│                       │
  │                           │  decode JWT           │
  │                           │  validate signature   │
  │                           │  check expiry         │
  │                           │  inject user_id       │
  │                           │  → route handler      │
  │◄──────────────────────────│                       │
  │  200 OK { workspaces }    │                       │
```

## RBAC Authorization Flow

```
API Request
     │
     ▼
JWT Decoded → user_id extracted
     │
     ▼
Look up Membership for user_id + workspace_id
     │
     ▼
Check role level:
  OWNER(5) ≥ ADMIN(4) ≥ MAINTAINER(3) ≥ DEVELOPER(2) ≥ VIEWER(1)
     │
     ├─ Role sufficient → ✅ Allow
     └─ Role insufficient → 403 Forbidden
```

## OAuth Flow (GitHub Example)

```
Browser             FastAPI              GitHub
   │                   │                   │
   │  GET /auth/oauth/github              │
   │──────────────────►│                   │
   │                   │  build auth URL   │
   │◄──────────────────│                   │
   │  302 redirect     │                   │
   │──────────────────────────────────────►│
   │                   │                   │  user approves
   │◄──────────────────────────────────────│
   │  GET /auth/oauth/github/callback?code=│
   │──────────────────►│                   │
   │                   │  POST /token      │
   │                   │──────────────────►│
   │                   │◄──────────────────│
   │                   │  { user_info }    │
   │                   │  upsert user      │
   │                   │  issue JWT tokens │
   │◄──────────────────│                   │
   │  { access_token } │                   │
```

## JWT Token Structure

```json
// Access Token Payload
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "type": "access",
  "iat": 1722153600,
  "exp": 1722155400
}

// Refresh Token Payload
{
  "sub": "user-uuid",
  "type": "refresh",
  "iat": 1722153600,
  "exp": 1722758400
}
```

Tokens are signed with **HMAC-SHA256** using `SECRET_KEY`. No external libraries — standard library `hmac` and `hashlib` modules only.
