"""Grounding Shield. Stage 1 = retrieval gate (here). TODO stage 2 = LLM support/entailment check."""
from dataclasses import dataclass
from app.core.config import get_settings
from app.rag.store import Hit

REFUSAL = "Your uploaded course material does not contain enough information to answer this reliably."


@dataclass
class Grounding:
    label: str          # grounded | partial | not_covered
    top_score: float


def assess(hits: list[Hit]) -> Grounding:
    s = get_settings()
    top = max((h.score for h in hits), default=0.0)
    label = "grounded" if top >= s.ground_hi else "partial" if top >= s.ground_lo else "not_covered"
    return Grounding(label, top)
