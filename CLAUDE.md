# EOWE Workspace

Mini-ERP + e-commerce platform for European Open Water Events.
Backend: FastAPI + SQLAlchemy 2.0 + Alembic + PostgreSQL (`backend/`).
Frontend: React 19 + TypeScript + Vite (`frontend/`). Docker Compose for local dev.

## Required reading — load BOTH before writing or modifying any code

1. **`SECURITY_STANDARDS.md`** (repo root) — binding security policy. Wins on any
   conflict with other documents.
2. **`DEVELOPMENT_GUIDE.md`** (repo root) — architecture (module-first,
   controller/service/repository), layer + import rules, step-by-step recipes for
   adding modules and features, testing conventions, and the Definition of Done.

Read both in full at the start of any coding task — do not rely on this summary.

## Security — MANDATORY

**Before writing or modifying any code, read `SECURITY_STANDARDS.md` in the repo root
and follow it exactly.** It is binding for all agents and humans. Key points you must
never violate even without reading it: no secrets in code or commits; every endpoint
authenticated + role-checked (RBAC) unless marked `# PUBLIC:`; no string-built SQL;
participant data is GDPR-protected — never log PII or send it to external services;
AI features are suggestion-only (human-in-the-loop). Complete the §13 pre-commit
checklist from that file before declaring any task done, and include a "Security
notes" section in your final output.

After completing any coding task and before committing, run the **security-check**
skill (`/security-check`) to audit your changes against the standard. A FAIL verdict
(any Critical/High finding) must be fixed before the task is considered done.
