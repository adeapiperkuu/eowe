"""Participant registry models (C2 personal data, SECURITY_STANDARDS §1).

TODO(GDPR): soft-delete is retention, not erasure — the Art. 17 hard-erasure
routine does not exist yet; it is planned together with the participant
module work in M1-03. Until then, erasure requests require a manual,
documented process.
"""

import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Index, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.db.mixins import SoftDeleteMixin, TimestampMixin, UUIDPkMixin


class Participant(UUIDPkMixin, TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "participants"
    __table_args__ = (Index("ix_participants_tenant_id_last_name", "tenant_id", "last_name"),)

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    height_cm: Mapped[int | None] = mapped_column(Integer)
    weight_kg: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    # Not unique: one guardian may register several participants.
    email: Mapped[str | None] = mapped_column(String(320))
    phone: Mapped[str | None] = mapped_column(String(50))
    emergency_contact_name: Mapped[str | None] = mapped_column(String(200))
    emergency_contact_phone: Mapped[str | None] = mapped_column(String(50))
