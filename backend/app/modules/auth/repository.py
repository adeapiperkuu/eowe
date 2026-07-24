import uuid
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.auth.models import RefreshToken, User


def get_user_by_email(db: Session, email: str) -> User | None:
    return (
        db.query(User)
        .filter(func.lower(User.email) == email.lower(), User.deleted_at.is_(None))
        .first()
    )


def get_user_by_id(db: Session, user_id: uuid.UUID) -> User | None:
    return db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()


def create_refresh_token(
    db: Session, *, user_id: uuid.UUID, token_hash: str, expires_at: datetime
) -> RefreshToken:
    token = RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at)
    db.add(token)
    db.flush()
    return token


def get_refresh_token_by_hash(db: Session, token_hash: str) -> RefreshToken | None:
    return db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()


def revoke_refresh_token(db: Session, token: RefreshToken) -> None:
    token.revoked_at = func.now()
