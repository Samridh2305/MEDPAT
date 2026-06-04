from typing import Optional

from pydantic import (
    BaseModel,
    Field
)


class LabValue(BaseModel):
    raw_name: str

    normalized_name: Optional[str]

    value: Optional[float]

    unit: Optional[str]

    reference_range: Optional[str]

    low_ref: Optional[float]

    high_ref: Optional[float]

    confidence: float = Field(default=0.0)


class ExtractedReport(BaseModel):
    results: list[LabValue]
