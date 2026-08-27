> [繁體中文](./style-guide.md) | [简体中文](./style-guide.zh-Hans.md) | **English**

# `awesome-agentic-ai-zh` Style Guide

This is the **single source of truth** for the catalog: terminology, entry schema, license notation, writing style, banned words.

Read this before opening a PR. Maintainers will use this guide to review.

---

## 📋 Table of Contents

- [1. Project entry schema](#1-project-entry-schema)
- [2. Recommendation star definitions](#2-recommendation-star-definitions)
- [3. Banned words & alternatives](#3-banned-words--alternatives)
- [4. English nouns to keep](#4-english-nouns-to-keep)
- [5. License notation conventions](#5-license-notation-conventions)
- [6. Stage page template](#6-stage-page-template)
- [7. Branch page template](#7-branch-page-template)
- [8. Writing style](#8-writing-style)
- [9. Links and citations](#9-links-and-citations)

---

## 1. Project entry schema

Every project entry uses this structure:

```markdown
### [Repo Name](https://github.com/owner/repo) ⭐⭐⭐⭐

| Field | Value |
|---|---|
| Language | Python |
| Stars | ★ 12k+ |
| License | MIT |
| Recommendation | ⭐⭐⭐⭐ |

**What it teaches**: 1-2 sentences on what this project teaches at this stage.

**Best for**: 1 sentence on who should study this and why.

**Notes**: 1-3 sentences of personal evaluation. What's strong, what's weak, what to skip. (Optional.)

**Run it**:
\`\`\`bash
# minimal install / first-run command
\`\`\`
```

### Required fields (GitHub repo entry)
For entries that are real GitHub repos:

- `Stars` (`★ Xk+` format, no thousands separator)
- `License` (SPDX ID or annotated exception, see 5)
- `Recommendation` (⭐ × N, see 2)
- `What it teaches`, `Best for`

### Required fields (non-repo entry: article / course / video / protocol / documentation)
Some entries are blogs, videos, official docs, or catalog hubs — not GitHub repos. For these:

- `Recommendation` (required)
- `What it teaches`, `Best for` (required)
- `Format` (required, e.g. `Article` / `Video` / `Course` / `Curated list` / `Specification`)
- `Stars` / `License` may be omitted (no GitHub repo to attach)

Example: an `Anthropic — Building Effective Agents` blog entry uses `Format = Article` + `Recommendation`, without `Stars` or `License`.

### Optional fields
- `Language` — primary programming language (Python / TypeScript / Chinese)
- `Last update` / `Status` — flag if stale or maintenance slowed
- `Notes`, `Run it`

### Heading conventions
- Stages 1-4 / 6 use `### [Repo](url)`
- Stage 5 / 7 / branches use `#### [Repo](url)` (when there's a parent H3 category)
- Suffix with stars allowed: `### [Repo](url) ⭐⭐⭐⭐⭐` or sub-label: `### [Repo](url) ⭐ Official`

---

## 2. Recommendation star definitions

| Stars | Meaning | When to use |
|---|---|---|
| ⭐⭐⭐⭐⭐ | Must-read / must-run | Skipping this will get you stuck in this stage |
| ⭐⭐⭐⭐ | Highly recommended | Strong material to deepen the topic |
| ⭐⭐⭐ | Solid example | Worth running for cross-reference |
| ⭐⭐ | Useful reference | Browse if interested |
| ⭐ | Niche / advanced / for completeness | Most readers can skip |

These are editorial ratings, not GitHub stars. When removing volatile popularity numbers such as `★ 140k+`, preserve the existing `⭐⭐⭐⭐⭐` rating; change the rating only when evidence about the resource’s purpose, quality, or maintenance changes.

**Rules:**

- A repo cited in different stages / branches **should have the same rating** (unless audience-specific reason, then note it explicitly)
- Don't inflate stars to "look encouraging." Honesty > politeness
- Commercial products (Cursor, LangSmith, etc.) follow the same scale

---

## 3. Banned words & alternatives

The catalog's canonical text is **Traditional Chinese (zh-TW, Taiwan)**, so two of the three tables below are about Chinese wording and apply when you write or edit the zh-TW pages: the vocabulary swaps and the English-in-Chinese sentence patterns. Their terms stay in Chinese because the terms *are* the data. The **overclaim** table in between applies to every locale, including this English one.

> 📌 **Language tag convention (BCP 47 / W3C i18n)**: this repo uses `.zh-Hans.md` (not `.zh-CN.md`) for the Simplified Chinese mirror. `Hans` / `Hant` are [BCP 47 script subtags](https://www.w3.org/International/articles/language-tags/), decoupled from region — Simplified Chinese is also used in Singapore and Malaysia, not only mainland China, so `Hans` is more accurate than `CN`. The canonical `README.md` content is **zh-Hant-TW** (Traditional Chinese, Taiwan conventions), kept unsuffixed as GitHub's default landing page. Region distinctions can be added later as `zh-Hans-CN` / `zh-Hant-HK` etc. Thanks to [@xfq](https://github.com/xfq) (W3C i18n lead) for flagging this in [#9](https://github.com/WenyuChiou/awesome-agentic-ai-zh/issues/9).

### Simplified → Traditional vocabulary swaps

The terms are the data, so they stay in Chinese. Left column: the zh-Hans wording to avoid in canonical zh-TW pages. Right column: the zh-TW wording to use instead.

| Avoid (zh-Hans) | Use instead (zh-TW) |
|---|---|
| 教程 | 教學 / 課程 / 導讀 |
| 視頻 | 影片 |
| 軟件 | 軟體 |
| 文件 (meaning *file*) | 檔案 |
| 文档 / 文件 (meaning *docs*) | 文件 / 文件 (this one stays) |
| 代碼 | 程式碼 / 原始碼 |
| 用戶 | 使用者 |
| 網絡 | 網路 |
| 接口 | 介面 |
| 默認 | 預設 |
| 函数 | 函式 |
| 算法 | 演算法 |
| 程序 (meaning *program*) | 程式 |
| 質量 (meaning *quality*) | 品質 |
| 信息 | 資訊 |
| 數據 | 資料 |
| 內存 | 記憶體 |

### Avoid overclaim phrases

| Avoid | Use instead |
|---|---|
| "the best in the world" / "industry's strongest" | "comprehensive" / "well-known" / "widely-used" |
| "production-grade" (when describing teaching material) | "teaching-oriented" / "material to learn production patterns from" |
| "the only choice" / "definitive" | "a good option" / "an entry-level pick" |
| "the most urgent" / "the most important" | (just drop the modifier) |
| "authoritative reference" (unless truly the official spec) | "important reference implementation" / "official template" |
| "no problem" (re: legal/license) | "check the terms before use" / "verify the terms yourself" |

### Banned English-in-Chinese sentence patterns

Splicing an English verb or adjective into a Chinese sentence reads as untranslated draft text. Rewrite it in Chinese.

| Avoid | Use instead |
|---|---|
| follow 條款 | 遵守條款 |
| ready-made 教材 | 現成可改的教材 |
| NotebookLM-like 工具 | 類 NotebookLM 的工具 / 類似 NotebookLM 的工具 |
| 視覺化 node-based | 視覺化節點式 |
| Anthropic host 的 server | Anthropic 維護的 server |
| coding 流程 | 開發流程 / 程式開發流程 |

---

## 4. English nouns to keep

Technical writing has terms that **read more naturally in English** than translated:

- `LLM`, `API`, `SDK`, `MCP`
- `agent`, `tool use`, `function calling`, `prompt`, `prompt caching`
- `framework`, `library`, `repo`, `commit`, `PR`, `branch`
- `RAG`, `embedding`, `vector DB`, `retrieval`, `chunk`, `token`
- `streaming`, `async`, `batch`, `webhook`
- `marketplace`, `plugin`, `skill`, `hook`
- `production` (when meaning "production environment") — but the catalog deliberately avoids it in many places (see Chinese 3)
- `hello-world`, `hands-on exercise` — keep (zh-TW canonical uses `動手練習`; en mirror translates as `hands-on exercise(s)`)

**Test**: Would a technical reader pause at the translated form? If yes, keep English.

---

## 5. License notation conventions

### Direct SPDX
- `MIT`
- `Apache-2.0`
- `BSD-3-Clause`
- `GPL-3.0`
- `LGPL-3.0`

### Annotated exceptions

| Situation | Notation |
|---|---|
| No SPDX upstream | `NOASSERTION (no SPDX upstream; check LICENSE before use)` |
| AGPL (copyleft) | `AGPL-3.0` + Notes: `AGPL-3.0 license (copyleft) — derivative products that ship modifications must follow the terms.` |
| Custom non-commercial | `NOASSERTION (custom non-commercial)` + Notes: `License is a custom non-commercial term — read the original terms before use.` |
| Multiple per-plugin | `NOASSERTION (each plugin has its own license; check per plugin)` |
| Creative Commons | `CC-BY-4.0`, `CC-BY-NC-SA-4.0`, etc. |

**Rule**: **Never** read a license as legal advice. Don't say "fine for personal use." Say "read the original terms before use."

---

## 6. Stage page template

> The same template applies to two locations:
> - `stages/0X-*.md` — shared foundations (0-2) + Track B (Stage 3-8)
> - `tracks/cli/AX-*.md` — Track A (A1-A3) sub-stages also follow this template, with a higher proportion of cross-links (most entries reference existing Stage 5 / 7 / cli-agents-guide content)

Every stage (except Stage 0) should have:

```markdown
# Stage N — Topic

> **English** | [繁體中文](./0N-slug.md)

[1-2 sentence description of the stage's core question]

## 📌 Learning Goals
- bullet 1
- bullet 2

## 🧩 Core Terms to Know First

### **Correct term (add Chinese when useful)**
Give one plain-language definition. Then give an everyday analogy that does not distort the concept, and say which later exercise will use it.

## 🚪 Entry Conditions (Stage 1+ only)
<details markdown="1">
<summary>⏱ Before you start: time, prerequisites, and budget</summary>

**Time estimate**: N-M weeks (~X-Y hours)

You should have:
- ...

</details>

## 📚 Required Reading
You will use these sources during the exercises; expand them when needed.

<details markdown="1">
<summary>Show 3-5 required sources</summary>

1. [Link](url) — description
2. ...

</details>

## 🛠 Hands-on Exercises (do them, not just read)

### Exercise N: Title
One sentence describing the observable result. Keep the heading outside details so deep links remain visible.

<details markdown="1">
<summary>Show detailed steps</summary>

Time, cost, code, expected output, and troubleshooting.

</details>

Every runnable folder must provide copy-ready PowerShell commands first, followed by a closed `<details>` block with the macOS/Linux alternative; it must also provide Path A and Path B scripts plus offline mock tests. Bound SDK dependencies to major versions and use a pinned cloud model ID; validate untrusted tool names and arguments before execution. Describe cloud cost as a token formula with a verification date, rather than assuming a fixed amount.

[3-5 hands-on exercise items]

## 🎯 Curated Projects

### [Project Name](url) ⭐⭐⭐⭐
[entry schema per 1]

[N entries]

## ✅ Self-Check Before Stage N+1
Can you:

- [ ] ...
- [ ] ...

If yes → proceed to Stage N+1.
If no → ...

## 💡 What's Next (optional, mostly used in the last stage)
```

Keep the title, outcome, and first action visible. Secondary `<details>` blocks omit `open` by default. Ollama Path A remains the primary path, but do not expand every Path A automatically: use `open` only when it is the reader's single immediate action and its content is short. Keep long code and troubleshooting collapsed by default; Anthropic Path B is also collapsed by default. Do not place a linkable heading inside `<details>`, and do not nest more than three disclosure levels.

### Site-wide plain-language rule (ELI5)

This rule applies to the entire learning map. The goal is for a five-year-old to understand “what to do now,” without losing technical accuracy or using a childish voice.

- When a technical term appears for the first time in visible teaching text, put it in **bold**; H1 chapter titles are the exception, but the first use in body text still follows this rule. Explain its plain-language purpose first, then keep the correct term. Example: “an entry that lets a program get data (**API**).”
- Put one idea in each sentence. Give each step one main action. Split long sentences, abbreviations, and jargon, or add a short definition.
- Keep commands, file names, error codes, model names, prices, numbers, and security warnings exact.
- Even with every `<details>` closed, the reader should know the next step and what they will see when it works.
- During review, sample the visible main path. If a first-time reader cannot say the next step in their own words, rewrite it. Move multi-paragraph theory into collapsed content.

### Core-term writing

- Every Stage/Track that has completed a retrospective must put a visible core-term section before the first exercise. Core-term names and their shortest explanations must not go inside `<details>`.
- Each core term must answer four questions on its own: **what it is**, **what it is like**, **what this chapter uses it for**, and **what the correct term is**. Put deeper theory in a collapsed section when needed.
- Collect only key concepts used later in the text, exercises, or self-check. Do not pull out every ordinary noun just to fill a quota, and do not delete necessary terms such as Zero-Shot, Token, or MCP because they seem “too detailed.”
- Keep the concept, order, purpose, and limits consistent across the three languages. Keep English names, abbreviations, commands, and specification names exact.
- `scripts/reader-ux-pages.yml` uses `core_terms` to record the core section, first exercise, terms/labels in all three languages, their order, and the minimum explanation length. Once added, it may only be maintained or strengthened; it must not be silently removed.

### Concept-diagram writing

- Define core terms in plain text first, then use a diagram to organize their relationships. A diagram must not be the reader's first encounter with a term.
- Keep the same layout, order, numbers, and limits in all three locales. Provide a correctly localized image and alt text for each page.
- Exact numbers inside a diagram need the same official evidence as prose. When no fixed rule exists, write “multiple” or “varies by model” instead of inventing a neat range.
- Inspect every image at original size for text, locale characters, arrow direction, and contrast; then run the image-locale gate and all three MkDocs builds.

### Reader UX ratchet

- Add a chapter to `scripts/reader-ux-pages.yml` only after its three-language migration and human review are complete. This tightens the rules chapter by chapter; pages not yet organized do not need to pass all checks at once.
- `scripts/check-reader-ux.py` uses a conservative source-level proxy: non-whitespace Markdown visible on first load. Default-open content and visible fenced code count; HTML comments and collapsed bodies do not. This is a repeatable ratchet, not a browser DOM text-length claim.
- The configuration keeps per-language character limits, the number of blocks allowed open by default, exact headings/anchors that must remain visible, the core-term contract, and grouped row counts for resource tables. Do not raise limits or remove protections without re-review.
- An automated gate can only prevent known structural regressions. Human review must still confirm that, with every disclosure closed, readers know what to do and what success looks like.

### Grouped resource tables

- When the same category spans two or more consecutive resources, use an HTML `<table>` and merge the category with `<th scope="rowgroup" rowspan="N">`.
- Add `scope="col"` to every column-header `<th>` in `<thead>`.
- Give each category its own `<tbody>`; keep `<th scope="rowgroup" rowspan="N">` on the category's first row.
- Merge only a genuinely shared category. Do not merge unrelated groups merely because their status, context, or other text happens to match.
- Preserve the resource count, order, links, and three-locale correspondence, then verify the rendered result with MkDocs.
- Keep short tables without repeated categories in Markdown to avoid needless maintenance cost.

Pages containing models, prices, context limits, licenses, or lifecycle states place a visible verification date and a machine-readable marker near those facts:

```markdown
> Data verified: YYYY-MM-DD UTC. Prices and availability may change; check the official page before use.

<!-- freshness: canonical=stages/0N-slug.md; verified_on=YYYY-MM-DD; scope=models,pricing,availability,deprecations; max_age_days=90 -->
```

All three locale markers must be identical; `canonical` always points to the Traditional Chinese source page. If an official source does not publish a field, write “not published by the official source” instead of inferring it from a third-party leaderboard. Third-party benchmarks may only teach readers how to run their own evaluation.

**Stage 0 exception**: it may omit `Curated Projects` and `Entry Conditions` because it is a prerequisite gateway. The visible path keeps the skip check, four learning goals, one integrated practice, and a short completion check. Time, environment, extra practice, terms, and learning resources stay collapsed by default.

---

## 7. Branch page template

```markdown
# For [audience] — Specialized Branch

> **English** | [繁體中文](./for-X.md)

> [← Back to main path README](../README.en.md) · Branching from end of Stage 7

## Use Cases
- bullet 1
- bullet 2

## Curated Projects

### Sub-category 1
#### [Project](url) ⭐⭐⭐⭐
[entry]

### Sub-category 2
...

## Required Reading
1. ...

## Workflows To Master
- bullet 1
- bullet 2
```

Branch entries can be more concise than stage entries (full schema table optional), but link + stars + 1-2 sentence description is the minimum.

---

## 8. Writing style

### Sentence length
- **Single sentence ≤ 25-30 words** for English
- Break long sentences into two
- Don't force English rhythm into translated Chinese (or vice versa)

### Voice
- Prefer active: "Claude calls the tool" ✓
- Avoid passive: "The tool is called by Claude" ✗

### "You" vs "we"
- **"You" first** — this is learner-facing material
- "I" for author opinion: "I recommend ..."
- Avoid "we" (unless real co-authors exist)

### Connectives
- Prefer simple: "but, so, because"
- Avoid: "however, therefore, hence"

---

## 9. Links and citations

### Internal links
- Between stages: relative path `[Stage 4](04-agent-frameworks.en.md)`
- Branch ↔ README: `[← Back to main path](../README.en.md)`
- Cross-stage repo references: full name + link, not just "as cited earlier"

### External links
- GitHub repo: `https://github.com/owner/repo` (no trailing slash)
- Article / blog: full URL, bold title
- Commercial product (Cursor, Make.com, etc.): official URL, not affiliate

### Link text conventions
- Repo entry heading: `[owner/repo](url)` or `[Project Name](url)`
- In-prose citation: `[Repo Name](url)` or `\`owner/repo\`` (inline code for short references)
- **Avoid**: "click here," "press this"

---

## Related Internal Design Docs

This style guide covers "how to write an entry." For **design rationale** — why these 5 branches, why 8 stages — see:

- [`branches/DESIGN.md`](../branches/DESIGN.md) — Branch design notes (why these audiences, where entries belong) (zh)
- [`stages/DESIGN.md`](../stages/DESIGN.md) — Stage design notes (why this structure, how exercises are chosen) (zh)
- [`cli-agents-guide.en.md`](cli-agents-guide.en.md) — Cross-cutting CLI agent comparison

## Modifying this guide

PRs to this guide are welcome. Open an Issue first to discuss — terminology decisions affect 100+ entries.

Current maintainer: [@WenyuChiou](https://github.com/WenyuChiou).
