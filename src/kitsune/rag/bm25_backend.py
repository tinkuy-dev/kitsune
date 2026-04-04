"""BM25 vectorless RAG — zero external dependencies.

Uses TF-IDF-like scoring (BM25 Okapi) with pure Python.
Best for: keyword-heavy code search, low RAM, fast indexing.
Weakness: no semantic understanding ("fetch" won't match "download").
"""

import math
import re
import time
from collections import Counter

from kitsune.rag.base import (
    Chunk,
    IndexStats,
    RAGBackend,
    chunk_file,
    walk_code_files,
)

# BM25 parameters
K1 = 1.5
B = 0.75


def _tokenize(text: str) -> list[str]:
    """Simple tokenizer: split on non-alphanumeric, lowercase, filter short."""
    tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", text.lower())
    return [t for t in tokens if len(t) > 1]


class BM25Backend(RAGBackend):
    def __init__(self):
        self._chunks: list[Chunk] = []
        self._doc_freqs: Counter = Counter()
        self._doc_tokens: list[list[str]] = []
        self._avg_dl: float = 0.0
        self._n_docs: int = 0

    @property
    def name(self) -> str:
        return "BM25 (vectorless)"

    def index(self, directory: str, extensions: set[str] | None = None) -> IndexStats:
        start = time.monotonic()
        self.clear()

        files = walk_code_files(directory, extensions)
        for f in files:
            chunks = chunk_file(f)
            self._chunks.extend(chunks)

        # Build BM25 index
        for chunk in self._chunks:
            tokens = _tokenize(chunk.content)
            self._doc_tokens.append(tokens)
            unique = set(tokens)
            for token in unique:
                self._doc_freqs[token] += 1

        self._n_docs = len(self._chunks)
        total_tokens = sum(len(t) for t in self._doc_tokens)
        self._avg_dl = total_tokens / self._n_docs if self._n_docs else 1.0

        elapsed = int((time.monotonic() - start) * 1000)
        return IndexStats(
            total_files=len(files),
            total_chunks=len(self._chunks),
            index_size_bytes=total_tokens * 8,  # rough estimate
            index_time_ms=elapsed,
            backend=self.name,
        )

    def search(self, query: str, top_k: int = 5) -> list[Chunk]:
        query_tokens = _tokenize(query)
        if not query_tokens or not self._chunks:
            return []

        scores: list[tuple[int, float]] = []
        for idx, doc_tokens in enumerate(self._doc_tokens):
            score = self._bm25_score(query_tokens, doc_tokens)
            if score > 0:
                scores.append((idx, score))

        scores.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, score in scores[:top_k]:
            chunk = Chunk(
                content=self._chunks[idx].content,
                file_path=self._chunks[idx].file_path,
                start_line=self._chunks[idx].start_line,
                end_line=self._chunks[idx].end_line,
                language=self._chunks[idx].language,
                score=round(score, 4),
            )
            results.append(chunk)
        return results

    def _bm25_score(self, query_tokens: list[str], doc_tokens: list[str]) -> float:
        doc_len = len(doc_tokens)
        doc_counter = Counter(doc_tokens)
        score = 0.0

        for qt in query_tokens:
            if qt not in self._doc_freqs:
                continue
            df = self._doc_freqs[qt]
            idf = math.log((self._n_docs - df + 0.5) / (df + 0.5) + 1)
            tf = doc_counter.get(qt, 0)
            numerator = tf * (K1 + 1)
            denominator = tf + K1 * (1 - B + B * doc_len / self._avg_dl)
            score += idf * numerator / denominator

        return score

    def clear(self) -> None:
        self._chunks.clear()
        self._doc_freqs.clear()
        self._doc_tokens.clear()
        self._avg_dl = 0.0
        self._n_docs = 0
