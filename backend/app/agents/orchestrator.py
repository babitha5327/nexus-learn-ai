"""Deterministic router: intent -> ordered agent pipeline. LLM calls only inside agents, never for routing."""
from enum import Enum


class Intent(str, Enum):
    ASK = "ask"
    EXPLAIN_IMAGE = "explain_image"
    QUIZ = "quiz"
    TEACH_BACK = "teach_back"


PIPELINES: dict[Intent, list[str]] = {
    Intent.ASK: ["retrieve", "grounding", "tutor", "citation_validation", "learner_evidence"],
    Intent.EXPLAIN_IMAGE: ["vision", "retrieve", "grounding", "tutor", "citation_validation"],
    Intent.QUIZ: ["select_topic", "assessment", "verification", "dedupe", "serve"],
    Intent.TEACH_BACK: ["retrieve", "tutor_eval", "misconception", "learner_evidence", "recommend"],
}


def plan(intent: Intent) -> list[str]:
    return PIPELINES[intent]
