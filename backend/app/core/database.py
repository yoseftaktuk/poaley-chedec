from collections.abc import AsyncGenerator
from urllib.parse import urlparse
import json
import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import (
    classify_database_host,
    database_connect_args,
    normalize_database_url,
    settings,
)


class Base(DeclarativeBase):
    pass


def _debug_log(hypothesis_id: str, location: str, message: str, data: dict, run_id: str = "pre-fix") -> None:
    # #region agent log
    try:
        payload = {
            "sessionId": "1545be",
            "runId": run_id,
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data,
            "timestamp": __import__("time").time_ns() // 1_000_000,
        }
        line = json.dumps(payload)
        print(f"[debug-1545be] {line}", flush=True)
        with open("/Users/natankatz/poaley-chedec/.cursor/debug-1545be.log", "a") as f:
            f.write(line + "\n")
    except Exception:
        pass
    # #endregion


def _scheme_only(url: str | None) -> dict:
    if not url:
        return {"present": False}
    parsed = urlparse(url)
    return {
        "present": True,
        "scheme": parsed.scheme,
        "has_asyncpg": "+asyncpg" in (parsed.scheme or ""),
        "has_psycopg2": "psycopg2" in (parsed.scheme or ""),
        "hostKind": classify_database_host(parsed.hostname),
        "port": parsed.port or 5432,
        "hasSslMode": "sslmode" in (parsed.query or ""),
    }


_env_raw = os.environ.get("DATABASE_URL")
_connect_args = database_connect_args(settings.database_url, is_production=settings.is_production)
# #region agent log
_debug_log(
    "B",
    "database.py:before_engine",
    "DATABASE_URL host classification and connect_args",
    {
        "env": _scheme_only(_env_raw),
        "settings": _scheme_only(settings.database_url),
        "isProduction": settings.is_production,
        "connectArgsSsl": type(_connect_args.get("ssl")).__name__ if _connect_args.get("ssl") else None,
        "statementCacheSize": _connect_args.get("statement_cache_size"),
    },
)
# #endregion

try:
    engine = create_async_engine(
        settings.database_url,
        echo=settings.environment == "development",
        connect_args=_connect_args,
        pool_pre_ping=True,
    )
    # #region agent log
    _debug_log(
        "B",
        "database.py:engine_ok",
        "create_async_engine succeeded",
        {
            "dialect": str(engine.dialect.name),
            "driver": str(getattr(engine.dialect, "driver", None)),
            "settings_scheme": urlparse(settings.database_url).scheme,
            "connectArgsSsl": type(_connect_args.get("ssl")).__name__ if _connect_args.get("ssl") else None,
            "statementCacheSize": _connect_args.get("statement_cache_size"),
        },
        run_id="post-fix",
    )
    # #endregion
except ModuleNotFoundError as exc:
    # #region agent log
    _debug_log(
        "A",
        "database.py:engine_fail",
        "create_async_engine ModuleNotFoundError",
        {
            "error": type(exc).__name__,
            "missing_module": getattr(exc, "name", None),
            "env": _scheme_only(_env_raw),
            "settings": _scheme_only(settings.database_url),
        },
    )
    # #endregion
    raise

async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
