# Testing Plan — T3+ Verification Log

> Updated 2026-08-28. The opening table is the historical T3+ baseline; later
> sections record the current chapter-by-chapter modernization layers separately.
> The old branch `t3-stage-4-6-7-unverified` was merged into `main` and deleted,
> but a newer layer is not called shipped until its own branch reaches `main`.

## Historical T3+ baseline (on `main`)

| Batch | What | How verified | Bugs fixed |
|---|---|---|---|
| Phase 3 — Stage 1 + 3 folder renames (6 folders) | `starter.py` (Ollama) / `starter_anthropic.py` / both test suites | `python test.py` + `python test_anthropic.py` per folder | 0 |
| Phase A — `stages/03-tool-use-and-hello-agent.md` inline `<details>` (練習 2-6) | 5 simplified inline blocks + zh-Hans drift | `wc -l` parity, `grep` no residual Trad chars | 0 |
| Phase B — `examples/stage-5/tool-calling-tutor/` skill | SKILL.md + 3 trilingual references + executable offline contracts + trilingual READMEs | frontmatter, install-safe references, relative links, five routes, safety wording, PowerShell-first install, and offline checker are regression-tested | 0 (live model quality is intentionally not claimed) |
| Phase C — cross-references | stages/03 + stages/05 + CLAUDE.md links | `grep -c` confirms 10 references across 7 files | 0 |
| **Stage 4 (5 ex)** | LangGraph + CrewAI + LangGraph workflow + Smolagents + Pydantic AI | 8/8 test suites verified green; ex2 CrewAI install-blocked on Python 3.14 (tiktoken/regex wheels) — code shipped unmodified | 3 (i18n key mismatch in ex3 + Smolagents docstring `Args:` requirement in ex4 + Pydantic AI version fallback in ex5 test) |
| **Stage 6 (5 ex)** | embeddings + ChromaDB + chunking + full RAG + long-term memory | 10/10 test suites verified green | 2 (ChromaDB `kb` collection name too short for Chroma 1.0+; `EphemeralClient` state leak across test fixtures) |
| **Stage 7 (5 ex)** | multi-agent debate + eval + observability + streaming/caching + FastAPI deploy | 10/10 test suites verified green | 1 (operator precedence: `and` binds tighter than `or` in fake_agent dispatcher) |

**Total: 28/30 test files run green** + 1 install caveat (CrewAI on Python 3.14) + 1 pending live test (skill auto-load).

**Total bugs fixed**: 6 — all in commit [`50c3bf8`](https://github.com/WenyuChiou/awesome-agentic-ai-zh/commit/50c3bf8).

## ✅ Stage 2 prompt-eval example (2026-08-27)

`examples/stage-2/01-prompt-eval-loop/` now gives beginners one small, repeatable loop: run the same six support messages, add three examples to the prompt, rerun, and compare the two scores.

- `python starter.py` and `python starter_anthropic.py` both run a deterministic fixture without a model or API key. The visible `3/6 → 6/6` result explains the mechanics; it is **not** a model benchmark or a promise that few-shot examples always improve a result.
- `python test.py`: **4/4 passed** for prompt construction, strict label scoring, all six cases, and the Ollama/OpenAI-compatible response shape.
- `python test_anthropic.py`: **2/2 passed** for Anthropic text-block handling and request construction.
- Live Ollama and Anthropic quality are optional learner checks. CI does not depend on a nondeterministic model score or spend API money.

## 🟢 Pedagogy v1 also shipped (2026-05-13)

Recognized late in the session: every `starter.py` is a **complete solution**, not a TODO skeleton. A learner who clones and runs `python test.py` passes without writing any code.

v1 fix (doc-only, no code rename):

- `docs/HOW_TO_USE.md` — full active-vs-passive learning method (~200 lines, zh-TW)
- 22 exercise READMEs — 🎓 callout pointing to `mv starter.py starter_reference.py` shortcut + link to HOW_TO_USE
- Main README × 3 langs — surface the meta-instruction at the top-level

Shipped in commits [`d598e37`](https://github.com/WenyuChiou/awesome-agentic-ai-zh/commit/d598e37) + [`2cf99fe`](https://github.com/WenyuChiou/awesome-agentic-ai-zh/commit/2cf99fe).

## ⚠ Known caveats still on `main`

1. **CrewAI exercise (Stage 4 ex2)** not tested on Python 3.14 — tiktoken + regex don't have wheels yet. Code shipped unchanged; users on Python 3.11/3.12/3.13 should be fine. Document at top of `examples/stage-4/02-multi-agent-roles/README.md` if needed for future learners.

2. ~~**tool-calling-tutor skill only had structural validation**~~ — **RESOLVED 2026-08-28**. The 05B layer fixes the copy command, makes every bundled reference resolve through `${CLAUDE_SKILL_DIR}`, replaces the invalid promptfoo-config claim with `python evals/check_evals.py`, and executes five offline behavior contracts. The regression also checks three-locale frontmatter, reference paths, relative links, safety boundaries, unsupported benchmark removal, and PowerShell-first installation. It does not call a live model or claim a model-quality score; direct `/tool-calling-tutor` invocation remains the honest manual product check.

3. ~~**Walkthrough Python never executed**~~ — **RESOLVED 2026-08-10**. All 9 python blocks (304 lines) of `walkthroughs/build-first-agent-in-7-steps.md` were extracted to the filenames the doc names and executed in a clean venv on Python 3.14, with `Anthropic` and `requests` mocked (no API key, no spend): Stage 1-6 (6 blocks) plus all of Stage 7 (7.1 `eval_provider`, 7.2 `step7_observability`, 7.3 `main.py`). **Four** real defects were found and fixed in all three locales, plus two zh-Hans blocks that did not even parse (`
` expanded into real newlines, so Stage 1 and `reflect` raised `unterminated f-string literal` — a Simplified-Chinese reader's very first script crashed): Stage 6's vector memory stored nothing at all (empty-DB early return meant `store_paper` was never reached, compounded by a hardcoded `"..."` id that `collection.add()` silently ignores); `compare_with_memory`'s `comparison` was dropped because `State` never declared it; and `import step2_paper_summary` issued a billed API call at module level, which every later stage inherited. Post-fix, measured: memory count goes 1→2→3, `comparison` survives in state, and the four imported modules make 0 API calls; and Stage 6 now stores each paper's own summary rather than three byte-identical `[Reviewer verdict: PASS]` strings — the `compare` node read `messages[-1]`, which is `reflect`'s verdict, not the summary. Completed 2026-08-10: 7.2's import path was corrected (`observe` moved to the top-level package in langfuse **3.0**, not 4.x — verified by installing 2.60.10, 3.0.0 and 4.14.2; only 2.x has `langfuse.decorators`. `@observe(name=…)` itself is unchanged across all four, signature checked) and 7.3 was run with fastapi 0.141.1 — `TestClient` gets HTTP 200 and a `{'summary': …}` body from `POST /summarize`, and HTTP 422 on a missing field. **Still open**: end-to-end output quality against a live API key is untested — every run so far has mocked the model.

4. **starter.py = complete solution pedagogy gap** — flagged in `docs/HOW_TO_USE.md`. v2 would split into `starter_template.py` (TODO) + `starter_reference.py` (solution); v1 is doc-only meta-instruction.

5. ~~**Trilingual mirror of 🎓 callout incomplete**~~ — **RESOLVED 2026-08-02**. The 🎓 callout and the 📚 deeper-material block are now in the `.en.md` + `.zh-Hans.md` mirrors of **21 of the 22** exercise READMEs (202 blockquote lines). The 22nd, `examples/stage-1/04-cross-provider`, is **not a callout gap** — it is the only example folder with **no mirror files at all**, so it needs a full trilingual translation first, not a callout port. A blocking CI gate (`scripts/check-mirror-parity.py`) now stops this class of gap reappearing.

6. ~~**Pilot exercise drift**~~ — **RESOLVED 2026-08-02**. `examples/stage-3/03-react-from-scratch/README.en.md` + `.zh-Hans.md` were missing the entire free local Path A (Ollama) and ran the Ollama script under the Anthropic heading; both now match the dual-path canonical.

## 🔵 Stage 5 + Track A — current coverage

### Track A1-A3 CLI track — **outline complete, no `examples/` folder by design**

12 hands-on exercises documented across `tracks/cli/A{1,2,3}-*.md` × 3 langs (zh-TW canonical ~367 lines):

| File | Lines (zh-TW) | Exercises |
|---|---|---|
| `tracks/cli/A1-cli-intro.md` | 157 | CLI-1 安裝與第一次唯讀任務 / CLI-2 project instructions / CLI-3 第二個 CLI 重跑 / CLI-4 假憑證與安全失敗 |
| `tracks/cli/A2-cli-workflow.md` | 221 | CLI-5 project instructions / CLI-6 Skill / CLI-7 多步驟拆解 / CLI-8 portable prompt |
| `tracks/cli/A3-cli-production.md` | 241 | CLI-9 MCP server 接 CLI / CLI-10 GitHub Actions / CLI-11 cost tracking / CLI-12 plugin 跨 team 分享 |

**No `examples/track-a/` folder built — and this is intentional**. CLI exercises are:

- Bash commands (`ollama pull`, `claude` install, MCP-server install)
- Markdown authoring (project-instructions files and `SKILL.md`)
- YAML / JSON config (GitHub Actions `.yml`, `plugin.json`, `marketplace.json`)
- **Not Python SDK code**, so the dual-path Ollama/Anthropic `starter.py` + `test.py` pattern doesn't apply.

What learners do for Track A: follow each numbered exercise in the outline doc, on their own real repo (their work codebase, not a sample). The `tracks/cli/A*.md` files contain success criteria for self-check.

**Core reference**: [`resources/cli-agents-guide.md`](../resources/cli-agents-guide.md) — 9-CLI identity, provider, sign-in, and safety reference; the full comparison is collapsed by default.

**Potential v2** (not committed): could ship `examples/track-a/` containing a sample project-instructions file, `skills/review-changes/SKILL.md`, and a sample GHA workflow yml. Low priority — current outline is self-contained.

### Stage 5 — reader path covered; meta-example hardening pending

Stage 5 (`stages/05-claude-code-ecosystem.md`) has five cumulative exercises and eight reference sections (5.1–5.8). The first reader-UX layer keeps every exercise outcome and first copyable action visible, while longer setup and troubleshooting stay closed by default.

| Area | Current evidence |
|---|---|
| 5.1 `CLAUDE.md` | Copyable minimal rule card and manual success check in the stage page |
| 5.2 MCP | Restricted-directory exercise and explicit inside/outside-path success condition |
| 5.3 Skills | Copyable Skill plus [`examples/stage-5/tool-calling-tutor/`](../examples/stage-5/tool-calling-tutor/); the example receives its own 05B hardening layer |
| Hooks | Copyable observation-only `PreToolUse` logger, synthetic-event smoke test, `/hooks` landing check, and no-prompt/no-secret logging boundary |
| 5.5 Subagents | Read-only review exercise with isolated output and a visible success condition |
| 5.6–5.8 | Current Dynamic workflows／Worktree／Agent-loop／Agent SDK reference path; optional depth stays collapsed |

`scripts/test_stage05_content.py` permanently executes the Hook logger against a synthetic `PreToolUse` event, asserts that only timestamp／event／tool metadata is written, locks the three locale code blocks together, and compiles the current Python Agent SDK `AssistantMessage.content`／`TextBlock` example. It does not call a live model or claim live output quality.

The 05B layer validates the `tool-calling-tutor` frontmatter, installed and repository-relative links, translations, eval contract, model／SDK wording, and offline behavior. It stays separate from 05A so the reader rewrite and executable-example migration can be reviewed and rolled back independently.

### Stage 6 — reader path covered; executable hardening stays in the next layer

Stage 6 (`stages/06-memory-rag.md`) now keeps seven core terms, five cumulative exercise outcomes, the first copyable PowerShell action, one RAG + Memory mini-project, and the Stage 7 check visible. Time, setup, advanced RAG patterns, memory taxonomy, chunking, reflection, evaluation, and the 18-row resource table stay closed by default.

`scripts/test_stage06_content.py` locks the three locales to the same freshness marker, concepts, five exercise headings, 109 legacy heading aliases, 18 resource URLs and ratings, five accessible rowgroups (`4／5／4／3／2`), distinct `1672×941` localized images, current project owners/statuses, the honest temporary-storage boundary in Exercise 5, and the absence of stale or mixed-language text. `scripts/check-reader-ux.py` excludes empty compatibility anchors because they render no reader-visible text, measures the collapsed mainline at `3,290／6,367／3,340` non-whitespace characters, and permits only 50 characters of growth per locale.

This reader layer does not claim that the five example folders are fully hardened. The next stacked layer will separately test the chunk-overlap boundary, isolate Chroma collections, replace ephemeral “long-term” memory with real persistence, preserve Ollama／Anthropic paths, and make the teaching tests offline and behavior-based.

### Stage 7 — reader path and executable hardening covered in separate stacked layers

Stage 7 (`stages/07-multi-agent-production.md`) keeps the single-Agent／Multi-Agent decision, seven bold core terms, five-layer map, eight-part Harness checklist, OpenRouter／Pi／OpenCode／Orca／QM role split, five real exercise headings and commands, execution-receipt mini-project, benchmark-reading discipline, and self-check visible. Seven closed disclosures hold setup, full reading, Loop／Graph depth, recovery／cost details, full exercise steps, benchmark links, and the resource catalog.

`scripts/test_stage07_content.py` locks the three locales to the same 20 external URLs, four accessible rowgroups (`4／6／5／5`), 20 editorial ratings, seven closed disclosures, five real example directories, direct `python test.py` entry commands, quiet `2026-08-28 UTC` verification date, current canonical project owners, and the absence of frozen SOTA scores, stale redirects, GitHub star counts, empty-quote artifacts, or a fake sixth exercise. It also verifies six distinct locale-specific PNGs at full educational-diagram size and rejects untranslated CJK in the English page.

`scripts/check-reader-ux.py` measures the collapsed mainline at `5,770／9,925／5,863` non-whitespace characters and locks all seven core-term definitions before Exercise 1. `scripts/check-image-locale.py` ensures the English and Simplified Chinese pages use their own bright image variants.

The example-hardening layer keeps the five folders separate and adds `scripts/test_stage07_examples.py`. It locks 15 trilingual READMEs, each folder's rated `hello-agents` route to chapter-length material, five current-major requirements files, `qwen3.5:4b`, the pinned `claude-haiku-4-5-20251001` ID, PowerShell-first isolated setup, closed disclosures, ordered URL／price parity, and the absence of old fixed cost／latency／cache claims. The shared examples guide and three setup guides separately keep `qwen2.5:3b`／`llama3.2:3b` for Stage 3–6 function-calling exercises and `qwen3.5:4b` for Stage 7 production mechanics, so “Stage 3+” cannot silently choose two defaults or preserve `$0/run` wording outside the example folders.

All ten directly executable offline entrypoints pass in a clean `python:3.11-slim` container with the resolved current packages. Their 55 behavior tests cover empty and whitespace-only output rejection, exact Debate／Eval Judge contracts, sanitized exception categories that do not retain a secret-bearing raw message, provider usage recording, a cache demo deliberately above Haiku 4.5's 4,096-token minimum, FastAPI input bounds, secret-marker log regressions, and 200／422／429／502／503 behavior. Debate role separation is an example shape, not evidence that more agents reduce bias or improve correctness. The deploy image also builds from scratch, runs as UID `10001` (`appuser`), and returns `{"status":"ok"}` while mounted read-only with a temporary `/tmp` and a loopback-only host port. These checks do not call a live model, prove output quality, or turn the container into a sandbox.

### Stage 7.5 — progressive reading map covered; no example layer

Stage 7.5 keeps six bold core terms, all 12 advanced concepts grouped by problem, a five-branch choice map, a directly copyable four-line work-boundary card, five priority readings, and a short self-check visible. Nine closed disclosures hold prerequisites, source limits, failure cases, cross-vendor and coding harness detail, benchmark discipline, Dynamic Workflows, Model–Harness Fit, and the complete resource table.

`scripts/test_stage075_content.py` locks the three locales to 12 concepts in the same order, four concept rowgroups (`3／3／3／3`), 24 resource URL/rating pairs, five resource rowgroups (`5／5／5／5／4`), one matching freshness marker, nine closed disclosures, and the legacy Dynamic Workflows anchors. It also rejects the old Replit/Voyager years, fixed context/code-size/throughput claims, empty-quote artifacts, untranslated English fragments, and current-status drift for AutoGen, Microsoft Agent Framework, Sandbox Agents, and Dynamic Workflows.

Six newly generated `1672×941` PNGs cover the four problem groups and the five-branch reading decision. The test requires six distinct hashes and exact locale references; `scripts/check-image-locale.py` provides the whole-repository mirror check. `scripts/check-reader-ux.py` locks the collapsed mainline at `4,824／7,768／4,850` non-whitespace characters and all six core terms before the work-boundary card. Stage 7.5 is a reading-map, so there is deliberately no runnable example-hardening layer.

## v2 path (deferred)

Per `docs/HOW_TO_USE.md` "給維護者：v2 path":

- Split each `starter.py` → `starter_template.py` (TODO skeleton) + `starter_reference.py` (solution)
- Make `test.py` behavioral (input → output contract) instead of implementation-bound
- ~20 folders × 3 file changes = ~60 file changes
- Probably needs its own session

## Historical: what was on the unverified branch

Before verification, Stage 4 + 6 + 7 commits sat on branch `t3-stage-4-6-7-unverified` (rationale: framework deps not pip-installed at write time, API drift risk). After actual verification on 2026-05-13:

```
50c3bf8 fix(examples): 6 bugs found while verifying Stage 4/6/7 tests
9f60759 Stage 7 練習 5 (FastAPI deploy)
1a8ba16 Stage 7 練習 4 (streaming + caching)
128ca7a Stage 7 練習 3 (observability)
8119de0 Stage 7 練習 2 (eval)
5ff3ce3 Stage 7 練習 1 (multi-agent debate)
8150881 Stage 6 練習 5 (long-term memory)
7633874 Stage 6 練習 4 (full RAG pipeline)
7a8af9b Stage 6 練習 3 (chunking comparison)
b83a5e5 Stage 6 練習 2 (vector DB)
7d2c1b7 Stage 6 練習 1 (embeddings)
ab6d358 Stage 4 練習 5 (Pydantic AI)
6316d83 Stage 4 練習 4 (Smolagents CodeAct)
ea9c14a Stage 4 練習 3 (LangGraph branching)
dbe7c91 Stage 4 練習 2 (CrewAI multi-agent)
8051861 Stage 4 練習 1 (LangGraph + CrewAI)
```

All merged into `main` via [`cdb0ae3`](https://github.com/WenyuChiou/awesome-agentic-ai-zh/commit/cdb0ae3). Branch deleted from origin after merge.
