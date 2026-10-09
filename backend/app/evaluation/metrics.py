"""Deterministic retrieval metrics. RAGAS/DeepEval (faithfulness, answer relevancy) go in ragas_runner.py (TODO)."""


def hit_at_k(expected_ids: list[str | None], retrieved: list[list[str]], k: int) -> float:
    pairs = [(e, r) for e, r in zip(expected_ids, retrieved) if e is not None]
    return sum(e in r[:k] for e, r in pairs) / len(pairs) if pairs else 0.0


def refusal_accuracy(answerable: list[bool], labels: list[str]) -> dict[str, float]:
    off = [l for a, l in zip(answerable, labels) if not a]
    on = [l for a, l in zip(answerable, labels) if a]
    return {"correct_refusal": sum(l == "not_covered" for l in off) / len(off) if off else 0.0,
            "false_refusal": sum(l == "not_covered" for l in on) / len(on) if on else 0.0}
