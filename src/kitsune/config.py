"""Configuration via environment variables and pydantic-settings."""

import platform

from pydantic_settings import BaseSettings

_SYSTEM = platform.system()


def _default_backend() -> str:
    return "mlx" if _SYSTEM == "Darwin" else "ollama"


def _default_base_url() -> str:
    if _SYSTEM == "Darwin":
        return "http://localhost:8008/v1"  # mlx_lm.server
    return "http://localhost:11434/v1"  # ollama


def _default_model() -> str:
    if _SYSTEM == "Darwin":
        return "mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit"
    return "qwen2.5-coder:1.5b"


class Settings(BaseSettings):
    model_config = {"env_prefix": "KITSUNE_"}

    backend: str = _default_backend()
    base_url: str = _default_base_url()
    model_name: str = _default_model()
    temperature: float = 0.1
    fallback_threshold: int = 2000
    anthropic_api_key: str | None = None


settings = Settings()
