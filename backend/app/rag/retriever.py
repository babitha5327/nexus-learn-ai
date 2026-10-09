from app.rag import store


def retrieve(question: str, k: int = 5, course_id: int | None = None) -> list[store.Hit]:
    where = {"course_id": course_id} if course_id else None
    return store.query(question, k=k, where=where)  # TODO: rerank (cross-encoder) if time permits
