"""Configuration via environment variables and pydantic-settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "KITSUNE_"}

    ollama_base_url: str = "http://localhost:11434"
    model_name: str = "qwen2.5-coder:1.5b"
    temperature: float = 0.1
    fallback_threshold: int = 2000  # chars — above this, suggest Claude
    anthropic_api_key: str | None = None


settings = Settings()
