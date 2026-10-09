from app.learner import mastery as m
from app.learner.recommender import next_best_action


def test_update_moves_toward_evidence():
    assert abs(m.update(0.5, 1.0, 0.3) - 0.65) < 1e-9
    assert abs(m.update(0.5, 0.0, 0.3) - 0.35) < 1e-9


def test_evidence_weights_difficulty():
    assert m.evidence(True, 3) > m.evidence(True, 1)
    assert m.evidence(False, 3) > m.evidence(False, 1)


def test_new_student_gets_diagnostic():
    assert next_best_action({"SVM": (0.5, 0)}, {}, []).kind == "diagnostic"


def test_prerequisite_gap_recommended_first():
    a = next_best_action({"SVM": (0.5, 0), "Kernel": (0.3, 2)}, {"Kernel": ["SVM"]}, [])
    assert (a.kind, a.topic) == ("review_prerequisite", "SVM")
