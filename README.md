# Kitsune

Local code assistant powered by Small Language Models (SLMs) and [LangGraph](https://langchain-ai.github.io/langgraph/).

Runs entirely on your machine. No API keys, no cloud calls, no telemetry. Your code stays local.

## Platform Support

| OS | Backend | Model Server |
|----|---------|-------------|
| **macOS** (Apple Silicon) | MLX | `mlx_lm.server` |
| **Linux** (Ubuntu/Debian) | Ollama | `ollama serve` |
| **Windows** | Ollama | `ollama serve` |

Kitsune auto-detects your OS and configures the right backend. All backends expose the same OpenAI-compatible API.

## Quick Start

### 1. Install Kitsune

```bash
git clone https://github.com/dereyesm/kitsune.git
cd kitsune
uv sync
```

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

### 2. Start a model server

**macOS (Apple Silicon):**
```bash
uv tool install mlx-lm
mlx_lm.server --model mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit --port 8008
```

**Linux / Windows:**
```bash
# Install Ollama: https://ollama.com/download
ollama pull qwen2.5-coder:1.5b
ollama serve
```

### 3. Use

```bash
# Explain a file
uv run kit explain path/to/file.py

# Ask a question with code context
uv run kit ask "what does this function do?" -f path/to/file.py

# Pipe from clipboard (macOS)
pbpaste | uv run kit explain

# Check status
uv run kit status
```

## How It Works

```
Input --> [Router] --> explain  --> [Qwen 1.5B] --> Rich output
      (multi-gate)  --> ask      --> [Qwen 1.5B] --> Rich output
                    --> fallback --> "Use Claude for this" + reason
```

- **Router**: multi-gate escalation (security, architecture, complexity, token budget) — zero latency, no LLM call
- **Inference**: any OpenAI-compatible server (MLX, Ollama, llama.cpp, vLLM)
- **Prompts**: skill-based injection per programming language (Python, JS/TS, Go, Rust)
- **Orchestration**: LangGraph state graph
- **Output**: Rich panels with Markdown rendering

## Architecture

Kitsune connects to any server that exposes `/v1/chat/completions`. This means you can use any backend:

```bash
# macOS — MLX (native Apple Silicon, ~1GB RAM)
mlx_lm.server --model mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit --port 8008

# Linux/Windows — Ollama
ollama serve  # default port 11434, OpenAI compat at /v1

# Any — llama.cpp server
llama-server -m model.gguf --port 8008

# Override in Kitsune
KITSUNE_BASE_URL="http://localhost:8080/v1" uv run kit explain file.py
```

### RAM Usage

| Component | RAM |
|-----------|-----|
| Model server + Qwen 1.5B (4-bit) | ~1.2 GB |
| Python + LangGraph | ~0.2 GB |
| **Total** | **~1.4 GB** |

## Configuration

All settings via environment variables (prefix `KITSUNE_`):

| Variable | Default (macOS) | Default (Linux/Win) | Description |
|----------|----------------|-------------------|-------------|
| `KITSUNE_BACKEND` | `mlx` | `ollama` | Backend type |
| `KITSUNE_BASE_URL` | `http://localhost:8008/v1` | `http://localhost:11434/v1` | Server URL |
| `KITSUNE_MODEL_NAME` | `mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit` | `qwen2.5-coder:1.5b` | Model name |
| `KITSUNE_TEMPERATURE` | `0.1` | `0.1` | Generation temperature |

## Skill-Based Prompts

Kitsune injects language-specific knowledge into prompts based on file extension:

| Extension | Skill | Knowledge |
|-----------|-------|-----------|
| `.py` | Python | Decorators, async, type hints, FastAPI/Django patterns |
| `.js/.ts/.tsx` | JavaScript | Promises, closures, this binding, React/Node patterns |
| `.go` | Go | Goroutines, channels, error handling, interfaces |
| `.rs` | Rust | Ownership, borrowing, traits, async with tokio |

Add your own: create a `.md` file in `src/kitsune/prompts/skills/` and map the extension in `loader.py`.

## Multi-Gate Escalation

The router decides locally vs escalate using 4 deterministic gates:

| Gate | Trigger | Example |
|------|---------|---------|
| Security | XSS, SQL injection, CVE keywords | "check for vulnerabilities" |
| Architecture | design, microservice, redesign | "design a REST API" |
| Complex task | refactor, migrate, rewrite | "refactor to use DI" |
| Token budget | >1500 estimated tokens | Very large files |

When escalating, Kitsune tells you WHY and suggests a Claude Code prompt.

## Development

```bash
uv sync
uv run pytest tests/ -v        # 24 tests
uv run ruff check . && uv run ruff format --check .
```

## Roadmap

- [x] **v0.1** — `kit explain` + `kit ask` via MLX
- [x] **v0.2** — Skill-based prompts, multi-gate escalation, 24 tests
- [x] **v0.2.1** — Cross-platform support (MLX + Ollama + any OpenAI-compatible server)
- [ ] **v0.3** — RAG over codebase (ChromaDB + embeddings), DSP pattern
- [ ] **v0.4** — MCP server mode (`kit serve`), streaming output

## License

[MIT](LICENSE)
