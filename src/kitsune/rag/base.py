"""Base interface for RAG backends. All implementations share this contract."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

# Extensions to index
CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".go",
    ".rs",
    ".java",
    ".md",
    ".yaml",
    ".yml",
    ".toml",
    ".json",
    ".sh",
}

# Directories to skip
SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "dist",
    "build",
    ".egg-info",
}


@dataclass
class Chunk:
    content: str
    file_path: str
    start_line: int = 0
    end_line: int = 0
    language: str = ""
    score: float = 0.0


@dataclass
class IndexStats:
    total_files: int = 0
    total_chunks: int = 0
    index_size_bytes: int = 0
    index_time_ms: int = 0
    backend: str = ""
    extra: dict = field(default_factory=dict)


class RAGBackend(ABC):
    """Common interface for all RAG implementations."""

    @abstractmethod
    def index(self, directory: str, extensions: set[str] | None = None) -> IndexStats:
        """Index a directory. Returns stats about the index."""

    @abstractmethod
    def search(self, query: str, top_k: int = 5) -> list[Chunk]:
        """Search the index. Returns ranked chunks."""

    @abstractmethod
    def clear(self) -> None:
        """Clear the index."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Backend name for display."""


def walk_code_files(directory: str, extensions: set[str] | None = None) -> list[Path]:
    """Walk directory and return code files, respecting skip dirs."""
    exts = extensions or CODE_EXTENSIONS
    root = Path(directory).resolve()
    files = []
    for path in root.rglob("*"):
        if any(skip in path.parts for skip in SKIP_DIRS):
            continue
        if path.is_file() and path.suffix in exts:
            files.append(path)
    return sorted(files)


def chunk_file(path: Path, max_lines: int = 50) -> list[Chunk]:
    """Split a file into chunks of max_lines. Simple line-based chunking."""
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return []

    lines = content.split("\n")
    lang = path.suffix.lstrip(".")
    chunks = []

    for i in range(0, len(lines), max_lines):
        chunk_lines = lines[i : i + max_lines]
        chunk_text = "\n".join(chunk_lines)
        if chunk_text.strip():
            chunks.append(
                Chunk(
                    content=chunk_text,
                    file_path=str(path),
                    start_line=i + 1,
                    end_line=min(i + max_lines, len(lines)),
                    language=lang,
                )
            )
    return chunks
