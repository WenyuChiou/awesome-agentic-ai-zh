# Send-Day Packages (ready to paste)

> **What this file is**: the copy-paste operational source for outreach submissions. Open it on a send-day, pick ONE target, recheck the target section and links, then paste and submit. The per-target `.md` files in this folder hold the *positioning rationale* (why each target, pitch angle); **this** file holds the *exact content to send*.
>
> **Stable facts checked 2026-08-29 UTC**:
> - Trilingual: **繁中 (canonical) / English / 简中** — all three hand-maintained, not machine-translated
> - Route: Stage 0 → Stage 8, with a CLI track and role-based paths
> - **Curated resources and runnable examples** · MIT · CI lints links + anchors + banned-words on every PR
> - Repo: https://github.com/WenyuChiou/awesome-agentic-ai-zh · Docs: https://wenyuchiou.github.io/awesome-agentic-ai-zh/
> - Popularity numbers are intentionally omitted because they drift. Do not paste a cached star or traffic total.
>
> **Cadence (do NOT blast)**: one target per send-day, 1–2 sends/day max. Wait for a reply or ~1 week before the next. All submissions are done by you (maintainer identity); I prepare content only.

---

## Status board

| # | Target | Channel | Section | Lang | Fit | Status |
|---|---|---|---|---|---|---|
| A | Hannibal046/Awesome-LLM | PR | LLM Tutorials and Courses | en | good | ready (last batch) |
| B | HqWu-HITCS/Awesome-Chinese-LLM | PR | ### 7. LLM教程 | zh-Hans | good | ready (last batch) |
| C | kyrolabs/awesome-langchain | PR | Learn → Notebooks | en | good | ready |
| D | liyupi/ai-guide | PR | AI 学习路线 / 相关资源 | zh-Hans | good | ready |
| E | datawhalechina/hello-agents | **Issue** | (cross-link, not catalog) | zh-Hans | good | ready |
| F | Jenqyang/Awesome-AI-Agents | PR | Related | en | medium | ready (looser fit — see note) |
| — | AiHubCN/Awesome-Chinese-LLM | — | — | — | — | **SKIP** (fork of B) |

**Nudges pending** (your existing open PRs — you run these): #121 WangRongsheng, #754 travisvn — see bottom.

---

## A — Hannibal046/Awesome-LLM (PR)

**Section**: `## LLM Tutorials and Courses` (or the closest "Other Awesome Lists" subsection if the maintainer prefers).
**Entry line**:

```markdown
*   [awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh) - Trilingual (zh-TW / English / zh-Hans) learning roadmap for agentic AI, from LLM basics to multi-agent systems, with curated resources and runnable examples.
```

**PR title**: `Add awesome-agentic-ai-zh (trilingual agentic-AI learning roadmap)`

**PR body**:

```markdown
Hi Hannibal046,

Adding awesome-agentic-ai-zh to LLM Tutorials and Courses (move it if another spot fits better).

It's a trilingual learning roadmap for agentic AI — Traditional Chinese (canonical), English, and Simplified Chinese, all three hand-maintained. The path runs from Stage 0 (what an LLM is, how tokens work), through Stage 7 (multi-agent systems and production engineering), to Stage 8 (Agent Interfaces: Computer Use, Browser Use, and sandboxes), with curated resources and small runnable examples. MIT licensed; CI checks links and anchors on every PR.

Thanks for maintaining Awesome-LLM.

— Wenyu Chiou (individual maintainer)
```

---

## B — HqWu-HITCS/Awesome-Chinese-LLM (PR)

**Section**: `### 7. LLM教程` (nested format — match exactly, this repo uses 项目名称 / 地址 / 简介).
**Entry block**:

```markdown
* awesome-agentic-ai-zh:
    * 地址:[https://github.com/WenyuChiou/awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh)
    * 简介:三语(繁中 / English / 简中)agentic AI 学习地图,共 10 个学习站（8 个主题 Stage + Stage 0 准备关 + Stage 7.5 阅读站）+ 2 条学习路线 + 分组整理的 curated 资源,附可跑的范例。MIT。
```

**PR title**: `添加 awesome-agentic-ai-zh(三语 agentic AI 学习地图)到 7. LLM教程`

**PR body**:

```markdown
你好,

想把 awesome-agentic-ai-zh 加到「7. LLM教程」。这是一份 agentic AI 的三语学习地图(繁中 canonical / 简中 / English,三语手工维护),共 10 个学习站（8 个主题 Stage + Stage 0 准备关 + Stage 7.5 阅读站）,并提供分组整理的 curated 资源与可运行练习,MIT 协议。

已按本项目格式提供链接与简介。觉得不合适直接关掉就好,谢谢维护这份清单。

— Wenyu(个人 maintainer)
```

---

## C — kyrolabs/awesome-langchain (PR)

**Section**: `## Learn → ### Notebooks` — place **right after** the existing `liaokongVFX/LangChain-Chinese-Getting-Started-Guide` line (keeps the two zh learning resources adjacent). There is **no** "Tutorials" section; do not create one.

**Diff**:

```diff
  - [LangChain Chinese Getting Started Guide](https://github.com/liaokongVFX/LangChain-Chinese-Getting-Started-Guide): Chinese LangChain Tutorial for Beginners ![GitHub Repo stars](https://img.shields.io/github/stars/liaokongVFX/LangChain-Chinese-Getting-Started-Guide?style=social)
+ - [WenyuChiou/awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh): Trilingual (zh-TW / zh-Hans / en) 10-stop learning roadmap for agentic AI: 8 topic stages plus Stage 0 readiness and the Stage 7.5 reading stop. Stage 4 covers Workflow Graphs, LangGraph, AutoGen, CrewAI, and Smolagents with hands-on exercises ![GitHub Repo stars](https://img.shields.io/github/stars/WenyuChiou/awesome-agentic-ai-zh?style=social)
```

**PR title**: `Add awesome-agentic-ai-zh (trilingual learning roadmap) to Learn → Notebooks`

**PR body**:

```markdown
Hi kyrolabs maintainers,

Proposing [WenyuChiou/awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh) for **Learn → Notebooks**, next to the existing `liaokongVFX/LangChain-Chinese-Getting-Started-Guide` entry (same zh-learning surface).

Why it fits:
- Trilingual (zh-TW canonical · zh-Hans · en — all three hand-maintained, not MT), which fills a gap for non-English learners.
- Stage 4 (Workflow Graphs & Agent Frameworks) walks new developers through LangChain / LangGraph / AutoGen / CrewAI / Smolagents with prerequisites, time estimates, and hands-on exercises.
- The §11 catalog has 7 Chinese-ecosystem entries including `chatchat-space/Langchain-Chatchat` and the LangChain Chinese Getting Started Guide already in your list.

MIT licensed, with rendered docs at https://wenyuchiou.github.io/awesome-agentic-ai-zh/. CI runs banned-word, link-rot, and anchor-integrity lints on every PR. Popularity metrics are intentionally omitted because they drift.

If a different section works better, happy to redirect. Thanks for maintaining awesome-langchain.

— Wenyu Chiou (individual maintainer)
```

> **Send-day stat refresh**: `gh repo view WenyuChiou/awesome-agentic-ai-zh --json stargazerCount,forkCount` + `gh api repos/WenyuChiou/awesome-agentic-ai-zh/traffic/views` if you want fresh visitor numbers.

---

## D — liyupi/ai-guide (PR)

**Section**: 「AI 学习路线」或「相关资源」(放哪边由 liyupi 决定). liyupi 偏好简体 + 大陆友善措辞,PR 用 zh-Hans。

**Entry line**:

```markdown
- [WenyuChiou/awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh) — agentic AI 的三语学习地图（繁中 / English / 简中），从 Stage 0 的 LLM 基础，走到 Stage 7 的多 Agent 系统与稳定运作，再到 Stage 8 的 Agent Interfaces；包含 curated 资源与可运行范例，采用 MIT。和 ai-guide 互补：ai-guide 找 project，这份找学习顺序。
```

**PR title**: `添加 awesome-agentic-ai-zh(三语 agentic AI 学习地图)到「AI 学习路线」`

**PR body**:

```markdown
你好 liyupi,

想把 [awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh) 加到「AI 学习路线」或「相关资源」section(放哪边你决定)。

这份是 agentic AI 的三语学习地图（繁中 canonical / 简中 / English，三语手工维护，不是机翻）：从 Stage 0 的 LLM 基础，走到 Stage 7 的多 Agent 系统与稳定运作，再到 Stage 8 的 Agent Interfaces。每阶段标了预估时程、入门条件与该读什么，并提供分组整理的 curated 资源，采用 MIT 协议。

定位上和 ai-guide 互补,不是取代:ai-guide 是资源大全,这份补的是「该按什么顺序学」。常见读者是想学但不知道先学哪个的工程师,走完阶段后回 ai-guide 找具体 project 用。

觉得不合适直接关掉就好,谢谢你做的 ai-guide。

— Wenyu(个人 maintainer)
```

---

## E — datawhalechina/hello-agents (GitHub **Issue**, not a PR)

> This one is a **cross-link suggestion Issue** on the hello-agents repo, not a catalog entry. We already link Hello-Agents on our side (no strings); the issue just opens a reciprocal-link conversation.

**Repo**: https://github.com/datawhalechina/hello-agents → Issues → New issue
**Issue title**: `Cross-link 建议:一份会把读者导向 Hello-Agents 的结构化学习路线`

**Issue body**:

```markdown
你好 Datawhale 团队,

我在维护 [awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh) —— 一份 agentic AI 的三语(繁中 canonical / 简中 / English)10 站学习地图（8 个主题 Stage + Stage 0 准备关 + Stage 7.5 阅读站）,分组整理的 curated 资源,MIT。

我们这边已经把 Hello-Agents 放进了「走完前面阶段后的延伸阅读」(无条件,已经 ship)。读者主要是走完 Stage 4 之后想进 framework 跟 multi-agent 的人,Hello-Agents 正好是下一阶段最强的中文教材。

想问有没有可能做个双向 cross-link:
1. 我们已经 link 你们了。
2. 如果你们觉得合适,能不能在 Hello-Agents 的 README 或 docs 里提一句「想看更完整的学习路线可以参考 awesome-agentic-ai-zh」?
3. 或是 reverse PR:我们在中文圈那一节加 Hello-Agents 的正式 entry,你们 review。

不合适也完全 OK。谢谢你们把 Hello-Agents 做出来,这几年中文 agentic AI 学习的公共财都是你们扛的。

— Wenyu(PhD candidate · Lehigh,个人 maintainer)
```

> Note: WeChat 是 Datawhale 主要互动 channel,但 GitHub issue 比较可追踪。一周没回就放着,他们团队很忙、不要 ping。

---

## F — Jenqyang/Awesome-AI-Agents (PR)

> **Fit note (read before sending)**: this list has no Tutorials / Learning section. The closest home is `## Related`, but its visible subsection is "Paper-List Repo", which isn't a clean match for a learning roadmap. Send only if you're OK with the looser fit; the entry below leads with "happy to move it" so the maintainer can reslot. Check `CONTRIBUTING.md` in the repo first.

**Section**: `## Related` (maintainer to confirm exact subsection).
**Entry line** (matches their `*   [Name](URL) - desc ![stars]` format):

```markdown
*   [awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh) - Trilingual (Traditional Chinese / English / Simplified Chinese) 10-stop learning roadmap for agentic AI: 8 topic stages plus Stage 0 readiness and the Stage 7.5 reading stop, with curated resources and runnable examples. [![GitHub Repo stars](https://img.shields.io/github/stars/WenyuChiou/awesome-agentic-ai-zh?style=social)](https://github.com/WenyuChiou/awesome-agentic-ai-zh)
```

**PR title**: `Add awesome-agentic-ai-zh (trilingual agentic-AI learning roadmap) to Related`

**PR body**:

```markdown
Hi Jenqyang,

Proposing awesome-agentic-ai-zh for the Related section — happy to move it wherever fits best, I wasn't sure which subsection is right.

It's a trilingual learning roadmap for agentic AI: Traditional Chinese (canonical), English, and Simplified Chinese, all three hand-maintained rather than machine-translated. The structure runs from Stage 0 (what an LLM is, how tokens work), through Stage 7 (multi-agent systems and production engineering), to Stage 8 (Agent Interfaces: Computer Use, Browser Use, and sandboxes), with curated resources and small runnable examples.

The gap it fills: most agent lists, including yours, are catalogs you reach for once you know what you want. This is the "where do I start, and in what order" layer for people who don't yet. MIT licensed; CI checks links and anchors on every PR.

If it's not a fit, no problem at all. Thanks for maintaining the list.

— Wenyu Chiou (individual maintainer)
```

---

## SKIP — AiHubCN/Awesome-Chinese-LLM

**Do not submit.** It shares the repo name, the section structure (`7. LLM教程`), and the exact nested entry format with **HqWu-HITCS/Awesome-Chinese-LLM** (target B above). That's a fork/mirror signature. Submitting the same entry to both reads as duplicate/spam and dilutes the one that matters. Send B (the canonical HqWu-HITCS) only. If you ever confirm AiHubCN is genuinely independent **and** actively merges external PRs, reuse the B package verbatim — the format is identical.

---

## Nudges (your existing open PRs — run on a send-day, ~1 week apart)

Both are your own PRs, so these are yours to run. Polite single ping; if still no reply after another week, leave them.

```bash
# PR #121 — WangRongsheng/awesome-LLM-resources (zh-Hans)
gh pr comment 121 --repo WangRongsheng/awesome-LLM-resources \
  --body "Hi,这个 PR 开了一段时间了,不知道有没有机会 review 一下?如果格式或 section 需要调整我随时改。谢谢!"

# PR #754 — travisvn/awesome-claude-skills (en)
gh pr comment 754 --repo travisvn/awesome-claude-skills \
  --body "Gentle ping on this one — happy to adjust the entry or move it if a different section fits better. Thanks for maintaining the list!"
```

---

## After you submit

Tell me which target + the PR/issue URL, and I'll update the matrix in `channel-partners.md` (status: submitted → date + link). Keep the one-at-a-time cadence so none of these read as a coordinated blast.
