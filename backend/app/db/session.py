from collections.abc import Iterator
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.core.config import get_settings

_url = get_settings().database_url
if _url.startswith("sqlite:///"):
    Path(_url.replace("sqlite:///", "", 1)).parent.mkdir(parents=True, exist_ok=True)  # SQLite needs the folder
engine = create_engine(_url, connect_args={"check_same_thread": False} if _url.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
