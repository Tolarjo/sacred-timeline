import io
import os
from typing import Any, Dict, Optional, Tuple

import httpx
import pdfplumber
from PIL import Image

try:
    import pytesseract
except ImportError:
    pytesseract = None


async def download_file(url: str) -> Optional[bytes]:
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content
    except Exception:
        return None


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            text_blocks = []
            for page in pdf.pages[:10]:  # limit to first 10 pages
                text = page.extract_text()
                if text:
                    text_blocks.append(text)
            return "\n".join(text_blocks)[:8000]  # limit to 8000 chars
    except Exception:
        return ""


def extract_text_from_image(image_bytes: bytes) -> str:
    if pytesseract is None:
        return ""
    try:
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text[:4000]
    except Exception:
        return ""


async def extract_from_url(url: str) -> Tuple[str, str]:
    """
    Attempt to extract text from a URL.
    Returns (text, extraction_method).
    """
    content = await download_file(url)
    if not content:
        return "", "failed"

    if url.lower().endswith(".pdf") or b"%PDF" in content[:10]:
        text = extract_text_from_pdf(content)
        if text:
            return text, "pdf_plumber"

    if content[:4] in (b"\xff\xd8\xff\xe0", b"\xff\xd8\xff\xe1"):
        text = extract_text_from_image(content)
        if text:
            return text, "tesseract"

    return "", "unsupported"

