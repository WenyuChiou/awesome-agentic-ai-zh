# Project Memory — awesome-agentic-ai-zh

> Standing instructions for any AI agent (Claude, Codex, Gemini) working on this repo. Read this **first** before touching exercises or model recommendations.

## 📍 Repo positioning — read before adding anything

**This repo's role**: **learning roadmap + curated resources + simple illustrative cases.**

**Benchmark for "what we are NOT"**: [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) is the canonical chapter-length zh-TW depth tutorial (16 production capabilities, chapter format). **We don't compete with it; we route to it.**

**Implications when contributing**:

| Decision | Rule |
|---|---|
| New stage-level exercise folder | OK if it adds **a roadmap node + dual-path SDK demo + 1-line punchline**. 70-150 lines starter is the right size. |
| Expanding a starter beyond ~150 lines | **Push back**. If it's growing into chapter-length, add a 📚 callout pointing to hello-agents instead. |
| Adding a 5th `extension` to README | Diminishing return. Keep README tight (under ~200 lines); extra depth goes to the 📚 callout. |
| New resource (lib / paper / tool / framework) | Add it only when it has a clear teaching role, current documentation, a verified license or official source, and enough real adoption for the relevant section. A new third-party GitHub repository must have at least 1,000 stars at review time; official provider docs, standards, model cards, and irreplaceable canonical sources are exempt. Curation is the primary value. |
| New chapter-length tutorial inside this repo | **Push back**. If the topic deserves chapter-length, the right move is: write a 1-page summary + simple illustrative case + 📚 callout to a canonical source (hello-agents / Anthropic Cookbook / framework's own docs). |
| Trilingual mirror priority | Freeze zh-TW first, then ship matching en + zh-Hans mirrors in the same public-content PR. A partial mirror blocks shipping. |

**One-line summary**: **route → depth, not reinvent**. Every exercise folder includes a visible route back to its Stage resources or to suitable deeper material.

**Existing examples of this pattern** (verified 2026-09-13):

- Stage 3 / 4 / 6 / 7 example READMEs include visible learning resources and a Stage return route
- Main README and both locale mirrors state the roadmap position near the purpose section
- `tracks/cli/` is outline-only on purpose (CLI exercises are bash/markdown/config, not Python SDK; doesn't fit the dual-path frame — that's correct)

## Canonical Ollama models (verified against the user's `ollama list` and the official Ollama library)

| Model tag | When to use | Notes |
|---|---|---|
| **`gemma4:e4b`** | Stage 1 + 2 (plain chat, prompt engineering) | Effective 4B params; the official Ollama tag page showed a 9.6 GB download on 2026-08-30. **The `:e4b` tag matters** — NOT `gemma3n:e4b`, NOT `gemma3:4b`, NOT `gemma4:latest`. |
| **`gemma4:e2b`** | Smaller Stage 1+2 alternative | The official Ollama tag page showed a 7.2 GB download on 2026-08-30; actual memory needs vary by runtime and hardware, so do not promise it runs on every 4 GB machine. |
| **`qwen2.5:3b`** | Stages 3–6 (tool use / agent / ReAct) | 1.9 GB, **reliable tool-use support** (OpenAI function-calling format), default for the current function-calling exercises |
| **`qwen3.5:4b`** | Stage 7 (debate / eval / observability / streaming / deploy mechanics) | 3.4 GB official Ollama tag. These exercises do not depend on function calling; this row does not replace the Stage 3–6 tool-use default. |
| **`llama3.2:3b`** | `qwen2.5:3b` alternative for tool use | 2.0 GB, similar capability |
| **`mistral-nemo:12b`** | Higher-quality local fallback | 7.1 GB, closer-to-cloud quality |

**Wrong tags I've used in error before** (now fixed across 13 files via `.ai/.../rename_gemma.py`):

- ❌ `gemma3:4b` — older naming, replaced 2026-05-12
- ❌ `gemma3n:e4b` — wrong family, replaced 2026-05-12
- ✅ `gemma4:e4b` — correct (per user's Ollama installation screenshot)

If unsure, ask the user to run `ollama list` and verify.

## Canonical Anthropic models

| Model | Use case | Pricing (per 1M tokens) |
|---|---|---|
| **`claude-fable-5-1`** | Highest widely released Claude tier; 1M context, 128K max output, and stronger long-running agentic work | $10 input / $50 output; $0.25 cache read |
| **`claude-mythos-5-1`** | Same model as Fable 5.1, with access limited to vetted cybersecurity and life-science users | $10 input / $50 output; $0.25 cache read |
| **`claude-haiku-4-5`** | Cheapest cloud option, OK for all exercises | $1 input / $5 output |
| **`claude-sonnet-5`** | Production default, agent development | $2 input / $10 output |
| **`claude-opus-5-5`** | Current Opus-class default for most workloads; use Fable 5.1 when evals still fall short | $4 input / $20 output; $0.20 cache read |

## Framing rules (do not violate)

1. **Claude is the canonical / production reference** in documentation positioning.
2. **Ollama is the practice default** because of cost — students should not be blocked by API fees during learning.
3. **Every exercise must ship BOTH paths**:
   - Path A (Ollama, primary practice runnable): keep the exercise title, result,
     and first action visible. Use `<details markdown="1" open>` only when Path A
     is the single immediate action and its rendered body is short; otherwise use
     a closed `<details markdown="1">` block for code and troubleshooting.
   - Path B (Anthropic, `<details markdown="1">`, optional cloud-quality comparison)
4. **Every exercise must mention budget explicitly** — single-run cost + total stage cost.
5. **Local LLMs must appear in any model recommendation list** — never list cloud-only options.

## Exercise file conventions

- `starter.py` = Ollama / OpenAI-compatible default (Path A)
- `starter_anthropic.py` = Anthropic SDK version (Path B)
- `test.py` = mock-based tests for the Ollama starter (OpenAI-compat response shape)
- `test_anthropic.py` = mock-based tests for the Anthropic starter (content-block shape)
- `requirements.txt` = both `openai` and `anthropic` pinned
- `README.md` = trilingual switcher + 怎麼跑（兩條 path）+ budget per path + walkthrough + common pitfalls
- Each starter ends with `# === 自我驗證 ===` block containing 2+ `assert` statements
- Each Python file headers Windows-cp950 UTF-8 reconfigure:
  ```python
  import sys
  if hasattr(sys.stdout, "reconfigure"):
      sys.stdout.reconfigure(encoding="utf-8", errors="replace")
  ```

## Translation rules

- **zh-TW canonical** (`.md` without language suffix). zh-Hans + en mirror.
- Freeze the Traditional Chinese meaning before translation. A bounded translation agent may produce en + zh-Hans only after its file scope, URLs, numbers, headings, and safety boundaries are fixed.
- Mechanical conversion is only a first pass. Run the Hans, mirror, anchor, and locale-link gates, then do a human-readable semantic comparison.

## Codex delegation rules

- The primary agent owns scope, architecture, governance, final integration, Git, and user communication.
- Delegated executors receive bounded file ownership, acceptance commands, a return contract, and a stop condition. They must not revert concurrent work.
- A separate reviewer reads the final stable staged diff. Any later edit invalidates that review fingerprint.
- Agent boundaries do not create commit boundaries. Stage explicit paths only, run the required gates, and commit the accepted integrated result.

## Current curriculum contract (verified 2026-09-13)

| Component | Status |
|---|---|
| Public curriculum | Stage 0–8, Stage 7.5, A1–A3, five role paths, walkthrough, Capstone, Glossary, and core resource pages have Traditional Chinese, Simplified Chinese, and English routes. |
| Reader path | Enrolled pages keep goals, bold core terms, required reading, rated projects/resources, exercise outcomes, and completion checks visible; setup, long code, alternatives, and troubleshooting may be collapsed. |
| Examples | Model-backed teaching folders keep a free/local Ollama path, an optional Anthropic path, budget guidance, and offline behavior tests unless the exercise is deliberately model-free. |
| Stage 5 | The chapter contains five cumulative exercises plus 5.1–5.8 reference entrances; the tool-calling tutor remains the installable meta-example. |
| Stage 6 | The reader path, advanced RAG/Memory pages, isolated collections, chunk-overlap guard, persistent memory, and offline behavior tests are present. Live model output quality is not claimed. |
| Stage 7 | The main order is Eval → Observability → Approval/Recovery → Deploy; Multi-Agent remains optional. Six example folders cover the production mechanics. |
| Automated checks | On 2026-09-13, 58 `scripts/test_*.py` modules collect 1,145 tests. Counts are a dated observation; CI and `pytest --collect-only` are the current source of truth. |
| Merge gate | `Required / pr-gate` is the stable required check. A green machine gate does not replace maintainer review. |
