"""
Extracts text from uploaded PDF files for the PDF Chat Agent.
"""
from pypdf import PdfReader
from utils.logger import get_logger

logger = get_logger(__name__)

MAX_CHARS = 60_000  # keep extracted text within a sane prompt budget


def extract_text(file_path):
    """Read a PDF from disk and return its concatenated text content."""
    try:
        reader = PdfReader(file_path)
    except Exception as exc:
        logger.error("Failed to open PDF %s: %s", file_path, exc)
        raise ValueError("Could not read this PDF. It may be corrupted or password-protected.")

    pages_text = []
    for i, page in enumerate(reader.pages):
        try:
            pages_text.append(page.extract_text() or "")
        except Exception as exc:
            logger.warning("Failed to extract text from page %s: %s", i, exc)

    full_text = "\n\n".join(pages_text).strip()

    if not full_text:
        raise ValueError("No extractable text found in this PDF (it may be scanned images).")

    if len(full_text) > MAX_CHARS:
        full_text = full_text[:MAX_CHARS] + "\n\n[...truncated...]"

    return full_text
