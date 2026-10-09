import re
import uuid
from pathlib import Path
from fastapi import HTTPException, UploadFile
from app.core.config import get_settings


def safe_name(name: str) -> str:
    base = re.sub(r"[^A-Za-z0-9._-]", "_", Path(name).name)[:100] or "file"
    return f"{uuid.uuid4().hex[:8]}_{base}"


async def save_upload(f: UploadFile) -> Path:
    s = get_settings()
    ext = Path(f.filename or "").suffix.lower()
    if ext not in s.allowed_ext:
        raise HTTPException(415, f"Unsupported file type '{ext}'. Allowed: {', '.join(s.allowed_ext)}")
    dest = Path(s.upload_dir) / safe_name(f.filename or "file")
    dest.parent.mkdir(parents=True, exist_ok=True)
    size, limit = 0, s.max_upload_mb * 1024 * 1024
    with dest.open("wb") as out:
        while chunk := await f.read(1024 * 1024):
            size += len(chunk)
            if size > limit:
                out.close(); dest.unlink(missing_ok=True)
                raise HTTPException(413, f"File exceeds {s.max_upload_mb} MB limit.")
            out.write(chunk)
    if size == 0:
        dest.unlink(missing_ok=True)
        raise HTTPException(400, "Uploaded file is empty.")
    return dest
