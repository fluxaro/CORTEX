"""Simple in-memory rate limiting middleware."""

import time
from collections.abc import Callable
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# Client IP -> (request_count, window_start_time)
_rate_limit_db: dict[str, tuple[int, float]] = {}
RATE_LIMIT_REQUESTS = 100  # Max requests
RATE_LIMIT_WINDOW = 60  # per 60 seconds


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware protecting public endpoints."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        client_ip = request.client.host if request.client else "127.0.0.1"
        now = time.time()

        if client_ip in _rate_limit_db:
            count, window_start = _rate_limit_db[client_ip]
            if now - window_start > RATE_LIMIT_WINDOW:
                _rate_limit_db[client_ip] = (1, now)
            else:
                if count >= RATE_LIMIT_REQUESTS:
                    return JSONResponse(
                        status_code=429,
                        content={
                            "detail": "Rate limit exceeded. Please wait before retrying.",
                            "retry_after": int(
                                RATE_LIMIT_WINDOW - (now - window_start)
                            ),
                        },
                    )
                _rate_limit_db[client_ip] = (count + 1, window_start)
        else:
            _rate_limit_db[client_ip] = (1, now)

        response: Response = await call_next(request)
        return response
