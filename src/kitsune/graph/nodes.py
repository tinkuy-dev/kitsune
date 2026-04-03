"""Task-specific LangGraph nodes."""

from kitsune.graph.state import KitsuneState
from kitsune.inference.ollama_backend import invoke
from kitsune.prompts.templates import ASK, EXPLAIN, FALLBACK_MSG


def explain_node(state: KitsuneState) -> KitsuneState:
    code = state["code_context"]
    user_msg = state["user_input"]
    prompt = f"{user_msg}\n\n```\n{code}\n```" if user_msg.strip() else f"```\n{code}\n```"
    response = invoke(EXPLAIN, prompt)
    return {**state, "response": response}


def ask_node(state: KitsuneState) -> KitsuneState:
    code = state["code_context"]
    question = state["user_input"]
    prompt = f"Question: {question}"
    if code:
        prompt += f"\n\nCode context:\n```\n{code}\n```"
    response = invoke(ASK, prompt)
    return {**state, "response": response}


def fallback_node(state: KitsuneState) -> KitsuneState:
    response = FALLBACK_MSG.format(
        prompt=state["user_input"],
        file_path=state.get("file_path", "<stdin>"),
    )
    return {**state, "response": response}
