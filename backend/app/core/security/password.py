"""Standard library PBKDF2 password hashing & verification using hmac.compare_digest."""

import hashlib
import hmac
import os


def hash_password(password: str) -> str:
    """Hash password using PBKDF2 HMAC SHA256."""
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"{salt.hex()}${key.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against stored salt$key hash."""
    try:
        salt_hex, key_hex = hashed_password.split("$")
        salt = bytes.fromhex(salt_hex)
        expected_key = bytes.fromhex(key_hex)
        key = hashlib.pbkdf2_hmac(
            "sha256", plain_password.encode("utf-8"), salt, 100000
        )
        return hmac.compare_digest(key, expected_key)
    except Exception:
        return False
