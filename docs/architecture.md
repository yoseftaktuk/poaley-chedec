# Architecture

## Deployment (Render)

- **Frontend:** Static Site (Vite build)
- **Backend:** Web Service (FastAPI Docker)
- **Database:** Managed PostgreSQL

## Backend Clean Architecture

```
backend/app/modules/<feature>/
  domain/
  application/
  infrastructure/
  presentation/
```

Cross-cutting: `backend/app/core/` (config, security, database, audit, limiter)

## Frontend Structure

```
frontend/src/
  app/          - providers, router
  pages/        - route pages
  components/   - UI and layout
  hooks/        - custom hooks (one per file)
  types/        - TypeScript types
  lib/          - API client, utils, constants
  styles/       - RTL, theme tokens
```
