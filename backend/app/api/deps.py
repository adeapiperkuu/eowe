"""Canonical auth dependency chain (SECURITY_STANDARDS §2.3).

All protected routes depend on `get_current_user` or `require_roles(...)` —
never re-implement token parsing inline in a route.
"""

import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import InvalidTokenError, decode_jwt
from app.db.session import get_db
from app.modules.auth.models import User
from app.modules.auth.repository import get_user_by_id

_bearer_scheme = HTTPBearer(auto_error=False)

_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise _CREDENTIALS_EXCEPTION
    try:
        payload = decode_jwt(credentials.credentials, "access")
    except InvalidTokenError as exc:
        raise _CREDENTIALS_EXCEPTION from exc

    try:
        user_id = payload["sub"]
    except KeyError as exc:
        raise _CREDENTIALS_EXCEPTION from exc

    user = get_user_by_id(db, uuid.UUID(user_id))
    if user is None or not user.is_active:
        raise _CREDENTIALS_EXCEPTION
    return user


def require_roles(*role_codes: str):
    def checker(user: User = Depends(get_current_user)) -> User:
        if user.role.code not in role_codes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
            )
        return user

    return checker
