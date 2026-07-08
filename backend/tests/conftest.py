from collections.abc import AsyncGenerator, AsyncIterator
from contextlib import asynccontextmanager

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

_tables_created = False


@asynccontextmanager
async def _test_lifespan(_app) -> AsyncIterator[None]:
    yield


@pytest_asyncio.fixture
async def test_engine():
    global _tables_created
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
