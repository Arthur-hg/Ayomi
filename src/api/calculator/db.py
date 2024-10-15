from typing import List

from sqlalchemy import Column, func, text
from sqlalchemy.dialects.postgresql import NUMERIC, TEXT, TIMESTAMP, UUID
from sqlalchemy.orm import Session

from src.extensions import Base


class OperationRecord(Base):
    __tablename__ = "operations"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    operation = Column(TEXT, nullable=False)
    result = Column(NUMERIC, nullable=False)
    created_at = Column(TIMESTAMP, default=func.now())

    @classmethod
    def get_all(cls, session: Session) -> List["OperationRecord"]:
        return session.query(cls).all()
