# Capstone

> [繁體中文](./CAPSTONE.md) | [简体中文](./CAPSTONE.zh-Hans.md) | **English**

After finishing a track, **build something yourself** — this file is not a tutorial, not a walkthrough, and there is no model answer. Its purpose is to turn "I read the roadmap" into "I have something I can show + a grade I gave myself."

**How to use this file**:

1. Pick **a problem you actually have** (work, research, daily life). Don't pick a toy problem — a capstone's value comes from being real.
2. Check your track's "Prerequisites" and confirm the required stages have each passed their "Self-check".
3. When done, **self-assess with the matching rubric** (4 levels: Not yet / Basic / Good / Excellent). Scoring honestly is more useful than scoring high.
4. Want feedback? Post the artifact + your self-assessment to [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions) for peer review (optional, not required).

> What each stage teaches / what you need before it / how you know you've learned it — all of that stays with the stage file's "Learning objectives / Prerequisites / Self-check". This file only defines the **capstone** itself.

---

## Track A Capstone — CLI Power User

**Prerequisites:** Stage 0–2 + A1 + A2 + Stage 5's Track A core 5.1–5.4 + A3 have each passed their self-check. Stage 5 sections 5.5–5.8 do not block entry. Stage 8 is recommended, but it does not block Capstone entry either; the Track A Capstone focuses on the CLI workflow.

**Brief**: Assemble a CLI-agent workflow **you will reuse**, automating something you currently do by hand.

**Requirements** (all mandatory):

- A CLI agent (Claude Code or equivalent) at the core
- At least **1** MCP server **or** a skill / command you wrote yourself
- A clear input → a usable artifact out (not "chatting with it")
- **Reproducible by someone else**: include `how to run` (install, configure, run, expected output)
- Handles at least **1 failure case** (missing input, API failure, what happens when the result is wrong)

**Deliverables**: a folder / repo with the artifact + `README` + evidence of at least one real run (log / screenshot / output file) + a reflection under 150 words (where you got stuck, what you'd change next time).

**Time**: 3–8 hours (not counting time spent learning the stages).

### Track A scoring rubric (self-assessed, 4 levels)

| Dimension | Not yet | Basic | Good | Excellent |
|---|---|---|---|---|
| Problem realism | Toy problem | Somewhat useful | Real, will reuse | Real, with a quantifiable metric (time saved / fewer errors etc.) |
| Tool use | Plain chat only | Used a CLI agent | + MCP or self-written skill/command | Multi-component, with justified choices |
| Reproducibility | Only runs for you | Steps incomplete | Others can run it from the README | One-click / fully automated with pre-checks |
| Robustness | Crashes on any error | Risks mentioned | Handles 1 failure | Multiple failures have fallbacks |
| Docs & reflection | None | Has a README | Clear README + reflection | Reflection points to a concrete next improvement |

---

## Track B Capstone — Agent Builder

**Prerequisites**: Stage 0–8 (including Stage 3, 4, 5, 6, 7, 7.5, 8) have each passed their self-check.

**Brief**: Design, build, and **evaluate** a small system that solves a concrete problem. Pick one:

- **A. Multi-agent**: ≥ 2 cooperating agents with orchestration logic; or
- **B. RAG system**: a complete retrieval + generation pipeline.

**Requirements** (all mandatory):

- Has tool use
- Has one outward interface (CLI / API / chat — any one, mapping to Stage 8)
- **Has explicit evaluation**: version an Eval suite with at least 5 development cases + 3 frozen holdout cases; define success criteria, grader, trial count, and baseline, then report quantitative and qualitative results
- **Failure-mode analysis**: write down under what conditions it breaks and how you'd know
- An architecture sketch (a diagram or a paragraph describing components and data flow)

**Deliverables**: a code repo + architecture description + Eval report (dataset version, development/holdout split, per-case results, trial count, baseline, and regression) + `README` + a reflection under 200 words.

**Time**: 8–20 hours (not counting time spent learning the stages).

### Track B scoring rubric (self-assessed, 4 levels)

| Dimension | Not yet | Basic | Good | Excellent |
|---|---|---|---|---|
| Problem definition | Vague | Has a goal | Clear scope, acceptance-checkable | Clear, and states why it's worth doing |
| Architecture | No design | Just runs | Justified multi-agent / RAG choice | Can articulate the trade-offs |
| Implementation correctness | Doesn't run | Main path runs | Handles edge cases | Stable and the code is readable |
| **Evaluation rigor** | Not tested | Tried it a few times by hand | Versioned development/holdout cases, success criteria, and grader | Multiple trials, baseline comparison, rerunnable regression, and no holdout tuning |
| Robustness & failure analysis | None | Risks mentioned | Concrete failure modes | Failures are detected + mitigated |
| Interface & docs | None | Runs | Interface + clear README | Others can use it directly |
| Reflection | None | One sentence | Concrete (names a specific problem in the architecture or component choice) | Points to an architecture-level next step |

---

## Pick a brief by role (audience flavor)

Same capstone — just swap in your scenario; no need to do a separate one:

- 🔬 **researcher**: literature Q&A / experiment-log organization / data-preprocessing agent
- 💻 **developer**: a review/triage agent inside CI / repo Q&A / automated release notes
- 🎓 **teacher**: question generation + grading support / material rewriting / course Q&A (mind the academic-integrity boundary)
- 📊 **knowledge-worker**: meeting notes → action items / cross-document synthesis / first-draft weekly report
- 👥 **everyday-user**: personal-data consolidation / scheduling and reminders / repetitive-chore automation

---

## How to show your work

- Post to the matching [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions) category with a link to the artifact + your rubric self-assessment.
- Put it in your own portfolio / GitHub; describe it with concrete facts (what you did, what you measured), and **avoid** hype like "the strongest / the best in the world".
- Want to review someone else's: give feedback against that person's track rubric — about the work, not the person.

> This file only defines the capstone and its scoring. Each stage's learning content and pass conditions stay with that stage's file.
