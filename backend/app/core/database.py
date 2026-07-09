from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.core.config import database_connect_args, is_supabase_pooler, settings


class Base(DeclarativeBase):
    pass


_connect_args = database_connect_args(settings.database_url)
_engine_kwargs: dict = {
    "echo": settings.environment == "development",
    "connect_args": _connect_args,
    "pool_pre_ping": True,
}
if is_supabase_pooler(settings.database_url):
    _engine_kwargs["poolclass"] = NullPool

# #region agent log
import json
import sys
import time

_engine_debug = {
    "sessionId": "1545be",
    "timestamp": int(time.time() * 1000),
    "location": "database.py:engine",
    "message": "engine configuration",
    "data": {
        "isPooler": is_supabase_pooler(settings.database_url),
        "poolClass": _engine_kwargs.get("poolclass", "default").__name__
        if "poolclass" in _engine_kwargs
        else "default",
        "connectArgKeys": sorted(_connect_args.keys()),
    },
    "runId": "pre-fix",
    "hypothesisId": "C",
}
_line = json.dumps(_engine_debug) + "\n"
try:
    with open("/Users/natankatz/poaley-chedec/.cursor/debug-1545be.log", "a", encoding="utf-8") as _f:
        _f.write(_line)
except OSError:
    pass
sys.stderr.write(f"[agent-debug] {_line}")
# #endregion

engine = create_async_engine(settings.database_url, **_engine_kwargs)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
