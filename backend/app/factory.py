from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.database import Base, async_session_factory, engine
from app.core.limiter import limiter
from app.services.db_migrate import run_schema_migrations
from app.services.seed import run_seed


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

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        if settings.is_production:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

    @app.get("/")
    async def root():
        return {"message": "Poalei Tzedek API", "docs": "/api/v1/docs"}

    app.include_router(api_router, prefix="/api/v1")
    return app
