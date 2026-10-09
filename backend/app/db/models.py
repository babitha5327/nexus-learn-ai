"""Core schema. Every chunk -> unit -> source, so each citation resolves to a real locator."""
from datetime import datetime
from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


def _now() -> datetime:
    return datetime.utcnow()


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    language_pref: Mapped[str] = mapped_column(String(8), default="en")


class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    language: Mapped[str] = mapped_column(String(8), default="en")


class Source(Base):
    __tablename__ = "sources"
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    type: Mapped[str] = mapped_column(String(16))  # pdf|pptx|video|image|txt
    file_name: Mapped[str] = mapped_column(String(255))
    path: Mapped[str] = mapped_column(String(512))
    status: Mapped[str] = mapped_column(String(16), default="queued")  # queued|processing|ready|error
    error: Mapped[str | None] = mapped_column(Text, nullable=True)


class Unit(Base):
    """Smallest locatable piece of content: a page, slide, figure or transcript segment."""
    __tablename__ = "units"
    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    kind: Mapped[str] = mapped_column(String(16))  # text|table|image|diagram|transcript
    page: Mapped[int | None] = mapped_column(nullable=True)
    slide: Mapped[int | None] = mapped_column(nullable=True)
    t_start: Mapped[float | None] = mapped_column(Float, nullable=True)
    t_end: Mapped[float | None] = mapped_column(Float, nullable=True)
    text: Mapped[str] = mapped_column(Text, default="")
    image_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    vision_caption: Mapped[str | None] = mapped_column(Text, nullable=True)


class Chunk(Base):
    __tablename__ = "chunks"
    id: Mapped[int] = mapped_column(primary_key=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    text: Mapped[str] = mapped_column(Text)


class Topic(Base):
    __tablename__ = "topics"
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    name: Mapped[str] = mapped_column(String(255))
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("topics.id"), nullable=True)


class ConceptLink(Base):
    __tablename__ = "concept_links"
    id: Mapped[int] = mapped_column(primary_key=True)
    from_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    to_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    type: Mapped[str] = mapped_column(String(16))  # prerequisite|related|subtopic


class ChunkTopic(Base):
    __tablename__ = "chunk_topics"
    chunk_id: Mapped[int] = mapped_column(ForeignKey("chunks.id"), primary_key=True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), primary_key=True)


class Mastery(Base):
    __tablename__ = "mastery"
    __table_args__ = (UniqueConstraint("user_id", "topic_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    score: Mapped[float] = mapped_column(Float, default=0.5)
    n_evidence: Mapped[int] = mapped_column(Integer, default=0)


class MasteryEvent(Base):
    """Audit trail: every before/after number shown in the UI must be read from here."""
    __tablename__ = "mastery_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    before: Mapped[float] = mapped_column(Float)
    after: Mapped[float] = mapped_column(Float)
    origin: Mapped[str] = mapped_column(String(16))  # quiz|battle|teachback|chat|diagnostic
    ts: Mapped[datetime] = mapped_column(DateTime, default=_now)


class Misconception(Base):
    __tablename__ = "misconceptions"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    description: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float, default=0.3)
    count: Mapped[int] = mapped_column(Integer, default=1)


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    type: Mapped[str] = mapped_column(String(16))  # mcq|short|numeric|scenario
    stem: Mapped[str] = mapped_column(Text)
    options: Mapped[list | None] = mapped_column(JSON, nullable=True)
    answer: Mapped[str] = mapped_column(Text)
    explanation: Mapped[str] = mapped_column(Text, default="")
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    difficulty: Mapped[int] = mapped_column(Integer, default=1)
    source_chunk_ids: Mapped[list] = mapped_column(JSON, default=list)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    verify_report: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    fingerprint: Mapped[str] = mapped_column(String(64), index=True)


class Attempt(Base):
    __tablename__ = "attempts"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    response: Mapped[str] = mapped_column(Text)
    correct: Mapped[bool] = mapped_column(Boolean)
    ts: Mapped[datetime] = mapped_column(DateTime, default=_now)
