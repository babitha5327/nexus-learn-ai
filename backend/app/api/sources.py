from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.db.models import Course, Source
from app.db.session import get_db
from app.ingestion.pipeline import process_source
from app.services.storage import save_upload

router = APIRouter(prefix="/sources", tags=["sources"])


@router.post("/upload")
async def upload(bg: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db)) -> dict:
    path = await save_upload(file)
    course = db.query(Course).first() or Course(title="My course")
    db.add(course); db.flush()
    src = Source(course_id=course.id, type=path.suffix.lstrip("."), file_name=file.filename or path.name, path=str(path))
    db.add(src); db.commit()
    bg.add_task(process_source, src.id)
    return {"source_id": src.id, "status": src.status}


@router.get("/{source_id}/status")
def status(source_id: int, db: Session = Depends(get_db)) -> dict:
    s = db.get(Source, source_id)
    return {"status": s.status if s else "not_found", "error": s.error if s else None}
