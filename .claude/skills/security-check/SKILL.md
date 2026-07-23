---
name: security-check
description: Audit code against EOWE's SECURITY_STANDARDS.md. Use after completing any coding task, before committing, when the user asks to verify security compliance, or when reviewing a PR/diff. Checks auth/RBAC coverage, secrets, SQL safety, PII logging, GDPR handling, and the full §13 checklist, then produces a pass/fail report with file:line findings.
---

# EOWE Security Compliance Check

You are auditing this repository against `SECURITY_STANDARDS.md` (repo root). That file
is the **source of truth** — this skill tells you how to check it, not what the rules
are. If this skill and the standards file ever disagree, the standards file wins.

## Step 0 — Load the standard and determine scope

1. Read `SECURITY_STANDARDS.md` in full. Do not audit from memory.
2. Determine audit scope:
   - **If an argument was given** (e.g. `/security-check full`, `/security-check backend/app/api`),
     audit that scope: `full` = entire repo; a path = that subtree.
   - **Otherwise, default to the change set**: `git status` + `git diff` (unstaged),
     `git diff --cached` (staged), and `git diff main...HEAD` if on a branch.
     If there are no changes at all, fall back to a full audit and say so.
3. For diff-scope audits: audit every changed file **in full** (not just changed lines) —
   a changed line can activate a vulnerability elsewhere in the file. Also open any file
   that a changed file imports auth/deps/schemas from, to verify the chain actually
   enforces what the route assumes.

## Step 1 — Mechanical sweeps (run all of these)

Run these searches over the scope. Every hit must be either cleared with a stated reason
or reported as a finding. Do not skip a sweep because it "probably doesn't apply".

**Secrets (Standard §0.1, §7):**
- Grep for: `secret`, `password`, `token`, `api[_-]?key`, `BEGIN (RSA|EC|OPENSSH) PRIVATE KEY`,
  `postgres://`, `postgresql://`, `sk_live`, `sk_test`, `whsec_`, `AKIA[0-9A-Z]{16}`,
  `eyJ[A-Za-z0-9_-]{10,}` (hardcoded JWTs) — in source, tests, migrations, docs, compose files.
- Check `.env` is git-ignored and **not tracked**: `git ls-files | grep -E '\.env$'` must be empty.
- Check `.env.example` contains placeholder values only.
- Check no `VITE_` variable carries a secret (frontend §7).
- Check Dockerfiles: no `COPY .env`, no secrets in `ENV`/`ARG`.
- If a secret appears in **git history** (`git log -p` on suspicious files when warranted):
  report as Critical — rotation required, not just deletion.

**SQL safety (§0.3, §5):**
- Grep backend for: `text(f`, `text(".*%s`, `text(".*{`, `execute(f`, `f"SELECT`, `f"INSERT`,
  `f"UPDATE`, `f"DELETE`, `% (`, `.format(` near SQL keywords, string `+` concatenation
  building queries, `getattr(` used with request-derived names for columns/order_by.
- Check Alembic migrations (`alembic/versions/` or equivalent) for raw SQL with
  interpolated values.

**Auth & RBAC (§2, §3):**
- Enumerate every route in scope (`@app.get|post|put|patch|delete`, `@router.*`).
  For each route verify: (a) it has `get_current_user`/`require_roles` (or equivalent
  from `app/api/deps.py`) in its dependency chain, or (b) it carries a `# PUBLIC: <reason>`
  comment. Anything else is a High finding.
- For each mutating route (`POST/PUT/PATCH/DELETE`): confirm Read-only role is excluded.
- For each route taking an object ID: confirm an ownership/tenant check exists before
  returning or mutating the object (IDOR, §3).
- JWT code: `algorithms=[...]` pinned on every decode; no `verify_signature=False`,
  `verify_exp` disabled, or `options={` weakening verification outside tests that assert
  rejection; refresh-token handling checks the `type` claim; no PII in JWT claims.
- Password handling: bcrypt/argon2 only — grep for `md5`, `sha1(`, `sha256(` near password code.

**Schemas & responses (§4):**
- Every route has `response_model=`. Flag routes returning ORM objects or bare dicts of
  model data.
- Request schemas use `extra="forbid"`. Flag request bodies typed as `dict`, `Any`,
  or raw `Request` parsing.
- Response schemas: check none expose `password_hash`, `hashed_password`, tokens, or C3
  fields (IBAN etc.) where not strictly needed.
- List endpoints: pagination present with an enforced cap.
- Money fields: `Decimal`/`condecimal`, never `float`.

**PII & logging (§1, §12):**
- Grep for `logger.`, `logging.`, `print(`, Sentry calls — inspect each for interpolation
  of: email, name, iban, phone, address, dob, token, authorization headers, full request
  bodies on C2/C3 endpoints.
- Test files / fixtures / seeds: no realistic personal data.
- Check no tokens are passed in URL query strings.

**Frontend (§4, §7):**
- Grep for `dangerouslySetInnerHTML` (any hit with user-touched data = High; even
  static usage must be justified), `eval(`, `new Function(`, `innerHTML`,
  `localStorage`/`sessionStorage` used for tokens, `window.open(` / `href=` built from
  user data, `http://` hardcoded URLs (non-localhost).

**Transport, external calls & webhooks (§6, §8):**
- CORS config: no `allow_origins=["*"]`; flag `allow_methods`/`allow_headers` wildcards
  once auth exists (currently a tracked gap — see standard §14, report as Info until F-05 lands).
- Grep for `verify=False`, `ssl._create_unverified`, `check_hostname = False`.
- Every `httpx`/`requests`/`urllib` call has a timeout.
- Webhook handlers verify provider signatures before parsing; handlers are idempotent.
- No URL fetched from user-supplied input (SSRF).

**Migrations & DB (§5):**
- Every new migration has a non-trivial `downgrade()`.
- New core-entity mutations write audit-log entries (once the audit module exists;
  before then, flag the absence as a Medium with reference to F-08).
- Soft-delete convention followed on core entities.

**Dependencies & Docker (§10, §11):**
- If `requirements.txt`, `package.json`, or lockfiles changed: run
  `pip install pip-audit && pip-audit -r backend/requirements.txt` (or `pip-audit` in the
  venv) and `npm audit --omit=dev` in `frontend/`. High/Critical on production deps = High finding.
- New dependencies: pinned, maintained, actually needed, name checked for typosquatting.
- Dockerfile changes: non-root `USER` for prod targets, no `--reload` in prod CMD,
  no dev-deps in prod images.

**AI code paths (§9)** — if scope touches email intake, payment matching, or photo features:
- Verify AI output lands as a pending suggestion and a separate human-triggered,
  role-checked endpoint confirms it. Any path where model output directly mutates
  financial/customer-facing state = Critical.
- Verify LLM output is validated against a strict schema before persistence.
- Verify no C3 data (IBAN etc.) is sent to external AI services; PII minimized.
- Photo/face features: must not exist without documented consent handling (Critical if scaffolded).

## Step 2 — §13 checklist verdict

Go through the §13 pre-commit checklist in `SECURITY_STANDARDS.md` **item by item** and
record for each: ✅ pass / ❌ fail (with finding reference) / ➖ not applicable (with a
one-clause reason). Every item gets one of the three — no silent skips.

## Step 3 — Report

Do **not** auto-fix anything unless the user asked for fixes; this skill's job is the audit.
(Offer to fix at the end.) Produce the report as your final message:

```
## Security Check — <scope> — <PASS | FAIL>

### Findings (most severe first)
[SEV] file:line — §<rule> — one-line description
      Impact: <what an attacker/auditor gains>
      Fix: <concrete change>

### §13 Checklist
✅/❌/➖ per item, one line each

### Cleared items worth noting
<hits from sweeps that were investigated and are fine, with the reason — so reviewers
don't re-litigate them>
```

Severity scale:
- **Critical** — exploitable now or a leaked secret: committed credentials, SQLi,
  auth bypass, AI auto-executing financial actions, PII sent to unapproved third party.
- **High** — missing required control: unauthenticated non-public endpoint, missing
  ownership check, missing webhook signature verification, PII in logs, token in localStorage.
- **Medium** — weakens defense-in-depth: missing pagination cap, missing `extra="forbid"`,
  missing timeout, unpinned dep, missing `downgrade()`.
- **Low / Info** — hygiene or tracked gaps (§14 items reported as Info until their trigger point).

**Verdict rule: any Critical or High finding = FAIL.** Medium-only = PASS with warnings.
If a finding matches a known gap in standard §14, report it as Info and reference §14
rather than failing the audit — unless the diff makes the gap *worse*.

Findings must cite real `file:line` locations you verified by reading the file — never
report a grep hit you didn't open and confirm. If you cannot verify something within
scope (e.g. a tool fails), list it under "Not verified" rather than guessing.
