"""MLX inference backend via OpenAI-compatible API (mlx_lm.server)."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from kitsune.config import settings


def get_llm() -> ChatOpenAI:
    return ChatOpenAI(
        base_url=settings.mlx_base_url,
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
    # Strip EOS tokens that MLX may leak
    for token in ("<|im_end|>", "<|endoftext|>", "<|im_start|>"):
        text = text.replace(token, "")
    return text.strip()
