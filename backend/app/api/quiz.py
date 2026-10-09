from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.post("/next")
def next_question() -> dict:
    # TODO: pick topic/difficulty from mastery -> AssessmentAgent -> verify() -> dedupe -> serve
    raise HTTPException(501, "Adaptive quiz not implemented yet (Phase 8-9).")
