import enum
import uuid

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.db.mixins import SoftDeleteMixin, TimestampMixin, UUIDPkMixin


class PartnerType(str, enum.Enum):
    SPONSOR = "sponsor"
    SERVICE_PROVIDER = "service_provider"


class Partner(UUIDPkMixin, TimestampMixin, SoftDeleteMixin, Base):
    # Contribution tracking (monetary + in-kind) and event links arrive with
    # M5 (Sprint 5). No C3 fields (IBAN/contracts) in this table — §1.
    __tablename__ = "partners"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    partner_type: Mapped[PartnerType] = mapped_column(
        Enum(
            PartnerType,
            name="partner_type",
            native_enum=False,
            length=20,
            values_callable=lambda e: [m.value for m in e],
        ),
        nullable=False,
    )
    contact_name: Mapped[str | None] = mapped_column(String(200))
    contact_email: Mapped[str | None] = mapped_column(String(320))
    contact_phone: Mapped[str | None] = mapped_column(String(50))
    website: Mapped[str | None] = mapped_column(String(255))
    notes: Mapped[str | None] = mapped_column(Text)
