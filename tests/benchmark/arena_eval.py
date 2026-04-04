"""Arena Quality Benchmark — evaluate Kitsune output quality.

Scores each response on 3 dimensions (1-5):
  - Precision: Does it correctly identify what the code does?
  - Brevity: Is it concise without losing key info?
  - Usefulness: Would a developer find this helpful?

Usage:
    uv run python tests/benchmark/arena_eval.py

Outputs a score table + overall grade. Use to compare models/versions.
"""

import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

FIXTURES = Path(__file__).parent.parent / "fixtures"
PROJECT_ROOT = Path(__file__).parent.parent.parent

BENCHMARK_CASES = [
    {
        "id": "py-explain",
        "command": ["explain", str(FIXTURES / "sample_python.py")],
        "expected_concepts": ["user", "dataclass", "async", "active"],
        "max_lines": 25,
    },
    {
        "id": "js-explain",
        "command": ["explain", str(FIXTURES / "sample_javascript.js")],
        "expected_concepts": ["event", "retry", "fetch", "callback"],
        "max_lines": 25,
    },
    {
        "id": "go-explain",
        "command": ["explain", str(FIXTURES / "sample_go.go")],
        "expected_concepts": ["goroutine", "context", "wait", "concurrent"],
        "max_lines": 25,
    },
    {
        "id": "py-ask-specific",
        "command": [
            "ask",
            "what does find_active_users return?",
            "-f",
            str(FIXTURES / "sample_python.py"),
        ],
        "expected_concepts": ["list", "active", "user"],
        "max_lines": 15,
    },
    {
        "id": "js-ask-pattern",
        "command": [
            "ask",
            "how does the retry logic work?",
            "-f",
            str(FIXTURES / "sample_javascript.js"),
        ],
        "expected_concepts": ["retry", "catch", "timeout", "error"],
        "max_lines": 15,
    },
    {
        "id": "escalation-security",
        "command": [
            "ask",
            "check for XSS vulnerabilities",
            "-f",
            str(FIXTURES / "sample_javascript.js"),
        ],
        "expected_concepts": ["security", "claude", "exceeds"],
        "max_lines": 10,
        "expect_fallback": True,
    },
]


@dataclass
class BenchmarkResult:
    case_id: str
    output: str
    latency_ms: int
    precision: int = 0  # 1-5
    brevity: int = 0  # 1-5
    usefulness: int = 0  # 1-5
    notes: str = ""
    concept_hits: int = 0
    concept_total: int = 0


def run_case(case: dict) -> BenchmarkResult:
    start = time.monotonic()
    result = subprocess.run(
        [sys.executable, "-m", "kitsune", *case["command"]],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=PROJECT_ROOT,
    )
    elapsed = int((time.monotonic() - start) * 1000)
    output = (result.stdout + result.stderr).lower()

    # Auto-score precision from concept hits
    concepts = case.get("expected_concepts", [])
    hits = sum(1 for c in concepts if c in output)

    # Auto-score brevity from line count
    content_lines = [ln for ln in output.strip().split("\n") if ln.strip() and "─" not in ln]
    max_lines = case.get("max_lines", 25)

    # Precision: concept coverage
    if concepts:
        precision = min(5, max(1, int(hits / len(concepts) * 5)))
    else:
        precision = 3

    # Brevity: line economy
    if len(content_lines) <= max_lines * 0.5:
        brevity = 5
    elif len(content_lines) <= max_lines:
        brevity = 4
    elif len(content_lines) <= max_lines * 1.5:
        brevity = 3
    else:
        brevity = 2

    # Usefulness: combination of precision + not fabricating
    fabrications = sum(
        1
        for fake in ["authenticate", "database", "sql", "flask"]
        if fake in output and not case.get("expect_fallback")
    )
    usefulness = max(1, precision - fabrications)

    # Fallback cases: check escalation worked
    if case.get("expect_fallback"):
        if "security" in output or "exceeds" in output or "claude" in output:
            precision = 5
            usefulness = 5
        else:
            precision = 1
            usefulness = 1

    return BenchmarkResult(
        case_id=case["id"],
        output=output[:300],
        latency_ms=elapsed,
        precision=precision,
        brevity=brevity,
        usefulness=usefulness,
        concept_hits=hits,
        concept_total=len(concepts),
    )


def main():
    print("=" * 70)
    print("KITSUNE ARENA BENCHMARK")
    print("=" * 70)
    print()

    results: list[BenchmarkResult] = []
    for case in BENCHMARK_CASES:
        print(f"  Running {case['id']}...", end=" ", flush=True)
        r = run_case(case)
        results.append(r)
        print(f"done ({r.latency_ms}ms)")

    print()
    print(f"{'Case':<22} {'Prec':>4} {'Brev':>4} {'Use':>4} {'Avg':>5} {'Concepts':>10} {'Latency':>8}")
    print("-" * 70)

    total_scores: list[float] = []
    for r in results:
        avg = (r.precision + r.brevity + r.usefulness) / 3
        total_scores.append(avg)
        concepts_str = f"{r.concept_hits}/{r.concept_total}"
        print(
            f"{r.case_id:<22} {r.precision:>4} {r.brevity:>4} {r.usefulness:>4} "
            f"{avg:>5.1f} {concepts_str:>10} {r.latency_ms:>7}ms"
        )

    overall = sum(total_scores) / len(total_scores) if total_scores else 0
    print("-" * 70)
    print(f"{'OVERALL':<22} {'':>4} {'':>4} {'':>4} {overall:>5.1f}")
    print()

    # Grade
    if overall >= 4.5:
        grade = "A"
    elif overall >= 3.5:
        grade = "B"
    elif overall >= 2.5:
        grade = "C"
    elif overall >= 1.5:
        grade = "D"
    else:
        grade = "F"

    print(f"Grade: {grade} ({overall:.1f}/5.0)")
    print()

    # Save results
    output_path = PROJECT_ROOT / "tests" / "benchmark" / "results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(
            {
                "timestamp": time.strftime("%Y-%m-%d %H:%M"),
                "overall": round(overall, 2),
                "grade": grade,
                "cases": [
                    {
                        "id": r.case_id,
                        "precision": r.precision,
                        "brevity": r.brevity,
                        "usefulness": r.usefulness,
                        "latency_ms": r.latency_ms,
                        "concepts": f"{r.concept_hits}/{r.concept_total}",
                    }
                    for r in results
                ],
            },
            indent=2,
        )
    )
    print(f"Results saved to {output_path}")


if __name__ == "__main__":
    main()
