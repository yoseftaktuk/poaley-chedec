# Database Schema

## Tables

- users
- settings (JSONB key-value)
- prayer_times
- torah_lessons
- events
- gallery_albums
- gallery_images
- mikveh
- contact_messages
- banner_messages
- audit_logs

See `backend/app/models/__init__.py` for SQLAlchemy model definitions.

## Settings Keys

- homepage, contact, donation, site, seo_global, seo_pages, accessibility_statement
