from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.db.mixins import SoftDeleteMixin, TimestampMixin, UUIDPkMixin


class Tenant(UUIDPkMixin, TimestampMixin, SoftDeleteMixin, Base):
    # Multi-tenancy enforcement (filtering/RLS) is Module 6 / post-MVP;
    # the table + tenant_id FKs exist from v1 so no backfill is needed later.
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(nullable=False, server_default=text("true"))
