"""Ollama inference backend via LangChain."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from kitsune.config import settings


def get_llm() -> ChatOllama:
    return ChatOllama(
        base_url=settings.ollama_base_url,
        model=settings.model_name,
        temperature=settings.temperature,
    )


def invoke(system_prompt: str, user_content: str) -> str:
    llm = get_llm()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_content),
    ]
    response = llm.invoke(messages)
    return response.content
