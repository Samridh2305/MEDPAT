import io
from typing import BinaryIO

import pytesseract
from PIL import Image
from pypdf import PdfReader

def extract_text_from_upload(
        uploaded_file: BinaryIO,
        filename: str | None = None
) -> str:
    """Extract text from uploaded report files without forcing every optional dependency."""
    name = (filename or getattr(uploaded_file, "name", "")).lower()
    data = uploaded_file.read()

    if name.endswith(".txt"):
        return data.decode("utf-8", errors="replace")
    if name.endswith(".pdf"):
        return extract_pdf_text(data)
    if name.endswith((".png", ".jpg", ".jpeg")):
        return extract_image_text(data)

    return data.decode("utf-8", errors="replace")


def extract_pdf_text(data: bytes) -> str:

    reader = PdfReader(io.BytesIO(data))

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n\n".join(pages)


def extract_image_text(data: bytes) -> str:
    image = Image.open(io.BytesIO(data))
    return pytesseract.image_to_string(image)

