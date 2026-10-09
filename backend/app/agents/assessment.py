from typing import Any
from app.agents.base import Agent


class AssessmentAgent(Agent[dict[str, Any], dict[str, Any]]):
    """scope + difficulty + question history -> candidate question grounded in chunks."""
    name = "assessment"

    def run(self, data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("TODO: implement in its roadmap phase")
