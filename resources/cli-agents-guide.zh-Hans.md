> [繁體中文](./cli-agents-guide.md) | **简体中文** | [English](./cli-agents-guide.en.md)

# CLI Agents 比较指南

> [← 回主路线 README](../README.zh-Hans.md)

> 📌 **这份是 reference doc**（深度比较、选择逻辑、坑、推荐搭配）。
> 第一次接触 CLI agent、想要 step-by-step 上手 → 看 [`tracks/cli/A1-cli-intro.zh-Hans.md`](../tracks/cli/A1-cli-intro.zh-Hans.md)（Track A 第一站）。
> 想先理解“为什么有的 agent 在 terminal、有的在 Telegram、有的在 Jetson”这层 mental model → 看 [`resources/agent-paradigms.zh-Hans.md`](agent-paradigms.zh-Hans.md)（5 种 agent 型态）。
> 已经在用、想决定 / 比较 / 升级 → 留在这份。

跨 5 个 branch + Track A 共用的参考——**Claude Code / Codex / OpenCode / Gemini CLI / goose / Aider / Hermes Agent / Grok Build 之间怎么挑？** Track A（A1-A3）的 CLI workflow 设计、5 条 branch 内的 CLI 引用都连到这份；每个 branch 都会用到 CLI agent，但没有一个 branch 真的“拥有”这份比较，所以放在 `resources/`。

## 📋 8 个主流 CLI agent

只列在 terminal 跑的（IDE-based 如 Cursor / Cline / Continue 不在这份；那些放在 [for-developer](../branches/for-developer.zh-Hans.md)）。前 6 个数字 `gh api` 验证于 2026-05-06；Hermes Agent 验证于 2026-05-10；Grok Build 验证于 2026-07-16（⚠️ 2026-07-14 才开源、非常新，数字与功能都还在快速变动）。

| 工具 | 提供者 | License | 主推 LLM | 认证 / 计费 | Stars |
|---|---|---|---|---|---|
| [Claude Code](https://github.com/anthropics/claude-code) | Anthropic（官方） | NOASSERTION | Claude | Claude 订阅 **或** Anthropic Console API key | ★ 140k+ |
| [Codex](https://github.com/openai/codex) | OpenAI（官方） | Apache-2.0 | GPT 系列 | ChatGPT 账号登录 **或** OpenAI API key | ★ 105k+ |
| [OpenCode](https://github.com/sst/opencode) | 社群（repo 已迁至 `anomalyco/opencode`） | MIT | 任意（多 provider） | BYO API key 或 OpenCode Zen 内建 hosted | ★ 190k+ |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Google（官方） | Apache-2.0 | Gemini | 免费额度宽，超出收费 | ★ 103k+ |
| [goose](https://github.com/block/goose) | Agentic AI Foundation（repo 已迁至 `aaif-goose/goose`） | Apache-2.0 | 15+ provider（含 Ollama） | BYO API key 或既有 Claude / ChatGPT / Gemini 订阅（ACP） | ★ 51k+ |
| [Aider](https://github.com/Aider-AI/aider) | Aider-AI（社群） | Apache-2.0 | 任意 | BYO API key | ★ 47k+ |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Nous Research | MIT | 200+ via OpenRouter / NVIDIA NIM / 智谱 GLM / Kimi / 小米 MiMo / MiniMax / HF / OpenAI | BYO API key（多 provider） | ★ 224k+ |
| [Grok Build](https://github.com/xai-org/grok-build) | SpaceXAI（xAI，官方） | Apache-2.0 | Grok | 首次启动开浏览器完成登录 | ★ 25k+ |

---

## 🎯 该选哪个？依 use case 决定

### 写 paper / 文献 / 研究
**首推**：Claude Code（长 context、reasoning 强、挡幻觉扎实）。Gemini CLI 是备选——它的百万 token 适合丢整本 PDF / dataset 进去问。

### 写 code / 改 codebase
**首推**：Aider（git-native——每次改完自动 commit，方便 revert）或 Claude Code。OpenCode 适合需要在多 LLM 间切的场景。

### 隐私 / offline / 不送云端
**首推**：goose 或 OpenCode + 本地 Ollama。两个都支持 BYO LLM，可以接 `http://localhost:11434/v1`（Ollama 默认）。

### 已订 ChatGPT Plus / Pro
**首推**：Codex——同一个账号就能用，不另外付费。

### 用 Google 生态 + 想要 1M token 长 context
**首推**：Gemini CLI。免费额度宽、长 context 是强项。注意：Google 服务（Gmail / Drive / Docs）的集成靠 MCP 扩展，不是内建——跟其他 CLI 一样需要安装 MCP server。

### 不想被 vendor lock-in
**首推**：OpenCode > goose > Aider。三个都不绑特定 provider，模型可换。

### 第一次装 CLI agent，先试手感
**首推**：Claude Code。生态广泛、CLAUDE.md 机制让 prompt 可以版本控制、出问题时社群资源多。

### 想跑在 cloud VM、用 Telegram / Slack 等多平台跟它聊 + 用中国大陆 LLM
**首推**：Hermes Agent。差异化在三件事：

- **不绑 laptop**——agent 跑在 $5 VPS / Modal serverless，你从 Telegram / Discord / Slack / WhatsApp / Signal 任一个介面对话
- **多 LLM 中性**——支持 GLM / Kimi / 小米 MiMo / MiniMax，刚好对应 11 中文圈生态
- **内建 self-improving skill loop + cron 排程**——agent 跟你互动久了会自动生成 skill，跨 session 持续优化
- ⚠️ skill 自动演化是 frontier feature，目前缺独立审计；对 production 任务建议先在低风险场景试

---

## 📝 跨 CLI 都通用的 prompt 写法

如果想让 prompt 在不同 CLI 之间 portable（或想随时换工具不重写），照这几条原则：

1. **明确指定文件路径**——“修改 `src/auth.py`”比“修改那个 auth 档”好
2. **要求多步骤拆解**——`先列 plan、确认后再动手`，所有 CLI 都吃这个结构
3. **避免依赖特定 CLI 的 magic 指令**——`/init` `/compact` 是 Claude Code 专属，OpenCode 没有
4. **用 `.cursorrules` / `CLAUDE.md` / `AGENTS.md` 记持续性偏好**——Claude Code 用 `CLAUDE.md`，Codex 用 `AGENTS.md`，OpenCode 用 `OPENCODE.md`，**内容可以一样**
5. **明确要 review 的 scope**——“只 review 我这次的 diff”vs “review 整个 repo”

跨 CLI 写的 prompt 通常会比 CLI-specific prompt 麻烦 5-10%，但好处是切换工具时不用重写。

---

## ⚠️ 常见坑

### File path 处理
- Windows 路径用反斜线（`C:\Users\...`），多数 CLI 内部会转，但有时会搞混
- 建议：在 git-bash / WSL 下用 forward slash，避免奇怪 quoting

### git 集成差异
- **Aider** 自动 commit 每次改动（这是它的设计，不是 bug）
- **Claude Code / Codex / OpenCode / goose** 默认不自动 commit，需要手动或 prompt 要求

### Sandbox 默认值（每个 CLI 文件略有差异，使用前请对照官方文件）
- **Claude Code**：bash 写入默认限定 cwd，读取范围较广（被 deny rule 排除的除外）
- **Codex**：版本控制目录建议 `Auto`（workspace-write + on-request 提权）；非 git 目录建议 `read-only`
- **goose / OpenCode**：相对宽松——建议自己加 sandbox / approval 设置，不要靠默认

### Token cost 累积
- 在大 codebase 上跑 `grep` 一次可能消耗 10 万+ token
- 在大 PDF 上摘要可能 50 万 token（Gemini 适合，其他要 cost-aware）
- 建议：每次操作前估 cost；订 monthly cap

### 多 CLI session 互相干扰
- 同一个 repo 开两个 CLI（譬如 Claude Code + Aider），改档可能 race condition
- 建议：一个 repo 一个 CLI（除非真的有并行需求）

---

## 🔧 实用搭配（real-world setup）

下面 3 个常见搭配，挑一个合的场景：

### Setup A：Claude Code 主推 + OpenCode 备援
- Claude Code 处理日常 90%（写 code、写 doc、debug）
- OpenCode 接 Ollama，处理隐私数据（医疗记录、财务分析）
- 一个 prompt 写一次，两边都能跑

### Setup B：Codex（GPT）+ Aider（Claude）混用
- Codex 处理 ChatGPT Plus 额度内的小事
- Aider 接 Claude API key 处理大重构（git-native commit 方便）
- 两个账单分开算、互不影响

### Setup C：Gemini CLI 主推（给长 context 场景）
- 整本 PDF / 整个 codebase 一次喂进去
- 加 Aider 处理需要精确 git diff 的场景
- 适合学者、知识工作者

### Setup D：Hermes Agent + 本地 Ollama（多平台 + 中国大陆 LLM + offline）
- **Hermes Agent** 跑在 $5 VPS 或自己的机器上，当作多平台 agent gateway
- **LLM endpoint** 用 Ollama（`http://localhost:11434/v1`），也可以改接 z.ai GLM / Kimi 等 provider
- **聊天入口** 用 Telegram / Slack / Discord；Hermes 负责把平台消息转进 agent workflow
- **完全不想接 Anthropic / OpenAI** 时，这条路线适合做离线、隐私资料、低成本重复实验
- Step-by-step 做法看 [`resources/cookbook.zh-Hans.md` Recipe 6](cookbook.zh-Hans.md#6-本地-llm--cli-agent-快速-walkthrough)

---

## 从这份指南连回各 branch

不同 audience 对 CLI 的需求不一样：

- **[for-developer](../branches/for-developer.zh-Hans.md)**：除了 CLI，也看 IDE-based agents（Cursor、Cline、Continue）
- **[for-everyday-users](../branches/for-everyday-users.zh-Hans.md)** Tier 2：CLI 是进阶选项，先试 Tier 0 / 1 的 Web / Desktop App
- **[for-researcher](../branches/for-researcher.zh-Hans.md)**：除了 CLI，也看 paper-specific 工具（paper-qa、gpt-researcher、ChatPaper）
- **[for-knowledge-worker](../branches/for-knowledge-worker.zh-Hans.md)**：除了 CLI，也看 workflow 自动化（n8n、Make）
- **[for-teacher](../branches/for-teacher.zh-Hans.md)**：CLI 对教师偏进阶；建议先看 prompt 素材库

---

## 维护备注

- 8 个 CLI 的 stars / license / pushed_at 由 `weekly-catalog-refresh` CI 每周自动更新（手动可跑 `python scripts/refresh-stars.py`）
- CLI 工具市场变化快——新工具出现要评估是否加入这份比较（门槛：> 30k stars + 维护中 + 真的 CLI 不是 IDE；官方大厂或极新的 CLI 可破例、如 Grok Build）
- 比较表格的“强项 / 弱项”栏位刻意没填——避免产生主观 bias，让 use case section 跟读者自己的判断做这件事
