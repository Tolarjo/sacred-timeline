import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "sacred_timeline.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
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
            status TEXT DEFAULT 'ingested',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def seed_documents():
    conn = get_connection()
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
            "status": "downloaded",
        },
        {
            "title": "Psalms, Book I",
            "religion": "Judaism",
            "tradition": "Hebrew Bible",
            "language": "Hebrew",
            "source": "Project Ben-Yehuda",
            "source_url": "https://example.org/psalms-book-i",
            "category": "Poetry",
            "date_start": -1000,
            "date_end": -300,
            "summary": "Liturgical hymns and devotional poetry with broad theological themes.",
            "status": "indexed",
        },
        {
            "title": "Gospel of Matthew",
            "religion": "Christianity",
            "tradition": "Synoptic",
            "language": "Greek",
            "source": "Early Christian Manuscript Archive",
            "source_url": "https://example.org/gospel-of-matthew",
            "category": "Canonical text",
            "date_start": 50,
            "date_end": 110,
            "summary": "Narrative of Jesus with emphasis on teaching, fulfillment, and kingdom themes.",
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
            "summary": "Early revelation manuscripts and recitation units forming the opening surahs.",
            "status": "downloaded",
        },
        {
            "title": "Dhammapada",
            "religion": "Buddhism",
            "tradition": "Theravada",
            "language": "Pali",
            "source": "Buddhist Digital Archive",
            "source_url": "https://example.org/dhammapada",
            "category": "Ethical aphorisms",
            "date_start": -400,
            "date_end": 200,
            "summary": "Teaching verses on ethics, mindfulness, and the path to liberation.",
            "status": "indexed",
        },
    ]

    conn.executemany(
        """
        INSERT INTO documents (
            title, religion, tradition, language, source, source_url, category,
            date_start, date_end, summary, status
        ) VALUES (:title, :religion, :tradition, :language, :source, :source_url,
            :category, :date_start, :date_end, :summary, :status)
        """,
        sample_documents,
    )
    conn.commit()
    conn.close()
