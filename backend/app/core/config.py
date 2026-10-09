from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """All config comes from environment variables (see .env.example). Never hard-code secrets."""
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")

    app_name: str = "NEXUS LEARN AI"
    database_url: str = "sqlite:///./data/nexus.db"
    upload_dir: str = "./data/uploads"
    chroma_dir: str = "./data/chroma"
    max_upload_mb: int = 100
    allowed_ext: tuple[str, ...] = (".pdf", ".ppt", ".pptx", ".mp4", ".mov", ".png", ".jpg", ".jpeg", ".txt")
    cors_origins: list[str] = ["http://localhost:5173"]

    llm_base_url: str = "https://api.openai.com/v1"
    llm_api_key: str = ""
    llm_model: str = ""
    vision_model: str = ""
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    stt_model: str = "small"

    mastery_alpha: float = 0.3   # learner-model update rate
    ground_hi: float = 0.75      # >= grounded (calibrate on the eval set!)
    ground_lo: float = 0.40      # >= partial, else not covered


@lru_cache
def get_settings() -> Settings:
    return Settings()
