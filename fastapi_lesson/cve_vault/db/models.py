from click import DateTime
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Column, String, Text, DateTime, ForeignKey

from cve_vault.db.db import Base


class CVERecordDB(Base):
    __tablename__ = "cve_records"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    date_published = Column(TIMESTAMP(timezone=True))
    date_updated = Column(TIMESTAMP(timezone=True))

