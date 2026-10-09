from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, Citation
from app.rag import grounding, retriever
from app.rag.citations import format_locator, validate_citations
from app.rag.store import StoreUnavailable

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    try:
        hits = retriever.retrieve(req.question, course_id=req.course_id)
    except StoreUnavailable as e:
        raise HTTPException(503, f"Search index unavailable: {e}")
    g = grounding.assess(hits)
    if g.label == "not_covered":
        return ChatResponse(answer=grounding.REFUSAL, grounding=g.label)
    # TODO: TutorAgent.run(...) personalised by mastery/misconceptions; for now return the best excerpt.
    ids = validate_citations([h.chunk_id for h in hits[:2]], hits)
    cites = [Citation(chunk_id=h.chunk_id, locator=format_locator(h.meta), source_type=h.meta.get("source_type", ""),
                      file_name=h.meta.get("file_name", "")) for h in hits if h.chunk_id in ids]
    return ChatResponse(answer=hits[0].text, grounding=g.label, citations=cites)
