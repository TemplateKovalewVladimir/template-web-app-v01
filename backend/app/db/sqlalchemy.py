from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

IS_ECHO = False

# Sync
sync_engine = create_engine(
    url=settings.database_url_psycopg,
    echo=IS_ECHO,
    # pool_size=4,
    # max_overflow=10,
)

session_maker = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_session() -> Session:
    with session_maker() as session:
        yield session


# Async
# from typing import AsyncGenerator
# from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# async_engine = create_async_engine(
#     url=settings.database_url_asyncpg,
#     echo=IS_ECHO,
# )
# async_session_maker = async_sessionmaker(
#     bind=async_engine,
#     autocommit=False,
#     autoflush=False,
# )

# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session
