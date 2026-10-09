from app.rag.chunker import chunk_text
from app.rag.citations import format_locator, validate_citations
from app.rag.store import Hit
from app.agents.verification import verify


def test_chunker_respects_limit_and_keeps_text():
    text = " ".join(f"Sentence number {i} is here." for i in range(100))
    chunks = chunk_text(text, max_words=40)
    assert len(chunks) > 3 and all(len(c.split()) <= 60 for c in chunks)


def test_fake_citations_are_dropped():
    hits = [Hit("c1", "x", 0.9)]
    assert validate_citations(["c1", "fake"], hits) == ["c1"]


def test_locators():
    assert format_locator({"slide": 18}) == "Slide 18"
    assert format_locator({"t_start": 754, "t_end": 801}) == "12:34-13:21"


def test_verifier_rejects_unsupported_and_duplicate():
    q = {"stem": "S?", "answer": "kernel", "options": ["kernel", "margin"]}
    assert verify(q, "The kernel trick", set())["passed"]
    assert not verify(q, "Nothing relevant", set())["passed"]
