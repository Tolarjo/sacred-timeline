import os
from typing import Any

from celery import Celery

from app.database import get_connection
from app.extraction import extract_from_url
from app.semantic import compute_semantic_similarity, extract_events_from_text, extract_key_phrases

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery(__name__, broker=redis_url, backend=redis_url)


@celery_app.task(bind=True, max_retries=3)
def ingest_and_extract_text(self, document_id: int, source_url: str) -> Any:
    try:
        text, method = extract_from_url(source_url)
        with get_connection() as conn:
            if hasattr(conn, "execute"):
                conn.execute(
                    "UPDATE documents SET body_text = ?, extraction_method = ?, status = ? WHERE id = ?",
                    (text or "", method, "extracted" if text else "extraction_failed", document_id),
                )
                conn.commit()
            else:
                with conn.cursor() as cur:
                    cur.execute(
                        "UPDATE documents SET body_text = %s, extraction_method = %s, status = %s WHERE id = %s",
                        (text or "", method, "extracted" if text else "extraction_failed", document_id),
                    )
                    conn.commit()
        return {"status": "ok", "document_id": document_id, "method": method, "text_length": len(text or "")}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@celery_app.task(bind=True)
def extract_events_task(self, document_id: int, body_text: str) -> Any:
    try:
        events = extract_events_from_text(body_text)
        phrases = extract_key_phrases(body_text)
        with get_connection() as conn:
            if hasattr(conn, "execute"):
                for event in events:
                    conn.execute(
                        "INSERT INTO extracted_events (document_id, event_text, event_type, confidence) VALUES (?, ?, ?, ?)",
                        (document_id, event["text"], event["type"], 0.75),
                    )
                conn.commit()
            else:
                with conn.cursor() as cur:
                    for event in events:
                        cur.execute(
                            "INSERT INTO extracted_events (document_id, event_text, event_type, confidence) VALUES (%s, %s, %s, %s)",
                            (document_id, event["text"], event["type"], 0.75),
                        )
                    conn.commit()
        return {
            "status": "ok",
            "document_id": document_id,
            "events_extracted": len(events),
            "key_phrases": phrases,
        }
    except Exception as exc:
        return {"status": "error", "error": str(exc)}


@celery_app.task(bind=True)
def compare_documents_task(self, doc_id_1: int, doc_id_2: int) -> Any:
    try:
        with get_connection() as conn:
            if hasattr(conn, "execute"):
                row1 = conn.execute("SELECT body_text FROM documents WHERE id = ?", (doc_id_1,)).fetchone()
                row2 = conn.execute("SELECT body_text FROM documents WHERE id = ?", (doc_id_2,)).fetchone()
            else:
                with conn.cursor() as cur:
                    cur.execute("SELECT body_text FROM documents WHERE id = %s", (doc_id_1,))
                    row1 = cur.fetchone()
                    cur.execute("SELECT body_text FROM documents WHERE id = %s", (doc_id_2,))
                    row2 = cur.fetchone()

        text1 = dict(row1).get("body_text") if row1 else ""
        text2 = dict(row2).get("body_text") if row2 else ""
        similarity = compute_semantic_similarity(text1, text2)
        return {
            "status": "ok",
            "doc_id_1": doc_id_1,
            "doc_id_2": doc_id_2,
            "semantic_similarity": float(similarity),
        }
    except Exception as exc:
        return {"status": "error", "error": str(exc)}

