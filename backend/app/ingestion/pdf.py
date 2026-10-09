from pathlib import Path
from app.ingestion.base import ParsedUnit


def parse_pdf(path: Path) -> list[ParsedUnit]:
    import fitz  # PyMuPDF
    units: list[ParsedUnit] = []
    with fitz.open(path) as doc:
        for i, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            if text:
                units.append(ParsedUnit("text", text, page=i))
            # TODO: tables (pdfplumber), embedded images -> Vision Agent, OCR fallback when text is empty
    return units
