from typing import Any
from app.agents.base import Agent


class KnowledgeAgent(Agent[dict[str, Any], dict[str, Any]]):
    """chunks -> topics, concepts, prerequisites (structured JSON from LLM, then dedupe/merge)."""
    name = "knowledge"

    def run(self, data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError("TODO: implement in its roadmap phase")
