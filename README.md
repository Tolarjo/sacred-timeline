# sacred-timeline

A minimal MVP for a global, multi-religion, multi-history manuscript library and comparison dashboard.

This starter project includes:
- a FastAPI backend with SQLite persistence
- a document ingestion API for metadata and source URLs
- a searchable document library
- a dashboard with timeline, summary stats, and source filters

## Stack
- Python 3.11+
- FastAPI
- SQLite
- Vanilla JS + HTML/CSS dashboard

## Quick start

### 1) Create a virtual environment

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Run the backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3) Open the dashboard

Open your browser to:

```text
http://localhost:8000
```

The dashboard will load document data from the API automatically.

## API endpoints

- `GET /api/documents`
- `POST /api/documents`
- `GET /api/timeline`
- `GET /api/dashboard`
- `GET /health`

## Notes

This is intentionally a lightweight MVP focused on:
- ingesting metadata
- organizing documents by tradition, period, and source
- showing a visual dashboard and document collection

It is not yet a full multi-agent orchestration system; it is the foundation for that later.
