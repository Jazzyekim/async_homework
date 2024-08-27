from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from cve_vault.db.db import get_engine
from cve_vault.config import Settings

def get_settings() -> Settings:
    return Settings()


async def get_db_session(settings: Annotated[Settings, Depends(get_settings)]) -> AsyncIterator[AsyncSession]:
    engine = get_engine(settings)
    session_factory = async_sessionmaker(engine)
    async with session_factory() as session:
        yield session