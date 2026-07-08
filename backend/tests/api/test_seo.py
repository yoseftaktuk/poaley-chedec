import pytest


@pytest.mark.asyncio
async def test_sitemap(client):
    response = await client.get("/api/v1/sitemap.xml")
    assert response.status_code == 200
    assert "xml" in response.headers["content-type"]


@pytest.mark.asyncio
async def test_robots(client):
    response = await client.get("/api/v1/robots.txt")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
