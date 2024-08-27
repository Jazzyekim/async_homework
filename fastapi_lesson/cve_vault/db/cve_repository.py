from typing import Annotated

from cve_vault import deps
from cve_vault.db.models import CVERecordDB
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi_lesson.cve_vault.schemas import CVERecord


class CVERepository:
    def __init__(self, db: Annotated[AsyncSession, Depends(deps.get_db_session)]):
        self.db = db

    async def get_cve_by_id(self, cve_id: str) -> CVERecordDB:
        stmt = (select(CVERecordDB).where(CVERecordDB.id == cve_id))
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def add_cve_record(self, record: CVERecord) -> CVERecordDB:
        cve_record_db = CVERecordDB(**record.model_dump())
        self.db.add(cve_record_db)
        await self.db.commit()

        await self.db.refresh(cve_record_db)
        return cve_record_db


async def get_cve_repository(db: Annotated[AsyncSession, Depends(deps.get_db_session)]) -> CVERepository:
    return CVERepository(db)