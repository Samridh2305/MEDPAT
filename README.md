# MEDPAT Report Helper

MEDPAT is a FastAPI backend that helps users understand uploaded medical test reports in plain language.

It combines:

- PDF, text, and image report extraction
- OpenAI-powered lab-value extraction and report explanation
- SQL Server storage for uploaded reports and extracted lab results
- ChromaDB vector search over medical knowledge-base files
- ML disease-risk prediction for diabetes, kidney disease, and hypertension

This project is educational only. It must not be used as a diagnosis, treatment plan, or replacement for professional medical care.

## Architecture

```text
Upload report
-> extract report text
-> save report text in SQL Server reports table
-> extract lab values with OpenAI
-> save lab values in SQL Server lab_results table

Ask question
-> load report text and lab values from SQL Server
-> retrieve relevant medical context from ChromaDB
-> generate answer with OpenAI

Predict disease risk
-> load extracted lab values from SQL Server
-> build ML features
-> run trained local models
```

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4.1-mini
OPENAI_EXTRACTION_MODEL=gpt-4.1-mini

DATABASE_URL=mssql+pyodbc://@localhost/MedicalReports?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes

RAW_DATA_DIR=ml/data/raw
PROCESSED_DATA_DIR=ml/data/processed
MODEL_DIR=ml/models
```

Run database migrations:

```powershell
alembic upgrade head
```

Start the API:

```powershell
uvicorn main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Storage

SQL Server stores user-specific report data.

Tables are defined in [db/tables.py](C:/Users/Samridh/PycharmProjects/MEDPAT/db/tables.py):

- `reports`: uploaded report text and filename
- `lab_results`: extracted lab values linked to a report

ChromaDB stores medical knowledge embeddings in `chroma_db/`. On startup, the app loads Markdown files from `knowledge_base/`, embeds them, and upserts them into the `medical_knowledge` collection.

## API Endpoints

### Health Check

```powershell
curl.exe "http://127.0.0.1:8000/health"
```

### Upload A Report

Uploads a report, extracts text, stores the report in SQL Server, extracts lab values, and stores those lab values.

```powershell
curl.exe -X POST "http://127.0.0.1:8000/reports" `
  -F "file=@examples/sample_cbc_report.txt"
```

Response shape:

```json
{
  "report_id": "6f9b0db9-d7f2-45f1-9f2b-4a18d29f8d12",
  "filename": "sample_cbc_report.txt",
  "extracted_values": []
}
```

### Ask A Question

Uses SQL Server report data, extracted lab values, ChromaDB retrieval, and OpenAI to answer a user question.

```powershell
curl.exe -X POST "http://127.0.0.1:8000/questions" `
  -H "Content-Type: application/json" `
  -d "{\"report_id\":\"6f9b0db9-d7f2-45f1-9f2b-4a18d29f8d12\",\"question\":\"Explain this report simply\"}"
```

Response includes the answer and the knowledge-base source files used:

```json
{
  "report_id": "6f9b0db9-d7f2-45f1-9f2b-4a18d29f8d12",
  "question": "Explain this report simply",
  "answer": "Plain-language explanation...",
  "sources": ["lab_tests.md"]
}
```

### Get Extracted Labs

```powershell
curl.exe "http://127.0.0.1:8000/reports/6f9b0db9-d7f2-45f1-9f2b-4a18d29f8d12/labs"
```

### Predict Disease Risk

Runs local ML models using the extracted lab values.

```powershell
curl.exe -X POST "http://127.0.0.1:8000/reports/6f9b0db9-d7f2-45f1-9f2b-4a18d29f8d12/predict"
```

Response shape:

```json
{
  "diabetes_risk": 0.12,
  "kidney_risk": 0.08,
  "hypertension_risk": 0.21
}
```

## Project Structure

```text
main.py                         FastAPI app and endpoint wiring
common/config.py                Environment-based app settings
db/engine.py                    SQLAlchemy engine and session setup
db/tables.py                    SQL Server table models
alembic/                        Database migrations
medpat/report_parser.py          PDF, text, and OCR extraction
medpat/sql_report_repository.py  SQL Server report repository
medpat/rag.py                    ChromaDB-backed RAG retrieval
medpat/embeddings.py             SentenceTransformer embeddings
medpat/reranker.py               Retrieved-context reranking
llm/                             OpenAI prompt and service layer
extraction/                      Lab-value extraction and persistence
ml/models/                       Trained disease-risk models
ml/services/                     Feature building and prediction logic
knowledge_base/                  Markdown medical reference content for RAG
```

## Notes

- Install Microsoft ODBC Driver 18 for SQL Server before connecting with `pyodbc`.
- If image reports are used, install Tesseract OCR on the machine in addition to Python packages.
- Keep `.env`, database credentials, uploaded reports, and generated ChromaDB files out of git.
- Expand `knowledge_base/` with reviewed medical content to improve RAG quality.
