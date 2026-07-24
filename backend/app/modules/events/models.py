import enum
import uuid
from datetime import date

from sqlalchemy import CheckConstraint, Date, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.db.mixins import SoftDeleteMixin, TimestampMixin, UUIDPkMixin


class EventStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"


class Event(UUIDPkMixin, TimestampMixin, SoftDeleteMixin, Base):
    # Series/Race/Distance child tables arrive with M1-01 (Sprint 2) as
    # additive migrations — schema v1 carries the Event aggregate only.
    __tablename__ = "events"
    __table_args__ = (
        CheckConstraint("end_date IS NULL OR end_date >= start_date", name="end_after_start"),
        CheckConstraint("capacity IS NULL OR capacity > 0", name="capacity_positive"),
        Index("ix_events_tenant_id_status", "tenant_id", "status"),
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[EventStatus] = mapped_column(
        Enum(
            EventStatus,
            name="event_status",
            native_enum=False,
            length=20,
            values_callable=lambda e: [m.value for m in e],
        ),
        nullable=False,
        server_default=EventStatus.DRAFT.value,
    )
    venue: Mapped[str | None] = mapped_column(String(200))
    start_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    end_date: Mapped[date | None] = mapped_column(Date)
    capacity: Mapped[int | None] = mapped_column(Integer)
