"""Configuration via environment variables and pydantic-settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "KITSUNE_"}

    mlx_base_url: str = "http://localhost:8008/v1"
    model_name: str = "mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit"
    temperature: float = 0.1
    fallback_threshold: int = 2000  # chars — above this, suggest Claude
    anthropic_api_key: str | None = None


settings = Settings()
