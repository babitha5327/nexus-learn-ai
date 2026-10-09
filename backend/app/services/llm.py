import httpx
from app.core.config import get_settings


class LLMUnavailable(RuntimeError):
    pass


def chat(messages: list[dict], json_mode: bool = False, timeout: float = 30.0) -> str:
    """OpenAI-compatible chat call. Callers MUST handle LLMUnavailable and fall back gracefully."""
    s = get_settings()
    if not (s.llm_api_key or "localhost" in s.llm_base_url) or not s.llm_model:
        raise LLMUnavailable("LLM not configured (set LLM_API_KEY / LLM_MODEL in .env).")
    body = {"model": s.llm_model, "messages": messages, "temperature": 0.2}
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    try:
        r = httpx.post(f"{s.llm_base_url}/chat/completions", json=body, timeout=timeout,
                       headers={"Authorization": f"Bearer {s.llm_api_key}"})
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except httpx.HTTPError as e:
        raise LLMUnavailable(str(e)) from e
