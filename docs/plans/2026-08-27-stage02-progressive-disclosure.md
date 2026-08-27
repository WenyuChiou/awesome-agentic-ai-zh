# Stage 02 Progressive Disclosure Implementation Plan

> **For Codex:** Use `bounded-agent-harness`, write zh-TW first, verify the source pack, then use Luna or Terra only for bounded translation/mechanical work. The parent owns facts, semantic parity, review, commits, and PRs.

**Goal:** Turn Stage 02 into a short, modern prompt-design path where a beginner can write one useful prompt, test it on examples, improve it, and know when prompting is not the right tool.

**Architecture:** Keep three exercises and their outcomes visible. Collapse setup, cost, code, optional techniques, full resources, and troubleshooting. Ship the reader path first, then add one small runnable prompt-eval example in a dependent PR.

**Tech Stack:** Markdown, Python, Ollama through the OpenAI-compatible SDK, Anthropic SDK, mock-based tests, MkDocs, mdBook.

---

## 1. Confirmed defects in the current page

- The final reader-UX proxy counts 13,702 non-whitespace zh-TW characters on first load because all four default-open code paths are genuinely visible.
- Four long Path A code blocks are open by default.
- Required reading starts with a wall of links and has duplicate numbering (`3.` twice).
- The page repeats glossary links and introductory navigation text.
- It treats `Let's think step by step` as a central modern technique; current reasoning models often need different guidance.
- The legal-persona example asks the model to cite statutes and shows an unverified statute number, teaching hallucination-prone behavior.
- The JSON exercise catches `JSONDecodeError` and silently `pass`es, so invalid JSON can look successful.
- “Return JSON” is taught without clearly routing strict schemas to Structured Outputs/tool schemas.
- The project table mixes tutorials, cookbooks, frameworks, inspiration collections, and an archived library.
- Volatile star counts dominate the table even though they do not tell a beginner where to start.
- `microsoft/prompt-engine` is archived and should be historical, not a production recommendation.
- `f/awesome-chatgpt-prompts` now resolves to `f/prompts.chat`; its pattern collection is optional inspiration, not a core learning resource.
- There is no `examples/stage-2/` runnable example even though `ROADMAP.md` records this as a known gap.
- Stage 03's CoT definition and cross-link will become stale when Stage 02 is corrected.

## 2. Source pack and teaching decisions

Use official guidance in this order:

1. [Anthropic prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview): define success criteria and an empirical test before optimizing a prompt.
2. [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices): current guidance for clarity, examples, structure, thinking, and agentic systems.
3. [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering): message roles, Markdown/XML boundaries, few-shot examples, pinned model behavior, and evals.
4. [OpenAI evals](https://developers.openai.com/api/docs/guides/evals): test prompt behavior rather than trusting one successful output.
5. [Google prompt design strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies): clear instructions, consistent examples, prompt components, and model-specific caveats.

Teaching decisions:

- Main formula: **Goal → Data → Rules → Output**.
- Define an eval as “a small answer sheet that lets us check whether the prompt did what we asked.”
- Teach one change at a time: baseline, change one prompt element, rerun the same cases, compare.
- Few-shot remains core because current official sources still recommend examples for format and edge cases.
- Do not require hidden chain-of-thought. Ask for a final answer, a short justification, or externally verifiable work when needed.
- Explain that reasoning models and ordinary chat models can respond differently to the same prompt.
- Treat pasted documents and web text as **data**, not higher-priority instructions; route full prompt-injection security to Stage 08.
- For strict machine-readable output, route to Structured Outputs/tool schemas in Stage 03 instead of pretending prose alone guarantees valid JSON.

## 3. Target visible path

Without opening any menu, the reader sees:

1. One sentence: “This stage teaches you to say what you want, show what good looks like, and check the result.”
2. Four learning goals.
3. Four core terms with plain definition, one everyday analogy, and the correct term:
   - instruction / system or developer message;
   - input data;
   - example / few-shot;
   - eval.
4. The four-box prompt recipe: Goal → Data → Rules → Output.
5. Exercise 1: turn one vague request into a four-box prompt.
6. Exercise 2: add examples and test six fixed cases.
7. Exercise 3: change one thing, rerun the same cases, and record the score.
8. One recommended mini-project: a support-message classifier with a repeatable eval set.
9. A short self-check and the Stage 03 link.

Target: no more than 3,200 zh-TW characters under the final reader-UX source-level proxy.

## 4. Default-collapsed content

- Time, prerequisites, environment, and cost.
- Required reading and reading order.
- Ollama and Anthropic code for each exercise.
- Full resource table.
- Optional reasoning-model comparison.
- Optional safe prompt-injection demonstration.
- Structured-output explanation and Stage 03 route.
- Troubleshooting and model-specific notes.
- Prompt / context / harness layer comparison.

All exercise headings, anchors, one-sentence outcomes, and the first action remain outside `<details>`.

## 5. Exercises

### Exercise 1: Build a four-box prompt

**Visible task:** Rewrite “summarize this” as Goal, Data, Rules, and Output. Run the vague and structured versions on the same short passage.

**Success:** The learner can point to the four pieces and explain one visible difference in the outputs.

Do not use legal advice or fabricated citations. Use a low-risk support-message or meeting-note example.

### Exercise 2: Show examples and check six cases

**Visible task:** Classify six short support messages as `billing`, `bug`, or `other`. Compare zero-shot and three examples.

**Success:** Both versions run on the same six cases; the learner records the score and notices whether examples improved format or edge-case consistency.

Do not assert that few-shot must always improve accuracy.

### Exercise 3: Run the prompt-eval loop

**Visible task:** Pick one failed case, change exactly one prompt element, rerun all six cases, and write the before/after score.

**Success:** The learner has a tiny reproducible experiment, not a “this answer feels better” opinion.

### Optional Exercise 4: Reasoning-model comparison

Compare concise high-level guidance with explicit procedural guidance. Ask for a final answer plus a short checkable justification; do not ask the learner to expose or depend on private chain-of-thought.

### Optional Exercise 5: Data is not an instruction

Put a harmless conflicting sentence inside `<input_data>` and verify that the top-level task still wins. Explain that tags help organize data but are not a complete security boundary. Route production prompt-injection defenses to Stage 08.

## 6. Curated resources

Keep three visible starting points:

1. Anthropic interactive tutorial.
2. OpenAI prompt engineering guide.
3. Google prompt design strategies.

Place the full table in a collapsed section, with grouped accessible rows:

| Group | Resources | Count |
|---|---|---:|
| Official courses | `anthropics/prompt-eng-interactive-tutorial`, `anthropics/courses`, Anthropic docs, OpenAI docs, Google docs | 5 |
| Official cookbooks | `anthropics/claude-cookbooks`, `openai/openai-cookbook`, `google-gemini/cookbook`, `GoogleCloudPlatform/generative-ai` | 4 |
| Learn by examples | `dair-ai/Prompt-Engineering-Guide`, PromptingGuide.ai, `NirDiamant/Prompt_Engineering`, Hung-yi Lee's current course | 4 |
| Evaluate and optimize | `promptfoo/promptfoo`, `microsoft/promptflow`, `stanfordnlp/dspy`, `UKGovernmentBEIS/inspect_ai` | 4 |
| Historical only | `microsoft/prompt-engine` | 1 |

Total: 18 resources. Use five `<tbody>` groups with row spans `5 / 4 / 4 / 4 / 1`. Do not show GitHub star counts on the stage page.

Verified repository status on 2026-08-27 UTC:

- Active: Anthropic tutorial/courses/cookbooks, OpenAI cookbook, both Google cookbooks, DAIR guide, NirDiamant, Promptflow, DSPy, Promptfoo, Inspect AI.
- Archived: `microsoft/prompt-engine`.
- License must be copied from official repository metadata. If GitHub reports `NOASSERTION`, say “repository metadata does not declare an SPDX license”; do not infer non-commercial terms.

## 7. Short stacked PRs

### PR F0: Reader-UX contract

**Branch:** `codex/curriculum-reader-contract`

**Files:**

- Modify: `CLAUDE.md`
- Modify: `stages/DESIGN.md`
- Modify: `resources/style-guide.md`
- Modify: `resources/style-guide.en.md`
- Modify: `resources/style-guide.zh-Hans.md`
- Create: `scripts/check-reader-ux.py`
- Create: `scripts/test_reader_ux.py`
- Create: `scripts/reader-ux-pages.yml`
- Create: `scripts/requirements-reader-ux.txt`
- Modify: `.github/workflows/stage-template-check.yml`
- Modify: `scripts/README.md`
- Modify: `CHANGELOG.md`
- Add: `docs/plans/2026-08-27-curriculum-modernization-audit.md`
- Add: `docs/plans/2026-08-27-stage02-progressive-disclosure.md`
- Add: `docs/plans/2026-08-27-repository-freshness-gate.md`

**Purpose:** Resolve the unconditional Path A `open` rule and add a ratchet for migrated pages.

### PR F1: Repository freshness gate

**Branch:** `codex/repository-freshness-gate`, based on merged PR F0.

**Purpose:** Upgrade the existing advisory PR audit and scheduled link scan so every unique GitHub repository has machine-readable health evidence before Stage 02 adds or reclassifies learning resources. See [`2026-08-27-repository-freshness-gate.md`](./2026-08-27-repository-freshness-gate.md).

### PR 02A: Stage 02 reader path

**Branch:** `codex/stage02-reader-path`, based on merged PR F1.

**Files:**

- Modify: `stages/02-prompt-engineering.md`
- Modify: `stages/02-prompt-engineering.en.md`
- Modify: `stages/02-prompt-engineering.zh-Hans.md`
- Modify: `resources/glossary.md`
- Modify: `resources/glossary.en.md`
- Modify: `resources/glossary.zh-Hans.md`
- Modify: `stages/03-tool-use-and-hello-agent.md`
- Modify: `stages/03-tool-use-and-hello-agent.en.md`
- Modify: `stages/03-tool-use-and-hello-agent.zh-Hans.md`
- Modify: `CHANGELOG.md`

**Purpose:** Ship the modern beginner path, resources, and corrected CoT/reasoning definition.

### PR 02B: Runnable prompt-eval example

**Branch:** `codex/stage02-prompt-eval-example`, based on PR 02A.

**Files:**

- Create: `examples/stage-2/01-prompt-eval-loop/starter.py`
- Create: `examples/stage-2/01-prompt-eval-loop/starter_anthropic.py`
- Create: `examples/stage-2/01-prompt-eval-loop/test.py`
- Create: `examples/stage-2/01-prompt-eval-loop/test_anthropic.py`
- Create: `examples/stage-2/01-prompt-eval-loop/requirements.txt`
- Create: `examples/stage-2/01-prompt-eval-loop/README.md`
- Create: `examples/stage-2/01-prompt-eval-loop/README.en.md`
- Create: `examples/stage-2/01-prompt-eval-loop/README.zh-Hans.md`
- Modify: three Stage 02 pages with the example link
- Modify: `examples/README.md`
- Modify: `examples/README.en.md`
- Modify: `examples/README.zh-Hans.md`
- Modify: `ROADMAP.md`
- Modify: `ROADMAP.en.md`
- Modify: `ROADMAP.zh-Hans.md`
- Modify: `docs/TESTING_PLAN.md`
- Modify: `CHANGELOG.md`

**Purpose:** Close the known Stage 02 example gap without making the stage page long again.

## 8. Implementation tasks

### Task 1: Freeze facts and references

1. Record GitHub API UTC date.
2. Re-open all official prompting guidance.
3. Query repository metadata for all 18 resources.
4. Record redirects, archived flags, last push, and license.
5. Scan every inbound Stage 02 anchor and Stage 03 CoT reference.
6. Freeze the intended file list for PR F0.

### Task 2: Implement and test the reader-UX gate

1. Write failing unit tests for visible-character limits, forbidden open categories, visible anchors, and trilingual config.
2. Run `python scripts/test_reader_ux.py` and confirm failure.
3. Implement the minimum checker.
4. Add Stage 00 and Stage 01 as migrated baselines without changing their content.
5. Run the test and confirm pass.
6. Update the contributor contract and three style guides.
7. Run all existing doc gates.
8. Stage explicit files, review the final fingerprint, commit, open PR F0, and wait for main CI after merge.

### Task 3: Draft zh-TW Stage 02

1. Preserve existing public exercise headings and anchors when possible.
2. Write the visible path first.
3. Move long code, reading, cost, advanced concepts, and troubleshooting into closed details.
4. Replace the legal example.
5. Replace silent JSON success with a real failure or route to structured outputs.
6. Add the 18-resource grouped table.
7. Measure with `check-reader-ux.py` and keep the zh-TW proxy at or below 3,200.
8. Run strict anchors before translating.
9. Present zh-TW for user review.

### Task 4: Translate and mirror

1. Give Luna a bounded packet containing the approved zh-TW page, source glossary, exact URLs, anchors, table row order, and forbidden meaning changes.
2. Translate English and zh-Hans.
3. Independently compare every number, URL, model behavior statement, status, and security note.
4. Run Hans-character, locale-link, anchor-slug, and mirror gates.
5. Any semantic change returns to zh-TW first, then all mirrors.

### Task 5: Build the prompt-eval example

1. Write mock-based tests for both SDK response shapes.
2. Confirm the tests fail before implementation.
3. Implement a prompt builder, six fixed cases, scorer, and before/after report.
4. Provide a fixture mode that runs without credentials so every learner can see the eval loop.
5. Keep each starter near the repository's 70–150-line target.
6. Add explicit single-run and stage budget notes.
7. Add the deeper-learning callout required by `CLAUDE.md`.
8. Run both test suites and the fixture mode.
9. If Ollama is installed, run one live smoke test; label it non-deterministic and do not make CI depend on output quality.

### Task 6: Final review and merge each layer

For each PR:

1. Recheck official sources immediately before staging.
2. Run the standard gates and relevant example tests.
3. Stage explicit paths only.
4. Compare staged file count with the frozen list.
5. Record the staged fingerprint.
6. Invoke exactly one independent `code-reviewer`.
7. If anything changes, invalidate the acknowledgment and repeat the gate.
8. Commit without `--no-verify`.
9. Open the stacked PR against the previous branch.
10. Merge bottom-up only when checks are green and non-empty.
11. Verify main CI for the merged SHA before retargeting the next PR.

## 9. Acceptance criteria

- A reader can understand the chapter and start Exercise 1 without opening a menu.
- The final reader-UX proxy reports no more than 3,200 zh-TW characters.
- No Stage 02 `<details>` opens by default unless the approved reader-UX rule explicitly permits one short immediate-action block.
- Three core exercises remain visible by title, anchor, outcome, and first action.
- No exercise teaches fabricated legal citations.
- Invalid JSON cannot silently pass.
- CoT is not presented as a universal requirement for current reasoning models.
- The page teaches baseline → one change → same eval cases → compare.
- All 18 resources appear in the same order and group in all three languages.
- The archived Microsoft prompt-engine is historical only.
- Stage pages contain no volatile GitHub star counts.
- Stage 03 and the glossary use the same updated CoT/reasoning definition.
- The runnable example passes both mock suites and fixture mode.
- All existing repository gates and the new reader-UX gate pass.
- Reviewer acknowledgment matches the final staged fingerprint.

## 10. Deliberate non-goals

- Do not add OpenRouter, OpenCode, or Pi as Stage 02 teaching content; Stage 02 can mention only the generic difference between a model, provider, router, and harness if needed.
- Do not rewrite Stage 03 beyond the direct CoT/reasoning cross-reference.
- Do not redraw the main learning map in the Stage 02 stack.
- Do not turn this repository into a chapter-length prompt-engineering textbook; route readers to the 18 curated resources.
- Do not merge the two Stage 02 PRs into one large squash commit merely to save PR overhead.
