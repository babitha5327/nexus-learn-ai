from dataclasses import dataclass


@dataclass
class Action:
    kind: str       # diagnostic | review_misconception | review_prerequisite | practice | explore
    topic: str | None
    reason: str


def next_best_action(mastery: dict[str, tuple[float, int]], prereqs: dict[str, list[str]],
                     misconceptions: list[tuple[str, str, float]]) -> Action:
    """mastery: topic -> (score, n_evidence); misconceptions: (topic, description, confidence). Rule-based."""
    studied = {t: s for t, (s, n) in mastery.items() if n > 0}
    if not studied:
        return Action("diagnostic", None, "No learner history yet.")
    if misconceptions:
        t, d, c = max(misconceptions, key=lambda m: m[2])
        if c >= 0.45:
            return Action("review_misconception", t, f"{d} (confidence {c:.0%})")
    weakest = min(studied, key=studied.get)
    if studied[weakest] < 0.6:
        for p in prereqs.get(weakest, []):
            if mastery.get(p, (0, 0))[1] == 0 or mastery[p][0] < 0.5:
                return Action("review_prerequisite", p, f"{weakest} is weak and prerequisite {p} is not solid.")
        return Action("practice", weakest, f"Lowest mastery ({studied[weakest]:.0%}).")
    unstudied = next((t for t, (_, n) in mastery.items() if n == 0), None)
    return Action("explore", unstudied, "Not studied yet.") if unstudied else Action("practice", None, "Mixed review.")
