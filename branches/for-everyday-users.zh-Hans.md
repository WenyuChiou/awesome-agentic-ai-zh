# 日常用户延伸路线（For Everyday Users）

> [繁體中文](./for-everyday-users.md) | **简体中文** | [English](./for-everyday-users.en.md)

> 🚀 **日常用户可直接从 Tier 0 开始**（网页 / 手机 App）、**不需要任何 setup**。只有当你想跑本地 LLM（Tier 3）或用 CLI 自动化（Tier 2）时，才需要看 [`resources/setup-guide.zh-Hans.md` A-C](../resources/setup-guide.zh-Hans.md)（30 分钟从零装好）。

> [← 回主路线 README](../README.zh-Hans.md) · 你**不一定要走完主干**才能从这里开始——这条分支是给“**只想 USE AI、不一定要 BUILD agent**”的人。

## 使用场景（生活场景 × AI 怎么帮）

下表把日常用户一天会遇到的 7 个场景拆开——多数场景在网页版（Tier 0）就能搞定：

| 场景 | 你常遇到的痛点 | AI 能帮的部分 | 推荐工具 |
|---|---|---|---|
| **写 email / cover letter** | 卡在“该怎么开头” | 起草 + 改语气 + 多版本对比 | Claude.ai / ChatGPT |
| **学新技能** | 教材太正式、没人问问题 | 个性化 tutor、可随时打断问 | Claude.ai / ChatGPT |
| **练语言** | 没对话对象、不知道语法错哪 | 语音对话、即时纠错 | ChatGPT Voice / Gemini |
| **查资料 / 比较** | 不知道该信哪个来源 | 多源搜索 + 附引用 | Perplexity |
| **整理生活流程** | 食谱 / 行程 / 待办清单散落 | 整合 + 结构化 | Claude.ai / ChatGPT |
| **批量整理文件** | 100 个 PDF / 图片不知道怎么分 | 重命名 + 分类 + 摘要 | Claude Desktop / Claude Code |
| **隐私敏感 chat** | 医疗 / 法律 / 财务笔记不想送云 | 本地跑 LLM | Ollama + qwen2.5 |

> 💡 **不要被催着升级**：前 5 个场景都可以停在 Tier 0（网页版）。只有要“重复跑同一个流程”或“数据绝对不能送云”才需要 Tier 1-3。

## 起步：你应该从哪一层进入？

按“**动手意愿**”分 4 层，从低到高：

```
Tier 0：网页 / 手机 App（推荐从这里开始）
   ↓
Tier 1：Desktop App（要处理本地文件再升级）
   ↓
Tier 2：CLI Agent（愿意学一点命令行，能自动化日常流程）
   ↓
Tier 3：本地 LLM（隐私敏感、API 费用敏感、想 offline）
```

**多数人停在 Tier 0 / Tier 1 就够用了**——Tier 2-3 是给有特殊需求或想学的人。

---

## 🎯 精选 Projects

### Tier 0 — 网页 / 手机 App ⭐ 入门

#### [Claude.ai](https://claude.ai) ⭐⭐⭐⭐⭐
Anthropic 官方界面。长文章、深度讨论、复杂问题很适合用——回答风格较收敛、不太瞎掰。

#### [ChatGPT](https://chatgpt.com) ⭐⭐⭐⭐⭐
OpenAI 官方界面。生态最广（GPTs、Custom Instructions、Voice mode）。一般用途的标准选择。

#### [Gemini](https://gemini.google.com) ⭐⭐⭐⭐
Google 出品。长 context（一次能读很长文件、约一本厚书的量）特别适合丢整本 PDF 进去问问题；仍要自己检查引用与摘要是否正确。集成 Google 服务（Gmail、Docs）。

#### [Perplexity](https://perplexity.ai) ⭐⭐⭐⭐
搜索引擎 × LLM——每个答案都附引用来源。比 ChatGPT 适合“需要查最新信息”的场景。

---

### Tier 1 — Desktop App

#### [Claude Desktop](https://claude.ai/download) ⭐⭐⭐⭐⭐
比网页版多了：拖文件进去、本地文件读取、保留长期对话脉络。**也是进入 AI 工具整合生态（MCP）的入口**——可以接 Slack / Gmail / 日历，让你在 Claude 里直接操作这些服务。

#### [ChatGPT Desktop](https://chatgpt.com/download/) ⭐⭐⭐⭐
ChatGPT 桌面版。可以对屏幕截图问问题、语音对话、跟其他 App 集成。

---

### Tier 2 — CLI Agent（愿意学命令行的进阶用户）

> 这些工具虽然定位给开发者，但**日常用户也能用**——例如批量重命名文件、整理下载文件夹、自动写每周回顾、把 PDF 摘要存成 Markdown。
>
> 想知道哪种 CLI agent 适合你？见 [`resources/cli-agents-guide.zh-Hans.md`](../resources/cli-agents-guide.zh-Hans.md)（依工作方式选工具、常见坑、实用搭配）。
>
> 想要 step-by-step 上手？见 [`tracks/cli/A1-cli-intro.zh-Hans.md`](../tracks/cli/A1-cli-intro.zh-Hans.md)（Track A 第一站，从安装到第一个任务）。
>
> 想把 CLI agent 接到你的 Notion / Obsidian / Excel / Google 文件等日常工具？见 [`resources/mcp-skills-catalog.zh-Hans.md`](../resources/mcp-skills-catalog.zh-Hans.md)（按分类整理 81+ 个 MCP server / Skill）。

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 138k+ — Anthropic 官方的 CLI agent。能读写文件、执行指令、做多步骤任务。**日常用户最容易上手的 CLI 工具**。

#### [openai/codex](https://github.com/openai/codex) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 115k+ |
| License | Apache-2.0 |

**教什么**：OpenAI 出品的终端机 agent——可以在命令行帮你整理文件、批量处理文字、执行多步骤任务；写程序只是其中一种用途。跟 Claude Code 同类，但用的是 OpenAI 的模型。

**适合谁**：已经订 ChatGPT Plus / Pro，想在终端机用同一个账号做事的人。

#### [anomalyco/opencode](https://github.com/anomalyco/opencode) ⭐⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 196k+ |
| License | MIT |

**教什么**：开源版的 coding agent，**不绑定特定 LLM provider**——可以用 Claude、GPT、Gemini、本地 Ollama 任何一个。社群维护、迭代速度快。

**适合谁**：想 self-host、不想被 API provider 绑定，或要在多个 LLM 之间切换的人。

#### [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) ⭐⭐⭐⭐

| 栏位 | 内容 |
|---|---|
| Stars | ★ 103k+ |
| License | Apache-2.0 |

**教什么**：Google 官方的 Gemini CLI agent。把 Gemini 的长 context 跟 Google 生态集成到终端机。

**适合谁**：Google 生态的重度用户（Gmail、Drive、Docs）。

---

### Tier 3 — 本地 LLM（隐私 / 离线 / 省钱）

#### [Ollama](https://github.com/ollama/ollama) ⭐⭐⭐⭐⭐
★ 170k+ — 一行指令跑本地 LLM。隐私敏感数据（病历、合约、家人对话）不适合送去云端时用这个。详见 [Stage 1 — Local LLM 执行](../stages/01-llm-basics.zh-Hans.md)。

#### [LM Studio](https://lmstudio.ai/)
非开源但对非开发者最友好——拖拉界面、不用 command line。Mac / Windows / Linux 都有。

---

### Prompt 素材库

#### [f/prompts.chat](https://github.com/f/prompts.chat) ⭐⭐⭐⭐
★ 161k+ — 社群维护的 prompt 大全。“act as 翻译家 / 履历顾问 / 厨师...”几百种角色。**不知道怎么开头时从这里找灵感**。

---

## 必修阅读

1. [**Anthropic — How to write effective prompts**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — 不用代码也能读的 prompt 写法
2. [**OpenAI — Prompting Guide**](https://platform.openai.com/docs/guides/prompt-engineering) — 对称的官方文件
3. [**ChatGPT 怎么用得最好（中文）**](https://www.runoob.com/) — 各家中文博客的整理（runoob 等等）

如果有兴趣再深入，看 [Stage 2 — Prompt 设计](../stages/02-prompt-engineering.zh-Hans.md)，那边有正式系统性教学。

## 可以建的流程（按使用频率）

下表 5 条是模板，配合你自己的场景调整：

| 频率 | 流程 | 怎么做（≤ 3 步） | 推荐工具 |
|---|---|---|---|
| **每天** | Email 分流 | (1) 早上把待回信件贴进 Claude<br>(2) 请它分类“立即回 / 今天回 / 这周回 / 不用回”<br>(3) 草拟回信让你 review | Claude.ai / ChatGPT |
| **每天** | 练语言（口说） | (1) 打开 ChatGPT Voice 模式<br>(2) 对话练英 / 日<br>(3) 请它指出语法错误 | ChatGPT Voice / Gemini |
| **每周** | 周记整理 | (1) 跟 Claude 讲这周做什么<br>(2) 请它整理成周记 + 下周重点<br>(3) 存到 Obsidian / Notion | Claude.ai |
| **不定期** | 批量整理文件 | (1) Claude Code 进 Downloads 文件夹<br>(2) 按日期 + 主题重命名<br>(3) 自动分到子文件夹 | Claude Code |
| **隐私场景** | 本地医疗 / 法律 / 财务笔记 | (1) Ollama 跑 qwen2.5:7b<br>(2) 整理个人笔记，数据不送云<br>(3) ⚠️ 保护的是**隐私**，不是**正确性**——具体诊断 / 法律判断 / 投资决策仍需专业人士 | Ollama + qwen2.5 |

> 💡 **新手起手式**：先把“每天 Email 分流”+“练语言”做一个月，习惯 AI 在日常的位置，再加其他流程。

## 给日常用户的层级建议

下表是建议的进阶路径：

| Tier | 工具 | 适合谁 | 学习成本 |
|---|---|---|---|
| **Tier 0** | Claude.ai / ChatGPT / Gemini / Perplexity（网页版） | 90% 的场景都在这里——免安装、免付费 | 0（会用浏览器就行） |
| **Tier 1** | Claude Desktop / ChatGPT Desktop + MCP | 要处理本地文件、保留对话历史、接 Gmail / Notion | 半小时装好 |
| **Tier 2** | Claude Code / opencode（CLI） | 有重复自动化需求（每天做同样的事 100 次） | 1-2 天上手 |
| **Tier 3** | Ollama 本地 LLM | 隐私敏感数据不能送云、API 费用敏感、想 offline | 半天设置 |

> **不要被人催着升级**——多数人 Tier 0 就够用了。Tier 2-3 是工具，不是身份地位。

## 社群备注

这条分支也欢迎社群贡献：

- 推荐特定领域的 prompt template（料理、运动、学语言）
- 中文友善的 chat tools（国产 LLM、本地化 wrapper）
- 隐私 / 安全相关的最佳实践（什么数据能送 / 不能送）

详见 [CONTRIBUTING.zh-Hans.md](../CONTRIBUTING.zh-Hans.md)。
