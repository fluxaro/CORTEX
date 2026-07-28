# ADR 0006: Why Celery and Redis

## Status
Accepted

## Context
Repository cloning, static AST parsing, security scanning, and architecture detection can take 30 seconds to 5 minutes per repository. These operations cannot block HTTP request handlers.

## Decision
Use **Celery** as the distributed task queue with **Redis** as both the broker and result backend.

## Rationale
- **Non-blocking analysis**: Repository cloning and parsing run entirely in background workers, keeping API response times under 100ms.
- **Task chaining**: Celery's `chain()` and `group()` primitives enable the staged pipeline (clone → static → arch/sec/maintain → IQ) with clean dependency ordering.
- **Retry logic**: Built-in exponential backoff retry for transient network failures (e.g., GitHub rate limiting during clone).
- **Redis as broker**: Lightweight, fast, and already required for rate limiting state — no additional infrastructure needed.
- **Monitoring**: Celery's task state machine (PENDING → STARTED → SUCCESS/FAILURE) maps directly to the `AnalysisRun.status` field.

## Alternatives Considered
| Alternative | Rejection Reason |
| :--- | :--- |
| FastAPI BackgroundTasks | Not suitable for long-running tasks; no persistence or retry |
| RQ (Redis Queue) | Less feature-rich; no built-in task chaining |
| AWS SQS + Lambda | Cloud-vendor lock-in; overkill for self-hosted deployment |

## Consequences
- Every analysis operation must be designed as an idempotent Celery task.
- Redis is a hard runtime dependency (cannot run without it).
