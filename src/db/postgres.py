from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

postgres_url = (
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}"
    f"@{settings.postgres_host}:{settings.postgres_port}/{settings.db_name}"
)
engine = create_async_engine(
    postgres_url,
    convert_unicode=True,
    pool_pre_ping=True,
)
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def get_async_session():
    return async_session
