# Subagent Cookbook — 15 个复制粘贴就能用的派遣 recipe

> [繁體中文](./subagent-cookbook.md) | **简体中文** | [English](./subagent-cookbook.en.md)

> 📋 **这是什么**：[Stage 5.5](../stages/05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能) 教你 subagent 是什么概念，这份 cookbook 教你**今天就能用**——15 个场景，每个都包含“该用哪个 subagent + 完整 prompt 模板（复制即可用）+ 何时不用”。
>
> ⚠️ **第一次看？先读 Stage 5.5 的“可派遣的 subagent 有哪些”+“decision table”两节**——理解“什么是 subagent”“Claude Code 内置有哪些”之后再来查 recipe。

---

## 怎么读这份 cookbook

每个 recipe 都用同样的 4 段结构：

| 段 | 内容 | 为什么有这段 |
|---|---|---|
| **场景** | 你今天工作会遇到的具体场景 | 从“我有 X 问题”找到 recipe，而不是从“我想用 subagent”找 |
| **Subagent** | 用哪一个（Claude Code 内置名称） | 直接 copy 名字，不用想 |
| **Prompt 模板** | 复制粘贴即可用的指令文字 | 不用自己想怎么写 |
| **何时不用** | 比用 subagent 更好的替代方案 | 避免“大材小用” |

> 💡 **怎么实际派遣 subagent**：在你的 Claude Code 终端对话框里，**直接输入（或粘贴）prompt 模板**——就这样。Claude 看到指令，会自动通过 **Agent tool**（内部派遣机制）找到对应 subagent 跑，跑完后向主 session 回报一段摘要。**不需要 slash command，不需要特殊语法**。
>
> 📌 **subagent ≠ slash command**：`/agents` 是列表命令，**不是调用 subagent 的方式**；派遣 subagent 直接打对话 prompt 文字即可。完整对比表（subagent vs skill / vs slash command / description router）见 [Stage 5.5 §易混淆观念厘清](../stages/05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能)。

---

## 先确认你有哪些 subagent 可用

在你的 Claude Code session 里跑 `/agents` 这个指令，会列出全部当前可用的 subagent（内置 + plugin + 自定义）。

**Claude Code 默认内置 7 个** subagent：`general-purpose` / `code-reviewer` / `Explore` / `Plan` / `frontend-developer` / `claude-code-guide` / `statusline-setup`（截至 2025-11，可能会变动）。

> 📌 **每个内置 subagent 的功能说明 + “遇到 X 任务用 Y”decision table 的 canonical 在 [Stage 5.5 §可派遣的 subagent 有哪些](../stages/05-claude-code-ecosystem.zh-Hans.md#可派遣的-subagent-有哪些)**——本 cookbook 聚焦“怎么派遣”的 15 个 recipe，内置清单与选用逻辑以 Stage 5.5 为准。

> 💡 **如果 `/agents` 列表跟这份 cookbook 不一致**：表示你装了 plugin，或 Claude Code 版本不同。**recipe 名字对不上时，找最接近的 subagent 用就好**（例如没有 `Explore`，用 `general-purpose` 也能跑搜索）。

确认完当前可用清单之后，就可以照下面 15 个 recipe 派遣了——**找到符合你场景的 recipe，把 Prompt 模板复制到 Claude Code 对话框即可**。

---

## 15 个 Recipe

### Recipe 1: 写完一批新 code，要 commit 前的 review

**场景**：你刚写了 ≥ 50 行新 code，想 commit 但怕有 bug / security 问题没看到

**Subagent**：`code-reviewer`

**Prompt 模板**：
```
Review the staged changes in this repo (git diff --cached).
Focus on: (1) security issues (hardcoded secrets, SQL injection, XSS),
(2) error handling gaps, (3) missing tests, (4) violations of CLAUDE.md
conventions. Per-category PASS/FAIL + concrete fix for each issue with
file:line reference + overall verdict (APPROVE / REQUEST CHANGES).
```

**何时不用**：< 20 行的 typo / formatting fix（直接 `git diff` 自己扫就好，不用花 subagent token）

---

### Recipe 2: 进入新 repo，不知道该从哪个 file 开始读

**场景**：复制完一个别人的 repo，`README.md` 讲不清楚程序入口在哪，不想随便挖

**Subagent**：`Explore`

**Prompt 模板**：
```
Map the entry points and core structure of this codebase. Report:
(1) main entry script(s) — what file gets run first,
(2) core module organization — top 3-5 directories and what each does,
(3) test directory layout,
(4) any "where to start reading" guidance in docs/.
Under 300 words with file paths.
```

**何时不用**：你已经知道要看的 file 路径（直接用 Read tool）

---

### Recipe 3: 设计 refactor / migration plan（先想清楚再动手）

**场景**：要重构一个大 module 或做 framework migration，不确定步骤，想先有 plan 再开始

**Subagent**：`Plan`

**Prompt 模板**：
```
Design a step-by-step plan to refactor <module-name> (currently a single
file with tight coupling) into clear, testable components with explicit
interfaces. Include: (1) phased breakdown (≤ 5 phases), (2) which files
touched per phase, (3) what tests gate each phase, (4) rollback strategy
if a phase fails. Don't write code — just the plan.
```

**何时不用**：refactor 只动 1-2 个 file（直接动手，不需要 plan overhead）

---

### Recipe 4: 多文件 / 跨 locale parity 审查

**场景**：你改了 zh-TW + zh-Hans + en 三个 mirror，想确认三边内容一致

**Subagent**：`code-reviewer`

**Prompt 模板**：
```
Review the staged diff for cross-locale parity across the 3 locale
variants of <file-stem> (.md / .zh-Hans.md / .en.md). Check: (1) same
section structure (## headers match), (2) same table row counts, (3)
same required terms present in each locale, (4) locale conventions
correct (zh-Hans uses "" not 「」; en uses English). Report per-file
PASS/FAIL.
```

**何时不用**：只改 1 个 locale（没有 parity 问题）

---

### Recipe 5: 多 source fact-check / research

**场景**：要写一段引用，不确定多个 source 讲的是不是同一件事，需要交叉验证

**Subagent**：`general-purpose`

**Prompt 模板**：
```
Fact-check this claim: "<claim>". Search for: (1) primary source / official
docs / paper, (2) 2-3 independent secondary sources, (3) any contradictions
or version differences. Report: confirmed / contradicted / nuanced, with
direct quotes and URLs. Under 400 words.
```

**何时不用**：你已经有 1 个权威 source（直接读那一个就好）

---

### Recipe 6: 找某个 symbol / function 在哪定义

**场景**：codebase 里到处都在导入 `parse_config`，想知道实作在哪个 file

**Subagent**：`Explore`

**Prompt 模板**：
```
Find where `<symbol-name>` is defined in this codebase. Report: (1) the
file:line where it's defined, (2) what it does (1-line summary), (3) which
files import / use it (top 5). Use Grep, not full file reads.
```

**何时不用**：你已经用 IDE 的 "Go to definition" 可以跳过去（IDE 比 subagent 快）

---

### Recipe 7: 比较多篇 paper / source 的 claim 是否一致

**场景**：写文献回顾，3 篇 paper 对同一件事说法不同，不知道该信谁

**Subagent**：`general-purpose`

**Prompt 模板**：
```
Find and compare 3 independent sources on the topic <topic>. For each
source, capture: title + author + year + URL. Then report: (1) what
they agree on, (2) where they disagree (with direct quotes), (3) which
is most recent / authoritative, (4) suggested phrasing if you had to
summarize the consensus. Flag if a key source is behind a paywall and
unreadable.
```

**何时不用**：3 篇都是同一个作者 / 同 lab（没有“多 perspective”可比）

---

### Recipe 8: Release commit security audit

**场景**：要发 v1.0 / 升 major version，想最后做一次安全扫描

**Subagent**：`code-reviewer`

**Prompt 模板**：
```
Pre-release security audit for <release-tag> (use git log to find the
relevant commit range since last release). Check: (1) hardcoded
credentials / API keys, (2) eval() / exec() / shell injection risks,
(3) deprecated dependencies with known CVEs, (4) any auth / session
handling changes since last release, (5) public API surface changes
(breaking? documented?). Per-category PASS/FAIL + remediation per
finding.
```

**何时不用**：patch release（hotfix）只动 1 行（人工扫 < 1 分钟）

---

### Recipe 9: 评估架构变动的 blast radius

**场景**：想改一个 base class / 共用 utility，不确定会影响多少 file

**Subagent**：`Plan`

**Prompt 模板**：
```
Assess the blast radius of changing <component>. Report: (1) direct
dependents (which files import this), (2) indirect dependents (transitive
imports), (3) tests that gate the change, (4) suggested rollout order
(safest → riskiest), (5) feature flag / kill switch strategy if available.
Don't make the change yet — just the impact analysis.
```

**何时不用**：只影响 1 个 file 内部（没有 blast radius 概念）

---

### Recipe 10: Spawn 并行 subagent 跑同一任务 × 多目标

**场景**：4 个 branches file 都要做同样的“academic-style audit”，想一次跑 4 个 parallel

**Subagent**：`general-purpose` × N（同时 spawn 多个）

> 💡 **怎么“同时 spawn 多个”**：在 Claude Code 对话框内，**连续输入下面的 prompt 4 次**（每次换 `<file-path>`）。Claude Code 会自动并行跑，不需要等第一个 subagent 结束才能输入第二个——这就是“parallel spawn”的实际操作方式。

**Prompt 模板**（每次换 `<file-path>`）：
```
Audit `<file-path>` for academic-style issues: (1) over-engineering
jargon without first-use explanation, (2) clarity (long sentences,
vague pronouns), (3) unsupported % claims, (4) persona-fit (wrong
technical level for the file's stated target audience — see the
file's banner / intro callout for who it's for). Report 4-category
PASS/FAIL + fix-list with line numbers. Under 500 words.
```

**何时不用**：1 个目标就够（直接调用 1 次，不要 over-orchestrate）

---

### Recipe 11: 找跨 repo 的相似 implementation

**场景**：你在某个 repo 看到一个 pattern，想知道另一个 repo 有没有类似实作

**Subagent**：`Explore`

**Prompt 模板**：
```
In <repo-path>, search for code patterns similar to: <description of
pattern, e.g., "retry decorator with exponential backoff">. Report:
(1) up to 5 candidates with file:line, (2) brief description of each,
(3) which is most idiomatic for this codebase's style.
```

**何时不用**：你有具体 function 名要找（用 Recipe 6 / `Explore` 加精确 grep 更快）

---

### Recipe 12: LLM-as-judge eval（structured PASS / FAIL）

**场景**：跑了 100 个 test case，要评每个 output 是否符合 spec，不想人工看

**Subagent**：`general-purpose`

**Prompt 模板**：
```
Evaluate the agent outputs in <eval-file.jsonl> against the spec stated
in the file's first 5 lines (or in <spec-file.md>). For each row: PASS /
FAIL with 1-sentence reason. Aggregate: pass rate + top-3 failure modes.
Output as structured JSON: {"case_id": "...", "verdict": "PASS|FAIL",
"reason": "..."}.
```

**何时不用**：< 5 个 case（自己看更快）；evaluation 涉及主观判断（LLM judge 不可靠）

---

### Recipe 13: UI component design / accessibility audit

**场景**：写了一个 React component，想确认 ARIA + keyboard nav + responsive 都做对

**Subagent**：`frontend-developer`

**Prompt 模板**：
```
Audit <component-file> for: (1) ARIA roles + labels (screen reader
compatibility), (2) keyboard navigation (tab order, Enter / Esc / arrows
behavior), (3) responsive breakpoints (mobile 360px / tablet 768px /
desktop 1280px), (4) color contrast (WCAG AA), (5) touch target size
(≥ 44px). Report per-category findings + fixes.
```

**何时不用**：纯后端 / CLI 工具（没有 UI 可 audit）

---

### Recipe 14: 问 Claude Code feature 怎么用

**场景**：忘了 hooks 怎么设、忘了 slash command 的 frontmatter 字段，想查文件

**Subagent**：`claude-code-guide`

**Prompt 模板**：
```
How do I <specific Claude Code feature question, e.g., "configure a
PreToolUse hook to block dangerous bash commands">? Show: (1) minimum
config in settings.json, (2) example hook script (Python or shell),
(3) 1 common gotcha, (4) where in the official docs to read more.
```

**何时不用**：你已经写过几次（直接看自己 `~/.claude/settings.json` 范例更快）

---

### Recipe 15: 写 React form validation 逻辑

**场景**：要做一个 sign-up form，要 email format / password strength / real-time validation

**Subagent**：`frontend-developer`

**Prompt 模板**：
```
Implement a React sign-up form with: (1) email format validation
(real-time, debounce 300ms), (2) password strength meter (≥ 8 chars,
mixed case, digit, symbol), (3) inline error messages with ARIA
live region, (4) submit button disabled until valid. Use <library, e.g.,
React Hook Form + Zod>. Include: component code, validation schema,
1 happy-path test, 1 error-path test.
```

**何时不用**：非 React stack（用 Vue / Svelte 对应的 subagent，或 `general-purpose`）

---

## Recipe 索引（按 subagent type 找）

不确定该用哪个 subagent？从**任务类型**反查：

| Subagent | Recipes |
|---|---|
| `code-reviewer` | **1**（pre-commit review）/ **4**（cross-locale parity）/ **8**（release security audit）|
| `Explore` | **2**（new codebase）/ **6**（find symbol）/ **11**（cross-repo similar code）|
| `Plan` | **3**（refactor plan）/ **9**（blast radius）|
| `general-purpose` | **5**（fact-check）/ **7**（multi-paper compare）/ **10**（parallel multi-target）/ **12**（LLM-as-judge eval）|
| `frontend-developer` | **13**（a11y audit）/ **15**（React form）|
| `claude-code-guide` | **14**（Claude Code feature 查询）|

---

## 何时 NOT 该用 subagent

Subagent 不是免费的——每次派遣**会烧 token，也有延迟**。下面 4 种场景**不该用 subagent**，自己跑更划算：

1. **任务 < 5 分钟可自己完成** — 大材小用；subagent overhead 不划算
2. **结果需要逐步 user feedback** — subagent 是“派出去、跑完回报一次”，不能中间问你；要逐步确认的任务直接在主 session 跑
3. **任务需要主 session 的 context memory** — subagent 是**独立 context window**，看不到主 session 前面的对话；要用“我们刚刚讨论的 X...”这种 reference 的任务，不适合
4. **任务涉及 conversation-level judgment** — 像“这个 architecture 决策该怎么权衡”，需要对话协作，不适合丢给 subagent

> 💡 **判断的快速办法**：如果任务可以用“**写一份完整 brief 给陌生人接手做**”描述清楚 → 适合 subagent；如果需要“**我跟你讨论一下**”→ 留在主 session。

---

## 接下来

- **想理解完整理论**（subagent 跟 skill / MCP 的差别、3 种 multi-agent 机制）→ [Stage 5.5](../stages/05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能)
- **CLI 日常用法 playbook** → [`tracks/cli/A3-cli-production.zh-Hans.md` Playbook 4](../tracks/cli/A3-cli-production.zh-Hans.md#-playbook-4派遣-subagent-跑独立任务)
- **想看 subagent 在 agent paradigm 体系内的定位** → [`resources/agent-paradigms.zh-Hans.md`](./agent-paradigms.zh-Hans.md#subagent--在-agent-runtime-里再-spawn-agent)
- **词汇快查** → [`resources/glossary.zh-Hans.md` § 5. Claude Code 生态 — Subagent](./glossary.zh-Hans.md#subagent子-agent)
