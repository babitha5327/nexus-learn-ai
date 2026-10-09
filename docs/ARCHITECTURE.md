# Architecture

Upload -> parse (PDF/PPTX/video/image) -> units with locators -> chunks -> embeddings (Chroma) -> topics/graph
Ask -> retrieve -> Grounding Shield (gate -> support check -> citation validation) -> Tutor -> response
Assess -> select topic/difficulty -> generate -> verify -> dedupe -> serve -> grade -> mastery update -> misconception -> recommendation

Principles
- Every citation resolves to an ingested unit (chunk -> unit -> source). Citations are validated against retrieved chunk IDs.
- Learner model is pure math (`learner/mastery.py`), every change is logged in `mastery_events`.
- LLM calls are isolated in `services/llm.py` and always have a fallback.
- Never report metrics that were not computed. Label unfinished features Prototype / Experimental / Future.
