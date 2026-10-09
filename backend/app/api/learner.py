from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.db.models import Mastery, MasteryEvent, User
from app.db.session import get_db
from app.learner import mastery as m
from app.models.schemas import EvidenceIn

router = APIRouter(prefix="/learner", tags=["learner"])


def demo_user(db: Session) -> User:
    u = db.query(User).first() or User(email="demo@nexus.ai")
    db.add(u); db.flush()
    return u


@router.post("/evidence")
def add_evidence(e: EvidenceIn, db: Session = Depends(get_db)) -> dict:
    u = demo_user(db)
    row = db.query(Mastery).filter_by(user_id=u.id, topic_id=e.topic_id).first() or Mastery(user_id=u.id, topic_id=e.topic_id)
    before = row.score if row.n_evidence else m.PRIOR
    row.score = m.update(before, m.evidence(e.correct, e.difficulty), get_settings().mastery_alpha)
    row.n_evidence = (row.n_evidence or 0) + 1
    db.add(row); db.add(MasteryEvent(user_id=u.id, topic_id=e.topic_id, before=before, after=row.score, origin=e.origin))
    db.commit()
    return {"before": before, "after": row.score}


@router.get("/twin")
def twin(db: Session = Depends(get_db)) -> dict:
    u = demo_user(db)
    rows = db.query(Mastery).filter_by(user_id=u.id).all()
    return {"mastery": [{"topic_id": r.topic_id, "score": r.score, "n": r.n_evidence, "status": m.status(r.score, r.n_evidence)} for r in rows]}
