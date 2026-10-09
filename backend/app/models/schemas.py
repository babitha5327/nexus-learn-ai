from pydantic import BaseModel


class Citation(BaseModel):
    chunk_id: str
    locator: str                 # e.g. "Slide 18", "Page 42", "12:34-13:21"
    source_type: str
    file_name: str


class ChatRequest(BaseModel):
    question: str
    course_id: int | None = None
    allow_external: bool = False  # TODO: external answers must be clearly labelled


class ChatResponse(BaseModel):
    answer: str
    grounding: str                # grounded | partial | not_covered
    citations: list[Citation] = []


class EvidenceIn(BaseModel):
    topic_id: int
    correct: bool
    difficulty: int = 1
    origin: str = "quiz"
