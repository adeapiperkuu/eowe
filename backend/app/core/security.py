"""Password hashing and JWT primitives.

bcrypt is used directly (not passlib): the pinned passlib 1.7.4 is
unmaintained and incompatible with bcrypt >= 4.1. PyJWT is used with the
algorithm always pinned at the call site — never taken from the token
header or from settings (SECURITY_STANDARDS §2.2, "alg: none" attacks).
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import bcrypt
import jwt

from app.core.config import settings

ALGORITHM = "HS256"
TokenType = Literal["access", "refresh"]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("ascii")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("ascii"))


class InvalidTokenError(Exception):
    pass


def encode_jwt(claims: dict[str, Any], token_type: TokenType, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        **claims,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_jwt(token: str, expected_type: TokenType) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise InvalidTokenError("Token invalid or expired") from exc
    if payload.get("type") != expected_type:
        raise InvalidTokenError(f"Expected token type {expected_type!r}")
    return payload
