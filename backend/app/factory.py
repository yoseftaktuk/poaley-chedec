from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import Base, async_session_factory, engine
from app.core.limiter import limiter
from app.services.db_migrate import run_schema_migrations
from app.services.seed import run_seed


class SecurityHeadersMiddleware:
    """Pure ASGI middleware — avoids BaseHTTPMiddleware task-group loop issues in tests."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    def _extra_headers(self) -> list[tuple[bytes, bytes]]:
        headers = [
            (b"x-content-type-options", b"nosniff"),
            (b"x-frame-options", b"DENY"),
            (b"x-xss-protection", b"1; mode=block"),
            (b"referrer-policy", b"strict-origin-when-cross-origin"),
        ]
        if settings.is_production:
            headers.append((b"strict-transport-security", b"max-age=31536000; includeSubDomains"))
        return headers

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        extra_headers = self._extra_headers()

        async def send_with_security_headers(message: Message) -> None:
            if message["type"] == "http.response.start":
                message = {
                    **message,
                    "headers": list(message.get("headers", [])) + extra_headers,
                }
            await send(message)

        await self.app(scope, receive, send_with_security_headers)


def _default_lifespan_context() -> Callable:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            await run_schema_migrations(conn)
        async with async_session_factory() as session:
            await run_seed(session)
        yield
        await engine.dispose()

    return lifespan


def create_app(*, lifespan: Callable | None = None) -> FastAPI:
    app = FastAPI(
        title="Poalei Tzedek API",
        description="API for Beit Knesset Poalei Tzedek website",
        version="1.0.0",
        docs_url="/api/v1/docs",
        openapi_url="/api/v1/openapi.json",
        lifespan=lifespan or _default_lifespan_context(),
    )

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SecurityHeadersMiddleware)

    @app.get("/")
    async def root():
        return {"message": "Poalei Tzedek API", "docs": "/api/v1/docs"}

    app.include_router(api_router, prefix="/api/v1")
    return app
