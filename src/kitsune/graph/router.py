"""Keyword-based task router for MVP. LLM router planned for v0.2."""

import re

from kitsune.config import settings
from kitsune.graph.state import KitsuneState

EXPLAIN_PATTERNS = re.compile(
    r"\b(explain|what does|how does|what is|describe|walk me through)\b", re.IGNORECASE
)
ARCHITECTURE_PATTERNS = re.compile(
    r"\b(architect|design|microservice|system design|infrastructure|scalab)\b", re.IGNORECASE
)


def route(state: KitsuneState) -> KitsuneState:
    user_input = state["user_input"]
    code_context = state.get("code_context", "")
    total_len = len(user_input) + len(code_context)

    if total_len > settings.fallback_threshold and ARCHITECTURE_PATTERNS.search(user_input):
        task_type = "fallback"
    elif state.get("task_type") == "ask":
        task_type = "ask"
    elif EXPLAIN_PATTERNS.search(user_input) or (not user_input.strip() and code_context):
        task_type = "explain"
    else:
        task_type = "ask"

    return {**state, "task_type": task_type}


def get_next_node(state: KitsuneState) -> str:
    return state["task_type"]
