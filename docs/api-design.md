# API Design

Base URL: `/api/v1`

## Public Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /homepage | Aggregated home content |
| GET | /prayer-times | Prayer times |
| GET | /torah-lessons | Torah lessons |
| GET | /events | Events (?homepage=true) |
| GET | /gallery/albums | Published albums |
| GET | /gallery/albums/{id}/images | Album images |
| GET | /mikveh | Mikveh content |
| GET | /settings/public | Public settings |
| GET | /banners/active | Active banners |
| POST | /contact | Submit contact form |
| GET | /sitemap.xml | Sitemap |
| GET | /robots.txt | Robots |

## Auth

| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/login | Login |
| POST | /auth/logout | Logout |
| GET | /auth/me | Current user |

## Admin (JWT required)

CRUD on all content entities, `/admin/contact-messages`, `/admin/audit-logs`.

Swagger: `/api/v1/docs`
