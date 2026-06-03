from db.engine import SessionLocal
from db.tables import LabResult


class LabResultRepository:

    def save(
        self,
        report_id,
        lab_value,
    ):

        with SessionLocal() as session:

            row = LabResult(
                report_id=report_id,
                raw_name=lab_value.raw_name,
                normalized_name=lab_value.normalized_name,
                value=lab_value.value,
                unit=lab_value.unit,
                reference_range=lab_value.reference_range,
                low_ref=lab_value.low_ref,
                high_ref=lab_value.high_ref,
                confidence=lab_value.confidence,
            )

            session.add(row)
            session.commit()

    def get_by_report_id(
            self,
            report_id,
    ):
        with SessionLocal() as session:
            return (
                session.query(LabResult)
                .filter(
                    LabResult.report_id == report_id
                )
                .all()
            )