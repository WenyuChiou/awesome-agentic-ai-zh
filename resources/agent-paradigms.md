> **繁體中文** | [简体中文](./agent-paradigms.zh-Hans.md) | [English](./agent-paradigms.en.md)

# Agent 5 種型態 — 你的 agent 跑在哪、為誰服務？

> [← 回主路線 README](../README.md)

> 📌 **這份是 mental model reference**。看完之後你會知道：「同樣叫 agent、為什麼 Claude Code、Hermes Agent、OpenClaw 用起來完全不同感受？」
> 已經知道想用哪個 → [`resources/cli-agents-guide.md`](cli-agents-guide.md)（CLI agent 身分與選擇指南）或 [`resources/cookbook.md`](cookbook.md)（step-by-step 部署）。

「Agent」一詞被用得很泛。Cursor 是 agent、Claude Code 是 agent、Telegram 上跟你聊天的 Hermes 也是 agent、家裡 Jetson 板子跑的 OpenClaw 也是 agent。但這 4 個東西用起來完全不同感受 —— 因為它們屬於**不同 paradigm**。差別不在 LLM 是哪家、而在 **agent 跑在哪、你用什麼介面跟它互動、需不需要連網**。

理解 paradigm 之後你才知道：搬一個 use case 從 Type 2 到 Type 4 不是「換工具」、是**換思考方式**。

---

## 一張表先建立認知

| Type | 代表 | Agent 跑在哪 | 你用什麼介面 | LLM | 離線 OK？ | 月成本（粗估）|
|---|---|---|---|---|---|---|
| **1. IDE-coupled** | Cursor / Cline / Continue | 你 IDE 內 | IDE sidebar | 多 provider | ❌ | $0-20 |
| **2. Terminal pair-programmer** | Claude Code / Codex / Gemini CLI | 你 terminal | terminal REPL | 綁特定家 | ❌ | $20 訂閱 或 API 用量 |
| **3. BYO-LLM CLI** | Aider / OpenCode / goose | 你 terminal | terminal REPL | 自帶 API key | ❌ | API 用量 |
| **4. Cloud-deployed** | **Hermes Agent** | $5 VPS / Modal | **Telegram / Slack / 任一 chat app** | 200+ provider routing | ❌ | $5 server + API |
| **5. Edge-deployed** | **OpenClaw / ClawBox** | Jetson 板子 / Raspberry Pi | local chat / SSH | **本機 Ollama**（Qwen / Llama / Mistral）| **✅** | 一次硬體 €549、之後 0 |

→ 4 跟 5 都是「**deployed autonomous agent**」（agent **不在你 laptop 前**、跑在外面 24×7 serve 你）。4 在 cloud、5 在 edge。剩下的 1-3 是「**co-located agent**」（agent 跟你一起在 laptop 上、你走它停）。

---

## Type 1: IDE-coupled — 「sidebar pair-programmer」

**代表**：[Cursor](https://cursor.com) / [Windsurf](https://codeium.com/windsurf) / [Cline](https://cline.bot) / [Continue](https://continue.dev) / [Zed](https://zed.dev)

**Hero example**：
你在 Cursor 寫一個 React component。左邊 editor、右邊 Cursor sidebar 聊天。你選一段 code 按 `Cmd+K`、Cursor 就地改寫。改完之後你看 inline diff、accept/reject。

**為什麼這型存在**：寫 code 的時候你**眼睛要看 code**、不能去 terminal 對話。IDE-coupled agent 把 LLM 放在你視線旁邊、保留視覺 context。

**適合**：edit 多、explore 少；side-by-side coding；需要 visual diff。
**不適合**：需要 agent 自己跑多步驟（agent 在 sidebar 不太自由）；non-coding task。

---

## Type 2: Terminal pair-programmer — 「Claude Code paradigm」

**代表**：[Claude Code](https://github.com/anthropics/claude-code) / [Codex](https://github.com/openai/codex) / [Gemini CLI](https://github.com/google-gemini/gemini-cli)

**Hero example**：
你在 terminal 開 Claude Code、輸入「refactor 整個 auth module、把 callback 改成 async/await、跑 tests」。Claude Code 自己讀檔、改檔、跑 pytest、報告結果。整個過程 5-10 分鐘、你看 streaming output。

**為什麼這型存在**：Claude Code / Codex 把整個 terminal 變成 agent 的 workspace。agent 有 file system / shell / git 完整 access、可以自主完成多步驟 task。比 Type 1 更 autonomous。

**特色**：訂閱制（$20/月可用整月、不算 token）；綁定特定 LLM 家族（Claude Code = Claude only）。

**適合**：agentic task；長 refactor；paper writing；任何 1-2 step 之上的工作。
**不適合**：跨多家 LLM 比較成本；非 coding/writing 場景；offline。

---

## Type 3: BYO-LLM CLI — 「multi-provider 同 mental model」

**代表**：[Aider](https://aider.chat) / [OpenCode](https://github.com/anomalyco/opencode) / [goose](https://block.github.io/goose) / [Hermes Agent](https://github.com/NousResearch/hermes-agent)*

**Hero example**：
你想用 DeepSeek-V4-Pro（前身 R1 reasoning lineage 已併入主線）寫 code（比 Claude Opus 便宜約 10×）。Aider 設 `--model deepseek/deepseek-v4-pro` + `OPENROUTER_API_KEY` 就能跑、git-aware、commit message 自動寫。

**跟 Type 2 的差別**：Type 2 綁特定家、Type 3 你帶 API key、任何 OpenAI-compatible endpoint 都行。

**特色**：cost-sensitive；多 provider 比較；自架 LLM（Ollama / vLLM）也能用。

**適合**：實驗多家 LLM；省 cost；本機 LLM；不想被一家綁。
**不適合**：怕 setup 複雜（要管 API key、provider config）。

*Hermes Agent 既屬於 Type 3（CLI mode）也屬於 Type 4（cloud mode）—— 取決於你怎麼部署。下面細講。

---

## Type 4: Cloud-deployed — 例：Hermes Agent

**代表**：[Hermes Agent](https://github.com/NousResearch/hermes-agent)（Nous Research、★ 224k+、MIT）

**Hero example**：
你坐在地鐵、手機開 Telegram、對 Hermes bot 說「整理今天 arXiv ML 新 paper、給我 3 個 highlights、傳回 Telegram」。Hermes agent 在你 $5 DigitalOcean VPS 上跑、收訊息、決定該用 GPT-5（找 paper）+ Claude Opus（寫 summary）+ Gemini Flash（壓縮成 3 條）、執行完傳結果回 Telegram。整個過程你沒碰 laptop。

**5 個 distinctive feature**：

1. **Multi-platform chat interface**：Telegram / Discord / Slack / WhatsApp / Signal 都能當入口。你在哪個平台 ping、agent 就在哪回。
2. **Multi-LLM routing（200+ model neutral）**：OpenRouter + NVIDIA NIM + 智譜 GLM + Kimi + 小米 MiMo + MiniMax + HF + OpenAI + Anthropic + Google。**同一 conversation 內可跨 LLM**。
3. **24/7 在線**：agent 不依賴你 laptop、cloud VPS host、任何時刻可用。
4. **Built-in cron**：「每天 9am 抓 X 給我 Y」這種 routine 直接內建。
5. **自我學習技能**（實驗中、尚未獨立審計）：agent 跟你互動久了、會自動歸納出可重用的 skill、跨 session 累積演化。

**為什麼這型存在**：當 agent 是「**個人助理**」而不是「pair programmer」時、它不該綁你 laptop。Type 4 把 agent 變成 24×7 service。

**特色**：deployment cost ~$5/月 VPS + API；中國圈 LLM 支援（GLM / Kimi）—— 國際服務中斷時可以改用這些接力。

**Trade-off**：

- ⚠️ 自我學習技能是新功能、還沒經過獨立安全檢驗；用在會造成嚴重後果的任務（醫療 / 法律 / 金流）前先別開
- 失去 IDE / terminal 的 file system 直接讀寫便利、變成 chat-first workflow
- 需要會 self-host VPS（Linux / docker / systemd 基礎）

**適合**：跨平台通知；24/7 routine（每天抓 paper / 看股票 / 提醒）；中國圈 LLM；多 LLM cost optimization；非 laptop-bound 工作流。
**不適合**：純寫 code（Type 2 native）；不想 self-host；對 production reliability 要求高。

---

## Type 5: Edge-deployed — 例：OpenClaw / ClawBox

**代表**：[OpenClaw](https://www.jetson-ai-lab.com/tutorials/openclaw/)（社群、Jetson 生態） / [ClawBox](https://openclawhardware.dev/)（€549 預裝 Jetson 套件、67 TOPS）

**Hero example**：
你是法律事務所、要 AI 幫你整理當事人病歷 + 醫療記錄 + 醫師證詞、產出時序表。**但這些資料絕對不能上 cloud**。你買一台 ClawBox（NVIDIA Jetson Orin Nano + 預裝 OpenClaw + Ollama + Qwen 3.5 7B）、放在事務所網路內、SSH 進去跟它工作。所有資料只在這台 €549 的盒子裡、無 telemetry、無 API call、完全可審計。

**5 個 distinctive feature**：

1. **Hardware-specific**：NVIDIA Jetson 系列（Orin Nano 8 GB、Thor 128 GB）或 Raspberry Pi。GPU 加速、邊緣推論。
2. **本機 LLM only**：Ollama backend、跑 Qwen 3.5 2B-7B / Llama / Mistral / Gemma 等 open-weight。**沒有任何 cloud API call**。
3. **零雲端依賴 / 完全可審計**：localhost-bound、network-isolated 可用、無 telemetry。
4. **Edge-optimized memory**：semantic search memory file < 10 MB、跨 session 記憶（例：[openclaw-memory-enhancer](https://github.com/henryfcb/openclaw-memory-enhancer)）。
5. **Physical AI bridge**：可控物理 device（robot / sensor / smart home）—— agent 跨 physical + digital 環境。

**為什麼這型存在**：當資料**不能離開本機**時（醫療 / 法律 / 軍工 / 隱私敏感）、cloud-deployed 不是選項。Type 5 把 agent 完全 on-device、用 €549 換 0 cloud cost + 0 data exposure。

**特色**：一次硬體投資、之後 API 0 元；對應 NVIDIA 邊緣硬體生態；Jetson Thor 跑 30B model 也 OK。

**Trade-off**：

- 模型受邊緣 hardware 限制（Orin Nano 跑 7B 上限、Thor 才到 30B）
- Setup 比 cloud 複雜（要會 NVIDIA Jetson 環境、JetPack、Docker、Ollama）
- 沒有 cloud-deployed 的 24/7 跨平台便利

**適合**：隱私敏感資料；offline-first；家用 AI box（smart home）；physical AI（robot）；長期持有、不想付 API recurring cost。
**不適合**：不會 Linux / NVIDIA 環境；需要前沿 model（GPT-5 / Claude Opus）；不想花 €549。

---

## Subagent — 「在 agent runtime 裡再 spawn agent」

上面 5 個 type 講的是 **agent 跑在哪裡**（IDE / Terminal / 任意 CLI / Cloud / Edge）。**Subagent** 是另一個維度：**一個 agent 在執行任務時、spawn 出另一個 agent 跑子任務**。

主要兩種實作路徑：

| 路徑 | 怎麼啟動 | 代表 |
|---|---|---|
| **Framework-based**（Stage 4） | `pip install langgraph / crewai / autogen` + Python orchestration code | LangGraph / CrewAI / AutoGen / Swarm / Strands |
| **Claude Code 原生**（Stage 5.5） | 寫 `.claude/agents/<name>.md`、主 session 用 Task tool invoke | Claude Code subagent + Claude Agent SDK |

**差別在 runtime ownership**：

- Framework path：你用 Python 寫一支主程式（orchestrator）來調度、每個 sub-agent 都是這支程式裡的物件
- Claude path：Claude Code 自動建立新的子 agent、主 agent 只拿到子 agent 的最終結果、不用管它的內部過程（context 自動隔離、互不干擾）

**選哪個**：要跨 LLM provider（GPT + Claude + Gemini 混用）或要把 multi-agent 包進別的應用程式 → framework path。已 commit Claude Code、只在 Claude 生態 → subagent path（少很多 boilerplate）。

完整對照表見 [Stage 5.5 開頭](../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)；**想直接看 15 個 daily dispatch recipe** → [`subagent-cookbook.md`](./subagent-cookbook.md)（每個含情境 + 用哪個 subagent + 複製即用的 prompt 範本）。

---

## 跨型態組合（power user pattern）

真實 user 常常**同時用 2-3 個 type**、各做擅長的事：

![個人 power-user 多 type workflow](../resources/diagrams/power-user-multi-type-workflow.png)

**為什麼這樣搭**：

- Type 2 處理 code（terminal 介面最自然）
- Type 4 處理 routine + 跨平台（laptop 沒開時也工作）
- Type 5 處理隱私（不可上 cloud）

---

## Decision tree（簡化文字版）

![選哪個 agent type 決策樹](../resources/diagrams/agent-paradigm-decision-tree.png)

---

## 跟既有 stage / branch 的連結

- **想學 Type 2 上手** → [Stage 5: Claude Code 生態](../stages/05-claude-code-ecosystem.md)
- **想選擇適合的 CLI agent**（Type 2 + Type 3）→ [`resources/cli-agents-guide.md`](cli-agents-guide.md)
- **想看 IDE-coupled 對比**（Type 1）→ [`branches/for-developer.md`](../branches/for-developer.md)
- **想 step-by-step 部署 Hermes** → [`resources/cookbook.md` Recipe 6](cookbook.md)（含 Hermes + Ollama walkthrough）
- **想搞 Jetson + OpenClaw** → [Jetson AI Lab tutorial](https://www.jetson-ai-lab.com/tutorials/openclaw/) + [Seeed Studio wiki](https://wiki.seeedstudio.com/local_openclaw_on_recomputer_jetson/)

---

## 我自己怎麼用

- **每天主開發**：Type 2（Claude Code、訂閱制）
- **paper monitoring**：暫時手動（每週手動掃 arXiv）—— 之後想試 Type 4 Hermes 自動化
- **research vault**：Claude Code 在 laptop 內呼叫 [research-hub](https://github.com/WenyuChiou/research-hub) pipeline（Type 2 模式）
- **沒接觸 Type 5**：目前資料沒到「不能上 cloud」的敏感程度

Type 4 / Type 5 你之後玩了、可以再回來補這份 reference 自己的 use case。

---

## References

- [Jetson AI Lab: OpenClaw tutorial](https://www.jetson-ai-lab.com/tutorials/openclaw/)
- [ClawBox hardware](https://openclawhardware.dev/)
- [NVIDIA: Jetson Generative AI at the Edge](https://blogs.nvidia.com/blog/jetson-generative-ai-edge-oss/)
- [Hermes Agent (NousResearch)](https://github.com/NousResearch/hermes-agent)
- [claw-spark: One-click setup for Jetson / DGX Spark / RTX](https://github.com/theshiphq/claw-spark)
