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
# Frontend
cd frontend && npm run test
cd frontend && npm run test:coverage

# Backend (requires Python 3.12 + PostgreSQL test database)
cd backend && pytest
```

See [docs/testing.md](docs/testing.md) for full testing guide, coverage reports, and conventions.

## Documentation

See `docs/` for SRS, architecture, API design, database schema, and deployment guide.

Production API: https://poaley-chedec-1.onrender.com

Nedarim Plus donation webhooks and receipt tracking: [docs/nedarim-receipts.md](docs/nedarim-receipts.md). The transaction webhook is `https://poaley-chedec-1.onrender.com/api/v1/webhooks/nedarim/transactions`. On Render, `CORS_ORIGINS` is only for the frontend browser. Nedarim posts server-to-server, so set `NEDARIM_WEBHOOK_SECRET` on the API service and do not add Nedarim to `CORS_ORIGINS`.
