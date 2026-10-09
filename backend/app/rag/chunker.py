import re


def chunk_text(text: str, max_words: int = 180, overlap_sents: int = 1) -> list[str]:
    """Sentence-aware chunking with a small overlap. Never splits mid-sentence."""
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n{2,}", text) if s.strip()]
    chunks: list[str] = []
    cur: list[str] = []
    for s in sents:
        if cur and sum(len(x.split()) for x in cur) + len(s.split()) > max_words:
            chunks.append(" ".join(cur))
            cur = cur[-overlap_sents:] if overlap_sents else []
        cur.append(s)
    if cur:
        chunks.append(" ".join(cur))
    return chunks
