from typing import Any
from app.agents.base import Agent


class MisconceptionAgent(Agent[dict[str, Any], dict[str, Any]]):
    """wrong answer + question + chunks -> likely misconception + confidence."""
    name = "misconception"

    def run(self, data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("TODO: implement in its roadmap phase")
