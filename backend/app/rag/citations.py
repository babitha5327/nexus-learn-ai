from app.rag.store import Hit


def validate_citations(cited_ids: list[str], retrieved: list[Hit]) -> list[str]:
    """Drop any citation that was not actually retrieved: fake citations can never reach the UI."""
    ok = {h.chunk_id for h in retrieved}
    return [c for c in dict.fromkeys(cited_ids) if c in ok]


def format_locator(meta: dict) -> str:
    if meta.get("slide") is not None:
        return f"Slide {meta['slide']}"
    if meta.get("page") is not None:
        return f"Page {meta['page']}"
    if meta.get("t_start") is not None:
        f = lambda t: f"{int(t)//60:02d}:{int(t)%60:02d}"
        return f"{f(meta['t_start'])}-{f(meta['t_end'])}"
    return "Unknown location"
