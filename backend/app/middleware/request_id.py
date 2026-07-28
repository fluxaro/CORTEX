"""Request ID and Correlation ID middleware for HTTP tracing."""

import uuid
from collections.abc import Callable
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware attaching unique X-Request-ID and X-Correlation-ID headers."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        correlation_id = request.headers.get("X-Correlation-ID", request_id)

        request.state.request_id = request_id
        request.state.correlation_id = correlation_id

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Correlation-ID"] = correlation_id
        return response
