# Project Memory — awesome-agentic-ai-zh

> Standing instructions for any AI agent (Claude, Codex, Gemini) working on this repo. Read this **first** before touching exercises or model recommendations.

## 📍 Repo positioning — read before adding anything

**This repo's role**: **learning roadmap + 240+ curated resources + simple illustrative cases.**

**Benchmark for "what we are NOT"**: [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) is the canonical chapter-length zh-TW depth tutorial (16 production capabilities, chapter format). **We don't compete with it; we route to it.**

**Implications when contributing**:

| Decision | Rule |
|---|---|
| New stage-level exercise folder | OK if it adds **a roadmap node + dual-path SDK demo + 1-line punchline**. 70-150 lines starter is the right size. |
| Expanding a starter beyond ~150 lines | **Push back**. If it's growing into chapter-length, add a 📚 callout pointing to hello-agents instead. |
| Adding a 5th `extension` to README | Diminishing return. Keep README tight (under ~200 lines); extra depth goes to the 📚 callout. |
| New resource (lib / paper / tool / framework) | Almost always YES — add to the relevant `精選 Projects` section or `resources/` catalog. Curation is the primary value. |
| New chapter-length tutorial inside this repo | **Push back**. If the topic deserves chapter-length, the right move is: write a 1-page summary + simple illustrative case + 📚 callout to a canonical source (hello-agents / Anthropic Cookbook / framework's own docs). |
| Trilingual mirror priority | zh-TW canonical first; en + zh-Hans mirror when capacity allows. Don't block shipping waiting for 3-lang. |

**One-line summary**: **route → depth, not reinvent**. Every exercise folder ends with 📚 "want chapter-length? go to hello-agents X + [extra ref]".

**Existing examples of this pattern** (as of 2026-05-13):

- All Stage 3 / 4 / 6 / 7 example READMEs have the 📚 callout (20 folders × 1 callout)
- Main README + 3-lang mirror have the positioning statement near 🎯 Why this exists section
- `tracks/cli/` is outline-only on purpose (CLI exercises are bash/markdown/config, not Python SDK; doesn't fit the dual-path frame — that's correct)

## Canonical Ollama models (verified against user's `ollama list`)

| Model tag | When to use | Notes |
|---|---|---|
| **`gemma4:e4b`** | Stage 1 + 2 (plain chat, prompt engineering) | Effective 4B params, ~7.5 GB download, CPU-friendly. **The `:e4b` tag matters** — NOT `gemma3n:e4b`, NOT `gemma3:4b`, NOT `gemma4:latest`. |
| **`gemma4:e2b`** | Low-RAM-machine alternative for Stage 1+2 | ~4 GB, runs on 4 GB RAM machines |
| **`qwen2.5:3b`** | Stage 3+ (tool use / agent / ReAct) | 1.9 GB, **reliable tool-use support** (OpenAI function-calling format), default for any agent / function-calling exercise |
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
| **`claude-fable-5`** | Mythos-class (above Opus); suspended 2026-06-12, **restored 2026-07-01** (controls lifted 2026-06-30); the highest Claude tier | $10 input / $50 output |
| **`claude-haiku-4-5`** | Cheapest cloud option, OK for all exercises | $1 input / $5 output |
| **`claude-sonnet-5`** | Production default, agent development | $2 input / $10 output |
| **`claude-opus-5`** | Opus-class flagship (2026-07-24; succeeds Opus 4.8 at the same price, which stays available as legacy); high quality, complex reasoning (Fable 5 is the tier above) | $5 input / $25 output |

## Framing rules (do not violate)

1. **Claude is the canonical / production reference** in documentation positioning.
2. **Ollama is the practice default** because of cost — students should not be blocked by API fees during learning.
3. **Every exercise must ship BOTH paths**:
   - Path A (Ollama, `<details markdown="1" open>`, primary practice runnable)
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
- **Claude does translations** — do NOT delegate to Codex/Gemini.
- For zh-Hans bulk char conversion, use a per-char map (script in `.ai/2026/05/12/t2-trad-to-simp/`) then manual fix-up for remaining stragglers.

## Codex delegation rules

- Codex executes bulk batches (multiple exercises following an established pattern).
- Claude writes the pilot template + reviews codex output.
- Codex briefs must include the file structure (starter.py + starter_anthropic.py + test.py + test_anthropic.py + README.md + requirements.txt) and the framing rules above.
- Codex cannot commit (sandbox `.git` permission); Claude commits on its behalf per CLAUDE.md `~/.claude/CLAUDE.md` "agent boundary = commit boundary" rule.

## Existing curriculum state (as of 2026-05-12)

| Component | Status |
|---|---|
| Stage 0-3 inline exercises (3 langs) | ✅ Done — Path A Ollama / Path B Anthropic + budget callouts |
| Stage 3 folder `03-react-from-scratch` | ✅ Pilot rename done — `starter.py` (Ollama) + `starter_anthropic.py` (Anthropic) + dual test files |
| Stage 3 folders `02/04/05/06` | ✅ Phase 3 done (2026-05-12) — Ollama `starter.py` + rename existing → `starter_anthropic.py` + trilingual READMEs in dual-path style |
| Stage 1 folder `04-cross-provider` | ✅ Multi-provider (already includes Ollama via `call_ollama` in README) |
| Stage 1 folder `05-error-handling` | ✅ Phase 3 done (2026-05-12) — openai SDK exceptions + same retry wrapper, trilingual READMEs |
| Stage 3 doc inline simplified examples (練習 2-6) | ✅ Done (2026-05-12) — 5 new `<details>` blocks added inline (Path A 8-15 line cores), trilingual mirror, zh-Hans Trad-char drift fixed at lines 44/47/77/110/152 |
| `examples/stage-5/tool-calling-tutor/` skill | ✅ Done (2026-05-12) — installable Claude Code skill (frontmatter + 5-step body), 3 references (debug-flowchart / schema-evolution / sdk-diff), evals.json with 5 cases, trilingual READMEs + translations. Dual purpose: learner-aid + Stage 5 5.3 meta-example. Cross-referenced from stages/03 + stages/05 |
| Stage 4 (5 exercises) | ✅ Verified 2026-05-13 — ex1 LangGraph+CrewAI comparison, ex2 CrewAI multi-agent roles (CrewAI install fails on Python 3.14, code unmodified), ex3 LangGraph branching+HITL, ex4 Smolagents CodeAct, ex5 Pydantic AI typed output. 14 of 15 test suites verified green; ex2 CrewAI untestable on 3.14 due to tiktoken/regex wheel build failures |
| Stage 6 (5 exercises) | ✅ Verified 2026-05-13 — all 10 test suites green. Fixed 2 bugs: ChromaDB 'kb' collection name (needs 3-512 chars; renamed knowledge_base) + EphemeralClient state leak across test fixtures (added uuid suffix per test) |
| Stage 7 (5 exercises) | ✅ Verified 2026-05-13 — all 10 test suites green. Fixed 1 bug: eval test fake_agent operator precedence (and binds tighter than or) caused test_run_eval_aggregates to fail. FastAPI deploy includes Dockerfile |
| Track A1-A3 (12 CLI exercises) | 🟡 Outline complete (`tracks/cli/A{1,2,3}-*.md` × 3 langs, ~367 lines zh-TW; 12 numbered exercises documented end-to-end with goal / required-reading / hands-on / curated-projects / self-check). `examples/track-a/` folder intentionally NOT built — these exercises are bash + CLAUDE.md + slash command + MCP integration + GitHub Actions yml, **NOT** Python SDK code; the dual-path Ollama/Anthropic framing doesn't apply. Reference doc: [`resources/cli-agents-guide.md`](resources/cli-agents-guide.md) (148 lines). |
| Stage 5 (11 sub-exercises) | ⚪ Pending — different shape (bash / MCP / markdown / CLAUDE.md / SKILL.md / plugin.json authoring, not OpenAI SDK Python). 5.3 has 1 meta-example shipped: [`examples/stage-5/tool-calling-tutor/`](examples/stage-5/tool-calling-tutor/). Other sub- framing TBD — see [`docs/TESTING_PLAN.md`](docs/TESTING_PLAN.md). |
| `examples/README` LLM list + budget table | ✅ Done (3 langs) |
| Per-stage budget callouts | ✅ Done for Stage 1+2+3 (3 langs each) |

## Known follow-up: pilot `03-react-from-scratch` README.en.md + README.zh-Hans.md drift

The zh-TW `README.md` of `examples/stage-3/03-react-from-scratch/` already uses the dual-path layout (Path A primary / Path B optional + budget callouts + mock test mention for both backends). The `README.en.md` and `README.zh-Hans.md` siblings were NOT updated when the pilot's dual-path zh-TW README was written — they still describe the pre-dual-path layout (Anthropic-only `starter.py`, single `test.py`). After Phase 3 the other 5 folders all have aligned trilingual dual-path READMEs, so the pilot is now the lone outlier. Fix when revisiting Stage 3 docs polish — straight translation pass of the zh-TW README is enough.

## Reference scripts (in `.ai/2026/05/12/`)

- `t2-trad-to-simp/convert.py` — zh-TW → zh-Hans bulk char map (Stage 2)
- `t2-trad-to-simp/stage3_convert.py` — Stage 3 練習 1 inline section conversion
- `t2-trad-to-simp/en_swap.py` — Anthropic SDK → OpenAI SDK bulk substitution
- `t2-trad-to-simp/en_pathb_expand.py` — Compact 🦙 hint → full Path B `<details>` block
- `t2-trad-to-simp/rename_gemma.py` — `gemma3n:e4b` → `gemma4:e4b` (this commit's fix)

Keep these scripts — they're reusable for T3+ work.
