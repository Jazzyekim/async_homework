from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from cve_vault.config import Settings


def get_engine(settings: Settings) -> AsyncSession:
    from sqlalchemy.ext.asyncio import create_async_engine
    return create_async_engine(settings.db_uri, echo=True)


class Base(DeclarativeBase, AsyncAttrs):
    pass