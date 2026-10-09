# sacred-timeline

A multi-religion, multi-history manuscript library and comparative dashboard focused on global textual traditions.

## MVP status

This branch adds the next milestone:
- PostgreSQL-ready database layer with SQLite fallback for local development
- source ingestion endpoints for URL-driven document discovery
- enhanced dashboard with richer metadata and filtering
- improved document library and timeline visualization

## Stack
- FastAPI
- PostgreSQL (or SQLite fallback)
- HTML/CSS/JS dashboard frontend
- Python ingestion utilities

## Local development

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

```text
http://localhost:8000
```

## API

- `GET /health`
- `GET /api/documents`
- `POST /api/documents`
- `POST /api/ingest-source`
- `GET /api/timeline`
- `GET /api/dashboard`

## Notes

This is still a focused MVP builder for ingestion and comparison workflows. It intentionally emphasizes data acquisition and a structured library before full AI orchestration layers are added.
