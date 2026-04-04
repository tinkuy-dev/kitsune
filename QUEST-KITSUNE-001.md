# QUEST-KITSUNE-001: Auditoria de Sistemas y Proyeccion Evolutiva

> Quest Nivel 4 — Arena Multi (cross-dimensional)
> Registrada: 2026-04-03 | Status: FASE 1 COMPLETA, FASES 2-3 PENDIENTES

## Skills Requeridos

| Skill | Rol en la Quest | Dimension |
|-------|----------------|-----------|
| **Claude Sensei** | Director de auditoria, evaluador de ecosistema | Global |
| **Protocol Architect** | Evaluador de integracion HERMES, spec compliance | HERMES |
| **MomoProdDev** | Coordinador cross-proyecto, viabilidad profesional | Laboral |
| **Sales-Engineering-Director** | Costeo, pricing, GTM, modelo de negocio | Laboral |
| **Ares** | Foco en milestones ejecutables, cortar scope creep | Global |

## Prerequisitos para la sesion

```bash
# 1. MLX server corriendo
mlx_lm.server --model mlx-community/Qwen2.5-Coder-1.5B-Instruct-4bit --port 8008

# 2. Verificar MCP server funciona (nuevo en esta sesion)
# Iniciar Claude Code fresh → buscar tools kitsune_*

# 3. HERMES bus limpio
cat ~/.claude/sync/bus.jsonl | wc -l  # debe ser ~64
```

---

## FASE 1: AUDITORIA EMPIRICA (COMPLETA — 2026-04-03)

### 1.1 Hitos tecnicos compilados y ejecutados

| # | Hito | Commits | Tests | Status |
|---|------|---------|-------|--------|
| 1 | Scaffold proyecto (uv + LangGraph + Typer) | 1 | 10 | DONE |
| 2 | MVP: kit explain + kit ask via MLX | 1 | 10 | DONE |
| 3 | Skill-based prompts (4→10 lenguajes) | 2 | 25 | DONE |
| 4 | Multi-gate escalation (4 gates) | 1 | 25 | DONE |
| 5 | Cross-platform (MLX + Ollama + any OpenAI-compat) | 1 | 25 | DONE |
| 6 | RAG framework (BM25 + ChromaDB) | 1 | 25 | DONE |
| 7 | QA: e2e smoke tests + Arena benchmark | 1 | 36 | DONE |
| 8 | MCP server (Mode 2) | 1 | 36 | DONE |
| 9 | HERMES node (Mode 3) | 1 | 36 | DONE |
| 10 | 6 skill files via Gemini collab | 1 | 25 | DONE |
| **Total** | **15 commits, 1 sesion** | **15** | **36** | **LIVE** |

### 1.2 Que funciona perfectamente

| Componente | Score | Evidencia |
|------------|-------|-----------|
| Keyword router | 5/5 | 0ms latency, 11 tests, cero false positives |
| Skill injection por lenguaje | 5/5 | Detecta Python/JS/Go/Rust/TS/Java/C#/Ruby/PHP/Swift |
| Multi-gate escalation | 5/5 | Security, architecture, complexity, token budget |
| BM25 RAG | 5/5 | 0.88 precision, 0ms search, 135ms index |
| Explain (Python, Go) | 4.5/5 | Concepts hit rate 100%, no fabrication |
| Explain (JavaScript) | 3.7/5 | Misses retry/backoff patterns |
| Ask (specific questions) | 5/5 | Perfect on targeted questions |
| Escalation to Claude | 5/5 | Instant detection, clear reason |
| Cross-platform config | 5/5 | Auto-detect OS, correct defaults |
| CLI UX (Typer + Rich) | 4/5 | Clean panels, markdown rendering |

### 1.3 Que falla o genera friccion

| Issue | Severidad | Causa raiz | Fix propuesto |
|-------|-----------|-----------|---------------|
| Ollama Metal shaders broken | BLOCKER (Mac Tahoe) | Darwin 25.x bfloat16 mismatch | RESUELTO: pivot a MLX |
| JS ask sobre retry logic | MEDIUM | 1.5B no captura control flow complejo | Enrich JS skill con patrones retry |
| MCP server sin testear live | MEDIUM | Requiere restart de Claude Code | Test en proxima sesion |
| HERMES node sin daemon | LOW | No hay launchd plist | Crear com.momoshod.kitsune-hermes.plist |
| ChromaDB 160x mas lento que BM25 | DATO | Embedding overhead vs keyword match | BM25 como default, Chroma como opcion |
| Pydantic V1 warning | COSMETIC | langchain-core legacy compat | Esperar fix upstream |
| `<\|im_end\|>` token leak | RESUELTO | MLX no filtra EOS tokens | Strip en backend.py |

### 1.4 Que deberia funcionar segun spec pero no en la realidad

| Spec | Realidad | Gap |
|------|----------|-----|
| Ollama como backend universal | Broken en Mac Tahoe | MLX cubre Mac, Ollama solo Linux/Win |
| ChromaDB semantic advantage | Misma precision que BM25 en code search | Semantic solo ayuda en NL queries |
| 7B model >> 1.5B | Solo +0.1 calidad, 4.4x mas lento | Skill enrichment > model size |
| HERMES MCP bridge bidireccional | MCP server registrado, no testeado live | Fase 2 |

### 1.5 Benchmarks de referencia

**Model Arena (Qwen 1.5B — Grade B, 4.1/5.0)**
```
py-explain    4.3 | js-explain    3.7 | go-explain    4.7
py-ask        5.0 | js-ask        2.7 | escalation    4.3
```

**RAG Comparison**
```
           BM25          ChromaDB
Index:     135ms         21,773ms
Search:    0ms           73ms
Precision: 0.88          0.88
```

---

## FASE 2: TOPOLOGIA ARQUITECTONICA (PENDIENTE — Arena Multi)

### 2.1 Corto Plazo (Tactico — 1-3 meses)

Ejecutar en sesion con: **Ares + Protocol Architect + Claude Sensei**

Temas a resolver:
- [ ] MCP server live test y estabilizacion
- [ ] HERMES node daemon (launchd plist auto-start)
- [ ] JS skill enrichment (score 2.7 → 4.0)
- [ ] RAG cross-dimensional (indexar 7 dims con BM25)
- [ ] LoRA fine-tuning piloto (estilo Daniel)
- [ ] PyPI publish de HERMES (`hermes-agent-protocol`)
- [ ] GitHub Actions CI para Kitsune (unit tests only, no server)
- [ ] Kitsune CLAUDE.md para el proyecto

### 2.2 Medio Plazo (Estrategico — 6 meses)

Ejecutar en sesion con: **MomoProdDev + Sales-Engineering-Director + Palas**

Temas a resolver:
- [ ] Delegacion autonoma: Claude envia batches de explain a Kitsune sin intervencion
- [ ] Multi-agent local: Kitsune coordina con heraldo-gateway via HERMES
- [ ] RAG con tree-sitter (structure-aware chunking vs line-based)
- [ ] Streaming output (token-by-token para latencia percibida)
- [ ] Kitsune como MCP server publicable (Plugin Marketplace de Anthropic)
- [ ] FlowForgers integration (Kitsune como modulo de oferta con Patricio)

### 2.3 Largo Plazo (Visionario — 1+ anos)

Ejecutar en sesion con: **Consejo Ampliado (5 voces) + Protocol Architect**

Temas a deliberar:
- [ ] Kitsune como nodo soberano de compute en red HERMES federada
- [ ] Resolucion semantica de intenciones (query → best agent routing)
- [ ] Fine-tuning continuo: modelo aprende del uso de Daniel
- [ ] Marketplace de skills locales (cada usuario trae sus skills)
- [ ] HERMES S2S: Kitsune de Daniel habla con Kitsune de Patricio

---

## FASE 3: PRODUCT ROADMAP (PENDIENTE — Arena Multi)

### 3.1 Milestone 1: "Kitsune Works" (Mes 1)

Ejecutar con: **Ares (foco) + Claude Sensei (benchmark)**

| Entregable | Metrica de exito | Demo |
|------------|-----------------|------|
| MCP server estable | 0 errores en 50 llamadas consecutivas | Claude Code delega 3 explains a Kitsune |
| JS skill enrichment | Score js-ask >= 3.5 (de 2.7) | `kit ask "how does retry work?"` da respuesta correcta |
| GitHub Actions CI | Green on every push | Badge en README |
| HERMES node daemon | Auto-start en boot, 0 crashes en 24h | `hermes bus --pending` muestra 0 pendientes de kitsune |

### 3.2 Milestone 2: "Kitsune Learns" (Mes 2-3)

Ejecutar con: **MomoProdDev + Sales-Engineering-Director**

| Entregable | Metrica de exito | Demo |
|------------|-----------------|------|
| RAG cross-dimensional | Indexa 7 dims, search < 5ms, precision >= 0.85 | `kit search "authentication"` encuentra codigo correcto |
| LoRA fine-tuning v1 | Respuestas en estilo Daniel (conciso, directo) | Comparar output pre/post fine-tune |
| PyPI `hermes-agent-protocol` | `pip install` funciona en Mac/Linux/Win | Fresh virtualenv install demo |
| Arena benchmark v2 | 15+ cases, 5 lenguajes, Grade A (>= 4.5) | Benchmark report automatizado |

### 3.3 Milestone 3: "Kitsune Ships" (Mes 4-6)

Ejecutar con: **Consejo + FlowForgers alignment**

| Entregable | Metrica de exito | Demo |
|------------|-----------------|------|
| Plugin Anthropic Marketplace | Listed, 10+ installs primera semana | `claude plugin install kitsune` |
| Skill Factory pitch deck | 5 skills empaquetados con pricing | Presentacion a Patricio/clientes |
| Streaming output | Time to first token < 200ms | Side-by-side: batch vs stream |
| Multi-agent delegation | 0 intervenciones humanas en task de 5 pasos | Claude planifica → Kitsune ejecuta 5 explains → Claude resume |

---

## Instrucciones de ejecucion para proxima sesion

1. **Arrancar desde ~/Dev/kitsune/** con MLX server activo
2. **Invocar**: `/arena multi` con skills: Ares + Claude Sensei + Protocol Architect
3. **Fase 1**: Leer este documento (ya completa)
4. **Fase 2**: Deliberar y priorizar los items por horizonte
5. **Fase 3**: Costear con Sales-Engineering-Director, definir pricing targets
6. **Entregable**: Actualizar este archivo con decisiones + crear GitHub Issues

## Insight fundamental de la sesion inaugural

> **La calidad de un asistente local escala con PROMPT ENGINEERING (skill files), no con model size.** 1.5B con buenos skills iguala a 7B con prompts genericos. Este insight es la base empirica de la Skill Factory: los skills son el producto, el modelo es commodity.
