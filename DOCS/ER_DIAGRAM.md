# EOWE Workspace — ER Diagram (Schema v1, F-04)

Generated from migration `a49c23c0ed80` (schema v1 core entities).
All PKs are UUIDs with `gen_random_uuid()` server defaults; all timestamps are
UTC (`timestamptz`). Soft-delete (`deleted_at`) on every business table
(not on `roles` — global fixed catalog). Enums are stored as VARCHAR + CHECK
(`native_enum=False`).

```mermaid
erDiagram
    tenants ||--o{ users : "tenant_id"
    tenants ||--o{ events : "tenant_id"
    tenants ||--o{ participants : "tenant_id"
    tenants ||--o{ products : "tenant_id"
    tenants ||--o{ partners : "tenant_id"
    roles ||--o{ users : "role_id"

    tenants {
        uuid id PK
        varchar_200 name
        varchar_100 slug UK "unique, indexed"
        boolean is_active "default true"
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at "soft-delete"
    }

    roles {
        uuid id PK
        varchar_50 code UK "admin | management | staff | readonly"
        varchar_100 name
        varchar_255 description
        timestamptz created_at
        timestamptz updated_at
    }

    users {
        uuid id PK
        uuid tenant_id FK "RESTRICT"
        varchar_320 email UK "globally unique (F-05 login)"
        varchar_255 password_hash
        varchar_200 full_name
        uuid role_id FK "RESTRICT"
        boolean is_active "default true"
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at
    }

    events {
        uuid id PK
        uuid tenant_id FK "RESTRICT"
        varchar_200 name
        text description
        varchar_20 status "draft | published | closed (CHECK)"
        varchar_200 venue
        date start_date "indexed"
        date end_date "CHECK >= start_date"
        int capacity "CHECK > 0"
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at
    }

    participants {
        uuid id PK
        uuid tenant_id FK "RESTRICT"
        varchar_100 first_name "C2 PII"
        varchar_100 last_name "C2 PII"
        date date_of_birth "C2 PII"
        int height_cm
        numeric_5_2 weight_kg
        varchar_320 email "C2 PII, not unique"
        varchar_50 phone "C2 PII"
        varchar_200 emergency_contact_name
        varchar_50 emergency_contact_phone
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at
    }

    products {
        uuid id PK
        uuid tenant_id FK "RESTRICT"
        varchar_64 sku "unique per tenant"
        varchar_200 name
        text description
        numeric_10_2 price "CHECK >= 0"
        varchar_3 currency "default EUR"
        int stock_quantity "default 0, CHECK >= 0"
        boolean is_active "default true"
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at
    }

    partners {
        uuid id PK
        uuid tenant_id FK "RESTRICT"
        varchar_200 name
        varchar_20 partner_type "sponsor | service_provider (CHECK)"
        varchar_200 contact_name
        varchar_320 contact_email
        varchar_50 contact_phone
        varchar_255 website
        text notes
        timestamptz created_at
        timestamptz updated_at
        timestamptz deleted_at
    }
```

## Indexes (beyond PK/unique)

| Table | Index |
|---|---|
| events | `(tenant_id, status)` composite; `start_date`; `tenant_id` |
| participants | `(tenant_id, last_name)` composite; `tenant_id` |
| users | `email` (unique); `role_id`; `tenant_id` |
| products / partners | `tenant_id` |
| tenants | `slug` (unique) |

## Planned — NOT in v1 (deliberate deferrals)

| Addition | Arrives with | Notes |
|---|---|---|
| `series`, `races`, `distances` | M1-01 (Sprint 2) | Children of `events`; purely additive |
| `registrations` (event ↔ participant) | M1-04 (Sprint 2) | Enrollment junction + capacity enforcement |
| `audit_log` | F-08 (Sprint 2) | F-08 defines actor/action/diff semantics |
| Partner contributions (monetary + in-kind), event links | M5 (Sprint 5) | |
| C3 fields (IBAN, payments, contracts) | M2 (Sprint 4) | Requires at-rest-encryption team decision (SECURITY_STANDARDS §5) |
| Multi-tenancy enforcement (query filtering / RLS) | Module 6 (post-MVP) | `tenant_id` columns already in place — no backfill needed |
| GDPR Art. 17 erasure routine | M1-03 (Sprint 2) | Soft-delete is retention, not erasure — see TODO in `participants/models.py` |
