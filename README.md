# MEDPAT Report Helper

MEDPAT is a RAG prototype that helps users understand uploaded medical test reports in simple language.

It combines:

- report text extraction from PDF, image, or text files
- retrieval from a small medical lab-test knowledge base stored in ChromaDB
- deep-learning embeddings with `sentence-transformers/all-MiniLM-L6-v2`
- an LLM answer layer using OpenAI

This project is educational only. It must not be used as a diagnosis or replacement for professional medical care.

## Quick start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-lite.txt
$env:OPENAI_API_KEY="your_api_key"
$env:DATABASE_URL="mssql+pyodbc://@localhost/MedicalReports?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes"
alembic upgrade head
uvicorn main:app --reload
```

Open the API docs at `http://127.0.0.1:8000/docs`.

For the full deep-learning embedding setup, install:

```powershell
pip install -r requirements.txt
```

## LLM setup

```powershell
$env:OPENAI_API_KEY="your_api_key"
$env:OPENAI_MODEL="gpt-4.1-mini"
uvicorn main:app --reload
```

`OPENAI_MODEL` is optional. The default is `gpt-4.1-mini`.

## SQL Server setup

Report text is stored in the SQL Server `reports` table defined in [db/tables.py](C:/Users/Samridh/PycharmProjects/MEDPAT/db/tables.py).

Set `DATABASE_URL` if you want to override the default connection in [db/engine.py](C:/Users/Samridh/PycharmProjects/MEDPAT/db/engine.py):

```powershell
$env:DATABASE_URL="mssql+pyodbc://@localhost/MedicalReports?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&TrustServerCertificate=yes"
alembic upgrade head
```

The migration creates this table:

```sql
CREATE TABLE reports (
    report_id UNIQUEIDENTIFIER NOT NULL PRIMARY KEY,
    filename NVARCHAR(255) NOT NULL,
    text TEXT NOT NULL,
    created_at DATETIME NULL DEFAULT CURRENT_TIMESTAMP
);
```

## API endpoints

### Upload a report

```powershell
curl.exe -X POST "http://127.0.0.1:8000/reports" `
  -F "file=@examples/sample_cbc_report.txt"
```

Response:

```json
{
  "report_id": "generated_id",
  "filename": "sample_cbc_report.txt",
  "extracted_text": "Complete Blood Count..."
}
```

### Ask a question

```powershell
curl.exe -X POST "http://127.0.0.1:8000/questions" `
  -H "Content-Type: application/json" `
  -d "{\"report_id\":\"generated_id\",\"question\":\"Explain this report simply\"}"
```

## Project structure

```text
main.py                       FastAPI app and API endpoints
medpat/report_parser.py        PDF, text, and OCR extraction
medpat/sql_report_repository.py SQL Server report storage
medpat/embeddings.py           Deep-learning embeddings plus offline fallback
medpat/rag.py                  ChromaDB-backed retrieval pipeline
medpat/llm.py                  OpenAI answer generation
knowledge_base/lab_tests.md    Starter medical context
examples/sample_cbc_report.txt Demo report
```

## Next improvements

- Add user accounts and encrypted report storage.
- Expand the knowledge base with clinician-reviewed references.
- Add structured lab-value extraction and range comparison.
- Add multilingual explanations.
- Add audit logs and stronger medical safety filters before production.
