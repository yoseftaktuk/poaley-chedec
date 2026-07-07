# Deployment Guide

## Render Setup

1. Create PostgreSQL database on Render
2. Deploy backend from `backend/` using `render.yaml`
3. Deploy frontend static site from `frontend/` using `render.yaml`
4. Set environment variables (see `.env.example`)

## Required Environment Variables

### Backend
- DATABASE_URL, SECRET_KEY, CORS_ORIGINS
- ADMIN_USERS (JSON array)
- SMTP_* for contact form email
- CLOUDINARY_* for image uploads

### Frontend
- VITE_API_BASE_URL (production API URL)

## Docker Local

```bash
docker compose up --build
```
