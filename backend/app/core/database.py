from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.core.config import _debug_log, database_connect_args, is_supabase_pooler, settings


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
_debug_log(
    "database.py:engine",
    "engine kwargs",
    {
        "isPooler": is_supabase_pooler(settings.database_url),
        "poolClass": _engine_kwargs.get("poolclass", NullPool).__name__
        if "poolclass" in _engine_kwargs
        else "default",
        "connectArgKeys": sorted(_connect_args.keys()),
    },
    "C",
)
# #endregion

engine = create_async_engine(settings.database_url, **_engine_kwargs)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
