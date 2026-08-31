# Testing Plan — T3+ Verification Log

> Updated 2026-08-30. The opening table is the historical T3+ baseline; later
> sections record the current chapter-by-chapter modernization layers separately.
> The old branch `t3-stage-4-6-7-unverified` was merged into `main` and deleted,
> but a newer layer is not called shipped until its own branch reaches `main`.

## Visible required-reading and resource contract

Important reading, featured projects, and complete rated learning-resource tables are part of the
learner's path, so a closed `<details>` block cannot be their only landing place. The global
`forbidden_closed_summary_terms` list blocks disclosure summaries such as “Required reading” or
“Learning resources” in every enrolled locale. Each page also configures
`visible_section_minimums` in `scripts/reader-ux-pages.yml` with `min_links` and `min_ratings` for
the relevant visible section. The checker renders the visible Markdown, then counts real text links
and visible rating text. It accepts inline, reference-style, autolink, and HTML `<a href>` entries,
but ignores closed disclosures, code examples, image-only links, image alt text, link destinations,
fragment-only navigation, hidden HTML, and attributes that only look like entries. Long setup notes,
alternatives, cost, and troubleshooting may remain collapsed. A dedicated very large catalog is the
one deliberate exception: its category choices and safety boundaries remain visible while hundreds
of individual entries may open by category on demand.

The closed-summary gate applies to all 25 enrolled pages. Exact section minimums protect the
modernized chapter and role paths, including Stage 0–8, Stage 7.5, Track A1–A3, and the Researcher
and Developer paths. This keeps the rule measurable: removing or re-hiding one rated row now fails
before review instead of relying on memory.
Install its pinned local dependencies with
`pip install --require-hashes -r scripts/requirements-reader-ux.txt`.

## Public entry-route contract

`scripts/test_site_route_coherence.py` now treats the README and docs landing page as part of the
curriculum, not decoration. The trilingual README must name eight topic stages plus the Stage 0
readiness check and Stage 7.5 reading stop, show outcome-first route tables, and keep all duration
figures inside one closed time-estimate disclosure. The test blocks the old stage-count shorthand,
fixed frontier year windows, approximate code-line claims, and the old blank-file rewrite exercise.

Each landing page must show ten cards in order from Stage 0 through Stage 8, including Stage 7.5.
The banner trio must be three distinct PNG files on the same `1672×941` canvas and remain under
2 MB each. The reproducibility contract records Track A as A1 → A2 → Stage 5 → A3 → Stage 8 and
Track B as 3 → 4 → Stage 5 → 6 → 7 → 7.5 → Stage 8 before the role paths. It forbids mutable
duration, price, version, year, and stars metrics. Human review still checks text rendering,
alignment, and arrow／icon overlap.

`scripts/test_main_readme_content.py` protects the README's progressive reading path. It requires
the main route, role choices, important terms, required reading, and ten rated learning resources to
stay visible. Only four secondary groups may start closed. The resource table must keep three real
row groups (`3／3／4`), and the three locales must keep the same links, order, ratings, and meaning.
The size limit prevents the entrance from slowly becoming crowded again. These checks protect the
shape; final human review still confirms that simple wording has not removed an important idea.

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
- 22 exercise READMEs — 🎓 callout once taught a rename-and-rewrite shortcut and linked to HOW_TO_USE; the 2026-08-30 reader-UX layer replaced that shortcut with run → change one thing → retest
- Main README × 3 langs — surface the meta-instruction at the top-level

Shipped in commits [`d598e37`](https://github.com/WenyuChiou/awesome-agentic-ai-zh/commit/d598e37) + [`2cf99fe`](https://github.com/WenyuChiou/awesome-agentic-ai-zh/commit/2cf99fe).

## ⚠ Known caveats still on `main`

1. **CrewAI exercise (Stage 4 ex2)** not tested on Python 3.14 — tiktoken + regex don't have wheels yet. Code shipped unchanged; users on Python 3.11/3.12/3.13 should be fine. Document at top of `examples/stage-4/02-multi-agent-roles/README.md` if needed for future learners.

2. ~~**tool-calling-tutor skill only had structural validation**~~ — **RESOLVED 2026-08-28**. The 05B layer fixes the copy command, makes every bundled reference resolve through `${CLAUDE_SKILL_DIR}`, replaces the invalid promptfoo-config claim with `python evals/check_evals.py`, and executes five offline behavior contracts. The regression also checks three-locale frontmatter, reference paths, relative links, safety boundaries, unsupported benchmark removal, and PowerShell-first installation. It does not call a live model or claim a model-quality score; direct `/tool-calling-tutor` invocation remains the honest manual product check.

3. ~~**Walkthrough Python never executed**~~ — **RESOLVED 2026-08-10**. All 9 python blocks (304 lines) of `walkthroughs/build-first-agent-in-7-steps.md` were extracted to the filenames the doc names and executed in a clean venv on Python 3.14, with `Anthropic` and `requests` mocked (no API key, no spend): Stage 1-6 (6 blocks) plus the Stage 7 provider, observability wrapper, and FastAPI service. **Four** real defects were found and fixed in all three locales, plus two zh-Hans blocks that did not even parse (`
` expanded into real newlines, so Stage 1 and `reflect` raised `unterminated f-string literal` — a Simplified-Chinese reader's very first script crashed): Stage 6's vector memory stored nothing at all (empty-DB early return meant `store_paper` was never reached, compounded by a hardcoded `"..."` id that `collection.add()` silently ignores); `compare_with_memory`'s `comparison` was dropped because `State` never declared it; and `import step2_paper_summary` issued a billed API call at module level, which every later stage inherited. Post-fix, measured: memory count goes 1→2→3, `comparison` survives in state, and the four imported modules make 0 API calls; and Stage 6 now stores each paper's own summary rather than three byte-identical `[Reviewer verdict: PASS]` strings — the `compare` node read `messages[-1]`, which is `reflect`'s verdict, not the summary. Completed 2026-08-10: the observability import was corrected to the package-level `observe`, and the FastAPI endpoint was checked for HTTP 200 and missing-field HTTP 422 behavior. **Still open**: end-to-end output quality against a live API key is untested — every run so far has mocked the model.

The 2026-08-31 coherence layer adds `scripts/test_walkthrough_coherence.py`. It locks the three locale pages to the same current official sources and freshness marker; removes deprecated LangGraph `create_react_agent`, insecure arXiv HTTP／no-timeout fetches, global Promptfoo installation, and version-history prose from the learner path; and requires the visible 20-case Eval seed, current Langfuse LangChain callback／base URL／flush contract, Human Approval／Checkpoint／Resume／Idempotency／Recovery contract, non-root read-only local container, locale-correct Safe Execution link, Stage 8 smallest-interface table, and `needs_review` safety exit. The regression executes the pure current-agent wrapper with a fake graph to prove Memory summary／comparison survive, callback and recursion budgets reach the graph, disallowed sources fail closed, and graph-budget exhaustion returns a typed safe exit. Structural and fake-boundary tests still do not claim live model quality, hosted trace delivery, provider token／cost reporting, prompt-injection resistance, or production isolation.

4. ~~**Complete-solution pedagogy gap**~~ — **RESOLVED 2026-08-30**. `docs/HOW_TO_USE.md` and 39 trilingual Stage 1–4 exercise READMEs now teach one small loop: run the provided starter, change exactly one thing, rerun the existing tests, then fix or undo that one change if it fails. The maintained examples stay directly runnable; learners are not asked to rename files or rebuild the whole solution before they can start.

5. ~~**Trilingual mirror of 🎓 callout incomplete**~~ — **RESOLVED 2026-08-02**. The 🎓 callout and the 📚 deeper-material block are now in the `.en.md` + `.zh-Hans.md` mirrors of **21 of the 22** exercise READMEs (202 blockquote lines). The 22nd, `examples/stage-1/04-cross-provider`, is **not a callout gap** — it is the only example folder with **no mirror files at all**, so it needs a full trilingual translation first, not a callout port. A blocking CI gate (`scripts/check-mirror-parity.py`) now stops this class of gap reappearing.

   The softer `scripts/check-mirror-sync.py` reminder also treats `/` and `\` as the same repository path. `scripts/test_mirror_sync.py` feeds it both POSIX and Windows path spellings, so a synchronized trio cannot be reported as missing only because the contributor ran the gate on Windows. The Mirror Sync workflow watches both the detector and its regression file, then runs the dependency-free test before detecting a PR gap.

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

### Stage 3–4 — Agent Loop to Workflow Graph bridge covered

Stage 3 is the first **Agent Loop** chapter. Its three localized titles, opening definition, and visible core terms use the exact sequence `model → tool call → execute → tool result → model`. Three required readings, all six exercise outcomes and first actions, and the complete 21-row rated resource map remain visible. Eleven closed disclosures hold setup, budget, long code, provider-specific detail, troubleshooting, and optional depth.

Stage 4 keeps **Agent Frameworks** in the title and places **Workflow Graphs** first; it is not renamed to Graph Engineering. A five-row visible bridge separates Agent Loop, Agent Framework, Workflow Graph, Loop Engineering, and Production orchestration. The contract treats a framework as a toolbox, a Workflow Graph as the node／edge／branch／state map built with those tools, and Production orchestration as the Stage 7 work that makes the route observable, recoverable, and safe to operate. Graph Engineering remains an emerging alternate label rather than a cross-vendor standard. The contract also rejects the old implication that an Agent framework requires multiple Agents. Four required-reading steps with five official links, five exercise entries, and the complete 18-row rated project map remain visible; six disclosures hold setup and secondary detail.

`scripts/test_stage04_content.py` locks the three localized H1s, the exact visible loop sequence in both stages, the five-row bridge, old and new framework-heading anchors, Agent-framework boundary, required-reading URLs, 21／18 resource counts and ratings, mdBook summary labels, and the localized Stage 3／4 return labels in the directly affected example READMEs. `scripts/test_agent_engineering_route.py` locks the Stage 3 → Stage 4 → Stage 7 terminology route. `scripts/test_site_route_coherence.py` additionally locks the same localized titles in README, index, PROGRESS, the Stage 2 exit, the examples overview, all six Stage 3 example folders, the Stage 5 tool-calling tutor, and the schema-design cheatsheet; it requires README to distinguish learning order from the five overlapping control questions and scans non-historical Markdown for legacy full-title strings. `scripts/check-reader-ux.py` requires exactly `11／6` closed disclosures, zero default-open disclosures, the visible resource minimums, and the localized section order. These title changes do not alter executable behavior, filenames, or legacy anchors.

### Stage 5 — reader path covered; meta-example hardening pending

Stage 5 (`stages/05-claude-code-ecosystem.md`) has five cumulative exercises and eight reference sections (5.1–5.8). It keeps every exercise outcome, first copyable action, the complete required-reading order, and all 35 rated learning resources visible. Fourteen disclosures hold setup, syntax, optional depth, and troubleshooting.

| Area | Current evidence |
|---|---|
| 5.1 `CLAUDE.md` | Copyable minimal rule card and manual success check in the stage page |
| 5.2 MCP | Restricted-directory exercise and explicit inside/outside-path success condition |
| 5.3 Skills | Copyable Skill plus [`examples/stage-5/tool-calling-tutor/`](../examples/stage-5/tool-calling-tutor/); the example receives its own 05B hardening layer |
| Hooks | Copyable observation-only `PreToolUse` logger, synthetic-event smoke test, `/hooks` landing check, and no-prompt/no-secret logging boundary |
| 5.5 Subagents | Read-only review exercise with isolated output and a visible success condition |
| 5.6–5.8 | Current Dynamic workflows／Worktree／Agent-loop／Agent SDK reference path; optional depth stays collapsed |

`scripts/test_stage05_content.py` permanently executes the Hook logger against a synthetic `PreToolUse` event, asserts that only timestamp／event／tool metadata is written, locks the three locale code blocks together, and compiles the current Python Agent SDK `AssistantMessage.content`／`TextBlock` example. It also requires the full reading and project sections to remain outside `<details>`, locks the three distinct `1672×941` 5.1–5.7 relationship diagrams, their visible position before 5.1, locale-correct references, and a linked first mention of the official `modelcontextprotocol/servers` repository. The diagrams keep context, action, event checks, context isolation, file-tree isolation, and packaging as separate roles; they do not turn Worktree into a complete sandbox, Plugin into a runtime step, or Plugin packaging into a connection with Worktree. These checks do not call a live model or claim live output quality.

The 05B layer validates the `tool-calling-tutor` frontmatter, installed and repository-relative links, translations, eval contract, model／SDK wording, and offline behavior. It stays separate from 05A so the reader rewrite and executable-example migration can be reviewed and rolled back independently.

### Stage 6 — reader path covered; executable hardening stays in the next layer

Stage 6 (`stages/06-memory-rag.md`) now keeps seven core terms, four required readings, five cumulative exercise outcomes, the first copyable PowerShell action, one RAG + Memory mini-project, the 18-row rated resource table, and the Stage 7 check visible. Time, setup, advanced RAG patterns, memory taxonomy, chunking, reflection, and evaluation depth stay closed by default.

`scripts/test_stage06_content.py` locks the three locales to the same freshness marker, concepts, five exercise headings, 109 legacy heading aliases, four visible required-reading URLs, 18 visible resource URLs and ratings, five accessible rowgroups (`4／5／4／3／2`), distinct `1672×941` localized images, current project owners/statuses, the honest temporary-storage boundary in Exercise 5, and the absence of stale or mixed-language text. `scripts/check-reader-ux.py` excludes empty compatibility anchors because they render no reader-visible text, measures the first-view path at `7,482／11,546／7,530` non-whitespace characters, permits only 50 characters of growth per locale, and blocks any attempt to hide the four readings or 18 rated resources in a disclosure.

`scripts/test_stage06_rag_pipeline.py` separately locks the detailed closed-disclosure diagram: three distinct high-resolution locale images, exact locale references, two-lane wording, optional-step language, vector-database-independent retrieval, 2-step／Agentic／Hybrid RAG distinctions, current Qdrant／Weaviate URLs, and Microsoft GraphRAG's maintenance-mode caveat. The diagram's arrow geometry and localized glyphs still require visual inspection; the prompt log records the corrected retrieve landing point and the Simplified-Chinese cleanup.

This reader layer does not claim that the five example folders are fully hardened. The next stacked layer will separately test the chunk-overlap boundary, isolate Chroma collections, replace ephemeral “long-term” memory with real persistence, preserve Ollama／Anthropic paths, and make the teaching tests offline and behavior-based.

### Stage 7 — reader path and executable hardening covered in separate stacked layers

The synchronized Stage 7 title is **Agent Production Engineering: Harness, Loops, and Graphs** (with localized equivalents). It is the learning map's umbrella for overlapping production responsibilities, not a claim that every vendor uses one formal standard name. Sixteen terms remain visible and defined: Eval, Outcome, Trajectory, Observability, Guardrail, Human Approval, Checkpoint, Resume, Recovery, Idempotency, Harness, Loop Engineering, Graph Engineering, Orchestration, Multi-Agent, and Handoff.

Stage 7 (`stages/07-multi-agent-production.md`) keeps the single-Agent／Multi-Agent decision, 16 bold core terms, five overlapping control questions, six required readings, a visible control-responsibility diagram, the eight-part Harness checklist, separate Loop Engineering and Workflow Graph／Production Orchestration sections, the OpenRouter／Pi／OpenCode／Orca／QM role split, four core exercises in Eval → Observability → Approval／Recovery → Deploy order, two visible advanced-option entrances, the research-assistant-with-receipt mini-project, benchmark-reading discipline, the 20-row rated resource map, and self-check visible. It explicitly distinguishes a program loop, an Agent Loop, and Loop Engineering; says that Harness commonly executes the Agent Loop; and rejects both “Loop replaces Harness” and a strict product-generation ladder. Seven closed disclosures hold setup, further reading, recovery／cost details, Graph／Multi-Agent depth, full exercise steps, and benchmark links. Required reading, the project, rated resources, core terms, and completion checks stay visible.

`scripts/test_stage07_content.py` locks the three locales to the same 16 terms in accessible rowgroups (`4／6／6`), five control questions, three Loop scopes, Harness／Loop／Graph overlap, six visible required-reading URLs, 20 resource URLs, four accessible resource rowgroups (`4／6／5／5`), 20 editorial ratings, seven closed disclosures, six real example directories, the four ordered core commands, two optional entrances without mainline commands, the matching Docker entry sentence, quiet `2026-08-31 UTC` verification date, current canonical project owners, and the absence of frozen SOTA scores, stale redirects, GitHub star counts, old “project teaching term” labels, or empty-quote artifacts. It verifies three distinct `1672×941` Image 2.0 control-question PNGs plus three localized Workflow Graph PNGs and rejects untranslated CJK in the English page.

`scripts/test_agent_engineering_route.py` locks Stage 3 as the Agent Loop entry, Stage 4 as the Workflow Graph／Agent Framework entry, and Stage 7 as the Agent Production Engineering chapter that integrates Harness, Loop, and Graph. It also locks the glossary boundary: Loop Engineering can happen in one long run or across sessions, Graph means an execution／workflow graph rather than GraphRAG, and the responsibility names are not misrepresented as one formal cross-vendor standard. The glossary must keep the course order separate from the five overlapping control questions and must not fall back to either the old Harness-only or Loop／Graph-only Stage 7 label.

`scripts/check-reader-ux.py` ratchets each locale's visible mainline with a narrow measured ceiling, requires at least six visible required-reading links plus 20 visible resource links and ratings, and locks all 16 core-term definitions before Core Exercise 1. `scripts/check-image-locale.py` ensures the English and Simplified Chinese pages use their own bright image variants. The three control-question PNGs separate one Agent run from the whole long-running task: Prompt／Context enter Harness, the Agent Loop stays inside Harness, Loop Engineering owns Goal／Action／Observation／Adjustment plus stop rules, and Workflow Graph connects Harness, fixed checks, and human approval. The separate localized Workflow Graph diagrams deepen nodes, branches, checkpoints, and return routes without claiming that every node is an Agent.

The example-hardening layer keeps six folders separate and uses `scripts/test_stage07_examples.py`. It locks 18 trilingual READMEs, each model-backed folder's rated `hello-agents` route to chapter-length material, five current-major requirements files, `qwen3.5:4b`, the pinned `claude-haiku-4-5-20251001` ID, PowerShell-first isolated setup, closed disclosures, ordered URL／price parity, and the absence of old fixed cost／latency／cache claims. The sixth folder is a no-model safe-execution exercise with checkpoint, approval, ledger reconciliation, recovery, and fail-closed tests. The shared examples guide and three setup guides separately keep `qwen2.5:3b`／`llama3.2:3b` for Stage 3–6 function-calling exercises and `qwen3.5:4b` for Stage 7 production mechanics, so “Stage 3+” cannot silently choose two defaults or preserve `$0/run` wording outside the example folders.

All 11 directly executable offline entrypoints pass in a clean `python:3.11-slim` container with the resolved current packages. Their behavior tests cover empty and whitespace-only output rejection, exact Debate／Eval Judge contracts, sanitized exception categories that do not retain a secret-bearing raw message, provider usage recording, a cache demo deliberately above Haiku 4.5's 4,096-token minimum, checkpoint／ledger disagreement, late rejection after a recorded side effect, FastAPI input bounds, secret-marker log regressions, and 200／422／429／502／503 behavior. Debate role separation is an example shape, not evidence that more agents reduce bias or improve correctness. The deploy image also builds from scratch, runs as UID `10001` (`appuser`), and returns `{"status":"ok"}` while mounted read-only with a temporary `/tmp` and a loopback-only host port. These checks do not call a live model, prove output quality, or turn the container into a sandbox.

### Stage 7.5 — progressive reading map covered; no example layer

Stage 7.5 keeps six bold core terms, all 12 advanced concepts grouped by problem, a five-branch choice map, a directly copyable four-line work-boundary card, a visible Model–Harness Fit keep／simplify／remove decision, five priority readings, the complete 24-entry rated resource table, and a short self-check visible. Eight closed disclosures hold prerequisites, source limits, failure cases, cross-vendor and coding harness detail, benchmark discipline, Dynamic Workflows, and Model–Harness Fit evidence／Bitter Lesson／human division.

`scripts/test_stage075_content.py` locks the three locales to 12 concepts in the same order, the visible evidence-based Model–Harness Fit table, four concept rowgroups (`3／3／3／3`), 24 visible resource URL/rating pairs, five resource rowgroups (`5／5／5／5／4`), one matching freshness marker, eight closed disclosures, and the legacy Dynamic Workflows anchors. A nesting-depth regression requires the resource heading, table, every URL, and document end to remain outside `<details>`. It also rejects the old Replit/Voyager years, fixed context/code-size/throughput claims, empty-quote artifacts, untranslated English fragments, and current-status drift for AutoGen, Microsoft Agent Framework, Sandbox Agents, and Dynamic Workflows.

Nine distinct locale PNGs cover the four problem groups, the five-branch reading decision, and the parallel keep／simplify／remove Model–Harness Fit decision. The test requires nine distinct hashes and exact locale references; `scripts/check-image-locale.py` provides the whole-repository mirror check. `scripts/check-reader-ux.py` ratchets the progressive mainline, keeps all six core terms before the work-boundary card, and counts the visible resource table instead of hiding it from the reading budget. Stage 7.5 is a reading-map, so there is deliberately no runnable example-hardening layer.

### Stage 8 — interface choice and safety map covered

Stage 8 keeps eight bold core terms, the four parallel interface choices, four safety checks,
two immediately copyable first actions, all four exercise titles and outcomes, five featured entries,
the complete 21-entry rated resource table, and a short self-check visible. Nine closed disclosures
hold current Computer Use contracts, OSWorld benchmark discipline, Browser Use signals, Sandbox
terminology, Track A／B depth, security cases, and future interfaces. The four choice
cards are alternatives chosen by task need; the test rejects wording that turns them into a ladder.

`scripts/test_stage08_content.py` locks the three locales to the same eight terms, nine closed
disclosures, 21 visible resource URL/rating pairs, five accessible rowgroups (`5／5／4／5／2`), one matching
freshness marker, all legacy H2／H3 anchors, safe `example.com` exercises, current tool and license
facts, and identical official-source order. It rejects the old Computer Use preview contract,
unsupported model rankings, volatile GitHub stars, fixed line/startup claims, blanket Gemini
availability, OmniParser Apache claims, unsafe credential tasks, and empty-quote artifacts. The test
also executes the copyable policy example: only explicit low-impact actions over HTTPS to the exact
allowlisted host pass; mixed-case high-impact actions ask, while unknown actions, userinfo, non-HTTPS
schemes, and look-alike hosts fail closed. Resource checks require Cloudflare Sandbox SDK to remain
labelled Beta with APIs that may change before v1.0, so a live repository cannot be mistaken for a stable product.
A nesting-depth regression requires the resource heading, check date, table, every URL, and document end
to remain outside `<details>`.

Six locale-specific PNGs cover interface selection and the four safety checks. The test requires
readable dimensions, six distinct hashes, and exact locale references; `scripts/check-image-locale.py`
provides the whole-repository mirror check. `scripts/check-reader-ux.py` locks the progressive mainline,
including the visible resource table, at `8,931／12,471／9,016` non-whitespace characters with only a
50-character allowance per locale,
and requires all eight core terms before Exercise 1. The freshness gate separately enforces
the 90-day fact pack for Computer Use, Browser Use, sandboxes, availability, benchmarks, and security.

### Role paths — progressive entry, current identities, and safe first tasks

All five enrolled role paths keep the next safe action visible before optional detail. The researcher
path starts with eight evidence terms and a public-paper citation check. The developer path starts
with eight coding-safety terms and a copyable
`read-only plan → small change → diff → test → human approval → rollback` exercise that explicitly
withholds push, merge, and deploy authority. The teacher path starts with eight teaching terms, five
safety lines, and a fictional lesson-review task. The knowledge-worker path starts with nine terms
and a fictional meeting-to-action table. The everyday-user path starts with nine terms and a
fictional draft that separates copied facts from details that still need confirmation.

The current structural contract is:

| Path | Core terms | Closed disclosures | Rated resources | Accessible rowgroups |
|---|---:|---:|---:|---|
| Researcher | 8 | 3 | 15 | `3／4／5／2／1` |
| Developer | 8 | 3 | 14 | `4／6／2／2` |
| Teacher | 8 | 5 | 12 | `3／3／3／3` |
| Knowledge worker | 9 | 3 | 15 | `4／4／2／3／2` |
| Everyday user | 9 | 3 | 15 | `4／4／4／2／1` |

`scripts/test_role_paths.py` compares the five role paths and three locales structurally rather than by keyword count.
It locks each resource row's identity, surface, status, license or service type, safety limitation,
URL, and rating; the five rowgroup shapes and disclosure counts in the table above; freshness
markers; copy-block steps; and semantic legacy-anchor landings. A mutation
test proves that a row cannot borrow a surface or safety fact from the row above it. It also
rejects volatile GitHub stars, maintainer self-promotion, fixed line-count safety rules, current use
of archived `open_deep_research` or Roo Code, and the old NotebookLM name without Gemini Notebook.
Developer checks keep core identity separate from multi-valued surface: Cursor, Cline, and Continue
remain coding-agent products even when they expose IDE, CLI, cloud, SDK, or CI surfaces; OpenRouter
remains a router and Ollama remains a local model runtime.

The everyday-user contract removes the old Tier upgrade ladder and locks four job-based doors:
Chat surface, App／Connector, CLI Agent, and Local LLM／Runtime. It requires nine bold terms before
a fictional copyable exercise, six visible official readings, three closed disclosures, and a
15-row rated resource table with `4／4／4／2／1` accessible rowgroups. It rejects volatile stars and
setup times, unsupported product rankings, stale prompt links, high-risk medical／legal／financial
starter workflows, and blanket local-privacy claims. Ollama cloud models and LM Studio cloud
features must remain distinct from local execution; write actions and CLI mutations keep an
Approval Gate and human confirmation.

This gate covers the researcher, developer, teacher, knowledge-worker, and everyday-user pages
enrolled in `scripts/reader-ux-pages.yml`, across all three locales. Package and repository
identifiers keep their published names. Cookbook, glossary, README, and other site-wide surfaces
have separate contracts and release layers; passing the role-path gate does not claim those surfaces
are already migrated.

### Public resource entry and MCP／Skills catalog

`scripts/test_public_entry_resources.py` covers `RESOURCES`, the resource index, and the MCP／Skills
catalog in all three locales. It keeps the task choices, core definitions, safe starts, and curated
resources visible; requires all 16 highlight links and ratings to remain outside closed disclosures,
and verifies the accessible `4／3／4／4／1` rowgroups;
requires current Notion, Google Workspace, GitHub, Atlassian, Linear, Slack, Canva, MCP Registry,
reference-server, and Anthropic Skills entry points; and rejects the replaced Linear and Slack
community defaults. A per-locale fact matrix locks Developer Preview, dedicated product servers,
OAuth 2.0／2.1, least-privilege tokens, Streamable HTTP, read-only options, signed-in-user permissions,
and human approval instead of checking URLs and ratings alone. The resource index mirrors canonical,
official-source, unknown-value, rating, and next-step rules across all three locales. Gemini Notebook
is the display name unless NotebookLM is part of an exact package, URL, or historical identifier.

The catalog contract requires 17 visible category landings, 17 closed disclosures, zero default-open
disclosures, and matching entry URL／editorial-rating order across all locales. It rejects volatile
GitHub stars, advertised catalog totals, popularity rankings, fixed integration or context counts,
stale last-commit claims, free-plan promises, and permanent model job assignments. Targeted semantic
assertions keep least privilege, source-version checks, bounded delegation, financial disclaimers, and
human review of freshness warnings in every locale. `scripts/check-catalog-counts.py` may report the
machine count but blocks reader-facing totals and per-category count labels. Its repository-wide
scan also rejects `NN+` and approximate project／resource／integration totals, exact use-case category
counts, and stale Stage 7／8 route claims in current READMEs, site cards, outreach copy, and repository
contracts. Outreach additionally rejects cached stars, stargazers, forks, clone counts, views, visitors,
and other traffic snapshots through the same shared gate functions used by the file-level regression;
changelog history, implementation plans, and test fixtures remain evidence rather than current advertising.

Repository health is a separate fact layer. `Required / pr-gate` checks changed lines on PRs, while
`content-health.yml` performs a scheduled full scan of every unique GitHub repository. It records canonical owner,
redirect, archive／disabled status, license metadata, release and push signals. Hard contradictions can
block; missing release metadata or older activity remains a human-review warning and never deletes an
entry automatically. The ordinary URL checker continues to cover non-GitHub documentation and hosted
service links.

### Setup guide — choose one door and finish one result

`resources/setup-guide*` keeps the five parallel entry choices, seven bold core terms, five rated
required starting points, A–E headings, first actions, safety rules, completion check, and locale-correct
next routes visible. Seven closed disclosures hold time and prerequisites, the full product catalog,
Provider alternatives, platform-specific installation fallbacks, troubleshooting, `CLAUDE.md`, and the
complete Skill example. The three HTML tables use accessible rowgroups `4／4／5／7`, `2／1／1／1`, and
`7／1`; required reading remains visible even though the complete catalogs are secondary.

`scripts/test_setup_guide_content.py` locks the exact freshness marker, external URL order, native Claude
Code installers, Python 3.12／`uv`, `claude-sonnet-5`, copyable secret setup, real rowgroups, editorial
ratings, and README routing. It rejects the old Node 18／npm-first path, fixed setup times, frozen prices,
promotional credits, stale desktop availability, volatile GitHub stars, and empty-quote artifacts.
Reader UX, strict anchors, mirror／locale checks, freshness, and the trilingual site build run beside it.

### Resource hub index — task-first navigation covered

`resources/README*` is a router, not another long catalog. Its visible path now asks what the
learner is stuck on, defines five resource types in bold plain language, shows all 11 maintained
reference files, points back to Stage 0／Track A1／Stage 3, and ends with a 30-second check. The
complete reference table stays visible because it is the page's navigation. Only the explanation
of why the files stay separate and the maintainer rules are in two closed disclosures.

`scripts/test_resource_index_content.py` locks the 11-file inventory, task-router links, five
core labels, five accessible rowgroups (`4／2／2／2／1`), two closed disclosures, three-locale file
coverage, and the absence of stale approximate line counts, the former seven-file claim, and the
old NotebookLM product name. `scripts/check-reader-ux.py` enrolls this page group, keeps all five
definitions before the visible table, and ratchets each locale to its measured
mainline plus only 50 non-whitespace characters.

### Course map — learn first, certificate second

`resources/courses*` keeps five bold credential terms, a task-first chooser, 12 rated courses, a
copyable five-line work-evidence card, and visible return links to Stages 3／4／7. The two disclosures
hold only certificate caveats and maintainer rules. The main table uses four accessible rowgroups
(`3／5／2／2`); each course row has one primary URL, while the Datawhale companion stays outside the
table so category and rating semantics remain unambiguous.

`scripts/test_courses_content.py` locks the 12 URL／rating pairs, full 22-link order, exact freshness
marker, closed disclosure count, portfolio card, locale-correct stage links, and current facts such
as the Hugging Face 80% Unit 1 threshold, Microsoft／Datawhale no-certificate status, DeepLearning.AI
Pro boundary, W&B's unstated public certificate rule, Claude quiz badge, and Alibaba identity
condition. It rejects the former tier labels, Skilljar entrance, Edureka／Huawei rows, frozen prices,
volatile stars, empty-quote artifacts, and generic verification-date filler. The freshness config
separately enrolls course availability, cost, certificate, assessment, and repository status on a
90-day review cycle.

### Glossary — visible definitions and stable facts

`scripts/test_glossary_content.py` keeps all 71 term headings and their shortest definitions visible,
including the legacy Subagent deep-link target. It locks a 12-term quick map, the five-way distinction
among Provider API／Router／Model Runtime／Coding Agent or Harness／Agent Framework, exactly two closed
maintainer disclosures, and the accessible terminology rowgroups `2／17／9／5／4`. The three locales
must use the same external URLs and freshness marker.

The glossary rejects fixed token conversions, frozen frontier-model rosters, stale A2A organization
counts, a fixed Claude Hook event count, and a replacement ladder that says Context Engineering
supersedes Prompt Engineering. Volatile prices, model context, availability, and protocol status route
to a freshness-gated chapter or first-party source instead of being copied into a timeless definition.
`scripts/check-reader-ux.py`, strict anchors, mirror checks, locale-link checks, and the freshness gate
run beside the dedicated content test.

### Whole-site learner-route coherence

`scripts/test_site_route_coherence.py` treats text navigation as the source of truth before diagrams
are redrawn. It locks Track A to `A1 → A2 → Stage 5 → A3 → Stage 8`, requires A2 to hand off to
Stage 5, requires Stage 5 to split Track A toward A3 and Track B toward Stage 6, and requires A3 to
list the Track A core of Stage 5 as a prerequisite. It also keeps Stage 8 recommended for Track A
without making it a Capstone entry requirement, and rejects completed or stale ROADMAP gap claims
in any locale.

## v2 path (deferred)

The project-wide learner workflow is: run the provided starter first, change exactly one small thing, rerun the existing test command(s), and undo or fix that one change if the tests fail. Learner-facing exercise READMEs must not instruct renaming files or rewriting the whole solution. Keep the current runnable starter and test files as the maintained examples.

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
