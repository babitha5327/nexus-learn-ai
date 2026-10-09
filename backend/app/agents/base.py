from abc import ABC, abstractmethod
from typing import Generic, TypeVar

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")


class Agent(ABC, Generic[TIn, TOut]):
    """Typed unit of work. Agents are plain classes; the Orchestrator composes them deterministically."""
    name: str = "agent"

    @abstractmethod
    def run(self, data: TIn) -> TOut: ...
