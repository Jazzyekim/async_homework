from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import Sequence
from models import CVERecord, ProblemType


def make_cve(cve_id: str, title: str, description: str, date_published: datetime, date_updated: datetime) -> CVERecord:
    return CVERecord(id = cve_id,
                     title = title,
                     description = description,
                     date_published = date_published,
                     date_updated = date_updated
                     )

def make_problem_type(description: str, cve_record: CVERecord) -> ProblemType:
    return ProblemType(description = description, cve_record = cve_record)

async def get_all_cve(session: AsyncSession) -> Sequence[CVERecord]:
    stmt = select(CVERecord).order_by(CVERecord.date_updated)
    result = await session.execute(stmt)
    return result.scalars().all()