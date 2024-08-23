import uuid

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column



Base = declarative_base()

class CVERecord(Base):
    __tablename__ = "cve_records"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    date_published = Column(DateTime)
    date_updated = Column(DateTime)
    problem_types = relationship("ProblemType", back_populates="cve_record")

    def __repr__(self) -> str:
        return f"<CVE(id={self.id}, title={self.title}, description={self.description})>"

class ProblemType(Base):
    __tablename__ = "problem_types"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    description = Column(Text, nullable=False)
    cve_record_id = Column(String, ForeignKey("cve_records.id"))
    cve_record = relationship("CVERecord", back_populates="problem_types")



