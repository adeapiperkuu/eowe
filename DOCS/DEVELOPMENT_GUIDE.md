# EOWE Workspace — Development Guide

> **Audience: every AI agent and human developer implementing features in this repo.**
>
> **Read order — mandatory before writing any code:**
> 1. `SECURITY_STANDARDS.md` (repo root) — **binding** security policy. If this guide and
>    the security standard ever conflict, the security standard wins; stop and flag it.
> 2. This document — architecture, conventions, and the step-by-step recipes below.
>
> The older NestJS plan in `DOCS/` is **not** the implemented stack. The docs remain the
> source of truth for *scope and requirements* (modules M1–M6, sprint plan), but all
> technology decisions below reflect the actual code.

---

## 1. Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.10), SQLAlchemy 2.0, Alembic, PostgreSQL, Pydantic v2 |
| Auth | JWT access + refresh (prefer **PyJWT** over python-jose, see SECURITY_STANDARDS §11), passlib/bcrypt, RBAC roles: Admin, Management (GF), Staff, Read-only |
| Frontend | React 19 + TypeScript + Vite; React Query, React Hook Form + Zod (per requirements F-07) |
| Infra | Docker Compose local stack; CI/CD with auto-deploy to staging |

---

## 1.1 Tooling — lint, format, types (run before declaring any task done)

The config files are the source of truth; this section just tells you where they are
and how to run them. **Never edit a config, add an ignore/disable comment, or loosen a
compiler option to silence an error** — fix the code, or flag the rule if you believe
it's wrong.

**Backend** (`backend/`, configs in `pyproject.toml`; ruff pinned in
`requirements-dev.txt`):

```
.venv\Scripts\python -m ruff check .            # lint (rules: E, F, I, UP, B, SIM)
.venv\Scripts\python -m ruff format .           # format (line length 100, double quotes)
```

Ruff's `I` rule handles import sorting — never hand-order imports. `fastapi.Depends`
/ `Query` / `Path` in default arguments are already exempted from B008; don't add
`# noqa` for them.

**Frontend** (`frontend/`, configs: `eslint.config.js`, `.prettierrc`,
`tsconfig.app.json` + `tsconfig.node.json`):

```
npm run lint            # ESLint (typescript-eslint, react-hooks, react-refresh)
npm run format          # Prettier (single quotes, semi, trailing commas, width 100)
npm run format:check    # CI-style check without writing
npm run build           # tsc -b (type-check, strict mode) + vite build
```

TypeScript runs with `"strict": true` — no `any` escapes, no `@ts-ignore`
(`@ts-expect-error` with a reason comment is acceptable in tests only). ESLint's
react-hooks rules are not to be disabled per-line; restructure the hook instead.

Prettier and ruff-format own all formatting decisions — never argue with them in
review or hand-format against them.

---

## 2. Architecture: modules × layers

The backend is organized **module-first** (mirroring ERP modules M1–M6 from the
requirements doc), and **within each module** by the controller–service–repository
pattern. In FastAPI the "controller" is the router.

```
backend/app/
├── main.py                  # app factory; mounts the aggregated v1 router
├── core/                    # config (Settings), security helpers, exceptions
├── db/                      # engine, session, Base, shared mixins (soft-delete, timestamps)
├── common/                  # cross-module shared code: pagination, base repository, audit
├── api/
│   ├── deps.py              # get_current_user, require_roles — the ONLY auth deps (canonical)
│   └── v1/__init__.py       # aggregates all module routers under /api/v1
├── modules/
│   ├── auth/                # users, roles, login/refresh          (Sprint 1)
│   ├── events/              # Series, Event, Race, Distance        (M1)
│   ├── participants/        # registry, wetsuit AI, shirt sizes    (M1)
│   ├── documents/           # S3 storage, SharePoint hook          (S2)
│   ├── contracts/           # digital contracts                    (M2)
│   ├── finance/             # Qonto, payment matching, DATEV       (M2)
│   ├── marketing/           # campaigns, Grid Sports assets        (M4)
│   ├── partners/            # sponsor CRM, alerts                  (M5)
│   └── shop/                # catalog, checkout, inventory         (M3)
└── integrations/            # one package per external system:
    ├── tiger_timing/        #   thin API client only — no business logic
    ├── raceresult/
    ├── qonto/
    └── datev/
```

Every module folder has the same five files (plus tests):

```
modules/<name>/
├── __init__.py
├── router.py        # controller — HTTP concerns only
├── service.py       # business logic — the only layer with rules/decisions
├── repository.py    # all DB access for this module's models
├── models.py        # SQLAlchemy entities
└── schemas.py       # Pydantic request/response DTOs
```

### 2.1 Layer responsibilities — what goes where

| Layer | DOES | NEVER |
|---|---|---|
| **router.py** | Declare path + HTTP method; attach `Depends(require_roles(...))`; validate via request schema; set `response_model`; call one service function; map domain exceptions to HTTP errors | Business logic, DB queries, imports of SQLAlchemy models into signatures, loops over query results |
| **service.py** | Business rules, orchestration, transactions (commit/rollback), calls to repositories and `integrations/` clients, audit-log writes, human-in-the-loop state machines | Direct `db.execute`/`select()` construction, HTTP concerns (status codes, headers), importing from `fastapi` |
| **repository.py** | Construct and execute queries; apply soft-delete filtering; pagination; return ORM models or None | Committing (the service owns the transaction), business decisions, raising HTTP exceptions |
| **models.py** | Table definitions, relationships, constraints, mixins | Behavior/business methods beyond trivial properties |
| **schemas.py** | Request schemas (`extra="forbid"`), response schemas (explicit fields), enums shared with the frontend contract | Being reused as ORM models; catch-all `dict`/`Any` fields |

### 2.2 Import rules (module boundaries — enforced in review)

- `router → service → repository → models` — one direction only, never skip layers
  (a router never imports a repository), never backwards.
- A module may import from `core/`, `db/`, `common/`, `api/deps.py`, and its **own** files.
- A module must **not** import another module's `repository.py` or `models.py`
  internals. Cross-module needs go through the other module's **service** function, or
  through an explicit relationship defined on the shared data model. If two modules keep
  reaching into each other, raise it — that's a boundary design smell, not something to
  route around.
- `integrations/*` clients are called **only from services**, never from routers, and
  contain no business logic themselves (they translate HTTP ↔ typed Pydantic objects,
  with timeouts + retry/backoff per SECURITY_STANDARDS §8).

---

## 3. Recipe: adding a new module

Work top-down on the data, bottom-up on the code:

1. **Check the requirements doc** (`DOCS/EOWE_Technical_Requirements.docx`, section 5)
   for the module's task IDs (e.g. M1-01…) and confirm scope with the sprint plan.
2. **Create the folder** `modules/<name>/` with the five standard files.
3. **models.py** — define entities using the shared mixins from `db/`:
   - UUID primary keys (`id: Mapped[uuid.UUID]`, server default `gen_random_uuid()`),
   - `created_at` / `updated_at` (UTC, server defaults),
   - `deleted_at` soft-delete column on core entities,
   - `Numeric`/`Decimal` for money — never float.
   Register the models in `db/base.py` so Alembic sees them.
4. **Migration** — `alembic revision --autogenerate -m "<module>: <what>"`, then
   **read the generated file** (autogenerate misses constraints/indexes), ensure a
   working `downgrade()`.
5. **schemas.py** — separate `XCreate` / `XUpdate` / `XRead` schemas. Request schemas:
   `model_config = ConfigDict(extra="forbid")`, length limits, enums, `EmailStr`,
   `Decimal` for money. Response schemas: explicit field lists only.
6. **repository.py** — extend the base repository from `common/` (gives soft-delete
   filtering + pagination); add module-specific queries. Sort/filter params map through
   an allowlist dict, never `getattr(Model, user_input)`.
7. **service.py** — business logic; writes audit-log entries for mutations on core
   entities (SECURITY_STANDARDS §5); owns the transaction.
8. **router.py** — every route gets `Depends(require_roles(...))` (deny by default —
   see SECURITY_STANDARDS §3 for the role rules) **and** a `response_model`. List
   endpoints are paginated with a hard cap. Object-level ownership checks on every
   ID-taking route.
9. **Mount it** — add the router to `api/v1/__init__.py` with a prefix and tags.
10. **Tests** — see §6 below. Then run the **Definition of Done** checklist (§7).

## 4. Recipe: adding a feature to an existing module

1. Read the module's existing `service.py` and `schemas.py` first — extend the
   established patterns; do not introduce a parallel style.
2. Schema change? → new/updated schema with the same strictness rules.
3. Data change? → model + migration (reversible).
4. Logic goes in the service; queries in the repository; the router stays thin.
5. New external call? → put the client in `integrations/`, config in `Settings`
   (+ name-only entry in `.env.example`).
6. Run the Definition of Done checklist (§7).

### 4.1 AI-assisted features (email intake, payment matching, tagging)

Human-in-the-loop is **architectural** (SECURITY_STANDARDS §9): the AI path writes a
*suggestion* row (`status=pending_review`, confidence, model ref); a separate
role-checked endpoint lets a human confirm or reject; only the confirm endpoint mutates
real state. Never collapse these into one code path.

### 4.2 Async / long-running work

Imports, exports, CV tagging run async (background task or worker), never inline in a
request handler. The route returns a job/entity ID immediately; status is polled or
pushed. Failures are logged and surfaced — never silently dropped.

---

## 5. Frontend structure

Mirror the module layout:

```
frontend/src/
├── components/          # design system: shared UI primitives (Sprint 1, F-06)
├── lib/                 # API client, React Query setup, auth context, error/toast
├── features/
│   ├── auth/
│   ├── events/
│   │   ├── api.ts       # typed endpoint calls + React Query hooks for this feature
│   │   ├── components/  # feature-specific components
│   │   └── types.ts     # mirrors backend schemas
│   └── ...
└── routes/              # route definitions + auth guards
```

Rules:

- All server state through **React Query** (no hand-rolled fetch-in-useEffect);
  all forms through **React Hook Form + Zod**, with the Zod schema mirroring the
  backend Pydantic schema.
- Role-based UI hiding is UX only — the backend enforces the real check
  (SECURITY_STANDARDS §3).
- No `VITE_*` variable may hold a secret; no `dangerouslySetInnerHTML` (§4, §7 of the
  security standard).

### 5.1 Recipe: adding a frontend feature

1. **Backend contract first** — the endpoint and its Pydantic schemas exist (or are
   agreed) before UI work starts; don't invent response shapes in the frontend.
2. **types.ts** — mirror the backend `XRead`/`XCreate` schemas as TypeScript types and
   a Zod schema. Field names and optionality must match the Pydantic definitions
   exactly; when the backend schema changes, this file changes in the same PR.
3. **api.ts** — typed functions using the shared API client from `lib/`, wrapped in
   React Query hooks (`useEventsQuery`, `useCreateEventMutation`). Query keys follow
   `[<feature>, <entity>, params]` (e.g. `['events', 'list', filters]`); mutations
   invalidate the affected keys.
4. **components/** — build from design-system primitives in `src/components/`; only
   create feature-local components for feature-specific composition. Forms: React Hook
   Form + the Zod schema from step 2; server-side validation errors are surfaced to the
   user, never swallowed.
5. **Route + guard** — register the page in `routes/` behind the auth guard with the
   same role list the backend enforces.
6. **States** — every data view handles loading, empty, and error states via the shared
   error/toast handling from `lib/` (F-07); no raw unhandled promise rejections.

### 5.2 Frontend testing

- **Zod schemas / logic**: unit tests (Vitest) for non-trivial validation and any
  client-side computation (e.g. size aggregation display logic).
- **Components with behavior** (forms, human-in-the-loop review UIs): React Testing
  Library — happy path + validation-error path, mocking at the API-client boundary
  (MSW or query-client mocks), not by stubbing React Query internals.
- Purely presentational design-system components need no dedicated tests beyond lint
  and type-checking; `tsc -b` passing is part of Done (it's in `npm run build`).

---

## 6. Testing

- **Services** carry the business logic, so they carry the tests: unit-test them with
  repository fakes or a test DB session — this satisfies the "unit tests on business
  logic" NFR.
- **Routers** get thin integration tests via `TestClient`: happy path + one 401 + one
  403 (wrong role) per protected route. Auth in tests via dependency overrides —
  never by removing RBAC from the route.
- **Repositories** with real queries (test database), especially soft-delete filtering
  and pagination caps.
- Test data is obviously fake (SECURITY_STANDARDS §1) — never real participant data.
- Migrations: `upgrade` + `downgrade` must both run in CI.

---

## 7. Definition of Done — every task, no exceptions

1. Code follows the layer rules (§2.1) and import rules (§2.2).
2. Migrations reversible; models registered in `db/base.py`.
3. Tests per §6 pass; all tooling commands in §1.1 pass (ruff check + format,
   ESLint, Prettier check, `tsc -b` via `npm run build`).
4. **The full pre-commit checklist in `SECURITY_STANDARDS.md` §13 is completed** —
   it is not duplicated here on purpose; open the file and walk it.
5. Run the **security-check skill** (`/security-check`) on your changes; any
   Critical/High finding is fixed before the task is done.
6. Final output/PR includes the "Security notes" section required by
   SECURITY_STANDARDS §13.
7. New settings → `Settings` class + name-only `.env.example` entry; new dependencies
   → pinned version + justification in the PR.

---

*Document owner: Lum (backend lead). Update this guide in the same PR when a structural
convention changes. Scope/requirements questions → `DOCS/`; security questions →
`SECURITY_STANDARDS.md` (which wins on conflict).*
