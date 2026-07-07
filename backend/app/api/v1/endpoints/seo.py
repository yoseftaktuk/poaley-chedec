from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.seed import get_setting

router = APIRouter()

PAGES = [
    {"loc": "/", "priority": "1.0"},
    {"loc": "/gallery", "priority": "0.8"},
    {"loc": "/mikveh", "priority": "0.8"},
    {"loc": "/contact", "priority": "0.7"},
    {"loc": "/accessibility", "priority": "0.5"},
]


@router.get("/sitemap.xml")
async def sitemap(db: AsyncSession = Depends(get_db)) -> Response:
    site = await get_setting(db, "site")
    base_url = site.get("base_url", "https://poaleitzedek.org")
    urls = "\n".join(
        f"  <url><loc>{base_url}{page['loc']}</loc><priority>{page['priority']}</priority></url>"
        for page in PAGES
    )
    content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>"""
    return Response(content=content, media_type="application/xml")


@router.get("/robots.txt")
async def robots(db: AsyncSession = Depends(get_db)) -> Response:
    site = await get_setting(db, "site")
    base_url = site.get("base_url", "https://poaleitzedek.org")
    content = f"""User-agent: *
Allow: /
Disallow: /admin

Sitemap: {base_url}/api/v1/sitemap.xml
"""
    return Response(content=content, media_type="text/plain")
