from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, health, learner, quiz, sources
from app.core.config import get_settings
from app.core.logging import setup_logging
from app.db.models import Base
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    setup_logging()
    Base.metadata.create_all(engine)
    yield


s = get_settings()
app = FastAPI(title=s.app_name, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=s.cors_origins, allow_methods=["*"], allow_headers=["*"])
for r in (health.router, sources.router, chat.router, learner.router, quiz.router):
    app.include_router(r, prefix="/api")
