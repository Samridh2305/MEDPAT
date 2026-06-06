from dataclasses import dataclass

from pydantic import (
    BaseModel,
    Field
)

from extraction.schema import LabValue


class UploadReportResponse(BaseModel):
    report_id: str
    filename: str
    extracted_values: list[LabValue] = []

class AskQuestionRequest(BaseModel):
    report_id: str = Field(..., examples=["6f9b0db9-d7f2-45f1-9f2b-4a18d29f8d12"])
    question: str = Field(
        ...,
        examples=[
            "Explain this report in simple words and highlight values I should ask my doctor about."
        ],
    )


class AskQuestionResponse(BaseModel):
    report_id: str
    question: str
    answer: str
    sources: list[str]

class LabResultResponse(BaseModel):
    raw_name: str
    normalized_name: str | None
    value: float | None
    unit: str | None
    reference_range: str | None
    low_ref: float | None
    high_ref: float | None
    confidence: float

    class Config:
        from_attributes = True

class DiseasePredictionResponse(
    BaseModel
):
    diabetes_risk: float
    kidney_risk: float
    hypertension_risk: float

@dataclass
class RAGResponse:
    answer: str
    sources: list[str]


@dataclass
class KnowledgeChunk:
    text: str
    source: str


@dataclass
class RetrievedChunk:
    text: str
    score: float
    source: str


@dataclass
class MedicalEntity:
    name: str
