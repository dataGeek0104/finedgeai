import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .models import Base, SCHEMA_NAME
from sqlalchemy import text
from typing import AsyncGenerator

DATABASE_URL = os.getenv("PG_DATABASE_URL", "").encode("utf-8").decode("unicode_escape")

async def get_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session

# Async engine & session maker
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{SCHEMA_NAME}"'))
        await conn.run_sync(Base.metadata.create_all)
