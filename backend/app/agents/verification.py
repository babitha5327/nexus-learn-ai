import hashlib
from typing import Any


def fingerprint(stem: str, answer: str) -> str:
    return hashlib.sha1(f"{stem.lower().strip()}|{answer.lower().strip()}".encode()).hexdigest()


def verify(q: dict[str, Any], source_text: str, seen: set[str]) -> dict[str, Any]:
    """Deterministic checks. TODO: add cross-solve (LLM answers from source only) and embedding-similarity dedupe."""
    checks = {
        "answer_in_source": q["answer"].lower() in source_text.lower(),
        "not_duplicate": fingerprint(q["stem"], q["answer"]) not in seen,
        "options_unique": len({o.lower() for o in q.get("options", [])}) == len(q.get("options", [])),
        "answer_in_options": not q.get("options") or q["answer"] in q["options"],
    }
    return {"passed": all(checks.values()), "checks": checks}
