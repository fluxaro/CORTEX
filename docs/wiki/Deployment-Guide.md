# Production Deployment Guide

## Deploying with Docker Compose

Cortex provides a production-ready `docker-compose.yml` orchestrating FastAPI, Celery, Redis, and PostgreSQL.

```bash
docker-compose up -d --build
```

## Deploying Backend to Cloud Platforms (Render / Railway / Fly.io)

1. Set environment variables:
   - `DATABASE_URL`: PostgreSQL connection string.
   - `REDIS_URL`: Redis connection string.
   - `JWT_SECRET_KEY`: Random 64-character secret.
   - `CORS_ORIGINS`: Allowed frontend origins.
2. Build command: `pip install -r backend/requirements.txt && alembic -c backend/alembic.ini upgrade head`
3. Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir backend`

## Deploying Frontend to Vercel / Netlify / Cloudflare Pages

1. Build command: `cd frontend && npm run build`
2. Output directory: `frontend/dist`
3. Environment variables: `VITE_API_BASE_URL=https://api.yourdomain.com/api/v1`
