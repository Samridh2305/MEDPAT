from pydantic import BaseModel, Field


class LabValue(BaseModel):
    raw_name: str

    normalized_name: str | None = None

    value: float | None = None

    unit: str | None = None

    reference_range: str | None = None

    low_ref: float | None = None

    high_ref: float | None = None

    confidence: float = Field(default=0.0)

class ExtractedReport(BaseModel):

    results: list[LabValue]

