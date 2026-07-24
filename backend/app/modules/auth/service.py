"""Auth business logic: login, refresh rotation, logout.

Login-event logging follows SECURITY_STANDARDS §12: user id + IP + event
only — never the submitted email/password. Uses the standard `logging`
module, not `print`.
"""

import hashlib
import logging
import uuid
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import InvalidTokenError, decode_jwt, encode_jwt, verify_password
from app.modules.auth import repository
from app.modules.auth.models import User

logger = logging.getLogger("app.auth")


class InvalidCredentialsError(Exception):
    pass


# Per-account login rate limit (SECURITY_STANDARDS §2.1: per-IP AND
# per-account). In-memory, single-process — a real deployment behind a load
# balancer would need a shared store (Redis); acceptable simplification for
# this sprint's scope, noted for later hardening.
_FAILED_ATTEMPT_WINDOW = timedelta(minutes=1)
_FAILED_ATTEMPT_LIMIT = 5
_failed_attempts: dict[str, list[datetime]] = defaultdict(list)


def _check_account_rate_limit(email: str) -> None:
    key = email.lower()
    now = datetime.now(timezone.utc)
    attempts = [t for t in _failed_attempts[key] if now - t < _FAILED_ATTEMPT_WINDOW]
    _failed_attempts[key] = attempts
    if len(attempts) >= _FAILED_ATTEMPT_LIMIT:
        raise InvalidCredentialsError("Invalid email or password")


def _record_failed_attempt(email: str) -> None:
    _failed_attempts[email.lower()].append(datetime.now(timezone.utc))


def _hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def _issue_tokens(db: Session, user: User) -> tuple[str, str]:
    access_token = encode_jwt(
        {"sub": str(user.id), "role": user.role.code},
        "access",
        timedelta(minutes=settings.access_token_expire_minutes),
    )
    refresh_delta = timedelta(days=settings.refresh_token_expire_days)
    refresh_token = encode_jwt(
        {"sub": str(user.id), "jti": str(uuid.uuid4())}, "refresh", refresh_delta
    )
    expires_at = datetime.now(timezone.utc) + refresh_delta
    repository.create_refresh_token(
        db, user_id=user.id, token_hash=_hash_token(refresh_token), expires_at=expires_at
    )
    return access_token, refresh_token


def login(db: Session, email: str, password: str, client_ip: str) -> tuple[str, str, User]:
    _check_account_rate_limit(email)

    user = repository.get_user_by_email(db, email)
    if user is None or not user.is_active or not verify_password(password, user.password_hash):
        _record_failed_attempt(email)
        logger.warning("login failed ip=%s", client_ip)
        raise InvalidCredentialsError("Invalid email or password")

    access_token, refresh_token = _issue_tokens(db, user)
    db.commit()
    logger.info("login succeeded user_id=%s ip=%s", user.id, client_ip)
    return access_token, refresh_token, user


def refresh(db: Session, raw_refresh_token: str, client_ip: str) -> tuple[str, str]:
    payload = decode_jwt(raw_refresh_token, "refresh")  # raises InvalidTokenError
    token_hash = _hash_token(raw_refresh_token)
    stored = repository.get_refresh_token_by_hash(db, token_hash)
    now = datetime.now(timezone.utc)
    if stored is None or stored.revoked_at is not None or stored.expires_at <= now:
        raise InvalidTokenError("Refresh token invalid or expired")

    user = repository.get_user_by_id(db, uuid.UUID(payload["sub"]))
    if user is None or not user.is_active:
        raise InvalidTokenError("Refresh token invalid or expired")

    repository.revoke_refresh_token(db, stored)
    access_token, new_refresh_token = _issue_tokens(db, user)
    db.commit()
    logger.info("token refreshed user_id=%s ip=%s", user.id, client_ip)
    return access_token, new_refresh_token


def logout(db: Session, raw_refresh_token: str | None, client_ip: str) -> None:
    if not raw_refresh_token:
        return
    try:
        decode_jwt(raw_refresh_token, "refresh")
    except InvalidTokenError:
        return  # already invalid/expired — idempotent no-op

    token_hash = _hash_token(raw_refresh_token)
    stored = repository.get_refresh_token_by_hash(db, token_hash)
    if stored is not None and stored.revoked_at is None:
        repository.revoke_refresh_token(db, stored)
        db.commit()
        logger.info("logout user_id=%s ip=%s", stored.user_id, client_ip)
