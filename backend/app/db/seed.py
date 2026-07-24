"""Idempotent demo-data seed for local development (F-04 acceptance).

Run with: python -m app.db.seed

All data is obviously fake per SECURITY_STANDARDS §1 — never put real
participant or payment data in here. The demo password is a documented,
development-only constant; the production guard below blocks misuse.
"""

from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.modules.auth.models import Role, User
from app.modules.events.models import Event, EventStatus
from app.modules.participants.models import Participant
from app.modules.partners.models import Partner, PartnerType
from app.modules.shop.models import Product
from app.modules.tenants.models import Tenant

DEMO_PASSWORD = "Demo-Password-123!"  # dev-only; guard below refuses production

ROLES = [
    ("admin", "Admin", "Full system access"),
    ("management", "Management (GF)", "Business management access"),
    ("staff", "Staff", "Operational access"),
    ("readonly", "Read-only", "Read-only access"),
]


def _get_or_create(db: Session, model, defaults=None, **keys):
    instance = db.query(model).filter_by(**keys).first()
    if instance:
        return instance, False
    instance = model(**keys, **(defaults or {}))
    db.add(instance)
    db.flush()
    return instance, True


def seed(db: Session) -> dict[str, int]:
    created = {
        "roles": 0,
        "tenants": 0,
        "users": 0,
        "events": 0,
        "participants": 0,
        "products": 0,
        "partners": 0,
    }

    roles = {}
    for code, name, description in ROLES:
        role, was_created = _get_or_create(
            db, Role, code=code, defaults={"name": name, "description": description}
        )
        roles[code] = role
        created["roles"] += was_created

    tenant, was_created = _get_or_create(
        db, Tenant, slug="eowe-demo", defaults={"name": "EOWE Demo"}
    )
    created["tenants"] += was_created

    for role_code, email in [
        ("admin", "test+admin@example.com"),
        ("management", "test+gf@example.com"),
        ("staff", "test+staff@example.com"),
        ("readonly", "test+readonly@example.com"),
    ]:
        _, was_created = _get_or_create(
            db,
            User,
            email=email,
            defaults={
                "tenant_id": tenant.id,
                "password_hash": hash_password(DEMO_PASSWORD),
                "full_name": f"Demo {roles[role_code].name}",
                "role_id": roles[role_code].id,
            },
        )
        created["users"] += was_created

    for name, status, start in [
        ("Lake Demo Open Water 2026", EventStatus.PUBLISHED, date(2026, 8, 15)),
        ("Demo Night Swim (Draft)", EventStatus.DRAFT, date(2026, 9, 12)),
    ]:
        _, was_created = _get_or_create(
            db,
            Event,
            tenant_id=tenant.id,
            name=name,
            defaults={
                "status": status,
                "venue": "Demosee, Musterstadt",
                "start_date": start,
                "end_date": start,
                "capacity": 200,
            },
        )
        created["events"] += was_created

    for first, last, dob in [
        ("Testina", "Musterfrau", date(1990, 1, 1)),
        ("Testo", "Mustermann", date(1985, 6, 15)),
        ("Junior", "Musterkind", date(2010, 3, 30)),
    ]:
        _, was_created = _get_or_create(
            db,
            Participant,
            tenant_id=tenant.id,
            first_name=first,
            last_name=last,
            date_of_birth=dob,
            defaults={
                "email": f"test+{first.lower()}@example.com",
                "phone": "+49 000 0000000",
                "emergency_contact_name": "Emergency Muster",
                "emergency_contact_phone": "+49 000 0000001",
            },
        )
        created["participants"] += was_created

    for sku, name, price in [
        ("DEMO-CAP-001", "Demo Swim Cap", Decimal("9.90")),
        ("DEMO-TSHIRT-001", "Demo Finisher Shirt", Decimal("24.90")),
        ("DEMO-BUOY-001", "Demo Safety Buoy", Decimal("39.00")),
    ]:
        _, was_created = _get_or_create(
            db,
            Product,
            tenant_id=tenant.id,
            sku=sku,
            defaults={"name": name, "price": price, "stock_quantity": 50},
        )
        created["products"] += was_created

    for name, ptype in [
        ("Demo Sponsor GmbH", PartnerType.SPONSOR),
        ("Demo Wasserwacht e.V.", PartnerType.SERVICE_PROVIDER),
    ]:
        _, was_created = _get_or_create(
            db,
            Partner,
            tenant_id=tenant.id,
            name=name,
            defaults={
                "partner_type": ptype,
                "contact_name": "Kontakt Muster",
                "contact_email": "test+partner@example.com",
            },
        )
        created["partners"] += was_created

    db.commit()
    return created


def main() -> None:
    if settings.environment == "production":
        raise SystemExit("Refusing to seed demo data in production.")
    db = SessionLocal()
    try:
        created = seed(db)
        total = sum(created.values())
        print(f"Seed complete — {total} new rows: {created}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
