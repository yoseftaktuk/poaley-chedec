from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import asynccontextmanager
import asyncio
import json
import time

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.core.database import Base, get_db
from app.core.limiter import limiter
from app.core.security import hash_password
from app.factory import create_app
from app.models import User

_DEBUG_LOG = "/Users/natankatz/poaley-chedec/.cursor/debug-d00f51.log"
_tables_created = False


def _agent_log(hypothesis_id: str, location: str, message: str, data: dict) -> None:
    # #region agent log
    try:
        with open(_DEBUG_LOG, "a", encoding="utf-8") as log_file:
            log_file.write(
                json.dumps(
                    {
                        "sessionId": "d00f51",
                        "hypothesisId": hypothesis_id,
                        "location": location,
                        "message": message,
                        "data": data,
                        "timestamp": int(time.time() * 1000),
                    }
                )
                + "\n"
            )
    except OSError:
        pass
    # #endregion


@asynccontextmanager
async def _test_lifespan(_app) -> AsyncIterator[None]:
    yield


@pytest_asyncio.fixture
async def test_engine():
    global _tables_created
    # #region agent log
    _agent_log(
        "A",
        "conftest.py:test_engine",
        "creating test engine",
        {"loop_id": id(asyncio.get_running_loop()), "tables_created": _tables_created},
    )
    # #endregion
    engine = create_async_engine(settings.test_database_url, echo=False, poolclass=NullPool)
    if not _tables_created:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        _tables_created = True
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    # #region agent log
    _agent_log("B", "conftest.py:db_session", "opening db session", {"loop_id": id(asyncio.get_running_loop())})
    # #endregion
    connection = await test_engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint",
    )
    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    # #region agent log
    _agent_log("C", "conftest.py:client", "creating httpx client", {"loop_id": id(asyncio.get_running_loop())})
    # #endregion
    limiter.enabled = False

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    test_app = create_app(lifespan=_test_lifespan)
    test_app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    test_app.dependency_overrides.clear()
    limiter.enabled = True


@pytest_asyncio.fixture
async def admin_user(db_session: AsyncSession) -> User:
    user = User(username="testadmin", password_hash=hash_password("testpass123"))
    db_session.add(user)
    await db_session.flush()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient, admin_user: User) -> dict[str, str]:
    response = await client.post(
        "/api/v1/auth/login",
        json={"username": "testadmin", "password": "testpass123"},
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
