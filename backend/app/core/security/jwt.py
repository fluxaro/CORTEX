"""Standard library HMAC-SHA256 JWT Access & Refresh Token utilities."""

import base64
import hashlib
import hmac
import json
import time
from typing import Any, cast

SECRET_KEY = "projectiq-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours
REFRESH_TOKEN_EXPIRE_DAYS = 30  # 30 days


def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64_decode(data_str: str) -> bytes:
    padding = "=" * (4 - (len(data_str) % 4))
    return base64.urlsafe_b64decode(data_str + padding)


def create_access_token(data: dict[str, Any], expires_delta: int | None = None) -> str:
    """Generate JWT access token."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = data.copy()
    expire_time = int(time.time()) + (expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    payload.update({"exp": expire_time, "type": "access"})

    h_json = json.dumps(header, separators=(",", ":")).encode("utf-8")
    p_json = json.dumps(payload, separators=(",", ":")).encode("utf-8")

    unsigned_token = f"{_b64_encode(h_json)}.{_b64_encode(p_json)}"
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"), unsigned_token.encode("utf-8"), hashlib.sha256
    ).digest()
    return f"{unsigned_token}.{_b64_encode(signature)}"


def create_refresh_token(data: dict[str, Any]) -> str:
    """Generate JWT refresh token."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = data.copy()
    expire_time = int(time.time()) + REFRESH_TOKEN_EXPIRE_DAYS * 86400
    payload.update({"exp": expire_time, "type": "refresh"})

    h_json = json.dumps(header, separators=(",", ":")).encode("utf-8")
    p_json = json.dumps(payload, separators=(",", ":")).encode("utf-8")

    unsigned_token = f"{_b64_encode(h_json)}.{_b64_encode(p_json)}"
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"), unsigned_token.encode("utf-8"), hashlib.sha256
    ).digest()
    return f"{unsigned_token}.{_b64_encode(signature)}"


def decode_token(token: str) -> dict[str, Any]:
    """Decode and validate JWT token."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Malformed JWT token.")

        header_b64, payload_b64, sig_b64 = parts
        unsigned_token = f"{header_b64}.{payload_b64}"
        expected_sig = hmac.new(
            SECRET_KEY.encode("utf-8"), unsigned_token.encode("utf-8"), hashlib.sha256
        ).digest()

        if _b64_encode(expected_sig) != sig_b64:
            raise ValueError("Invalid JWT signature.")

        payload_bytes = _b64_decode(payload_b64)
        payload = json.loads(payload_bytes.decode("utf-8"))

        if "exp" in payload and payload["exp"] < int(time.time()):
            raise ValueError("Expired JWT token.")

        return cast(dict[str, Any], payload)
    except Exception as e:
        raise ValueError(f"Invalid JWT token: {str(e)}") from e
