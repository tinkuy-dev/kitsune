"""Tests for the keyword router."""

from kitsune.graph.router import route
from kitsune.graph.state import KitsuneState


def _make_state(**overrides) -> KitsuneState:
    base: KitsuneState = {
        "user_input": "",
        "task_type": "ask",
        "code_context": "",
        "file_path": "",
        "response": "",
    }
    return {**base, **overrides}


def test_explain_keyword():
    state = _make_state(user_input="explain this code", code_context="x = 1")
    result = route(state)
    assert result["task_type"] == "explain"


def test_what_does_keyword():
    state = _make_state(user_input="what does this function do?", code_context="def f(): pass")
    result = route(state)
    assert result["task_type"] == "explain"


def test_empty_input_with_code_defaults_to_explain():
    state = _make_state(user_input="", code_context="print('hello')")
    result = route(state)
    assert result["task_type"] == "explain"


def test_ask_preserved():
    state = _make_state(user_input="how many lines?", task_type="ask")
    result = route(state)
    assert result["task_type"] == "ask"


def test_generic_question_defaults_to_ask():
    state = _make_state(user_input="is this efficient?")
    result = route(state)
    assert result["task_type"] == "ask"


def test_fallback_on_architecture_long_input():
    long_code = "x = 1\n" * 500
    state = _make_state(
        user_input="design a microservice architecture for this",
        code_context=long_code,
    )
    result = route(state)
    assert result["task_type"] == "fallback"
