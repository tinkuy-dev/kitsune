"""Kitsune CLI — local code assistant."""

import sys
from pathlib import Path

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from kitsune.graph.build import app as graph_app
from kitsune.graph.state import KitsuneState

cli = typer.Typer(name="kit", help="Kitsune — local code assistant with SLMs", no_args_is_help=True)
console = Console()


def _read_file(path: str) -> tuple[str, str]:
    p = Path(path).expanduser().resolve()
    if not p.is_file():
        console.print(f"[red]File not found: {p}[/red]")
        raise typer.Exit(1)
    return p.read_text(encoding="utf-8"), str(p)


def _read_stdin() -> str:
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def _run(state: KitsuneState):
    result = graph_app.invoke(state)
    response = result["response"]
    task = result.get("task_type", "")
    title = f"Kitsune [{task}]"
    console.print(Panel(Markdown(response), title=title, border_style="cyan"))


@cli.command()
def explain(
    file: str = typer.Argument(None, help="File to explain (or pipe via stdin)"),
):
    """Explain what a piece of code does."""
    if file:
        code, fpath = _read_file(file)
    else:
        code = _read_stdin()
        fpath = "<stdin>"
        if not code:
            console.print("[yellow]Provide a file path or pipe code via stdin[/yellow]")
            raise typer.Exit(1)

    state: KitsuneState = {
        "user_input": "",
        "task_type": "explain",
        "code_context": code,
        "file_path": fpath,
        "response": "",
    }
    _run(state)


@cli.command()
def ask(
    question: str = typer.Argument(..., help="Question about the code"),
    file: str = typer.Option(None, "--file", "-f", help="File for context"),
):
    """Ask a question about code."""
    code = ""
    fpath = ""
    if file:
        code, fpath = _read_file(file)
    else:
        stdin_code = _read_stdin()
        if stdin_code:
            code = stdin_code
            fpath = "<stdin>"

    state: KitsuneState = {
        "user_input": question,
        "task_type": "ask",
        "code_context": code,
        "file_path": fpath,
        "response": "",
    }
    _run(state)


@cli.command()
def status():
    """Show Kitsune status."""
    import httpx

    from kitsune.config import settings

    console.print(f"[bold]Model:[/bold] {settings.model_name}")
    console.print(f"[bold]Ollama:[/bold] {settings.ollama_base_url}")

    try:
        r = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=3)
        models = [m["name"] for m in r.json().get("models", [])]
        if models:
            console.print(f"[bold]Available models:[/bold] {', '.join(models)}")
        else:
            console.print("[yellow]No models loaded in Ollama[/yellow]")
    except httpx.ConnectError:
        console.print("[red]Ollama not running. Start with: ollama serve[/red]")


# Typer app entry point
app = cli
