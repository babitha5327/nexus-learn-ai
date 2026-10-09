from typing import Any
from app.agents.base import Agent


class TutorAgent(Agent[dict[str, Any], dict[str, Any]]):
    """question + retrieved chunks + mastery + misconceptions -> concise cited explanation (no chain-of-thought)."""
    name = "tutor"

    def run(self, data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("TODO: implement in its roadmap phase")
