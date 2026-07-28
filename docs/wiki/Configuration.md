# Configuration Reference

ProjectIQ is fully configured via environment variables, following the [12-factor app](https://12factor.net/config) methodology.

---

## Core Configuration

| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `APP_NAME` | No | `ProjectIQ` | Application display name |
| `APP_VERSION` | No | `1.0.0` | Application version string |
| `DEBUG` | No | `false` | Enable debug mode (never in production) |
| `SECRET_KEY` | **Yes** | — | Min 64-char random secret for JWT signing |

## Database

| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `DATABASE_URL` | **Yes** | — | PostgreSQL async connection string: `postgresql+asyncpg://user:pass@host:5432/dbname` |
| `DB_POOL_SIZE` | No | `10` | SQLAlchemy async connection pool size |
| `DB_MAX_OVERFLOW` | No | `20` | Max pool overflow connections |

## Redis & Celery

| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `REDIS_URL` | **Yes** | — | Redis connection: `redis://localhost:6379/0` |
| `CELERY_BROKER_URL` | No | `REDIS_URL` | Celery broker (defaults to REDIS_URL) |
| `CELERY_RESULT_BACKEND` | No | `REDIS_URL` | Celery result backend |

## CORS & Security

| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `CORS_ORIGINS` | No | `["http://localhost:5173"]` | JSON list of allowed frontend origins |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` | Access token lifetime in minutes |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | No | `7` | Refresh token lifetime in days |

## AI Providers (Optional)

| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `AI_PROVIDER` | No | `mock` | Active AI provider: `openai`, `anthropic`, `gemini`, `azure`, `ollama`, `mock` |
| `OPENAI_API_KEY` | No | — | OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4o` | OpenAI model to use |
| `ANTHROPIC_API_KEY` | No | — | Anthropic Claude API key |
| `GEMINI_API_KEY` | No | — | Google Gemini API key |

## Git Platform OAuth (Optional)

| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `GITHUB_CLIENT_ID` | No | — | GitHub OAuth App client ID |
| `GITHUB_CLIENT_SECRET` | No | — | GitHub OAuth App client secret |
| `GITLAB_CLIENT_ID` | No | — | GitLab OAuth App client ID |
| `GITLAB_CLIENT_SECRET` | No | — | GitLab OAuth App client secret |
| `BITBUCKET_CLIENT_ID` | No | — | Bitbucket OAuth client ID |
| `BITBUCKET_CLIENT_SECRET` | No | — | Bitbucket OAuth client secret |

---

## Environment Profiles

### Development
```env
DEBUG=true
DATABASE_URL=postgresql+asyncpg://dev:dev@localhost:5432/projectiq_dev
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=dev-secret-key-not-for-production-use
AI_PROVIDER=mock
```

### Testing
```env
DATABASE_URL=sqlite+aiosqlite:///:memory:
REDIS_URL=redis://localhost:6379/1
SECRET_KEY=test-secret-key
AI_PROVIDER=mock
```

### Production
```env
DEBUG=false
DATABASE_URL=postgresql+asyncpg://prod_user:strongpassword@db.example.com:5432/projectiq
REDIS_URL=redis://redis.example.com:6379/0
SECRET_KEY=<64-character-random-string>
CORS_ORIGINS=["https://projectiq.io"]
AI_PROVIDER=openai
OPENAI_API_KEY=sk-...
```
