"""RAG Backend Comparison — BM25 vs ChromaDB.

Indexes the same directory, runs the same queries, compares:
- Indexing speed
- Search latency
- Result relevance (expected file hits)
- RAM usage (rough estimate)
- Dependencies count

Usage:
    uv run python tests/benchmark/rag_compare.py [directory]
"""

import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

# Queries with expected file patterns in results
QUERIES = [
    {
        "query": "router task classification",
        "expect_files": ["router.py"],
        "description": "Find the routing logic",
    },
    {
        "query": "system prompt skill loading",
        "expect_files": ["loader.py", "templates.py"],
        "description": "Find prompt construction",
    },
    {
        "query": "LangGraph state graph build",
        "expect_files": ["build.py", "state.py"],
        "description": "Find graph architecture",
    },
    {
        "query": "CLI explain command",
        "expect_files": ["cli.py"],
        "description": "Find CLI entry points",
    },
    {
        "query": "inference backend OpenAI",
        "expect_files": ["backend.py"],
        "description": "Find inference layer",
    },
    {
        "query": "async fetch user data",
        "expect_files": ["sample_python.py"],
        "description": "Find async patterns (semantic test)",
    },
]


def run_backend(backend, directory: str) -> dict:
    """Run full benchmark on one backend."""
    # Index
    stats = backend.index(directory)

    # Search each query
    search_results = []
    total_latency = 0
    total_hits = 0
    total_expected = 0

    for q in QUERIES:
        start = time.monotonic()
        results = backend.search(q["query"], top_k=5)
        latency = int((time.monotonic() - start) * 1000)
        total_latency += latency

        # Check if expected files are in results
        result_files = [Path(r.file_path).name for r in results]
        hits = sum(1 for ef in q["expect_files"] if any(ef in rf for rf in result_files))
        total_hits += hits
        total_expected += len(q["expect_files"])

        search_results.append(
            {
                "query": q["query"],
                "description": q["description"],
                "latency_ms": latency,
                "hits": hits,
                "expected": len(q["expect_files"]),
                "top_result": result_files[0] if result_files else "none",
                "top_score": results[0].score if results else 0,
            }
        )

    precision = total_hits / total_expected if total_expected else 0

    return {
        "backend": backend.name,
        "index_time_ms": stats.index_time_ms,
        "total_files": stats.total_files,
        "total_chunks": stats.total_chunks,
        "avg_search_ms": total_latency // len(QUERIES),
        "precision": round(precision, 2),
        "hits": f"{total_hits}/{total_expected}",
        "queries": search_results,
    }


def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else str(PROJECT_ROOT)

    print("=" * 70)
    print("RAG BACKEND COMPARISON")
    print(f"Directory: {directory}")
    print("=" * 70)

    from kitsune.rag.bm25_backend import BM25Backend

    backends = [("BM25", BM25Backend())]

    # Try ChromaDB if available
    try:
        import chromadb  # noqa: F401

        from kitsune.rag.chroma_backend import ChromaBackend

        backends.append(("ChromaDB", ChromaBackend()))
    except (ImportError, Exception) as e:
        print(f"\n[SKIP] ChromaDB not available: {e}")

    all_results = []
    for label, backend in backends:
        print(f"\n--- {label} ---")
        result = run_backend(backend, directory)
        all_results.append(result)

        print(
            f"  Index: {result['total_files']} files, {result['total_chunks']} chunks in {result['index_time_ms']}ms"
        )
        print(f"  Precision: {result['precision']} ({result['hits']})")
        print(f"  Avg search: {result['avg_search_ms']}ms")
        print()
        for q in result["queries"]:
            hit_marker = "OK" if q["hits"] == q["expected"] else "MISS"
            print(
                f"    [{hit_marker}] {q['description']:<35} {q['latency_ms']:>4}ms  → {q['top_result']}"
            )

    # Comparison table
    print("\n" + "=" * 70)
    print(f"{'Metric':<25}", end="")
    for r in all_results:
        print(f"{r['backend']:>22}", end="")
    print()
    print("-" * 70)

    metrics = [
        ("Index time", "index_time_ms", "ms"),
        ("Avg search latency", "avg_search_ms", "ms"),
        ("Precision", "precision", ""),
        ("Files indexed", "total_files", ""),
        ("Chunks created", "total_chunks", ""),
    ]

    for label, key, unit in metrics:
        print(f"{label:<25}", end="")
        for r in all_results:
            val = r[key]
            print(f"{val:>19}{unit:>3}", end="")
        print()

    # Winner
    print("-" * 70)
    if len(all_results) > 1:
        bm25 = all_results[0]
        chroma = all_results[1]
        speed_winner = "BM25" if bm25["avg_search_ms"] <= chroma["avg_search_ms"] else "ChromaDB"
        prec_winner = "BM25" if bm25["precision"] >= chroma["precision"] else "ChromaDB"
        print(f"Speed winner: {speed_winner}")
        print(f"Precision winner: {prec_winner}")
        print(
            f"\nRecommendation: {'BM25' if speed_winner == prec_winner == 'BM25' else 'Depends on use case'}"
        )

    # Save
    output_path = PROJECT_ROOT / "tests" / "benchmark" / "rag_results.json"
    output_path.write_text(json.dumps(all_results, indent=2))
    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
