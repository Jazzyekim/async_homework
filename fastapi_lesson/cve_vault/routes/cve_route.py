from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from cve_vault.db.models import CVERecordDB
from cve_vault import deps

from fastapi_lesson.cve_vault.schemas import CVERecord

cve_api = APIRouter(prefix="/cve_records")


@cve_api.get("/{cve_id}",
             name="Get CVERecord by ID",
             description="Returns a single CVERecord by its ID")
async def get_cve_by_id(cve_id: str, db: Annotated[AsyncSession, Depends(deps.get_db_session)]) -> CVERecord:
    stmt = (select(CVERecordDB).where(CVERecordDB.id == cve_id))
    result = await db.execute(stmt)
    cve_record = result.scalars().first()
    if cve_record is None:
        raise HTTPException(status_code=404, detail="CVERecord not found")
    return CVERecord.model_validate(cve_record)


@cve_api.post("/",
              name="Add new CVERecord",
              description="Returns the list of all registered CVERecords",
              status_code=201)
async def add_cve_record(record: CVERecord,
                         db: Annotated[AsyncSession, Depends(deps.get_db_session)],
                         response: Response) -> CVERecord:
    cve_record_db = CVERecordDB(**record.model_dump())
    db.add(cve_record_db)
    await db.commit()

    await db.refresh(cve_record_db)
    response.status_code = 201
    return CVERecord.model_validate(cve_record_db)
