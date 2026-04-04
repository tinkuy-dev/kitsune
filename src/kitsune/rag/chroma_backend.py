"""ChromaDB vector RAG — semantic search with embeddings.

Requires: `uv sync --group rag` (langchain-chroma + langchain-huggingface)
Best for: semantic search ("fetch" matches "download"), concept-level queries.
Weakness: slower indexing, more RAM (~300MB for embeddings model), heavier deps.
"""

import time

from kitsune.rag.base import (
    Chunk,
    IndexStats,
    RAGBackend,
    chunk_file,
    walk_code_files,
)


class ChromaBackend(RAGBackend):
    def __init__(self, persist_dir: str | None = None):
        self._persist_dir = persist_dir
        self._collection = None
        self._chunks: list[Chunk] = []
        self._client = None

    @property
    def name(self) -> str:
        return "ChromaDB (vector)"

    def _ensure_client(self):
        if self._client is None:
            try:
                import chromadb
            except ImportError:
                raise RuntimeError("ChromaDB not installed. Run: uv sync --group rag")
            if self._persist_dir:
                self._client = chromadb.PersistentClient(path=self._persist_dir)
            else:
                self._client = chromadb.Client()
            self._collection = self._client.get_or_create_collection(
                name="kitsune_code",
                metadata={"hnsw:space": "cosine"},
            )

    def index(self, directory: str, extensions: set[str] | None = None) -> IndexStats:
        start = time.monotonic()
        self._ensure_client()
        self.clear()

        files = walk_code_files(directory, extensions)
        all_chunks: list[Chunk] = []
        for f in files:
            all_chunks.extend(chunk_file(f))

        if not all_chunks:
            return IndexStats(backend=self.name)

        self._chunks = all_chunks

        # Batch add to ChromaDB (it handles embedding internally)
        batch_size = 100
        for i in range(0, len(all_chunks), batch_size):
            batch = all_chunks[i : i + batch_size]
            self._collection.add(
                ids=[f"chunk_{i + j}" for j in range(len(batch))],
                documents=[c.content for c in batch],
                metadatas=[
                    {
                        "file_path": c.file_path,
                        "start_line": c.start_line,
                        "end_line": c.end_line,
                        "language": c.language,
                    }
                    for c in batch
                ],
            )

        elapsed = int((time.monotonic() - start) * 1000)
        return IndexStats(
            total_files=len(files),
            total_chunks=len(all_chunks),
            index_size_bytes=0,  # ChromaDB manages storage
            index_time_ms=elapsed,
            backend=self.name,
        )

    def search(self, query: str, top_k: int = 5) -> list[Chunk]:
        self._ensure_client()
        if not self._collection or self._collection.count() == 0:
            return []

        results = self._collection.query(
            query_texts=[query],
            n_results=min(top_k, self._collection.count()),
        )

        chunks = []
        for i, doc in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][i]
            distance = results["distances"][0][i] if results.get("distances") else 0
            chunks.append(
                Chunk(
                    content=doc,
                    file_path=meta.get("file_path", ""),
                    start_line=meta.get("start_line", 0),
                    end_line=meta.get("end_line", 0),
                    language=meta.get("language", ""),
                    score=round(1 - distance, 4),  # cosine similarity
                )
            )
        return chunks

    def clear(self) -> None:
        if self._client and self._collection:
            self._client.delete_collection("kitsune_code")
            self._collection = self._client.get_or_create_collection(
                name="kitsune_code",
                metadata={"hnsw:space": "cosine"},
            )
        self._chunks.clear()
