import os
import sqlite3
from contextlib import contextmanager
from typing import Iterator

import psycopg2
from psycopg2.extras import RealDictCursor

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./data/sacred_timeline.db")


def is_postgres() -> bool:
    return DB_URL.startswith("postgresql") or DB_URL.startswith("postgres")


def get_db_url() -> str:
    return DB_URL


def get_sqlite_path() -> str:
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, "data", "sacred_timeline.db")


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    if is_postgres():
        conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
        try:
            yield conn
        finally:
            conn.close()
        return

    conn = sqlite3.connect(get_sqlite_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def ensure_document_columns(conn) -> None:
    if is_postgres():
        with conn.cursor() as cur:
            cur.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_name = 'documents'"
            )
            columns = {row[0] for row in cur.fetchall()}
            required = {"body_text", "extracted_at", "extraction_method"}
            for col in required:
                if col not in columns:
                    if col == "body_text":
                        cur.execute("ALTER TABLE documents ADD COLUMN body_text TEXT")
                    elif col == "extracted_at":
                        cur.execute("ALTER TABLE documents ADD COLUMN extracted_at TIMESTAMPTZ")
                    elif col == "extraction_method":
                        cur.execute("ALTER TABLE documents ADD COLUMN extraction_method TEXT")
        conn.commit()
        return

    cols = conn.execute("PRAGMA table_info(documents)").fetchall()
    existing = {row[1] for row in cols}
    required = {"body_text", "extracted_at", "extraction_method"}
    for col in required - existing:
        if col == "body_text":
            conn.execute("ALTER TABLE documents ADD COLUMN body_text TEXT")
        elif col == "extracted_at":
            conn.execute("ALTER TABLE documents ADD COLUMN extracted_at TEXT")
        elif col == "extraction_method":
            conn.execute("ALTER TABLE documents ADD COLUMN extraction_method TEXT")
    conn.commit()


def init_db() -> None:
    if is_postgres():
        with psycopg2.connect(DB_URL, cursor_factory=RealDictCursor) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS documents (
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL,
                        religion TEXT NOT NULL,
                        tradition TEXT,
                        language TEXT,
                        source TEXT,
                        source_url TEXT,
                        category TEXT,
                        date_start INTEGER,
                        date_end INTEGER,
                        summary TEXT,
                        body_text TEXT,
                        extracted_at TIMESTAMPTZ,
                        extraction_method TEXT,
                        embedding BYTEA,
                        status TEXT DEFAULT 'ingested',
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    )
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS sources (
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        url TEXT NOT NULL,
                        religion TEXT,
                        source_type TEXT,
                        metadata JSONB,
                        status TEXT DEFAULT 'queued',
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    )
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS ingestion_jobs (
                        id SERIAL PRIMARY KEY,
                        document_id INTEGER REFERENCES documents(id),
                        source_url TEXT,
                        extraction_method TEXT,
                        status TEXT DEFAULT 'pending',
                        result TEXT,
                        created_at TIMESTAMPTZ DEFAULT NOW(),
                        updated_at TIMESTAMPTZ DEFAULT NOW()
                    )
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS extracted_events (
                        id SERIAL PRIMARY KEY,
                        document_id INTEGER REFERENCES documents(id),
                        event_text TEXT NOT NULL,
                        event_type TEXT,
                        timestamp INTEGER,
                        confidence FLOAT,
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    )
                    """
                )
                ensure_document_columns(conn)
                conn.commit()
        return

    os.makedirs(os.path.dirname(get_sqlite_path()), exist_ok=True)
    conn = sqlite3.connect(get_sqlite_path())
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            religion TEXT NOT NULL,
            tradition TEXT,
            language TEXT,
            source TEXT,
            source_url TEXT,
            category TEXT,
            date_start INTEGER,
            date_end INTEGER,
            summary TEXT,
            body_text TEXT,
            extracted_at TEXT,
            extraction_method TEXT,
            embedding BLOB,
            status TEXT DEFAULT 'ingested',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            url TEXT NOT NULL,
            religion TEXT,
            source_type TEXT,
            metadata TEXT,
            status TEXT DEFAULT 'queued',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ingestion_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER REFERENCES documents(id),
            source_url TEXT,
            extraction_method TEXT,
            status TEXT DEFAULT 'pending',
            result TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS extracted_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER REFERENCES documents(id),
            event_text TEXT NOT NULL,
            event_type TEXT,
            timestamp INTEGER,
            confidence FLOAT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    ensure_document_columns(conn)
    conn.commit()
    conn.close()


def seed_documents() -> None:
    if is_postgres():
        with psycopg2.connect(DB_URL, cursor_factory=RealDictCursor) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) AS count FROM documents")
                if cur.fetchone()["count"] > 0:
                    return
                sample_documents = [
                    {
                        "title": "Rigveda, Book 10",
                        "religion": "Hinduism",
                        "tradition": "Vedic",
                        "language": "Sanskrit",
                        "source": "Internet Archive",
                        "source_url": "https://example.org/rigveda-book-10",
                        "category": "Scripture",
                        "date_start": -1200,
                        "date_end": -900,
                        "summary": "Early Vedic hymn collection preserving ritual and cosmological themes.",
                        "body_text": "The hymns praise the cosmic order, ritual sacrifice, and the divine powers associated with the sky and sacrifice.",
                        "extraction_method": "manual_seed",
                        "status": "downloaded",
                    },
                    {
                        "title": "Torah: Genesis",
                        "religion": "Judaism",
                        "tradition": "Hebrew Bible",
                        "language": "Hebrew",
                        "source": "Sefaria",
                        "source_url": "https://example.org/torah-genesis",
                        "category": "Canonical text",
                        "date_start": -1000,
                        "date_end": -400,
                        "summary": "Foundational narrative of creation, covenant, and early ancestral history.",
                        "body_text": "In the beginning God created the heavens and the earth. The narrative traces covenant, ancestry, and divine promise.",
                        "extraction_method": "manual_seed",
                        "status": "downloaded",
                    },
                    {
                        "title": "Gospel of Matthew",
                        "religion": "Christianity",
                        "tradition": "Synoptic",
                        "language": "Greek",
                        "source": "Patristic Archive",
                        "source_url": "https://example.org/gospel-of-matthew",
                        "category": "Canonical text",
                        "date_start": 50,
                        "date_end": 110,
                        "summary": "Narrative of Jesus focusing on teaching, fulfillment, and kingdom themes.",
                        "body_text": "The genealogy and teaching of Jesus emphasize fulfillment of prophecy, the kingdom of heaven, and the authority of the master teacher.",
                        "extraction_method": "manual_seed",
                        "status": "downloaded",
                    },
                    {
                        "title": "Quran, Surah 1-10",
                        "religion": "Islam",
                        "tradition": "Quranic",
                        "language": "Arabic",
                        "source": "OpenITI",
                        "source_url": "https://example.org/quran-surah-1-10",
                        "category": "Canonical text",
                        "date_start": 610,
                        "date_end": 632,
                        "summary": "Early revelation units forming the opening surahs.",
                        "body_text": "The opening supplication, praise of God, and the guidance of the straight path structure the early revelation and its ethical orientation.",
                        "extraction_method": "manual_seed",
                        "status": "downloaded",
                    },
                ]
                for item in sample_documents:
                    cur.execute(
                        """
                        INSERT INTO documents (title, religion, tradition, language, source, source_url, category, date_start, date_end, summary, body_text, extraction_method, status)
                        VALUES (%(title)s, %(religion)s, %(tradition)s, %(language)s, %(source)s, %(source_url)s, %(category)s, %(date_start)s, %(date_end)s, %(summary)s, %(body_text)s, %(extraction_method)s, %(status)s)
                        """,
                        item,
                    )
                conn.commit()
        return

    conn = sqlite3.connect(get_sqlite_path())
    conn.row_factory = sqlite3.Row
    existing = conn.execute("SELECT COUNT(*) AS count FROM documents").fetchone()["count"]
    if existing > 0:
        conn.close()
        return

    sample_documents = [
        {
            "title": "Rigveda, Book 10",
            "religion": "Hinduism",
            "tradition": "Vedic",
            "language": "Sanskrit",
            "source": "Internet Archive",
            "source_url": "https://example.org/rigveda-book-10",
            "category": "Scripture",
            "date_start": -1200,
            "date_end": -900,
            "summary": "Early Vedic hymn collection preserving ritual and cosmological themes.",
            "body_text": "The hymns praise the cosmic order, ritual sacrifice, and the divine powers associated with the sky and sacrifice.",
            "extraction_method": "manual_seed",
            "status": "downloaded",
        },
        {
            "title": "Torah: Genesis",
            "religion": "Judaism",
            "tradition": "Hebrew Bible",
            "language": "Hebrew",
            "source": "Sefaria",
            "source_url": "https://example.org/torah-genesis",
            "category": "Canonical text",
            "date_start": -1000,
            "date_end": -400,
            "summary": "Foundational narrative of creation, covenant, and early ancestral history.",
            "body_text": "In the beginning God created the heavens and the earth. The narrative traces covenant, ancestry, and divine promise.",
            "extraction_method": "manual_seed",
            "status": "downloaded",
        },
        {
            "title": "Gospel of Matthew",
            "religion": "Christianity",
            "tradition": "Synoptic",
            "language": "Greek",
            "source": "Patristic Archive",
            "source_url": "https://example.org/gospel-of-matthew",
            "category": "Canonical text",
            "date_start": 50,
            "date_end": 110,
            "summary": "Narrative of Jesus focusing on teaching, fulfillment, and kingdom themes.",
            "body_text": "The genealogy and teaching of Jesus emphasize fulfillment of prophecy, the kingdom of heaven, and the authority of the master teacher.",
            "extraction_method": "manual_seed",
            "status": "downloaded",
        },
        {
            "title": "Quran, Surah 1-10",
            "religion": "Islam",
            "tradition": "Quranic",
            "language": "Arabic",
            "source": "OpenITI",
            "source_url": "https://example.org/quran-surah-1-10",
            "category": "Canonical text",
            "date_start": 610,
            "date_end": 632,
            "summary": "Early revelation units forming the opening surahs.",
            "body_text": "The opening supplication, praise of God, and the guidance of the straight path structure the early revelation and its ethical orientation.",
            "extraction_method": "manual_seed",
            "status": "downloaded",
        },
    ]
    conn.executemany(
        """
        INSERT INTO documents (
            title, religion, tradition, language, source, source_url, category,
            date_start, date_end, summary, body_text, extraction_method, status
        ) VALUES (:title, :religion, :tradition, :language, :source, :source_url,
            :category, :date_start, :date_end, :summary, :body_text, :extraction_method, :status)
        """,
        sample_documents,
    )
    conn.commit()
    conn.close()

