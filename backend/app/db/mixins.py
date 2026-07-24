import uuid
from datetime import datetime

from sqlalchemy import DateTime, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class UUIDPkMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("timezone('utc', now())"),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("timezone('utc', now())"),
        onupdate=func.now(),
    )


class SoftDeleteMixin:
    # Soft-delete is a business-workflow convention (SECURITY_STANDARDS §5);
    # it does NOT satisfy GDPR Art. 17 erasure for C2/C3 data (§1).
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
