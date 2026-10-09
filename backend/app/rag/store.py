"""Chroma wrapper. Imports are lazy so the API still boots without the heavy ML deps."""
from dataclasses import dataclass, field


class StoreUnavailable(RuntimeError):
    pass


@dataclass
class Hit:
    chunk_id: str
    text: str
    score: float                    # similarity in [0, 1]
    meta: dict = field(default_factory=dict)  # source_id, source_type, file_name, page, slide, t_start, t_end, topic


def _collection():
    try:
        from app.core.config import get_settings
        import chromadb
        from chromadb.utils import embedding_functions as ef
        s = get_settings()
        client = chromadb.PersistentClient(path=s.chroma_dir)
        return client.get_or_create_collection(
            "chunks", embedding_function=ef.SentenceTransformerEmbeddingFunction(model_name=s.embedding_model),
            metadata={"hnsw:space": "cosine"})
    except Exception as e:  # noqa: BLE001
        raise StoreUnavailable(str(e)) from e


def add(ids: list[str], texts: list[str], metas: list[dict]) -> None:
    _collection().add(ids=ids, documents=texts, metadatas=metas)


def query(text: str, k: int = 5, where: dict | None = None) -> list[Hit]:
    res = _collection().query(query_texts=[text], n_results=k, where=where)
    return [Hit(i, d, 1 - dist, m) for i, d, dist, m in
            zip(res["ids"][0], res["documents"][0], res["distances"][0], res["metadatas"][0])]
