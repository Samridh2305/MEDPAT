import uuid

from sqlalchemy import (
    Column,
    Text,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func

from db.engine import Base


class Report(Base):
    __tablename__ = "reports"

    report_id = Column(
        UNIQUEIDENTIFIER,
        primary_key=True,
        default=uuid.uuid4
    )

    filename = Column(
        String(255),
        nullable=False
    )

    text = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class LabResult(Base):
    __tablename__ = "lab_results"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    report_id = Column(
        UNIQUEIDENTIFIER,
        ForeignKey("reports.report_id"),
        nullable=False
    )

    raw_name = Column(
        String(255),
        nullable=False
    )

    normalized_name = Column(
        String(255),
        nullable=True
    )

    value = Column(
        Float,
        nullable=True
    )

    unit = Column(
        String(50),
        nullable=True
    )

    reference_range = Column(
        String(100),
        nullable=True
    )

    low_ref = Column(
        Float,
        nullable=True
    )

    high_ref = Column(
        Float,
        nullable=True
    )

    confidence = Column(
        Float,
        nullable=False,
        default=0.0
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
