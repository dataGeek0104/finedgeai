import os
import pytest_asyncio
import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from app.app import app
from app.datapipeline.models import Base

# Override the DATABASE_URL for tests
# TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
TEST_DB_URL = os.getenv("PG_TEST_DB_URL").encode("utf-8").decode("unicode_escape")


@pytest_asyncio.fixture
async def test_engine():
    engine = create_async_engine(TEST_DB_URL, echo=False, future=True)
    async with engine.begin() as conn:
        # Ensure schema exists
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS finedgeai"))
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine):
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest.fixture(scope="module")
def client():
    # FastAPI test client (sync, but works with async endpoints)
    with TestClient(app) as c:
        yield c
