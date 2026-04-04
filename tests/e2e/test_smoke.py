"""E2E smoke tests — run against real MLX/Ollama server.

These tests require a running inference server. Skip automatically if not available.

Run explicitly:
    uv run pytest tests/e2e/ -v
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent.parent / "fixtures"
KIT = [sys.executable, "-m", "kitsune"]
PROJECT_ROOT = Path(__file__).parent.parent.parent


def _run_kit(*args: str, timeout: int = 45) -> str:
    env = {**os.environ, "COLUMNS": "120", "FORCE_COLOR": "0"}
    result = subprocess.run(
        [*KIT, *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=PROJECT_ROOT,
        env=env,
    )
    # Rich outputs to stdout, warnings to stderr
    return (result.stdout + result.stderr).lower()


def _server_available() -> bool:
    try:
        import httpx

        r = httpx.get("http://localhost:8008/v1/models", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _server_available(),
    reason="Inference server not running (start mlx_lm.server or ollama serve)",
)


# ===== DoD: kit explain =====


class TestExplainDoD:
    """Definition of Done for kit explain."""

    def test_python_mentions_key_concepts(self):
        output = _run_kit("explain", str(FIXTURES / "sample_python.py"))
        # Must identify at least 2 of these key concepts from the file
        hits = sum(
            1
            for term in ["user", "dataclass", "protocol", "async", "active", "fetch"]
            if term in output
        )
        assert hits >= 2, f"Only found {hits} key concepts. Output:\n{output[:500]}"

    def test_javascript_detects_patterns(self):
        output = _run_kit("explain", str(FIXTURES / "sample_javascript.js"))
        assert any(term in output for term in ["event", "emitter", "retry", "fetch", "callback"]), (
            f"No JS patterns found. Output:\n{output[:500]}"
        )

    def test_go_detects_concurrency(self):
        output = _run_kit("explain", str(FIXTURES / "sample_go.go"))
        assert any(
            term in output
            for term in ["goroutine", "concurrent", "parallel", "wait", "sync", "channel"]
        ), f"No Go concurrency patterns found. Output:\n{output[:500]}"

    def test_does_not_fabricate(self):
        """Explain should not mention things that don't exist in the file."""
        output = _run_kit("explain", str(FIXTURES / "sample_python.py"))
        for fake in ["authenticate", "database", "sql query", "http server", "flask app"]:
            assert fake not in output, f"Fabricated concept: {fake}"

    def test_response_is_bounded(self):
        output = _run_kit("explain", str(FIXTURES / "sample_python.py"))
        lines = [ln for ln in output.strip().split("\n") if ln.strip()]
        assert len(lines) < 40, f"Too verbose: {len(lines)} lines"


# ===== DoD: kit ask =====


class TestAskDoD:
    """Definition of Done for kit ask."""

    def test_answers_specific_question(self):
        output = _run_kit(
            "ask", "what does find_active_users return?", "-f", str(FIXTURES / "sample_python.py")
        )
        assert any(term in output for term in ["list", "active", "user", "filter"]), (
            f"Didn't answer about return value. Output:\n{output[:500]}"
        )

    def test_references_code_names(self):
        output = _run_kit(
            "ask", "what is the User class?", "-f", str(FIXTURES / "sample_python.py")
        )
        assert "user" in output
        assert any(term in output for term in ["name", "email", "dataclass", "active"])

    def test_does_not_overexplain(self):
        """Ask should answer the question, not explain the whole file."""
        output = _run_kit(
            "ask", "what does deactivate do?", "-f", str(FIXTURES / "sample_python.py")
        )
        content_lines = [ln for ln in output.strip().split("\n") if ln.strip() and "─" not in ln]
        assert len(content_lines) < 25, f"Too verbose: {len(content_lines)} lines"


# ===== DoD: Escalation =====


class TestEscalationDoD:
    """Definition of Done for escalation/fallback."""

    def test_security_escalates(self):
        output = _run_kit(
            "ask",
            "check for XSS vulnerabilities in this code",
            "-f",
            str(FIXTURES / "sample_javascript.js"),
        )
        assert "security" in output
        assert "claude" in output or "exceeds" in output or "larger model" in output

    def test_architecture_escalates(self):
        output = _run_kit("ask", "redesign this as a microservice architecture")
        assert "claude" in output or "exceeds" in output or "architecture" in output

    def test_simple_explain_stays_local(self):
        """A simple explain should NOT escalate."""
        output = _run_kit("explain", str(FIXTURES / "sample_python.py"))
        assert "exceeds" not in output
        assert "larger model" not in output


# ===== DoD: Status =====


class TestStatusDoD:
    def test_shows_backend_and_model(self):
        output = _run_kit("status")
        assert "backend" in output
        assert "model" in output
        assert "server" in output
