# Extension Path: For Researchers

> [繁體中文](./for-researcher.md) | [简体中文](./for-researcher.zh-Hans.md) | **English**

> 🚀 **Computational researchers** (can run Python scripts, have an API key, and can use git) can jump into the advanced path directly. **Non-programming researchers** (humanities/social sciences, clinical research, literature-first work) can start with literature Q&A (NotebookLM) and Zotero AI tools, then read [`resources/setup-guide.en.md` A-C](../resources/setup-guide.en.md) when needed.

> [← Back to main path README](../README.en.md) · Continue here after **Track A's A3** or **Track B's Stage 7**. Apply agentic AI to research workflows.

## Use Cases

Research days break into stages, and AI plays a different role at each stage. Use this table to orient yourself:

| Stage | Common pain point | How AI helps | Recommended tools (light to heavy) |
|---|---|---|---|
| **Literature exploration** | You do not know the classic papers in a field | Recommendations + summaries + comparison | NotebookLM → paper-qa → gpt-researcher |
| **Close reading** | You lose the thread halfway through a PDF / miss the claim | Extract claims, figures, citations, and notes | Zotero + zotero-gpt → zotero-skills |
| **Research design** | The RQ is fuzzy, or the method choice is unclear | Clarifying dialogue and trade-off mapping | Claude.ai chat → ai-research-skills |
| **Experiments / coding** | Boilerplate repeats and plotting eats time | Write / edit code and batch refactor | Claude Code → codex-delegate |
| **Manuscript writing** | Drafts stall or sentences do not land | Outline → paragraphs → polishing | Claude.ai → Gemini CLI (long drafts) |
| **Revision / submission** | Journal requirements are easy to miss | banned-word / figure-text / submission checklist | academic-writing-skills |
| **Cross-paper synthesis** | Five papers need to talk to each other and context explodes | Read 1M tokens at once and organize the synthesis | Gemini CLI |

> 💡 **Computational vs non-programming researchers**: the recommended tools run from light to heavy. Non-programming researchers can usually stop at the **first** tool in each row; computational researchers should move right only when they need automation.

## Curated Projects

> 💡 **Want to wire Claude Code into NotebookLM, Obsidian, Notion, Excel, PDF, Excalidraw, and other research tools?** 81+ integrations in [`resources/mcp-skills-catalog.en.md`](../resources/mcp-skills-catalog.en.md) (grouped by use case). The section below keeps research-specific tools and marketplaces.

### Research Workflow Marketplaces

#### [flonat/flonat-research](https://github.com/flonat/flonat-research) ⭐⭐⭐

Claude Code infrastructure for PhD researchers — skills, agents, hooks, rules for academic workflows. Strong LaTeX/bibliography focus.

---

### Literature RAG / Q&A

#### [Future-House/paper-qa](https://github.com/Future-House/paper-qa) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 8.9k+ |
| License | Apache-2.0 |

**What it teaches**: PDF Q&A designed for **citation-grounded Q&A** — every answer includes sentence-level citations to reduce hallucination risk. Actual accuracy depends on document type; use the official benchmarks / papers as the reference.

**Best for**: Researchers writing literature reviews who need "every answer must be traceable to its source." More rigorous than generic RAG.

---

#### [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 28k+ |
| License | Apache-2.0 |

**What it teaches**: Autonomous deep-research agent — planner + multi-source crawl + report synthesis. Give it a research topic, get a markdown / PDF brief out.

**Best for**: Researchers who need to quickly scope new topics and produce research briefs.

---

### Outline & Writing

#### [stanford-oval/storm](https://github.com/stanford-oval/storm) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 30k+ |
| License | MIT |

**What it teaches**: Multi-perspective outline-then-write pipeline — plain-language version: (1) simulate different perspectives asking questions, (2) organize those questions into an outline, then (3) generate a Wikipedia-style draft. From Stanford OVAL.

**Best for**: Learning **outline-driven writing**. Great for producing topic briefs from scratch; the closest open-source analog to NotebookLM's structured report flow.

**Notes**: Last push was over 6 months ago — verify the latest commit date before relying on it.

---

#### [kaixindelele/ChatPaper](https://github.com/kaixindelele/ChatPaper) ⭐⭐⭐⭐⭐ (Chinese readers)

| Field | Value |
|---|---|
| Language | Chinese + Python |
| Stars | ★ 19k+ |
| License | NOASSERTION (custom non-commercial) |

**What it teaches**: Full arXiv workflow for Chinese researchers — paper summary + translation + polishing + review-response generation. Maintained by a Chinese team; defaults are friendly to Chinese-language workflows.

**Best for**: Chinese graduate students looking for a Chinese-friendly entry-level paper workflow tool.

**Notes**: License is custom non-commercial — read the original terms before any use; common practice is research / personal use, but you should verify the terms yourself.

---

### Citation Manager Integrations

#### [MuiseDestiny/zotero-gpt](https://github.com/MuiseDestiny/zotero-gpt) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 7k+ |
| License | AGPL-3.0 |

**What it teaches**: A Zotero LLM plugin — chat with your library, summarize selections, generate inline notes.

**Best for**: Heavy Zotero users who want AI inside their reading workflow without switching tools.

**Notes**: AGPL-3.0 license (copyleft) — derivative products that ship modifications must follow the terms.

---

### Multi-LLM Research Stack (Maintainer Setup)

Some research tasks only need Claude (dialogue, design, review). Others waste Claude tokens (large code refactors, long-form drafts). The maintainer's actual setup is **Claude as planner / reviewer, Codex for code, and Gemini for long drafts**. Use this table to decide which model to use when:

| Task type | Example | LLM to use | Why |
|---|---|---|---|
| Research design / hypothesis discussion | "Should this RQ use logistic vs survival?" | Claude.ai chat | Collaborative dialogue and context memory |
| Writing / editing code | "Add logging to 50 simulation scripts" | codex-delegate | Fast mechanical edits without burning Claude tokens |
| Long-form drafting (Chinese / English) | "Draft an 8-page paper section" | Gemini CLI | 1M context and strong long-form prose |
| Second opinion | "Ask Gemini to review my discussion section" | Gemini CLI | LLM-vs-LLM comparison makes Claude's own biases easier to spot |
| Pre-submission audit | "Run banned-word + figure-text checklist" | academic-writing-skills | Structured audit instead of ad hoc LLM judgment |

#### Maintainer's 6 self-used research skills

> ⚠️ **Disclosure**: The following 6 tools are research skills used day to day by the maintainer [@WenyuChiou](https://github.com/WenyuChiou) (Lehigh CEE PhD candidate) and published for people with similar needs. **They have not been independently evaluated by third parties**. Best fit: PhD dissertation writing and cross-paper literature organization. They may not fit your field. Full entries are in [`resources/mcp-skills-catalog.en.md` 13 + 14](../resources/mcp-skills-catalog.en.md#13-research-workflow-skills-academic--paper--lit).

| Tool | Best for stage | One-liner |
|---|---|---|
| **[ai-research-skills](https://github.com/WenyuChiou/ai-research-skills)** ⭐⭐⭐⭐⭐ | Full pipeline | 14 research skills packaged as a 5-plugin marketplace; one command installs the set |
| **[research-hub](https://github.com/WenyuChiou/research-hub)** ⭐⭐⭐⭐ | Literature organization | Zotero + Obsidian + NotebookLM workspace with CLI / MCP / REST / dashboard interfaces |
| **[zotero-skills](https://github.com/WenyuChiou/zotero-skills)** ⭐⭐⭐⭐ | Reference management | Zotero CLI skill for search / add / classify / tag; complements zotero-gpt, which chats inside Zotero while this operates from outside |
| **[academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills)** ⭐⭐⭐ | Pre-submission | banned-word audit, figure-text coupling, and submission checklist; per-paper journal_format / style_overrides customization |
| **[codex-delegate](https://github.com/WenyuChiou/codex-delegate)** ⭐⭐⭐⭐⭐ | Coding | Standard Claude planner + Codex executor skill for batch refactor / boilerplate / migration work |
| **[gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill)** ⭐⭐⭐ (⚠️ archived) | Long drafts / synthesis | Claude planner + Gemini for 1M-context long-form writing / CJK / second opinions. **⚠️ Repo archived 2026-07** — the workflow still works directly via [Gemini CLI](https://github.com/google-gemini/gemini-cli) |

---

### Multi-Agent for Research

#### [langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research) ⭐⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 12k+ |
| License | MIT |

**What it teaches**: Open-source Deep Research — supports both single-agent and supervisor + multi-researcher architectures (the multi-agent path currently lives in `src/legacy/`), parallel search, citation-grounded report synthesis. A solid reference for "LLM agent that auto-produces a cited brief."

**Best for**: Researchers building "agent auto-generates a cited brief" workflows. A solid open-source pick when you want a maintained reference implementation.

**Notes**: Depends on LangGraph + search tools (API key required).

---

#### [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Stars | ★ 6.9k+ |
| License | The AI Scientist Source Code License (source-available, non-commercial + manuscript-disclosure clause) |

**What it teaches**: End-to-end multi-agent science loop: ideate → code → experiment → write → peer-review. Sakana AI's research implementation of "AI writes a full ML paper."

**Best for**: Researchers who want to see "what does a swarm of agents running a full research lifecycle look like." Architecture reference, not a production tool.

**Notes**: Outputs are demo-level (not field-ready), ML/CS-domain bias. License is a custom source-available term (with a manuscript-disclosure clause) — read the LICENSE file before use.

---

> Still missing: actively-maintained peer-review automation, conference-review pipelines. If you've built or know of one, please open a PR.

## Required Reading

1. [The Effortless Academic — Claude Code beginner guides](https://effortlessacademic.com/claude-code-and-cowork-for-academics-beginner-guide-part-1/)
2. [Pedro Sant'Anna — Researcher setup guide](https://paulgp.substack.com/p/getting-started-with-claude-code)

## Workflows to Master

The biggest mistake researchers make with AI is opening ChatGPT only when they get stuck. The key is making AI a daily tool by setting a cadence. The 7 workflows below are ordered by usage frequency and are routines the maintainer actually runs, not hypotheticals.

| Frequency | Workflow | How to run it (≤ 3 steps) | Recommended tools | Best for |
|---|---|---|---|---|
| **Daily** | Literature inbox triage | (1) Put yesterday's papers into paper-qa<br>(2) Extract claims + a 4-5 line summary<br>(3) Move notes into Zotero / Obsidian | paper-qa + zotero-gpt | All researchers |
| **Daily** | Writing sprint (25 min) | (1) Give one paragraph to Claude.ai<br>(2) Run banned-word + figure-text audit<br>(3) Merge the revision into the main draft | Claude.ai + academic-writing-skills | Paper-writing stage |
| **Weekly** | Cross-paper synthesis | (1) Feed 5-10 PDFs to Gemini<br>(2) Ask where the papers disagree<br>(3) Turn the answer into a 1-page brief | Gemini CLI (1M context) | Computational researchers |
| **Weekly** | Zotero cleanup | (1) Mark unread / read<br>(2) Retag items<br>(3) Pull out PDFs that should be archived | zotero-skills or zotero-gpt | All researchers |
| **Monthly** | Research progress brief | (1) Pull recent notes from Obsidian + Zotero + NotebookLM<br>(2) Summarize 5 progress points<br>(3) Send to your advisor | research-hub | People using all 3 tools |
| **Per paper** | Final pre-submission audit | (1) banned-word audit<br>(2) figure-text coupling check<br>(3) submission checklist | academic-writing-skills | Final week before submission |
| **Per paper** | Multi-agent peer review | (1) Claude reviews logic / argument<br>(2) Codex checks code / table numbers<br>(3) Gemini reviews prose / clarity | codex-delegate + Gemini CLI | Pre-submission second opinion |

> 💡 **Starter playbook**: run the daily inbox triage and writing sprint for one month first. Add advanced workflows only after the habit sticks.

## Tier Recommendations

Researchers do not need to install Claude Code on day one. This is the recommended progression:

| Tier | Tools | Best for | Learning cost |
|---|---|---|---|
| **Tier 0** | Claude.ai web + NotebookLM | Non-programming researchers, humanities / social sciences, clinical research | 0 (browser skills are enough) |
| **Tier 1** | Claude Desktop + Zotero MCP / Obsidian MCP | Researchers already using Zotero / Obsidian | Half-day setup |
| **Tier 2** | Claude Code + ai-research-skills | Computational researchers who mostly write / edit code | 1-2 days to get started |
| **Tier 3** | Claude Code + codex-delegate + Gemini CLI + research-hub | People building a multi-LLM research pipeline across multiple tools | 1 week setup + ongoing tuning |

**Most researchers can stop at Tier 1-2**. Tier 3 is worth it only when you have a lot of repeated workflows, such as running the same paper synthesis every week.
