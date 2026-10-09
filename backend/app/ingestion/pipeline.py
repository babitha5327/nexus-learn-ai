"""upload -> parse -> units (+locators) -> chunks -> embeddings -> vector store -> topics/graph."""
import logging
from pathlib import Path
from app.ingestion.base import ParsedUnit
from app.ingestion.pdf import parse_pdf
from app.ingestion.pptx import parse_pptx

log = logging.getLogger(__name__)


def parse_txt(path: Path) -> list[ParsedUnit]:
    return [ParsedUnit("text", path.read_text(errors="ignore"), page=1)]


def get_parser(ext: str):
    if ext == ".pdf":
        return parse_pdf
    if ext in (".pptx", ".ppt"):
        return parse_pptx
    if ext in (".mp4", ".mov"):
        from app.ingestion.video import parse_video
        return parse_video
    if ext == ".txt":
        return parse_txt
    # TODO: .png/.jpg/.jpeg -> Vision Agent (caption + labels + relations)
    raise ValueError(f"No parser for {ext}")


def process_source(source_id: int) -> None:
    """Background job. Must never raise: set status='error' with a user-friendly message instead."""
    from app.db.models import Chunk, Source, Unit
    from app.db.session import SessionLocal
    from app.rag.chunker import chunk_text

    db = SessionLocal()
    src = db.get(Source, source_id)
    try:
        src.status = "processing"; db.commit()
        units = get_parser(Path(src.path).suffix.lower())(Path(src.path))
        if not units:
            raise ValueError("No extractable content found (empty or scanned document; OCR not enabled yet).")
        for pu in units:
            u = Unit(source_id=src.id, kind=pu.kind, text=pu.text, page=pu.page, slide=pu.slide,
                     t_start=pu.t_start, t_end=pu.t_end, image_path=pu.image_path)
            db.add(u); db.flush()
            for c in chunk_text(pu.text):
                db.add(Chunk(unit_id=u.id, text=c))
        db.commit()
        # TODO: embed chunks -> rag.store.add(); Knowledge Agent -> topics/prereqs; link chunk_topics
        src.status = "ready"; db.commit()
    except Exception as e:  # noqa: BLE001
        log.exception("ingestion failed for source %s", source_id)
        db.rollback(); src.status = "error"; src.error = str(e)[:500]; db.commit()
    finally:
        db.close()
