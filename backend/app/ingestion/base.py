from dataclasses import dataclass


@dataclass
class ParsedUnit:
    """Parser output. Exactly one locator family is set: page | slide | (t_start, t_end)."""
    kind: str                      # text|table|image|diagram|transcript
    text: str = ""
    page: int | None = None
    slide: int | None = None
    t_start: float | None = None
    t_end: float | None = None
    image_path: str | None = None
