# Deployment Guide

## Render Setup

1. Deploy backend from `backend/` using `render.yaml` (Docker)
2. Deploy frontend static site from `frontend/` using `render.yaml`
3. Set environment variables in the Render dashboard (see below)

## Database (Supabase)

Production uses **Supabase Postgres**, not Render Postgres. In **Render → API service → Environment**:

| Variable | Value |
|----------|--------|
| `DATABASE_URL` | Supabase **pooler** URI (port **6543**, Transaction mode) |
| `ENVIRONMENT` | `production` |

Example `DATABASE_URL` format (replace password; percent-encode `@` as `%40`):

```
postgresql://postgres.eyagbvsdxbfpvrgdkbbs:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

Use **Connection pooling → Transaction** in the Supabase dashboard. Direct `db.*.supabase.co:5432` fails on Render (IPv6). The backend normalizes `postgresql://` to `postgresql+asyncpg://` and applies `ssl=require` for Supabase.

## Required Environment Variables

### Backend
- `DATABASE_URL` — Supabase connection string (see above)
- `TEST_DATABASE_URL` — local pytest only
- `SECRET_KEY`, `ENVIRONMENT`, `CORS_ORIGINS`, `TIMEZONE`
- `ZMANIM_LATITUDE`, `ZMANIM_LONGITUDE`, `ZMANIM_TZID` (Hebcal prayer-time location)
- `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS`
- `ADMIN_USERS` (JSON array)
- `SMTP_*` for contact form email
- `CLOUDINARY_*` for image uploads

### Frontend
- `VITE_API_BASE_URL` (production API URL)

## Docker Local

```bash
docker compose up --build
```
