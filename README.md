# Poalei Tzedek Synagogue Website

Production-grade Hebrew RTL website for Beit Knesset Poalei Tzedek (Ashkelon).

## Stack

- **Frontend:** React, TypeScript, Vite, TanStack Query, React Hook Form, Zod, Tailwind CSS
- **Backend:** FastAPI, SQLAlchemy 2, Alembic, Pydantic, JWT
- **Database:** PostgreSQL
- **Storage:** Cloudinary
- **Deployment:** Render (split: static frontend + API + PostgreSQL)

## Quick Start

```bash
cp .env.example .env
chmod +x scripts/*.sh
./scripts/install.sh
docker compose up --build
```

- Frontend: http://localhost:5173
- API: http://localhost:8000/api/v1/docs
- Admin: http://localhost:5173/admin/login

Default admin credentials (from `.env`): `admin` / `changeme123`

## Development

```bash
# Backend only
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload

# Frontend only
cd frontend && npm run dev
```

## Testing

```bash
cd backend && pytest
cd frontend && npm run test
```

## Documentation

See `docs/` for SRS, architecture, API design, database schema, and deployment guide.
