# FAQ & Troubleshooting

## Frequently Asked Questions

### Does ProjectIQ execute repository code during analysis?
**No.** ProjectIQ relies strictly on static analysis, AST parsing, structural indexers, and pattern matchers. No untrusted repository code is ever executed.

### Can ProjectIQ run offline without an AI key?
**Yes.** ProjectIQ includes an `AIProviderFactory` with a deterministic `MockAIProvider` fallback. All scoring, static analysis, security scans, and architecture graphs work 100% deterministically without external LLM API keys.

## Troubleshooting

### Celery task connection errors
Ensure Redis server is running on `redis://localhost:6379/0` or configure `REDIS_URL`.

### Database migration issues
Run `alembic -c backend/alembic.ini upgrade head` to ensure all 14 enterprise tables are created.
