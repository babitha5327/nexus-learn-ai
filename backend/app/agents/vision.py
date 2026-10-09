from typing import Any
from app.agents.base import Agent


class VisionAgent(Agent[dict[str, Any], dict[str, Any]]):
    """image -> caption, labels, relations, linked concepts (vision model, structured output)."""
    name = "vision"

    def run(self, data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("TODO: implement in its roadmap phase")
