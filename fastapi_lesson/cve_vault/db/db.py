from cve_vault.config import Settings
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase


class DatabaseEngineSingleton:
    _instance = None

    def __new__(cls, settings):
        if cls._instance is None:
            cls._instance = super(DatabaseEngineSingleton, cls).__new__(cls)
            cls._instance.engine = create_async_engine(settings.db_uri, echo=True)
        return cls._instance

    def get_engine(self):
        return self.engine


def get_engine(settings: Settings) -> AsyncSession:
    return DatabaseEngineSingleton(settings).get_engine()


class Base(DeclarativeBase, AsyncAttrs):
    pass
