# Kitsune

Local code assistant powered by Small Language Models (SLMs) and [LangGraph](https://langchain-ai.github.io/langgraph/).

Kitsune runs entirely on your machine using [MLX](https://github.com/ml-explore/mlx) on Apple Silicon. No API keys needed, no cloud calls, no telemetry. Your code stays local.

## Why

Cloud LLMs are powerful but expensive and slow for quick tasks. Kitsune handles the fast, simple stuff locally — explain code, answer questions, detect when a task needs a bigger model and tells you.

## Quick Start

### Prerequisites

- macOS with Apple Silicon (M1/M2/M3/M4)
- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- [mlx-lm](https://github.com/ml-explore/mlx-examples/tree/main/llms) (`uv tool install mlx-lm`)

### Install

```bash
git clone https://github.com/dereyesm/kitsune.git
cd kitsune
uv sync
```

### Download a model (~1GB)

```bash
mlx_lm.server --model mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit --port 8008
```

The first run downloads the model to `~/.cache/huggingface/`. Subsequent runs load from cache.

### Use

```bash
# Explain a file
uv run kit explain path/to/file.py

# Ask a question with code context
uv run kit ask "what does this function do?" -f path/to/file.py

# Pipe from clipboard
pbpaste | uv run kit explain

# Check status
uv run kit status
```

## How It Works

```
User Input --> [Router] --> explain --> [Qwen 1.5B] --> Rich output
                       --> ask     --> [Qwen 1.5B] --> Rich output
                       --> fallback --> "Use Claude for this"
```

- **Router**: keyword-based classifier (zero latency, no LLM call)
- **Inference**: MLX server with OpenAI-compatible API
- **Orchestration**: LangGraph state graph
- **Output**: Rich panels with Markdown rendering

## Architecture

Kitsune connects to `mlx_lm.server` via its OpenAI-compatible API (`/v1/chat/completions`). This means you can swap the model by just changing the `--model` flag:

```bash
# Ultra-light (~1GB)
mlx_lm.server --model mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit --port 8008

# More capable (~4GB)
mlx_lm.server --model mlx-community/Qwen2.5-Coder-7B-Instruct-4bit --port 8008

# Override model in Kitsune
KITSUNE_MODEL_NAME="mlx-community/Qwen2.5-Coder-7B-Instruct-4bit" uv run kit explain file.py
```

### RAM Usage

| Component | RAM |
|-----------|-----|
| MLX server + Qwen 1.5B (4-bit) | ~1.2 GB |
| Python + LangGraph | ~0.2 GB |
| **Total** | **~1.4 GB** |

## Configuration

All settings via environment variables (prefix `KITSUNE_`):

| Variable | Default | Description |
|----------|---------|-------------|
| `KITSUNE_MLX_BASE_URL` | `http://localhost:8008/v1` | MLX server URL |
| `KITSUNE_MODEL_NAME` | `mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit` | Model to use |
| `KITSUNE_TEMPERATURE` | `0.1` | Generation temperature |
| `KITSUNE_FALLBACK_THRESHOLD` | `2000` | Char count to trigger fallback |

## Why MLX instead of Ollama?

Ollama 0.19.0 has broken Metal shaders on macOS Tahoe (Darwin 25.x). MLX runs natively on Apple Silicon without this issue and generally provides better throughput for quantized models on M-series chips.

## Development

```bash
uv sync
uv run pytest tests/ -v
uv run ruff check . && uv run ruff format --check .
```

## Roadmap

- [x] **v0.1** — `kit explain` + `kit ask` via MLX
- [ ] **v0.2** — FIM code completion, refactor command, RAG over codebase (ChromaDB + nomic-embed)
- [ ] **v0.3** — MCP server mode (`kit serve`), multi-backend support, HERMES integration

## License

[MIT](LICENSE)
