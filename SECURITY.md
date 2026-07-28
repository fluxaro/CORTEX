# Security Policy

## Supported Versions

| Version | Supported |
| :--- | :--- |
| 1.0.x | ✅ Active support |

---

## Reporting a Security Vulnerability

**Please do not report security vulnerabilities through public GitHub Issues.**

If you discover a security vulnerability in ProjectIQ, please follow responsible disclosure by:

1. **Email**: Open a private security advisory via **GitHub Security Advisories** at:  
   `https://github.com/me-hv/ProjectIQ/security/advisories/new`

2. **Include in your report**:
   - A description of the vulnerability and its potential impact
   - Steps to reproduce the vulnerability
   - Any proof-of-concept code or screenshots
   - Your suggested fix (if you have one)

3. **Response timeline**:
   - We will acknowledge your report within **48 hours**
   - We will provide a detailed response within **7 days**
   - We will aim to release a fix within **30 days** for critical issues

---

## Security Best Practices for Self-Hosted Deployments

When running ProjectIQ in production:

1. **Change the default `SECRET_KEY`** — use a random 64+ character string.
2. **Use environment variables** — never hardcode secrets in source files or Docker images.
3. **Enable HTTPS** — configure a reverse proxy (Nginx/Caddy) with TLS certificates.
4. **Restrict CORS origins** — set `CORS_ORIGINS` to only your frontend domain.
5. **Use strong database passwords** — avoid default PostgreSQL credentials.
6. **Keep dependencies updated** — Dependabot is configured to open PRs for security updates.
7. **Monitor audit logs** — ProjectIQ's immutable `AuditLog` table tracks all authentication and permission events.

---

## Scope

The following are **in scope** for security reports:
- Authentication bypass or JWT forgery
- SQL injection or database access vulnerabilities
- Path traversal allowing read of arbitrary files
- CORS misconfiguration allowing unauthorized cross-origin access
- RBAC bypass allowing unauthorized workspace or repository access
- XSS vulnerabilities in the frontend

The following are **out of scope**:
- Denial of service attacks (rate limiting is already implemented)
- Social engineering attacks
- Issues in third-party dependencies that have no known exploit

---

## Known Security Considerations

- ProjectIQ clones repositories to a sandboxed local directory. **No repository code is executed at any point.**
- Secrets found during analysis are **masked** before being stored in the database.
- All passwords are hashed with **PBKDF2 HMAC-SHA256 (100,000 iterations)**.
- JWT tokens use **HMAC-SHA256** signatures via the Python standard library.
