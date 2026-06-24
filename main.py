import os

from fastapi import (
    FastAPI,
    File,
    HTTPException,
    UploadFile
)
from fastapi.middleware.cors import CORSMiddleware

from common.logger_config import logger
from exceptions.custom_exceptions import AppException
from exceptions.exception_handlers import app_exception_handler
from extraction.lab_metric_extraction import process_uploaded_report
from extraction.lab_repository import LabResultRepository
from extraction.schema import ExtractedReport
from llm.service import LLMClient
from medpat.embeddings import EmbeddingModel
from medpat.rag import (
    load_knowledge_base,
    build_collection,
    generate_embeddings,
    index_chunks,
    answer_question,
)
from medpat.report_parser import extract_text_from_upload
from medpat.schema import (
    UploadReportResponse,
    AskQuestionRequest,
    AskQuestionResponse,
    LabResultResponse,
    DiseasePredictionResponse,
)
from medpat.sql_report_repository import SQLReportRepository
from ml.services.build_features import (
    build_prediction_features,
    labs_to_feature_dict
)
from ml.services.prediction import predict_diseases

os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

app = FastAPI(
    title="MEDPAT API",
    description="RAG backend for explaining uploaded medical test reports in simple language.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

chunks = load_knowledge_base()

embedding_model = EmbeddingModel()

chunk_embeddings = generate_embeddings(
    chunks,
    embedding_model,
)

collection = build_collection()

index_chunks(
    collection=collection,
    chunks=chunks,
    embeddings=chunk_embeddings,
)

llm = LLMClient()
report_repository = SQLReportRepository()
lab_result_repository = LabResultRepository()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post(
    "/reports",
    response_model=UploadReportResponse,
)
async def upload_report(
        file: UploadFile = File(...)
) -> UploadReportResponse:
    try:
        report_text = extract_text_from_upload(
            uploaded_file=file.file,
            filename=file.filename,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    if not report_text.strip():
        raise HTTPException(
            status_code=422,
            detail="Could not extract readable text from this file.",
        )

    try:
        report = report_repository.save(
            filename=file.filename,
            text=report_text,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    #
    # Extract lab values
    #
    processed_report = ExtractedReport(
        results=[]
    )

    try:

        processed_report = process_uploaded_report(
            report_text, llm
        )

        logger.info(
            f"Extracted {len(processed_report.results)} lab values"
        )

        lab_result_repository.save_all(
            report_id=report.report_id,
            lab_values=processed_report.results,
        )

        for item in processed_report.results:
            logger.info(
                "Extracted lab value: %s",
                item.model_dump()
            )

    except Exception as exc:

        logger.info(
            f"Lab extraction failed: {exc}"
        )

    return UploadReportResponse(
        report_id=report.report_id,
        filename=report.filename,
        extracted_values=processed_report.results
    )


@app.post(
    "/questions",
    response_model=AskQuestionResponse,
)
def ask_question(
        payload: AskQuestionRequest,
) -> AskQuestionResponse:
    try:
        report = report_repository.get(
            payload.report_id
        )
        labs = lab_result_repository.get_by_report_id(
            payload.report_id
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found.",
        )

    llm = LLMClient()

    try:
        result = answer_question(
            collection=collection,
            embedding_model=embedding_model,
            question=payload.question,
            report_text=report.text,
            lab_values=labs,
            llm=llm,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return AskQuestionResponse(
        report_id=payload.report_id,
        question=payload.question,
        answer=result.answer,
        sources=result.sources,
    )

@app.get(
    "/reports/{report_id}/labs",
    response_model=list[LabResultResponse],
)
def get_report_labs(
    report_id: str,
):
    labs = lab_result_repository.get_by_report_id(
        report_id
    )

    if not labs:
        raise HTTPException(
            status_code=404,
            detail="No lab values found."
        )

    return labs

@app.post(
    "/reports/{report_id}/predict",
    response_model=DiseasePredictionResponse,
)
def predict_report_diseases(
    report_id: str,
):

    labs = (
        lab_result_repository
        .get_by_report_id(
            report_id
        )
    )

    if not labs:
        raise HTTPException(
            status_code=404,
            detail="No lab values found."
        )

    lab_dict = labs_to_feature_dict(
        labs
    )

    features = (
        build_prediction_features(
            lab_dict
        )
    )

    predictions = predict_diseases(
        features
    )

    return DiseasePredictionResponse(
        **predictions
    )