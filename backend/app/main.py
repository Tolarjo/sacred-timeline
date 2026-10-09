import json
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup


def infer_source_type(url: str) -> str:
    domain = urlparse(url).netloc.lower()
    if "sefaria" in domain:
        return "sefaria"
    if "openiti" in domain:
        return "openiti"
    if "archive.org" in domain or "archive" in domain:
        return "archive"
    if "books.google" in domain or "google" in domain:
        return "google_books"
    if url.lower().endswith(".pdf"):
        return "pdf"
    return "generic"


def metadata_from_html(html: str, url: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else "Untitled source"
    description_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    description = description_tag.get("content", "") if description_tag else ""
    text_blocks = [
        " ".join(p.get_text(" ", strip=True) for p in soup.select("p, li, h1, h2, h3, h4"))
    ]
    body_text = " ".join(part for part in text_blocks if part).strip()
    return {
        "title": title,
        "description": description,
        "url": url,
        "body_text": body_text[:4000],
    }


async def fetch_url_metadata(source_url: str) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=20.0) as client:
            response = await client.get(source_url)
            response.raise_for_status()
            html = response.text
            metadata = metadata_from_html(html, source_url)
            metadata["source_type"] = infer_source_type(source_url)
            return metadata
    except Exception:
        return {
            "title": "Imported source",
            "description": "",
            "url": source_url,
            "source_type": infer_source_type(source_url),
            "body_text": "",
        }


def build_document_from_source(source_url: str, religion: Optional[str] = None, source_name: Optional[str] = None) -> Dict[str, Any]:
    source_type = infer_source_type(source_url)
    return {
        "title": source_name or f"{source_type.title()} source",
        "religion": religion or "Unspecified",
        "tradition": "Imported",
        "language": "Unknown",
        "source": source_type,
        "source_url": source_url,
        "category": "Imported source",
        "date_start": None,
        "date_end": None,
        "summary": "Source discovered and cataloged by the ingestion pipeline.",
        "body_text": "",
        "status": "queued",
    }


def serialize_metadata(metadata: Dict[str, Any]) -> str:
    return json.dumps(metadata, ensure_ascii=False)


async def extract_text_from_url(source_url: str) -> str:
    metadata = await fetch_url_metadata(source_url)
    text = metadata.get("body_text") or ""
    if not text:
        return "No text extraction available for this source yet."
    return text

