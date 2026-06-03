from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError

from db.engine import SessionLocal
from db.tables import Report

from exceptions.custom_exceptions import (
    DatabaseSaveException,
    InvalidReportIdException,
    ReportNotFoundException,
    AppException,
)


@dataclass(frozen=True)
class StoredReport:
    report_id: str
    filename: str
    text: str


class SQLReportRepository:

    def save(self, filename: str, text: str) -> StoredReport:

        try:
            with SessionLocal() as session:

                db_report = Report(
                    filename=filename,
                    text=text,
                )

                session.add(db_report)
                session.commit()
                session.refresh(db_report)

                return to_stored_report(db_report)

        except SQLAlchemyError as exc:
            raise DatabaseSaveException() from exc

    def get(self, report_id: str) -> StoredReport:

        try:
            report_uuid = UUID(report_id)

        except ValueError as exc:
            raise InvalidReportIdException() from exc

        try:
            with SessionLocal() as session:

                db_report = session.get(
                    Report,
                    report_uuid,
                )

                if db_report is None:
                    raise ReportNotFoundException()

                return to_stored_report(db_report)

        except SQLAlchemyError as exc:
            print(exc)
            raise AppException(
                detail="Could not load report from database."
            ) from exc


def to_stored_report(report: Report) -> StoredReport:

    return StoredReport(
        report_id=str(report.report_id),
        filename=report.filename,
        text=report.text,
    )