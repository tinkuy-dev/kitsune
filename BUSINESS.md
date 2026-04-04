# Kitsune — Business Case & Skill Factory Angle

> Prepared by MomoProdDev + Sales-Engineering-Director | 2026-04-03

## Value Proposition (One-liner)

**Kitsune gives every developer a free, private code assistant that runs on their machine — and tells them when they need something bigger.**

## What We're Actually Selling

Kitsune (the tool) is open-source and free. The business is in what it proves:

### Product 1: Skill Files as a Service
- Each language skill file (Python, Go, Rust, etc.) makes a 1.5B model perform like a 7B
- **Insight**: prompt engineering > model size (empirically validated: +0.1 quality delta at 4.4x cost)
- **Offering**: custom skill files for enterprise codebases (internal frameworks, proprietary APIs, domain-specific patterns)
- **Pricing**: $500-2,000 per custom skill file (includes benchmarking + DoD validation)
- **Delivery**: 1-2 days per skill file, includes Arena benchmark report

### Product 2: RAG Architecture Consulting
- We validated BM25 vs ChromaDB empirically: same precision, 160x speed difference
- Most companies default to vector DB (expensive, slow) when keyword search is enough
- **Offering**: "RAG Architecture Audit" — evaluate your search pipeline, recommend right approach
- **Pricing**: $2,000-5,000 per audit (1-2 week engagement)
- **Deliverable**: benchmark report + implementation recommendation + working prototype

### Product 3: Local AI Agent Integration
- Kitsune's 3-mode architecture (CLI + MCP + HERMES) is a replicable pattern
- **Offering**: set up local SLM agents for teams that can't send code to cloud APIs (finance, defense, healthcare)
- **Pricing**: $5,000-15,000 per team setup
- **Includes**: model selection, skill file creation, MCP integration, benchmark baseline

### Product 4: HERMES Protocol Implementation
- Agent-to-agent coordination for enterprises with multiple AI tools
- **Offering**: deploy HERMES bus + adapters for their agent stack
- **Pricing**: $10,000-30,000 (depends on agent count and security requirements)
- **Includes**: adapter development, E2E encryption, bus monitoring, SLA

## Competitive Landscape

| Competitor | What they do | Our edge |
|-----------|-------------|----------|
| Ollama WebUI | Generic local LLM chat | We're code-specialized with skill injection |
| Continue.dev | IDE code assistant | They need cloud APIs; we're 100% local |
| Aider | CLI code assistant | They use GPT-4/Claude API; we use free local SLM |
| Cursor | AI IDE | $20/mo subscription; we're free + extensible |
| TabbyML | Self-hosted code assistant | Enterprise-focused; we're developer-first |

**Our unique position**: the only local code assistant that:
1. Knows when to escalate to a bigger model (multi-gate router)
2. Has empirically validated skill files that boost quality without bigger models
3. Integrates with Claude Code as an MCP tool (save API quota)
4. Speaks HERMES for multi-agent coordination

## Target Customers

| Segment | Pain | Our solution | Price point |
|---------|------|-------------|-------------|
| **Solo developers** | API costs, privacy | Free Kitsune + skill files | $0 (open source adoption) |
| **Startups (5-20 devs)** | Each dev has $20/mo Cursor subscription | Self-hosted Kitsune + custom skills | $2K setup + $500/skill |
| **Enterprise (regulated)** | Can't send code to cloud | Full local stack + HERMES | $15K-30K |
| **AI consultancies** | Need to demo multi-agent | HERMES + Kitsune as reference arch | Partnership |

## Go-to-Market (via Nymyka Skill Factory)

### Phase 1: Credibility (Month 1-2)
- Kitsune on GitHub with 100+ stars (target via HN/Reddit launch)
- HERMES on PyPI (`hermes-agent-protocol`)
- Arena benchmark reports as content marketing
- Blog post: "Why a 1.5B model with good prompts beats a 7B model"

### Phase 2: First Revenue (Month 3-4)
- 3 custom skill files for early adopters ($1,500 each = $4,500)
- 1 RAG audit for a startup ($3,000)
- CCA-F certification (Anthropic Partner Network credibility)

### Phase 3: Scale (Month 5-6)
- Anthropic Plugin Marketplace listing
- FlowForgers partnership (Patricio's telco network)
- Enterprise pilot (1 regulated client)

## Unit Economics

| Item | Cost | Revenue | Margin |
|------|------|---------|--------|
| Custom skill file | 4h Daniel time (~$200 at $50/h) | $1,000 | 80% |
| RAG audit | 16h Daniel time (~$800) | $3,000 | 73% |
| Local agent setup | 40h (~$2,000) | $10,000 | 80% |
| HERMES deployment | 80h (~$4,000) | $20,000 | 80% |

**Key**: Daniel's time is the bottleneck. Gemini handles volume generation, Claude handles quality review. Daniel does architecture + client interface.

## Risk Factors

| Risk | Mitigation |
|------|-----------|
| Claude Code adds local model support natively | We're MCP-integrated — we COMPLEMENT, not compete |
| Ollama fixes Metal shaders | Makes us stronger — Ollama is just another backend for Kitsune |
| Someone forks Kitsune | MIT license; our edge is skills + consulting, not the tool |
| Low GitHub traction | Content marketing via benchmarks, not vanity stars |

## Immediate Next Steps

1. [ ] HN launch post (after MCP server tested live)
2. [ ] Blog: "1.5B vs 7B: Why skill files matter more than model size"
3. [ ] CCA-F certification (Anthropic credibility)
4. [ ] FlowForgers alignment call with Patricio
5. [ ] First 3 custom skill files (internal: Nymyka FastAPI, HERMES protocol, Technetix GPON)
