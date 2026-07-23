# EOWE Workspace — Security Standards

> **Audience: every AI agent and human developer working in this repository.**
> These rules are **mandatory**. If a task conflicts with this document, stop and flag the
> conflict instead of proceeding. If a rule seems inapplicable, say so explicitly in your
> output — never silently skip it.
>
> Stack this document targets (the *actual* code, not the older NestJS plan in DOCS/):
> **Backend:** FastAPI (Python 3.10), SQLAlchemy 2.0, Alembic, PostgreSQL, Pydantic v2,
> passlib/bcrypt, JWT. **Frontend:** React 19 + TypeScript + Vite. **Infra:** Docker Compose,
> CI/CD with auto-deploy to staging.

---

## 0. Non-negotiables (read first)

1. **Never commit secrets.** No API keys, passwords, JWT secrets, DB URLs with credentials,
   or tokens in source code, migrations, tests, fixtures, docs, or commit messages.
   Secrets live only in `.env` (git-ignored) and the deployment secret store.
   `.env.example` must contain variable **names only**, with placeholder values like
   `changeme` — never real values.
2. **Every API endpoint is authenticated and role-checked by default.** The only
   deliberate exceptions: `/health`, login, refresh, and (later) explicitly public
   e-commerce catalog endpoints. Adding a new unauthenticated endpoint requires a code
   comment `# PUBLIC: <reason>` and a mention in the PR description.
3. **Never build SQL by string concatenation or f-strings.** Use SQLAlchemy ORM /
   bound parameters. This includes `text()` fragments, `order_by` from user input, and
   raw statements in Alembic migrations.
4. **All user input is untrusted** — including input from EOWE staff, uploaded files,
   emails parsed by the AI intake, webhook payloads, and data returned by integrations
   (Tiger Timing, RaceResult, Qonto, DATEV, Stripe).
5. **Participant data is GDPR-protected personal data.** Names, emails, phone numbers,
   dates of birth, IBANs, contracts, health notes, and photos must never be logged,
   never leave the EU-hosted infrastructure, and never be sent to third-party services
   without an explicit, documented decision by the team (not by an agent).
6. **AI features are human-in-the-loop only.** No AI-driven code path may auto-execute
   customer-facing or financial actions (send email to a customer, match/settle a
   payment, alter a contract). AI output is a *suggestion* that a human confirms.
7. **If you are unsure whether something is a security issue — treat it as one** and
   surface it in your final message instead of guessing.

---

## 1. Data classification

| Class | Examples | Rules |
|---|---|---|
| **C3 – Sensitive PII / financial** | IBAN, payment records, contracts, health/medical notes, ID documents | Encrypted at rest; never logged; never in test fixtures with real values; access restricted to Admin/Management roles; export only via audited endpoints |
| **C2 – PII** | Participant name, email, phone, DOB, address, photos of persons | Never logged in plaintext; pseudonymize in analytics; soft-delete + hard-delete path required (GDPR Art. 17 erasure) |
| **C1 – Internal** | Event configs, inventory, internal notes, non-personal business data | Auth + RBAC required; normal handling |
| **C0 – Public** | Published event pages, shop catalog | May be served unauthenticated once explicitly marked public |

Rules that follow from this:

- **Logging:** log user *IDs*, never names/emails. Log payment *references*, never IBANs
  or card data. Before adding any `logger.*` call or Sentry breadcrumb, check the
  interpolated values against this table.
- **Test data:** use obviously fake data (`test+p1@example.com`, IBAN test values like
  `DE89370400440532013000` clearly marked as the official test IBAN). Never copy real
  participant rows into tests, seeds, or fixtures.
- **GDPR erasure:** every model holding C2/C3 data must support both soft-delete
  (business workflow) and a true erasure path (anonymization or hard delete) for
  Art. 17 requests. When creating such a model, add it to the erasure routine or note
  the TODO explicitly in the PR.
- **Photos** (future CV photo-tagging module): face recognition creates biometric data —
  a GDPR special category. Any work on this module requires explicit consent handling
  and must be flagged to the team before implementation; agents must not scaffold it
  speculatively.

---

## 2. Authentication

### 2.1 Passwords
- Hash with **bcrypt** (current: `passlib` + `bcrypt`) or argon2id. Never MD5/SHA-x,
  never reversible encryption, never plaintext — including "temporary" columns.
- Enforce a minimum length of **10 characters** at the schema level (Pydantic validator).
  Do not implement composition rules (uppercase/digit requirements) or password hints.
- Login errors are uniform: `"Invalid email or password"` — never reveal whether the
  email exists. Same for password-reset: always respond "if the account exists, an email
  was sent".
- Rate-limit login and password-reset endpoints (per-IP and per-account). If no rate
  limiter exists yet when you touch auth code, add `slowapi` or equivalent — do not ship
  an unthrottled login route.

### 2.2 JWT + refresh tokens
- **Access token:** short-lived (≤ 30 min, config `access_token_expire_minutes`),
  signed **HS256** with `secret_key` from settings. Claims: `sub` (user id), `exp`,
  `iat`, `type: "access"`, and the user's role. Never put PII (email, name) or anything
  C2/C3 in a JWT — payloads are only base64, not encrypted.
- **Refresh token:** long-lived (≤ 14 days), `type: "refresh"`, stored server-side
  (hashed) so it can be revoked; rotate on every use (issue new, invalidate old).
  A refresh token must never be accepted where an access token is expected —
  **always check the `type` claim** when decoding.
- **Verification:** always verify signature *and* expiry. Never use decode options that
  disable verification (`verify_signature=False`, `options={"verify_exp": False}`)
  outside of a test explicitly asserting rejection behavior.
- **Algorithm pinning:** pass `algorithms=["HS256"]` explicitly on every decode call.
  Never accept the algorithm from the token header (`alg: none` attacks).
- **Secret:** `secret_key` must be ≥ 32 random bytes. If you find a weak/default value
  (e.g. `"secret"`, `"changeme"`) in `.env`, flag it. Never generate and hard-code one.
- **Frontend storage:** keep tokens in memory (React state/module scope) with the
  refresh token in an **httpOnly, Secure, SameSite=Lax cookie** if cookie flow is used.
  Never `localStorage`/`sessionStorage` for refresh tokens. If the team has already
  chosen a storage pattern in `frontend/src`, follow it consistently; if you must
  deviate, flag it.
- **Logout** must invalidate the server-side refresh token, not just clear client state.

### 2.3 Auth dependency pattern (FastAPI)
All protected routes use a shared dependency chain — never re-implement token parsing
inline in a route:

```python
# app/api/deps.py (canonical location)
async def get_current_user(...) -> User: ...          # 401 if token invalid/expired
def require_roles(*roles: Role):                       # 403 if role not allowed
    def checker(user: User = Depends(get_current_user)) -> User: ...
    return checker
```

Usage: `Depends(require_roles(Role.ADMIN, Role.MANAGEMENT))`. Routes without any auth
dependency are treated as bugs in review unless marked `# PUBLIC:`.

---

## 3. Authorization (RBAC)

Roles (fixed by the requirements doc): **Admin**, **Management (GF)**, **Staff**,
**Read-only**.

- **Deny by default.** Every route declares which roles may call it. If a task doesn't
  specify roles, choose the most restrictive plausible set and state your choice in the
  PR/output.
- **Read-only means read-only:** the role may never reach a handler that mutates state.
  All `POST/PUT/PATCH/DELETE` routes must exclude Read-only.
- **Financial and contract endpoints** (payments, refunds, DATEV export, contract
  generation/signing, Qonto data): Admin + Management only, unless the requirements say
  otherwise.
- **Object-level checks (IDOR):** role checks are not enough. When a route takes an ID
  (`/participants/{id}`, `/contracts/{id}/download`), verify the object belongs to the
  caller's tenant/scope before returning it. Never rely on IDs being unguessable —
  and prefer UUIDs over sequential integers for externally visible IDs anyway.
- **No client-side-only enforcement.** Frontend route guards and hidden buttons are UX,
  not security. Every rule enforced in React must also be enforced in FastAPI.
- **Privilege changes** (role assignment, user activation) are Admin-only and must write
  an audit-log entry.

---

## 4. Input validation & output encoding

- **Pydantic schemas on every request body, query param set, and path param.** Routes
  must not accept `dict`, `Any`, or raw `Request` bodies. Use `model_config =
  ConfigDict(extra="forbid")` on request schemas so unexpected fields are rejected
  (mass-assignment protection): a participant-update schema must not silently accept
  `role` or `is_admin` fields.
- **Separate read/write schemas.** Response schemas explicitly list fields — never
  return ORM objects directly or use catch-all serialization; that's how
  `password_hash` leaks. `response_model=` is mandatory on every route.
- Constrain everything: `EmailStr` for emails, `condecimal`/`Decimal` for money (never
  float), length limits on all strings (`max_length`), enums for status fields, range
  checks on numbers, explicit date parsing.
- **Sorting/filtering params:** map user-supplied sort/filter fields through an
  allowlist dict to real column objects. Never `getattr(Model, user_input)` or
  interpolate into `order_by`.
- **Pagination is mandatory** on every list endpoint with an enforced `limit` cap
  (e.g. ≤ 200). Unbounded `SELECT *` list endpoints are a DoS and data-exfiltration
  vector.
- **File uploads** (contracts, photos, imports):
  - Validate by content (magic bytes / verified parse), not just extension or
    Content-Type header.
  - Enforce a size limit at both proxy and app level.
  - Generate the stored filename server-side (UUID); never use the client filename in a
    filesystem path (path traversal). Keep original name only as a DB metadata field.
  - Store outside the web root / in object storage; serve via authenticated endpoint,
    never by exposing the storage path directly.
  - CSV/XLSX imports: treat cell values as data — guard against formula injection when
    re-exporting (prefix `=`, `+`, `-`, `@` cells with `'`).
- **Frontend:** never use `dangerouslySetInnerHTML` with data that ever touched user
  input. If rich text/HTML rendering is genuinely required, sanitize with DOMPurify and
  say so in the PR. Never build URLs like `javascript:` from user data; validate
  redirect targets against an allowlist.

---

## 5. Database

- **ORM/bound parameters only** (see non-negotiable #3). This applies to Alembic
  migrations too — data migrations use `op.get_bind()` with bound params.
- **Migrations:** every migration must have a working `downgrade()` (reversible, per the
  requirements doc). Migrations never contain real personal data. Destructive
  migrations (dropping columns/tables with C2/C3 data) must be called out in the PR.
- **Soft-delete convention:** core entities get `deleted_at` (nullable timestamp);
  default queries exclude soft-deleted rows. Remember: soft-delete does **not** satisfy
  GDPR erasure — see §1.
- **Audit log (F-08):** every create/update/delete on core entities (Tenant, User, Role,
  Event, Participant, Product, Partner, Contract, Payment) writes an audit entry:
  who (user id), what (entity + id), when (UTC), action, and a diff of changed fields —
  with C3 field *values* redacted (log that the IBAN changed, not the IBAN).
  When adding a new core entity or mutation, wiring the audit log is part of the task,
  not optional.
- **Least privilege:** the application's DB user must not be a superuser and must not
  have DDL rights in production (migrations run under a separate role/step). Never put
  `postgres`/superuser credentials in the app's `DATABASE_URL` beyond local dev.
- **At-rest encryption** of C3 fields (IBAN etc.): use application-level encryption
  (e.g. Fernet with a key from settings, separate from `secret_key`) or rely on the
  hosting's disk encryption *plus* restricted column access — the choice is a team
  decision; agents implementing IBAN storage must raise it, not pick silently.
- Connection strings: TLS to the DB in staging/production (`sslmode=require` minimum).

---

## 6. API & transport hardening

- **CORS:** exact origins only, from settings — never `allow_origins=["*"]`, and never
  `*` together with `allow_credentials=True`. Restrict `allow_methods` and
  `allow_headers` to what's actually used (the current `["*"]` in `app/main.py` should
  be tightened when auth lands — acceptable for local dev only).
- **Error handling:** production responses never include stack traces, SQL errors,
  file paths, or library internals. Use exception handlers that return generic messages
  with an error ID; details go to logs/Sentry only. Never run uvicorn with `--reload`
  or debug mode in production images.
- **Security headers** (via middleware or reverse proxy):
  `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`,
  `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, and a
  CSP for the frontend (no `unsafe-eval`; document any `unsafe-inline` exception).
- **TLS 1.3** (doc requirement) terminates at the proxy; the app never serves plain
  HTTP outside the Docker network.
- **Rate limiting** on auth endpoints (see §2.1) and on expensive endpoints (exports,
  AI-backed routes, search).
- **HTTP methods:** state-changing operations are never `GET`. Idempotency keys for
  payment-related mutations.
- **Docs endpoints:** `/docs`, `/redoc`, `/openapi.json` are disabled or auth-gated in
  production.

---

## 7. Secrets & configuration

- All secrets flow through `pydantic-settings` (`app/core/config.py`) → environment →
  deployment secret store. Adding a new secret means: add the field to `Settings`, add
  the *name* to `.env.example`, document it in the PR. Nothing else.
- Never print, log, or return settings objects; `Settings.__repr__` leaking
  `secret_key` into a traceback counts as an incident. Prefer `SecretStr` for new
  secret fields.
- **Frontend:** every `VITE_*` variable is public — it is bundled into the JS shipped
  to browsers. No secret may ever be a `VITE_` variable. API keys for integrations
  live only in the backend.
- Never commit `.env`, dumps, backups, private keys, `*.pem`, kube/cloud configs.
  If you notice a secret already committed in git history, **stop and report it** —
  rotation is required; deleting the file is not enough.
- Docker images must not contain secrets (no `COPY .env`, no secrets in `ENV`/`ARG`
  layers). Compose injects them at runtime via `env_file`.

---

## 8. Integrations & webhooks (Tiger Timing, RaceResult, Qonto, DATEV, Stripe/PSP)

- **Inbound webhooks** (Stripe, Qonto): verify the provider's signature
  (`Stripe-Signature` with the webhook secret, using the SDK's constant-time
  verification) **before** parsing the body. Reject unsigned/invalid requests with 400
  and no detail. Make handlers idempotent (dedupe by event ID) — providers retry.
- **Never trust webhook payloads for money math.** After receiving a Stripe event,
  fetch the object from the API by ID rather than trusting the posted amounts, or at
  minimum verify amounts against your own records.
- **Card data:** we are never PCI-scope — card numbers never touch our servers or logs.
  Only PSP tokens/references are stored.
- **Outbound calls:** timeouts on every external request (connect + read), retries with
  backoff only for idempotent calls, and treat all responses as untrusted input
  (validate with Pydantic before persisting).
- **SSRF:** never fetch a URL that came from user input. Integration base URLs come
  from settings only. If a feature genuinely needs user-supplied URLs (e.g. partner
  logos), allowlist schemes/hosts and block private IP ranges — and flag the feature.
- **DATEV/accounting exports** contain C3 data: Admin/Management-only endpoints,
  audit-logged, delivered over authenticated channels only.

---

## 9. AI features (email intake, payment matching, photo tagging)

- **Human-in-the-loop is architectural, not cosmetic:** AI components write
  *suggestions* to the DB (e.g. `suggested_match`, `status=pending_review`); a separate,
  human-triggered, role-checked endpoint confirms them. There must be no code path
  where AI output directly mutates financial or customer-facing state.
- **Prompt injection:** email bodies, attachments, and any user-originated text fed to
  an LLM are adversarial. Instructions found inside such content must never be
  executed — never build flows where LLM output triggers tool calls / DB writes /
  outbound emails without the human confirmation step above. Treat LLM output itself as
  untrusted input: validate it against a strict Pydantic schema before storing.
- **Data minimization:** send an external LLM provider only the fields needed for the
  task; strip or pseudonymize IBANs and anything C3 first. Sending participant PII to
  any new external AI service requires a documented team decision (GDPR processor
  agreement) — an agent must not add such a call on its own.
- Log AI decisions (model, input reference, suggestion, confidence, reviewer, outcome)
  for auditability — with the same PII redaction rules as §1.

---

## 10. Docker & CI/CD

- **Production images:** run as a non-root user (`USER app`), no `--reload`, no dev
  dependencies, pinned base image (e.g. `python:3.10-slim` — move to digest pinning for
  prod), `pip install --no-cache-dir` with hashes where feasible. Multi-stage builds for
  the frontend (build → static serve); never ship `node_modules` or source maps with
  secrets.
- The current `backend/Dockerfile` (root user, `--reload`) is **dev-only**; a separate
  production Dockerfile/target is required before any deploy.
- **Compose/local:** never publish PostgreSQL or internal services on `0.0.0.0` in
  shared environments; bind dev-only ports to `127.0.0.1`.
- **CI/CD:**
  - Dependency audit in CI: `pip-audit` (backend) and `npm audit --omit=dev` (frontend);
    a High/Critical finding on a production dependency blocks merge.
  - Secret scanning (e.g. gitleaks) in CI.
  - CI logs must never echo secrets; mask env vars.
  - Auto-deploy to staging on merge to main is fine; production deploys are
    human-approved.
- **Backups** (doc requirement): nightly production DB backups, encrypted, EU-located,
  restore procedure documented and tested before go-live.

---

## 11. Dependencies

- Pin exact versions (`requirements.txt` already does; keep it that way). New
  dependencies need: active maintenance, a real need that stdlib/existing deps can't
  cover, and a name-check against typosquatting. State new deps prominently in the PR.
- Do not add heavyweight or obscure packages for trivial tasks; prefer FastAPI/
  SQLAlchemy/React ecosystem standards.
- **Known watch-item:** `python-jose` (current JWT lib) has a history of CVEs and slow
  maintenance. When touching auth, prefer migrating to **PyJWT**; at minimum verify the
  pinned version has no open advisories.
- Never disable or downgrade a security control to fix a build (e.g. removing hash
  checking, `npm audit --force`, `verify=False` on TLS). If a dependency conflict
  forces that choice, stop and report.

---

## 12. Logging, monitoring & incident hygiene

- Central rule: **logs are for IDs and events, not payloads.** Never log: passwords,
  tokens (including in URLs — never put tokens in query strings), IBANs, full request
  bodies of C2/C3 endpoints, `Authorization` headers, cookies.
- Configure Sentry (F-08) with `send_default_pii=False` and scrubbing for the field
  names used in this codebase (`password`, `iban`, `token`, `authorization`, ...).
- Audit log requirements are in §5. Auth events (login success/failure, logout, refresh,
  role change, password change) are always logged with user id + IP + timestamp.
- If you (an agent) discover an existing vulnerability, leaked secret, or suspicious
  code while doing an unrelated task: **do not silently fix or ignore it** — finish or
  pause your task and report it clearly in your final message, marked as a security
  finding.

---

## 13. Agent working rules & pre-commit checklist

**While coding:**
- Follow existing security patterns in the codebase (auth deps in `app/api/deps.py`,
  schemas in the owning module's `app/modules/<name>/schemas.py` — see
  `DEVELOPMENT_GUIDE.md`); do not invent parallel auth mechanisms.
- No "TODO: add auth later" on merged endpoints — auth ships with the endpoint.
- Do not weaken anything to make tests pass (skipping RBAC in test setup is fine via
  fixtures/overrides; removing RBAC from the route is not).
- Do not scaffold speculative features that touch C2/C3 data (see §1 photos note).

**Before declaring a task done, verify each applicable item:**

- [ ] No secrets/credentials in the diff (`git diff` reviewed line by line).
- [ ] Every new/changed route has an auth dependency + explicit role list, or a
      `# PUBLIC:` justification.
- [ ] Every new/changed route has a `response_model` and a request schema with
      `extra="forbid"`; no C3 fields in responses that don't need them.
- [ ] Object-level ownership checks on every ID-taking route.
- [ ] No string-built SQL anywhere in the diff (including migrations).
- [ ] List endpoints paginated with a hard cap.
- [ ] New mutations on core entities write audit-log entries.
- [ ] No new `logger`/`print`/Sentry call emits C2/C3 values or tokens.
- [ ] Migrations have a working `downgrade()`.
- [ ] New settings added to `Settings` + `.env.example` (names only).
- [ ] External calls have timeouts; webhook handlers verify signatures.
- [ ] Frontend: no `dangerouslySetInnerHTML`, no secrets in `VITE_*`, role checks
      duplicated server-side.
- [ ] `pip-audit` / `npm audit` clean for any dependency you added or bumped.

**In your PR description / final output, always include a short "Security notes"
section**: what auth/roles apply to new endpoints, what data classes are touched, and
any deviations from this document with justification.

---

## 14. Currently known gaps (do not copy these patterns)

Tracked here so agents don't treat existing code as precedent:

1. `app/main.py` CORS uses `allow_methods=["*"]`/`allow_headers=["*"]` — acceptable
   only until auth lands; tighten then.
2. `backend/Dockerfile` runs as root with `--reload` — dev-only; production target
   needed before first deploy.
3. `/health` executes a DB query unauthenticated — fine, but keep it free of any
   detail beyond `{"status": "ok"}`; never expand it into a diagnostics endpoint
   without auth.
4. No rate limiting exists yet — must be added together with the first auth endpoints
   (F-05), not after.
5. `python-jose` is pinned — see §11 watch-item; prefer PyJWT when implementing F-05.

*Document owner: Lum (backend lead). Update this file in the same PR whenever a rule
changes or a gap above is closed.*
