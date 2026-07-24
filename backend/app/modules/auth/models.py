import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.mixins import SoftDeleteMixin, TimestampMixin, UUIDPkMixin


class Role(UUIDPkMixin, TimestampMixin, Base):
    # Global fixed catalog (admin/management/staff/readonly) — no tenant_id,
    # no soft-delete; the 4 rows are seeded and RESTRICT-protected.
    __tablename__ = "roles"

    code: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))


class User(UUIDPkMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    # Globally unique (not per-tenant): F-05 login has no tenant context.
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(nullable=False, server_default=text("true"))

    # Always needed together with the user (role gating on every request) —
    # joinedload avoids a second query per CLAUDE.md's N+1 guidance.
    role: Mapped[Role] = relationship(lazy="joined")


class RefreshToken(UUIDPkMixin, TimestampMixin, Base):
    # No tenant_id (tokens belong to a user, which already carries tenant_id)
    # and no soft-delete: validity is expressed by expires_at/revoked_at, not
    # a business soft-delete workflow.
    __tablename__ = "refresh_tokens"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        # CASCADE (unlike the RESTRICT used elsewhere for reference data):
        # deleting a user should delete their sessions.
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    # SHA-256 hex digest of the raw refresh JWT — never the raw token
    # (SECURITY_STANDARDS §2.2: stored server-side, hashed, so it can be
    # revoked without the DB itself holding a usable bearer credential).
    token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
