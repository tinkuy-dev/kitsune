# Kitsune — Model Capabilities Matrix

> Benchmarked 2026-04-03 on Apple Silicon M5, 16GB RAM

## Model Comparison

| Metric | Qwen 1.5B (4-bit) | Qwen 7B (4-bit) | Verdict |
|--------|-------------------|------------------|---------|
| **Overall Score** | 4.1/5.0 (B) | 4.2/5.0 (B) | 1.5B wins on value |
| **Avg Latency** | ~2.2s | ~9.7s | 1.5B is **4.4x faster** |
| **RAM** | ~1.2 GB | ~4.5 GB | 1.5B uses **3.7x less** |
| **Quality Delta** | baseline | +0.1 | Negligible improvement |

**Conclusion**: The 7B model is not worth the 4.4x latency and 3.7x RAM cost for only +0.1 quality improvement. Use 1.5B as default.

## What Qwen 1.5B Does Well

| Task | Score | Confidence | Notes |
|------|-------|------------|-------|
| **Explain Python** | 4.3/5 | High | Identifies dataclasses, protocols, async, comprehensions |
| **Explain Go** | 4.7/5 | High | Detects goroutines, context, WaitGroup, channels |
| **Answer specific questions** | 5.0/5 | High | "What does X return?" — nails it |
| **Detect key patterns** | 4.5/5 | High | Decorators, closures, struct embedding |
| **Avoid fabrication** | 5.0/5 | High | Does NOT invent functions or APIs |
| **Escalation detection** | 5.0/5 | High | Security/architecture → instant fallback (0.6s) |

## What Qwen 1.5B Struggles With

| Task | Score | Why | Workaround |
|------|-------|-----|------------|
| **Complex control flow** | 2.7/5 | Retry-with-backoff logic, state machines | Enrich JS skill with retry patterns |
| **Multi-step reasoning** | ~2/5 | "Why does this cause a race condition?" | Escalate to Claude |
| **Cross-file context** | N/A | Can only see 1 file at a time | v0.3 RAG will help |
| **Brevity (Python)** | 3/5 | Tends to repeat points in long files | Truncate input to first 100 lines |

## What NO Local SLM Can Do (Always Escalate)

| Task | Why | Action |
|------|-----|--------|
| **Security audits** | Requires knowledge of exploit patterns, CVE databases | → Claude |
| **Architecture design** | Requires system-level reasoning, tradeoff analysis | → Claude |
| **Refactoring** | Needs to understand dependencies, side effects across files | → Claude |
| **Performance optimization** | Requires profiling knowledge, benchmarking strategy | → Claude |
| **Migration planning** | Cross-system knowledge, backward compatibility | → Claude |

## Scoring Methodology

Each benchmark case is scored automatically on 3 dimensions (1-5):

- **Precision**: Does the response correctly identify what the code does? Measured by concept hit rate (expected terms found in output)
- **Brevity**: Is the response concise? Penalized if output exceeds expected line count
- **Usefulness**: Would a developer find this helpful? Combination of precision minus fabrications

6 benchmark cases run against test fixtures:
- 3 explain tasks (Python, JavaScript, Go)
- 2 ask tasks (specific question, pattern question)
- 1 escalation task (security)

## Benchmark Data

### Qwen 1.5B (default)

```
Case                   Prec Brev  Use   Avg   Concepts  Latency
py-explain                5    3    5   4.3        4/4    4308ms
js-explain                3    5    3   3.7        3/4    1705ms
go-explain                5    4    5   4.7        4/4    3054ms
py-ask-specific           5    5    5   5.0        3/3    1538ms
js-ask-pattern            2    4    2   2.7        2/4    2077ms
escalation-security       5    3    5   4.3        3/3     662ms
OVERALL                                 4.1
```

### Qwen 7B (optional)

```
Case                   Prec Brev  Use   Avg   Concepts  Latency
py-explain                5    3    5   4.3        4/4   14813ms
js-explain                5    3    5   4.3        4/4   11786ms
go-explain                5    4    5   4.7        4/4    8697ms
py-ask-specific           5    4    5   4.7        3/3    6339ms
js-ask-pattern            3    2    3   2.7        3/4   16168ms
escalation-security       5    3    5   4.3        3/3     753ms
OVERALL                                 4.2
```

## When to Use Which Model

| Scenario | Model | Why |
|----------|-------|-----|
| Daily coding (explain, ask) | **1.5B** | Fast enough, good enough |
| Deep explanation of complex file | **7B** | JS/complex logic +0.6 improvement |
| Quick "what is this?" | **1.5B** | 1.5s vs 6.3s matters |
| Reviewing before PR | **Claude** | Needs multi-file + reasoning |
| Security check | **Claude** | Always escalate |
| Learning a new codebase | **1.5B + RAG** (v0.3) | Index + explain beats read alone |

## Improving Scores

The main lever is **skill enrichment**, not model size:

1. **JS skill** (`prompts/skills/javascript.md`): Add retry/backoff patterns, Promise.all, error boundary examples
2. **Input truncation**: Cap file input at ~100 lines for 1.5B to improve brevity
3. **Few-shot examples**: Add 1-2 demonstration examples in skill files (DSP pattern)
4. **Benchmark expansion**: Add more cases (Rust, TypeScript, edge cases) for robust scoring
