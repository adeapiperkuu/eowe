# EOWE Workspace

Monorepo for the EOWE workspace app:

- `backend/` — FastAPI + SQLAlchemy (Python 3.10)
- `frontend/` — React + Vite + TypeScript
- `docker-compose.yml` — run both services together

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (recommended)
- For local (non-Docker) work: Python 3.10+, Node.js 20+, npm

## Environment setup

Create a root `.env` file (gitignored — never commit it or `.env.example`):

```powershell
@"
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/postgres
SECRET_KEY=change-me-to-a-long-random-string
ACCESS_TOKEN_EXPIRE_MINUTES=30
"@ | Set-Content .env
```

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string (e.g. Supabase) |
| `SECRET_KEY` | JWT / app secret — use a long random string |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token lifetime (default `30`) |

## Run with Docker (recommended)

From the repo root:

```powershell
docker compose up --build
```

| Service | URL |
|---|---|
| Backend API | http://localhost:8000 |
| Health check | http://localhost:8000/health |
| Frontend | http://localhost:5173 |

Stop with `Ctrl+C`, or run detached with `docker compose up --build -d`.

## Run locally (without Docker)

### Backend

```powershell
cd backend
python -m venv .venv or py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --port 8000
```

Create the venv inside `backend/` (or the repo root). Virtualenv folders (`.venv/`, `venv/`).

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Frontend expects the API at `http://localhost:8000` (see `VITE_API_URL` in Compose).
