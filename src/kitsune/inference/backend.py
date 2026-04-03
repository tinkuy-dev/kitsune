"""Unified inference backend via OpenAI-compatible API.

Works with any server that exposes /v1/chat/completions:
- macOS: mlx_lm.server (MLX, Apple Silicon native)
- Linux/Windows: ollama serve (with OpenAI compat layer)
- Any: llama.cpp server, vLLM, LocalAI, etc.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from kitsune.config import settings


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        base_url=settings.base_url,
        api_key="not-needed",
        model=settings.model_name,
        temperature=settings.temperature,
        max_tokens=500,
    )


def invoke(system_prompt: str, user_content: str) -> str:
    llm = get_llm()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_content),
    ]
    response = llm.invoke(messages)
    text = response.content
    # Strip EOS tokens that some servers leak
    for token in ("<|im_end|>", "<|endoftext|>", "<|im_start|>"):
        text = text.replace(token, "")
    return text.strip()
