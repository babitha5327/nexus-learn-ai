"""Transparent, configurable mastery model: m' = (1 - alpha) * m + alpha * evidence. No LLM involved."""
PRIOR = 0.5


def evidence(correct: bool, difficulty: int) -> float:
    """Correct on harder items counts more; a miss on a hard item is penalised less."""
    return 0.7 + 0.1 * difficulty if correct else 0.1 * (difficulty - 1)


def update(prev: float, e: float, alpha: float = 0.3) -> float:
    return (1 - alpha) * prev + alpha * max(0.0, min(1.0, e))


def status(score: float, n_evidence: int) -> str:
    if n_evidence == 0:
        return "not_studied"
    return "weak" if score < 0.4 else "learning" if score < 0.7 else "mastered"
