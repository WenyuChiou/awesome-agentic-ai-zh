> [繁體中文](./agent-paradigms.md) | **简体中文** | [English](./agent-paradigms.en.md)

# Agent 5 种型态 — 你的 agent 跑在哪、为谁服务？

> [← 回主路线 README](../README.zh-Hans.md)

> 📌 **这份是 mental model reference**。看完之后你会知道：“同样叫 agent、为什么 Claude Code、Hermes Agent、OpenClaw 用起来完全不同感受？”
> 已经知道想用哪个 → [`resources/cli-agents-guide.zh-Hans.md`](cli-agents-guide.zh-Hans.md)（CLI agent 身份与选择指南）或 [`resources/cookbook.zh-Hans.md`](cookbook.zh-Hans.md)（step-by-step 部署）。

“Agent”一词被用得很泛。Cursor 是 agent、Claude Code 是 agent、Telegram 上跟你聊天的 Hermes 也是 agent、家里 Jetson 板子跑的 OpenClaw 也是 agent。但这 4 个东西用起来完全不同感受 —— 因为它们属于**不同 paradigm**。差别不在 LLM 是哪家、而在 **agent 跑在哪、你用什么界面跟它互动、需不需要联网**。

理解 paradigm 之后你才知道:搬一个 use case 从 Type 2 到 Type 4 不是“换工具”、是**换思考方式**。

---

## 一张表先建立认知

| Type | 代表 | Agent 跑在哪 | 你用什么界面 | LLM | 离线 OK? | 月成本（粗估）|
|---|---|---|---|---|---|---|
| **1. IDE-coupled** | Cursor / Cline / Continue | 你 IDE 内 | IDE sidebar | 多 provider | ❌ | $0-20 |
| **2. Terminal pair-programmer** | Claude Code / Codex / Gemini CLI | 你 terminal | terminal REPL | 绑特定家 | ❌ | $20 订阅 或 API 用量 |
| **3. BYO-LLM CLI** | Aider / OpenCode / goose | 你 terminal | terminal REPL | 自带 API key | ❌ | API 用量 |
| **4. Cloud-deployed** | **Hermes Agent** | $5 VPS / Modal | **Telegram / Slack / 任一 chat app** | 200+ provider routing | ❌ | $5 server + API |
| **5. Edge-deployed** | **OpenClaw / ClawBox** | Jetson 板子 / Raspberry Pi | local chat / SSH | **本机 Ollama**（Qwen / Llama / Mistral）| **✅** | 一次硬件 €549、之后 0 |

→ 4 跟 5 都是“**deployed autonomous agent**”（agent **不在你 laptop 前**、跑在外面 24×7 serve 你）。4 在 cloud、5 在 edge。剩下的 1-3 是“**co-located agent**”（agent 跟你一起在 laptop 上、你走它停）。

---

## Type 1: IDE-coupled — “sidebar pair-programmer”

**代表**:[Cursor](https://cursor.com) / [Windsurf](https://codeium.com/windsurf) / [Cline](https://cline.bot) / [Continue](https://continue.dev) / [Zed](https://zed.dev)

**Hero example**:
你在 Cursor 写一个 React component。左边 editor、右边 Cursor sidebar 聊天。你选一段 code 按 `Cmd+K`、Cursor 就地改写。改完之后你看 inline diff、accept/reject。

**为什么这型存在**:写 code 的时候你**眼睛要看 code**、不能去 terminal 对话。IDE-coupled agent 把 LLM 放在你视线旁边、保留视觉 context。

**适合**:edit 多、explore 少;side-by-side coding;需要 visual diff。
**不适合**:需要 agent 自己跑多步骤（agent 在 sidebar 不太自由）;non-coding task。

---

## Type 2: Terminal pair-programmer — “Claude Code paradigm”

**代表**:[Claude Code](https://github.com/anthropics/claude-code) / [Codex](https://github.com/openai/codex) / [Gemini CLI](https://github.com/google-gemini/gemini-cli)

**Hero example**:
你在 terminal 开 Claude Code、输入“refactor 整个 auth module、把 callback 改成 async/await、跑 tests”。Claude Code 自己读档、改档、跑 pytest、报告结果。整个过程 5-10 分钟、你看 streaming output。

**为什么这型存在**:Claude Code / Codex 把整个 terminal 变成 agent 的 workspace。agent 有 file system / shell / git 完整 access、可以自主完成多步骤 task。比 Type 1 更 autonomous。

**特色**:订阅制（$20/月可用整月、不算 token）;绑定特定 LLM 家族（Claude Code = Claude only）。

**适合**:agentic task;长 refactor;paper writing;任何 1-2 step 之上的工作。
**不适合**:跨多家 LLM 比较成本;非 coding/writing 场景;offline。

---

## Type 3: BYO-LLM CLI — “multi-provider 同 mental model”

**代表**:[Aider](https://aider.chat) / [OpenCode](https://github.com/anomalyco/opencode) / [goose](https://block.github.io/goose) / [Hermes Agent](https://github.com/NousResearch/hermes-agent)*

**Hero example**:
你想用 DeepSeek-V4-Pro（前身 R1 reasoning lineage 已并入主线）写 code（比 Claude Opus 便宜约 10×）。Aider 设 `--model deepseek/deepseek-v4-pro` + `OPENROUTER_API_KEY` 就能跑、git-aware、commit message 自动写。

**跟 Type 2 的差别**:Type 2 绑特定家、Type 3 你带 API key、任何 OpenAI-compatible endpoint 都行。

**特色**:cost-sensitive;多 provider 比较;自架 LLM（Ollama / vLLM）也能用。

**适合**:实验多家 LLM;省 cost;本机 LLM;不想被一家绑。
**不适合**:怕 setup 复杂（要管 API key、provider config）。

*Hermes Agent 既属于 Type 3（CLI mode）也属于 Type 4（cloud mode）—— 取决于你怎么部署。下面细讲。

---

## Type 4: Cloud-deployed — 例:Hermes Agent

**代表**:[Hermes Agent](https://github.com/NousResearch/hermes-agent)（Nous Research、★ 224k+、MIT）

**Hero example**:
你坐在地铁、手机开 Telegram、对 Hermes bot 说“整理今天 arXiv ML 新 paper、给我 3 个 highlights、传回 Telegram”。Hermes agent 在你 $5 DigitalOcean VPS 上跑、收讯息、决定该用 GPT-5（找 paper）+ Claude Opus（写 summary）+ Gemini Flash（压缩成 3 条）、执行完传结果回 Telegram。整个过程你没碰 laptop。

**5 个 distinctive feature**:

1. **Multi-platform chat interface**:Telegram / Discord / Slack / WhatsApp / Signal 都能当入口。你在哪个平台 ping、agent 就在哪回。
2. **Multi-LLM routing（200+ model neutral）**:OpenRouter + NVIDIA NIM + 智谱 GLM + Kimi + 小米 MiMo + MiniMax + HF + OpenAI + Anthropic + Google。**同一 conversation 内可跨 LLM**。
3. **24/7 在线**:agent 不依赖你 laptop、cloud VPS host、任何时刻可用。
4. **Built-in cron**:“每天 9am 抓 X 给我 Y”这种 routine 直接内建。
5. **自我学习技能**（实验中、尚未独立审计）:agent 跟你互动久了、会自动归纳出可复用的 skill、跨 session 累积演化。

**为什么这型存在**:当 agent 是“**个人助理**”而不是“pair programmer”时、它不该绑你 laptop。Type 4 把 agent 变成 24×7 service。

**特色**:deployment cost ~$5/月 VPS + API;中国圈 LLM 支持（GLM / Kimi）—— 国际服务中断时可以改用这些接力。

**Trade-off**:

- ⚠️ 自我学习技能是新功能、还没经过独立安全检验；用在会造成严重后果的任务（医疗 / 法律 / 金流）前先别开
- 失去 IDE / terminal 的 file system 直接读写便利、变成 chat-first workflow
- 需要会 self-host VPS（Linux / docker / systemd 基础）

**适合**:跨平台通知;24/7 routine（每天抓 paper / 看股票 / 提醒）;中国圈 LLM;多 LLM cost optimization;非 laptop-bound 工作流。
**不适合**:纯写 code（Type 2 native）;不想 self-host;对 production reliability 要求高。

---

## Type 5: Edge-deployed — 例:OpenClaw / ClawBox

**代表**:[OpenClaw](https://www.jetson-ai-lab.com/tutorials/openclaw/)（社群、Jetson 生态） / [ClawBox](https://openclawhardware.dev/)（€549 预装 Jetson 套件、67 TOPS）

**Hero example**:
你是法律事务所、要 AI 帮你整理当事人病历 + 医疗记录 + 医师证词、产出时序表。**但这些资料绝对不能上 cloud**。你买一台 ClawBox（NVIDIA Jetson Orin Nano + 预装 OpenClaw + Ollama + Qwen 3.5 7B）、放在事务所网络内、SSH 进去跟它工作。所有资料只在这台 €549 的盒子里、无 telemetry、无 API call、完全可审计。

**5 个 distinctive feature**:

1. **Hardware-specific**:NVIDIA Jetson 系列（Orin Nano 8 GB、Thor 128 GB）或 Raspberry Pi。GPU 加速、边缘推论。
2. **本机 LLM only**:Ollama backend、跑 Qwen 3.5 2B-7B / Llama / Mistral / Gemma 等 open-weight。**没有任何 cloud API call**。
3. **零云端依赖 / 完全可审计**:localhost-bound、network-isolated 可用、无 telemetry。
4. **Edge-optimized memory**:semantic search memory file < 10 MB、跨 session 记忆（例:[openclaw-memory-enhancer](https://github.com/henryfcb/openclaw-memory-enhancer)）。
5. **Physical AI bridge**:可控物理 device（robot / sensor / smart home）—— agent 跨 physical + digital 环境。

**为什么这型存在**:当资料**不能离开本机**时（医疗 / 法律 / 军工 / 隐私敏感）、cloud-deployed 不是选项。Type 5 把 agent 完全 on-device、用 €549 换 0 cloud cost + 0 data exposure。

**特色**:一次硬件投资、之后 API 0 元;对应 NVIDIA 边缘硬件生态;Jetson Thor 跑 30B model 也 OK。

**Trade-off**:

- 模型受边缘 hardware 限制（Orin Nano 跑 7B 上限、Thor 才到 30B）
- Setup 比 cloud 复杂（要会 NVIDIA Jetson 环境、JetPack、Docker、Ollama）
- 没有 cloud-deployed 的 24/7 跨平台便利

**适合**:隐私敏感资料;offline-first;家用 AI box（smart home）;physical AI（robot）;长期持有、不想付 API recurring cost。
**不适合**:不会 Linux / NVIDIA 环境;需要前沿 model（GPT-5 / Claude Opus）;不想花 €549。

---

## Subagent — “在 agent runtime 里再 spawn agent”

上面 5 个 type 讲的是 **agent 跑在哪里**（IDE / Terminal / 任意 CLI / Cloud / Edge）。**Subagent** 是另一个维度：**一个 agent 在执行任务时，spawn 出另一个 agent 跑子任务**。

主要两种实作路径：

| 路径 | 怎么启动 | 代表 |
|---|---|---|
| **Framework-based**（Stage 4） | `pip install langgraph / crewai / autogen` + Python orchestration code | LangGraph / CrewAI / AutoGen / Swarm / Strands |
| **Claude Code 原生**（Stage 5.5） | 写 `.claude/agents/<name>.md`，主 session 用 **Agent tool** invoke | Claude Code subagent + Claude Agent SDK |

**差别在 runtime ownership**：

- Framework path：你用 Python 写一支主程序（orchestrator）来调度，每个 sub-agent 都是这支程序里的对象
- Claude path：Claude Code 自动建立新的子 agent，主 agent 只拿到子 agent 的最终结果、不用管它的内部过程（context 自动隔离、互不干扰）

**选哪个**：要跨 LLM provider（GPT + Claude + Gemini 混用）或要把 multi-agent 包进别的应用程序 → framework path。已 commit Claude Code、只在 Claude 生态 → subagent path（少很多 boilerplate）。

完整对照表见 [Stage 5.5 开头](../stages/05-claude-code-ecosystem.zh-Hans.md#55--subagentsclaude-code-原生-multi-agent-机制-2025-新功能)；**想直接看 15 个 daily dispatch recipe** → [`subagent-cookbook.zh-Hans.md`](./subagent-cookbook.zh-Hans.md)（每个含场景 + 用哪个 subagent + 复制即用的 prompt 模板）。

---

## 跨型态组合（power user pattern）

真实 user 常常**同时用 2-3 个 type**、各做擅长的事:

![个人 power-user 多 type workflow](../resources/diagrams/power-user-multi-type-workflow.zh-Hans.png)

**为什么这样搭**:

- Type 2 处理 code（terminal 界面最自然）
- Type 4 处理 routine + 跨平台（laptop 没开时也工作）
- Type 5 处理隐私（不可上 cloud）

---

## Decision tree（简化文字版）

![选哪个 agent type 决策树](../resources/diagrams/agent-paradigm-decision-tree.zh-Hans.png)

---

## 跟既有 stage / branch 的连结

- **想学 Type 2 上手** → [Stage 5: Claude Code 生态](../stages/05-claude-code-ecosystem.zh-Hans.md)
- **想选择适合的 CLI agent**（Type 2 + Type 3）→ [`resources/cli-agents-guide.zh-Hans.md`](cli-agents-guide.zh-Hans.md)
- **想看 IDE-coupled 对比**（Type 1）→ [`branches/for-developer.zh-Hans.md`](../branches/for-developer.zh-Hans.md)
- **想 step-by-step 部署 Hermes** → [`resources/cookbook.zh-Hans.md` Recipe 6](cookbook.zh-Hans.md)（含 Hermes + Ollama walkthrough）
- **想搞 Jetson + OpenClaw** → [Jetson AI Lab tutorial](https://www.jetson-ai-lab.com/tutorials/openclaw/) + [Seeed Studio wiki](https://wiki.seeedstudio.com/local_openclaw_on_recomputer_jetson/)

---

## 我自己怎么用

- **每天主开发**:Type 2（Claude Code、订阅制）
- **paper monitoring**:暂时手动（每周手动扫 arXiv）—— 之后想试 Type 4 Hermes 自动化
- **research vault**:Claude Code 在 laptop 内调用 [research-hub](https://github.com/WenyuChiou/research-hub) pipeline（Type 2 模式）
- **没接触 Type 5**:目前资料没到“不能上 cloud”的敏感程度

Type 4 / Type 5 你之后玩了、可以再回来补这份 reference 自己的 use case。

---

## References

- [Jetson AI Lab: OpenClaw tutorial](https://www.jetson-ai-lab.com/tutorials/openclaw/)
- [ClawBox hardware](https://openclawhardware.dev/)
- [NVIDIA: Jetson Generative AI at the Edge](https://blogs.nvidia.com/blog/jetson-generative-ai-edge-oss/)
- [Hermes Agent (NousResearch)](https://github.com/NousResearch/hermes-agent)
- [claw-spark: One-click setup for Jetson / DGX Spark / RTX](https://github.com/theshiphq/claw-spark)
