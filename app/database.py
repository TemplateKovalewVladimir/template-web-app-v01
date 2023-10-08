import asyncio

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine

from config import settings

sync_engine = create_engine(
    url=settings.database_url_psycopg,
    echo=False,
    # pool_size=5,
    # max_overflow=10,
)


async_engine = create_async_engine(
    url=settings.database_url_asyncpg,
    echo=False,
)


def get_version():
    with sync_engine.connect() as conn:
        res = conn.execute(text("SELECT VERSION()"))
        print(f"{res.all()=}")


async def a_get_version():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        print(f"{res.all()=}")


get_version()
asyncio.run(a_get_version())
