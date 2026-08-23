# 研究者延伸路线（For Researchers）

> [繁體中文](./for-researcher.md) | **简体中文** | [English](./for-researcher.en.md)

> 🚀 **计算型研究者**（会跑 Python script、有 API key、会用 git）可直接进阶；**非程序背景研究者**（人文社科、临床研究、文献为主）可先从文献 Q&A（NotebookLM）、Zotero AI 工具开始，需要时再看 [`resources/setup-guide.zh-Hans.md` A-C](../resources/setup-guide.zh-Hans.md)。

> [← 回主路线 README](../README.zh-Hans.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 后从这里接续。把 agentic AI 应用到研究流程上。

## 使用场景（研究阶段 × AI 怎么帮）

研究者一天分成几个阶段，AI 在每个阶段的角色不同。下表帮你定位：

| 阶段 | 你常遇到的痛点 | AI 能帮的部分 | 推荐工具（从轻到重） |
|---|---|---|---|
| **文献探索** | 不知道某个领域有哪些经典 paper | 推荐 + 摘要 + 比较 | NotebookLM → paper-qa → gpt-researcher |
| **文献精读** | PDF 翻一半就忘 / 抓不到 claim | 抓 claim、figure、citation、做笔记 | Zotero + zotero-gpt → zotero-skills |
| **研究设计** | RQ 模糊、不知选哪个 method | 对话厘清、列出 trade-off | Claude.ai 对话 → ai-research-skills |
| **实验 / 写代码** | 重复 boilerplate、写 plot 浪费时间 | 写 / 改 code、batch refactor | Claude Code → codex-delegate |
| **论文撰写** | 草稿卡关、句子不通 | 大纲 → 段落 → 润色 | Claude.ai → Gemini CLI（长稿） |
| **改稿 / 投稿** | 期刊规范一堆、容易漏 | banned-word / figure-text / submission checklist | academic-writing-skills |
| **跨 paper synthesis** | 5 篇 paper 互相对话、context 爆 | 1M token 一次读完 + 整理 | Gemini CLI |

> 💡 **计算型 vs 非程序背景**：表中“推荐工具”由轻到重——非程序背景研究者先停在每行**第一个**就够了；计算型研究者要自动化才往后挑。

## 精选 Projects

> 💡 **想把 Claude Code 接到 NotebookLM、Obsidian、Notion、Excel、PDF、Excalidraw 等研究常用工具？** 81+ 个集成在 [`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md)（按使用场景分类）。下面这节保留“研究专属”的工具与 marketplace。

### 研究流程 Marketplace

#### [flonat/claude-research](https://github.com/flonat/claude-research) ⭐⭐⭐

给博士研究者的 Claude Code 基础建设——学术流程用的 skill、agent、hook、规则。LaTeX / 文献管理为主。

---

### 文献 RAG / Q&A

#### [Future-House/paper-qa](https://github.com/Future-House/paper-qa) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 8.9k+ |
| License | Apache-2.0 |

**教什么**：对 PDF 文件以 **citation-grounded Q&A** 为设计目标——每个答案附句子层级的引用、减少幻觉风险。实际准确率依文件类型而异，评测结果以官方 benchmark / paper 为准。

**适合谁**：写文献回顾、需要“查文献时答案要可追溯”的研究者。比一般 RAG 更严谨。

---

#### [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 28k+ |
| License | Apache-2.0 |

**教什么**：自主 deep-research agent——planner + multi-source crawl + report 合成。给定一个研究主题，自动产出 markdown / PDF brief。

**适合谁**：要快速 scope 新题目、产 research brief 的研究者。

---

### 大纲与写作

#### [stanford-oval/storm](https://github.com/stanford-oval/storm) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 30k+ |
| License | MIT |

**教什么**：multi-perspective outline-then-write pipeline——**白话三步**：(1) 先模拟不同观点提出问题、(2) 把问题整理成大纲、(3) 最后生成 Wikipedia-style 草稿。Stanford OVAL 出品。

**适合谁**：想学“**outline-driven 写作**”的人。从零产主题 brief 时的好工具，类似 NotebookLM structured report 流程的开源版。

**备注**：最后一次推送已超过 6 个月，使用前确认最新 commit 日期。

---

#### [kaixindelele/ChatPaper](https://github.com/kaixindelele/ChatPaper) ⭐⭐⭐⭐⭐（中文读者）

| 栏位 | 内容 |
|---|---|
| 语言 | 中文 + Python |
| Stars | ★ 19k+ |
| License | NOASSERTION（自定义条款，非商用） |

**教什么**：中文研究者向的 arXiv 全流程工具——论文总结 + 翻译 + 润色 + 审稿回复生成。中国研究团队维护，默认值对中文场景友好。

**适合谁**：中文研究生想找对中文友好的 paper 全流程入门工具。

**备注**：License 是自定义的非商用条款，使用前请先读原始条款；研究或个人用途常见，但条款还是要自己看过确认。

---

### 文献管理集成

#### [MuiseDestiny/zotero-gpt](https://github.com/MuiseDestiny/zotero-gpt) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 7k+ |
| License | AGPL-3.0 |

**教什么**：Zotero 的 LLM plugin——可以跟你的文献库对话、总结 selection、生成 inline notes。

**适合谁**：Zotero 重度用户，想在阅读流程里直接接 AI 而不用切到别的工具。

**备注**：AGPL-3.0 license（传染性开源）— 修改后要散布的衍生产品需遵守条款。

---

### Multi-LLM 研究组合（本 repo 维护者的研究 setup）

研究流程里有些任务 Claude 一个就够（对话、设计、review），有些 Claude 做会浪费 token（大批 code refactor、长稿 draft）。维护者实际用的搭配是 **Claude 当 planner / reviewer、Codex 跑程序、Gemini 跑长稿**——下表列什么时候用哪个：

| 任务类型 | 例子 | 用哪个 LLM | 为什么 |
|---|---|---|---|
| 研究设计 / 假设讨论 | “这个 RQ 该用 logistic vs survival？” | Claude.ai 对话 | 对话协作、context memory |
| 写 / 改 code | “50 个 simulation script 都加 logging” | codex-delegate | 机械式编辑快、不烧 Claude token |
| 写长稿（中英文） | “draft 一个 8 页 paper section” | Gemini CLI | 1M context、长 prose 强项 |
| Second opinion | “请 Gemini 看我的 discussion 段落” | Gemini CLI | LLM-vs-LLM 对照，容易看出 Claude 自身偏误 |
| 投稿前 audit | “跑 banned-word + figure-text checklist” | academic-writing-skills | structured audit，不靠 LLM 即兴判断 |

#### 维护者自用的 6 个研究 skill

> ⚠️ **披露**：以下 6 个工具是维护者 [@WenyuChiou](https://github.com/WenyuChiou)（Lehigh CEE PhD candidate）日常在用的研究 skills，公开让有相似需求的人用。**未经第三方独立评测**——适合 PhD 学位写作 / 跨 paper 文献整理这类流程；不一定适合你的领域。详细 entry 看 [`resources/mcp-skills-catalog.zh-Hans.md` 13 + 14](../resources/mcp-skills-catalog.zh-Hans.md#13-研究工作流-skills学术--paper--文献)。

| 工具 | 适合阶段 | 一句话 |
|---|---|---|
| **[ai-research-skills](https://github.com/WenyuChiou/ai-research-skills)** ⭐⭐⭐⭐⭐ | 全流程 | 14 个研究 skill 打包成 5-plugin marketplace，一个指令装整套 |
| **[research-hub](https://github.com/WenyuChiou/research-hub)** ⭐⭐⭐⭐ | 文献整理 | Zotero + Obsidian + NotebookLM 三工具集成 workspace，CLI / MCP / REST / dashboard 四种接口 |
| **[zotero-skills](https://github.com/WenyuChiou/zotero-skills)** ⭐⭐⭐⭐ | 文献管理 | Zotero CLI skill（搜 / 加 / 分类 / 标记）——跟 zotero-gpt 互补（后者在 Zotero 里 chat，这份从外部操作） |
| **[academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills)** ⭐⭐⭐ | 投稿前 | banned-word audit、figure-text coupling、submission checklist；per-paper 可定制 journal_format / style_overrides |
| **[codex-delegate](https://github.com/WenyuChiou/codex-delegate)** ⭐⭐⭐⭐⭐ | 写代码 | Claude planner + Codex executor 的标准 skill——batch refactor / boilerplate / migration |
| **[gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill)** ⭐⭐⭐（⚠️ 已封存） | 长稿 / synthesis | Claude planner + Gemini 写 1M context 长文 / CJK / second-opinion。**⚠️ repo 已封存 2026-07**——workflow 仍可直接用 [Gemini CLI](https://github.com/google-gemini/gemini-cli) 做 |

---

### Multi-Agent for Research

#### [langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 12k+ |
| License | MIT |

**教什么**：开源版的 Deep Research——支持单 agent 跟 supervisor + multi-researcher 两种架构（multi-agent 那条目前在 `src/legacy/`）、平行搜索、再合成为有引用的 report。是学“LLM agent 怎么自动产出有引用 brief”的好参考。

**适合谁**：要打造“agent 自动产出有引用 brief”工作流程的研究者。是这个分类最 canonical 的开源选择。

**备注**：依赖 LangGraph + 搜索 tool（要 API key）。

---

#### [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 6.9k+ |
| License | The AI Scientist Source Code License（source-available，非商用 + 有 manuscript-disclosure 条款） |

**教什么**：端到端的 multi-agent 科学研究 loop：构想 → 写代码 → 跑实验 → 写 paper → 互审。Sakana AI 的“AI 写整篇 ML paper”研究实践。

**适合谁**：想看“多个 agent 跑完整研究生命周期会长什么样”的研究者。研究架构参考、不是 production 工具。

**备注**：产出是 demo 级别（不是直接投稿用），ML / CS 领域偏多。License 是自定义的 source-available 条款（含 manuscript-disclosure 规定），使用前请先读 LICENSE 文件。

---

> 还缺：peer-review 自动化、conference review pipeline 的活跃开源案例。如果你做过或知道有，欢迎开 PR。

## 必修阅读

1. [The Effortless Academic — Claude Code beginner guides](https://effortlessacademic.com/claude-code-and-cowork-for-academics-beginner-guide-part-1/)
2. [Pedro Sant'Anna — Researcher setup guide](https://paulgp.substack.com/p/getting-started-with-claude-code)

## 必练流程（按使用频率）

研究者用 AI 的最大误区是“只在卡关才打开 ChatGPT”。把 AI 变成日常工具的关键是**设好频率**——下表 7 条都是维护者自己每周都在跑的，不是空想。

| 频率 | 流程 | 怎么做（≤ 3 步） | 推荐工具 | 适合谁 |
|---|---|---|---|---|
| **每天** | 文献 inbox 分流 | (1) 把昨天看到的 paper 丢 paper-qa<br>(2) 抓 claim + 4-5 行 summary<br>(3) 进 Zotero / Obsidian | paper-qa + zotero-gpt | 全研究者 |
| **每天** | 写作 sprint（25 min） | (1) 写一段给 Claude.ai<br>(2) 跑 banned-word + figure-text audit<br>(3) 改完进 main draft | Claude.ai + academic-writing-skills | 写 paper 阶段 |
| **每周** | 跨 paper synthesis | (1) 把 5-10 篇 PDF 喂 Gemini<br>(2) 问“这几篇 disagree 在哪”<br>(3) 写成 1 页 brief | Gemini CLI（1M context） | 计算型 |
| **每周** | Zotero 整理 | (1) 标未读 / 已读<br>(2) 重 tag<br>(3) 抓出该归档的 PDF | zotero-skills 或 zotero-gpt | 全研究者 |
| **每月** | 研究进度 brief | (1) 从 Obsidian + Zotero + NotebookLM 抓近期笔记<br>(2) 整理出 5 个进度点<br>(3) 送指导教授 | research-hub | 同时用 3 工具的人 |
| **Per paper** | 投稿前 final audit | (1) banned-word audit<br>(2) figure-text coupling check<br>(3) submission checklist | academic-writing-skills | 投稿前 1 周 |
| **Per paper** | Multi-agent peer review | (1) Claude 看 logic / argument<br>(2) Codex 看 code / table 数字<br>(3) Gemini 看 prose / clarity | codex-delegate + Gemini CLI | 投稿前 second-opinion |

> 💡 **新手起手式**：先做“每天 inbox 分流”+“写作 sprint”两条一个月，习惯后再加进阶流程。一次装太多会养不起来。

## 层级建议

研究者不需要一开始就装 Claude Code。下表是建议的进阶路径：

| Tier | 工具 | 适合谁 | 学习成本 |
|---|---|---|---|
| **Tier 0** | Claude.ai 网页版 + NotebookLM | 非程序背景、人文社科、临床研究 | 0（会用浏览器就行） |
| **Tier 1** | Claude Desktop + Zotero MCP / Obsidian MCP | 已有 Zotero / Obsidian 习惯的研究者 | 半天装好 |
| **Tier 2** | Claude Code + ai-research-skills | 计算型研究者、写 / 改程序为主 | 1-2 天上手 |
| **Tier 3** | Claude Code + codex-delegate + Gemini CLI + research-hub | 想跑 multi-LLM 研究 pipeline、跨多工具集成 | 1 周 setup + 持续调 |

**多数研究者停在 Tier 1-2 就够了**——Tier 3 是有大量重复流程（比如每周跑同样的 paper synthesis）才值得。
