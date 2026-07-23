# EOWE Workspace

Mini-ERP + e-commerce platform for European Open Water Events.
Backend: FastAPI + SQLAlchemy 2.0 + Alembic + PostgreSQL (`backend/`).
Frontend: React 19 + TypeScript + Vite (`frontend/`). Docker Compose for local dev.

## Required reading — load BOTH before writing or modifying any code

1. **`DOCS/SECURITY_STANDARDS.md`** — binding security policy. Wins on any
   conflict with other documents.
2. **`DOCS/DEVELOPMENT_GUIDE.md`** — architecture (module-first,
   controller/service/repository), layer + import rules, step-by-step recipes for
   adding modules and features, testing conventions, and the Definition of Done.

Read both in full at the start of any coding task — do not rely on this summary.

## Security — MANDATORY

**Before writing or modifying any code, read `DOCS/SECURITY_STANDARDS.md`
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

---

# Coding Conventions

Rules every developer **and AI assistant** must follow when writing code in this repo.
These are not suggestions — a PR that breaks them should be sent back. On any conflict,
`SECURITY_STANDARDS.md` wins over this section. The code blocks below are **illustrative** —
they show the pattern to follow, not necessarily code that already exists.

## How to use this section

- **Read it before writing code.** Match what already exists; don't invent new patterns.
- **Backend** = FastAPI + SQLAlchemy 2.0 (Python 3.10). **Frontend** = React 19 + Vite + TypeScript.
- Formatting/linting is enforced by tools, not by taste: **Ruff** on the backend, **Prettier + ESLint** on the frontend. Run them before committing:
  - Backend: `ruff check . && ruff format .`
  - Frontend: `npm run lint && npm run format`

---

## 1. Don't duplicate code

**One-liner:** If you write the same logic twice, extract it.

**Why:** Duplicated logic drifts out of sync — a bug fixed in one copy stays broken in the other. One source of truth is cheaper to change, test, and reason about. Reusable backend logic belongs in a service or a shared helper; reusable frontend logic belongs in a hook or a util — not copy-pasted into each caller.

**❌ Bad** — same query logic copy-pasted into two routes:

```python
@router.get("/events/{id}")
def get_event(id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == id, Event.deleted_at.is_(None)).first()
    if not event:
        raise HTTPException(404, "Not found")
    return event

@router.put("/events/{id}")
def update_event(id: int, ...):
    event = db.query(Event).filter(Event.id == id, Event.deleted_at.is_(None)).first()  # duplicated
    if not event:
        raise HTTPException(404, "Not found")
    ...
```

**✅ Good** — one helper, reused:

```python
def get_event_or_404(db: Session, event_id: int) -> Event:
    event = db.query(Event).filter(Event.id == event_id, Event.deleted_at.is_(None)).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
```

---

## 2. Avoid N+1 queries

**One-liner:** Never fire one query per row in a loop — load related data in a single query.

**Why:** An N+1 pattern turns one list endpoint into hundreds of round-trips to Postgres. It looks fine on 5 rows in dev and falls over on 5,000 in production. SQLAlchemy 2.0 has first-class eager loading — use it.

**❌ Bad** — one query for the list, then one more per row (N+1):

```python
events = db.query(Event).all()
for event in events:
    print(event.owner.name)   # triggers a separate SELECT for every event
```

**✅ Good** — eager-load the relationship up front:

```python
from sqlalchemy.orm import selectinload

events = db.query(Event).options(selectinload(Event.owner)).all()
for event in events:
    print(event.owner.name)   # already loaded, zero extra queries
```

- Use `selectinload` for collections (one-to-many) and `joinedload` for single relations (many-to-one) you always need.
- When you only need a few columns, select them explicitly instead of loading full objects.

---

## 3. Reuse existing components, hooks, and utilities first

**One-liner:** Search before you build — check whether it already exists.

**Why:** Re-implementing a hook or component you didn't know existed creates two things to maintain and two ways for them to disagree. Reuse keeps behaviour and styling consistent. Before writing something new, check the shared UI components, the hooks, and the util/helper modules; on the backend, check existing services and core helpers before adding logic to a route.

> Rule of thumb: if logic uses React state/effects and is needed in more than one component, it's a **hook**, not copy-pasted `useState`/`useEffect`.

**❌ Bad** — inlining fetch + loading state in every component:

```tsx
function EventsList() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/events`)
      .then((r) => r.json())
      .then((d) => { setEvents(d); setLoading(false); });
  }, []);
  // ...same block re-pasted in EventDetail, Dashboard, ...
}
```

**✅ Good** — one hook, reused everywhere:

```tsx
export function useEvents() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/events`)
      .then((r) => r.json())
      .then((data) => {
        setEvents(data);
        setLoading(false);
      });
  }, []);
  return { events, loading };
}

// usage:
const { events, loading } = useEvents();
```

---

## 4. Follow the existing style & structure — no "vibe-coded" one-offs

**One-liner:** New code should look like it was written by the same person who wrote the rest.

**Why:** Consistent structure and naming make the codebase navigable and reviewable. One-off folder layouts, naming schemes, or import styles cost every future reader time and break tooling assumptions.

### Backend conventions (enforced by Ruff — line length 100, double quotes)

- **Layout** — keep the existing module structure; add new code to the matching layer (routes, models, schemas, services, core), don't flatten it.
- **Imports** are sorted by Ruff's isort: stdlib → third-party → app imports, blank line between groups. Don't hand-order them.
- **Naming:** `snake_case` for functions/vars/modules, `PascalCase` for classes/models/schemas.
- **DB access** always goes through the `get_db` dependency — never construct a session inline:

  **❌ Bad**
  ```python
  @app.get("/health")
  def health():
      db = SessionLocal()           # bypasses DI, never closed cleanly
      db.execute(text("SELECT 1"))
  ```
  **✅ Good**
  ```python
  @app.get("/health")
  def health(db: Session = Depends(get_db)):
      db.execute(text("SELECT 1"))
      return {"status": "ok"}
  ```
- **Config/secrets** come from the `settings` object — never read `os.environ` directly or hardcode a value.

### Frontend conventions (enforced by Prettier — semicolons, single quotes, trailing commas, width 100)

- **Components:** `PascalCase` files and function names (`EventCard.tsx`). **Hooks:** `useCamelCase` (`useEvents.ts`). **Helpers/vars:** `camelCase`.
- **Function components only** — no class components.
- **Respect the Rules of Hooks** — `eslint-plugin-react-hooks` is on and will fail the build. Call hooks at the top level, list effect dependencies.
- **TypeScript is strict** (`noUnusedLocals`, `noUnusedParameters`). Don't leave unused imports/vars; avoid `any`.
- **Quotes/semicolons/commas:** let Prettier decide — don't fight it by hand.

**❌ Bad** — one-off style that fights the tooling:

```tsx
import { useState } from "react"      // double quotes, no semicolon
export const app = () => {            // arrow + lowercase name
    let Count=0                       // wrong casing, no spacing
    return <div>{Count}</div>
}
```

**✅ Good** — matches the repo's style:

```tsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount((c) => c + 1)}>Count is {count}</button>;
}

export default Counter;
```

---

### Before you finish a task

- [ ] No copy-pasted logic — shared code extracted into a service, helper, hook, or util.
- [ ] No query inside a loop — relationships eager-loaded.
- [ ] Checked for an existing component / hook / service before writing something new.
- [ ] `ruff check . && ruff format .` clean (backend); `npm run lint && npm run format` clean (frontend).
- [ ] File names, naming, and imports match the existing structure.
- [ ] Ran `/security-check` and addressed any Critical/High findings (see Security — MANDATORY above).
