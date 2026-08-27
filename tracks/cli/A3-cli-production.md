# A3 — 把 CLI Agent 接進真實工作流程（Integration & Production）

> **繁體中文** | [简体中文](./A3-cli-production.zh-Hans.md) | [English](./A3-cli-production.en.md)

> [← A2 — CLI Workflow Patterns](A2-cli-workflow.md) · **Track A: CLI Power User** 第 3 站（最後）

⏱ **時間估算**：1-2 週（約 8-15 小時）

> 📋 **本章組成**：學習目標 → 進入條件 → 必修閱讀 → 動手練習 → 精選 Projects → 自我檢查
> 🔑 **關鍵名詞**（本章用到）：
> - **本章一定會用**：MCP（讓 CLI 接外部資料 / 工具）、CI（每次 push 自動跑檢查）
> - **延伸閱讀名詞**：observability（追蹤 CLI 行為）、eval（量化 CLI 品質）、prompt caching（重複 context 省錢）、cost tracking（token 花費紀錄）
>
> 完整定義見 [`resources/glossary.md` 5 + 6](../../resources/glossary.md#5-claude-code-生態)。

CLI 跑得順了之後、下一步：**把 CLI 接到你的真實團隊流程**。這節達成 3 件事：

1. **工具連接** — MCP server 把 CLI 接到 Slack / Gmail / 你的 internal API
2. **自動檢查** — CI（GitHub Actions）每個 PR 自動跑 CLI review
3. **成本與紀錄** — observability 工具追蹤每個任務的 cost / latency

這節之後、CLI 不只是你個人在用的工具、而是 team 工作流的一部分。

## 📌 學習目標

- 把 1-3 個 MCP server 接到你的 CLI（Slack / Gmail / 你的 internal API / DB）
- 設定 GitHub Actions 自動跑 Claude Code（PR review、release notes 等）
- 加 observability（trace、cost、latency）到 CLI workflow
- 規劃 cost budget，知道大 task 會花多少 token

## 🚪 進入條件

你應該已經：

- 完成 [A1](A1-cli-intro.md)：CLI 已選好、裝好、認證好
- 完成 [A2](A2-cli-workflow.md)：完成專案規則卡與 review Skill
- 對 GitHub Actions / CI 基礎熟悉（會看 `.yml` workflow）
- 對 MCP 概念有印象（沒有的話先翻 [Stage 5.2](../../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎)）

沒到的話 → 補完 [A1](A1-cli-intro.md) + [A2](A2-cli-workflow.md)。A3 是「組合所有前面學的 → 接到 production」、跳級會看不懂。

## 📚 必修閱讀

1. [**Stage 5.2 — MCP（Model Context Protocol）**](../../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎) — MCP 概念跟基礎
2. [**Anthropic — Prompt Caching**](https://www.anthropic.com/news/prompt-caching) — 在符合快取條件時（context 不變、≤ 5 分鐘 reuse window 等）可大幅降低重複上下文的成本；實際比例依工作流而異、請以官方文章的條件為準
3. [**Stage 7 — 常用 Multi-Agent / Production 工具推薦**](../../stages/07-multi-agent-production.md#-常用-multi-agent--production-工具推薦按用途分類) — langfuse / Helicone / weave 等 observability 工具表
4. [**`resources/cli-agents-guide.md`** 「常見坑」](../../resources/cli-agents-guide.md) — production 用 CLI 最常踩的問題

## 🛠 動手練習

### 動手練習 CLI-9：MCP server 接 CLI
照 [Stage 5.2 練習：MCP client](../../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎) 的步驟，把至少一個有用的 MCP server 接到你的 CLI：

- `filesystem` server → 讓 CLI 在指定目錄外也能讀檔
- `github` server → 讓 CLI 直接讀 PR / issue
- 自架 server → 接你的 internal API / DB

成功標準：在 CLI 對話裡直接問「我這個 PR 有 conflict 嗎」，CLI 透過 MCP 回答你（不用你開瀏覽器）。

### 動手練習 CLI-10：GitHub Actions + CLI
寫一個 `.github/workflows/cli-review.yml`：

- 觸發：PR opened / synchronize
- 跑：在 GH Actions runner 內執行 Claude Code（或 Codex），給它 `git diff`，並請它使用 A2 做好的 [`review-changes` Skill](A2-cli-workflow.md#動手練習-cli-6把重複-review-做成-skill)
- 輸出：PR comment

成功標準：開新 PR，1-2 分鐘內 PR 出現 review comment。

> 起點：Anthropic 官方有 [`claude-code-action`](https://github.com/anthropics/claude-code-action)（GitHub Actions 整合）；Codex 有 GitHub App 跟 CLI 兩種模式。

### 動手練習 CLI-11：Cost tracking
跑你日常的一個 task，**先預估** token 用量，再實際跑、查 token usage。差距通常很大（多半你低估）。

- 算式：input tokens + output tokens 各乘以 model 單價
- 接 langfuse 或 Helicone（[Stage 7 常用工具推薦](../../stages/07-multi-agent-production.md#-常用-multi-agent--production-工具推薦按用途分類) 表內 Observability 行）做 trace
- 觀察：哪個 sub-task 花最多 token？是不是有不必要的 long context？

### 動手練習 CLI-12：Skill / plugin 跨 team 分享
把 A2 的 `review-changes` Skill 放進 plugin 根目錄的 `skills/review-changes/SKILL.md`，再發布到內部 marketplace 或 GitHub。Team 其他人安裝 plugin 後，就能取得同一個 Skill。

`CLAUDE.md` 是專案自己的說明書，應留在 repo；它不是這個 plugin 要打包的內容。

- Skill / plugin 細節見 [Stage 5.3 + 5.4](../../stages/05-claude-code-ecosystem.md)
- 範本：[anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)

## 🧭 進階概念在 CLI 日常工作中的應用（7 個 playbooks）🆕

Track A 的人**已經在用** [Stage 7.5 的進階概念](../../stages/07.5-advanced-agentic-concepts.md)、只是沒命名它。下面挑 **最常用 2-3 個 playbook** 細看、其餘折疊為延伸閱讀——每個 ≤ 6 行。**想深挖原理 → 進 Stage 7.5。**

> 📌 **規則**：每個 playbook 看完先問自己「下一個 PR 會做不同的事嗎？」**會** → applied；**不會** → 跳下一個。

### 📋 Playbook 1：任務 scope 不明、agent 越界

- **When**：派 Codex/Gemini 跑 sweep、不確定它會不會擅自改別的檔（F11/F12 那種）
- **Do**：brief 開頭明寫「動 X / 不能跨 Y」、acceptance preset 加 path filter
- **Concepts**：Work Boundary + Hierarchical Task Decomposition · 📊 圖見 [concept-cluster](../../resources/diagrams/concept-cluster.png) Service × 編排 cluster
- **Read more**：

  | Source | Link |
  |---|---|
  | HumanLayer | [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) |
  | Anthropic | [How Anthropic teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) |
  | 內部 | [Stage 7.5 🧭 work boundary stack](../../stages/07.5-advanced-agentic-concepts.md#-概念地圖主軸四層工作邊界work-boundary) |

### 📋 Playbook 2：多 agent 平行、結果亂

- **When**：Claude planner + 2-3 Codex 平行跑、結果 merge 衝突 / drift
- **Do**：每個 agent 自己一個 commit、reviewer pattern 抓 drift（不是大合一）；brief 統一 task format + result.json schema
- **Concepts**：Contract Hand-offs + Speculative Parallel · 📊 圖見 [concept-cluster](../../resources/diagrams/concept-cluster.png) Service × 編排 + Types × 編排
- **Read more**：

  | Source | Link |
  |---|---|
  | Addy Osmani | [Code Agent Orchestra](https://addyosmani.com/blog/code-agent-orchestra/) |
  | Daniel Vaughan | [Running Multiple Codex Agents Parallel](https://codex.danielvaughan.com/2026/04/18/running-multiple-codex-agents-parallel-orchestration/) |
  | 內部 | [agent-collab-skills](https://github.com/WenyuChiou/agent-collab-skills)（`agent-task-splitter` + `agent-output-reconciler`）|

### 📋 Playbook 3：Review agent 輸出

- **When**：agent 寫完 PR、不放心直接 merge、人工 review 跟不上吞吐
- **Do**：加 LLM-as-judge subagent 自動評（binary pass/fail）、人類只 spot-check edge case；commit 前跑 acceptance-gate preset
- **Concepts**：Agent-as-Judge + Plan-Act-Reflect · 📊 圖見 [reading-decision-tree](../../resources/diagrams/reading-decision-tree.png) 藍色 eval 分支
- **Read more**：

  | Source | Link |
  |---|---|
  | Hamel Husain | [LLM-as-a-Judge: Complete Guide](https://hamel.dev/blog/posts/llm-judge/) |
  | Hamel Husain | [Your AI Product Needs Evals](https://hamel.dev/blog/posts/evals/) |
  | Simon Willison | [Sub-agents in Claude Code](https://simonwillison.net/2025/Oct/11/sub-agents/) |

### 📋 Playbook 4：派遣 subagent 跑獨立任務

> 💡 **第一次聽到 subagent？** 一句話：**subagent = 主 Claude session spawn 出來的「子 Claude」**、有自己獨立的 context、跑完回報結果。**派遣（dispatch）**就是叫 subagent 去做事——像派任務給同事。完整概念 → [Stage 5.5](../../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)。

- **When**：寫了大改動要 commit 前 / 進新 repo 不熟結構 / 想跑 LLM-as-judge 自動評估 / 4 個目標要做同樣審查
- **Do**：呼叫 Claude Code **內建** subagent（不用自己寫任何檔案）：
  - `code-reviewer` — review staged diff、找 bug + security
  - `Explore` — 唯讀搜尋 codebase、找 entry point / symbol
  - `Plan` — 設計 step-by-step 實作計畫
  - `general-purpose` — 不確定該用哪個 / 多步驟研究的 fallback
- **Concepts**：Hierarchical Task Decomposition + Context Isolation · 📊 圖見 [concept-cluster](../../resources/diagrams/concept-cluster.png) Service × 編排 cluster
- **Read more**：
  - [Stage 5.5 Subagents](../../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)（完整理論 + decision table）
  - [`resources/subagent-cookbook.md`](../../resources/subagent-cookbook.md)（**15 個 recipe**、複製貼上即可用的 prompt 範本）

---

### 📋 Playbook 5：在 CI 裡跑 CLI agent

- **When**：把 `codex exec` / `claude --print` 接進 GitHub Actions、不能每次需要人按 yes、頻寬限制不能用 Opus
- **Do**：分層 autonomy（preset 自動跑 / commit 需審 / push 需人簽）、設 fallback 便宜 model（Opus 掛了 fallback Haiku）
- **Concepts**：Autonomy Gradients + Graceful Degradation · 📊 圖見 [concept-cluster](../../resources/diagrams/concept-cluster.png) Config × 治理 cluster
- **Read more**：

  | Source | Link |
  |---|---|
  | Anthropic | [How Anthropic teams use Claude Code (PDF)](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf) |
  | Anthropic Engineering | [Equipping Agents with Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) |
  | 內部 | [Stage 5.5 Subagents](../../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能) + 動手練習 CLI-10 |

### 📋 Playbook 6：控制成本

- **When**：用 Codex 跑大批 work、每月 API 帳單失控、想壓在 budget 內
- **Do**：`plan.yml` 設 `max_cost_usd`、便宜 model（Haiku）跑探索 / 貴 model（Opus）只跑 polish；開 prompt caching（符合快取條件時可大幅降低重複 context 成本）；自動化 QA（不靠人時間）
- **Concepts**：Cost-aware Budget Gates + Throughput-Merge Philosophy · 📊 圖見 [concept-cluster](../../resources/diagrams/concept-cluster.png) Config × 韌性 cluster
- **Read more**：

  | Source | Link |
  |---|---|
  | Simon Willison | [Sub-agents](https://simonwillison.net/2025/Oct/11/sub-agents/) |
  | Anthropic | [Prompt Caching](https://www.anthropic.com/news/prompt-caching) |
  | 內部 | 本 stage 動手練習 CLI-11（token tracking + langfuse 整合）|

### 📋 Playbook 7：強化 workflow、防 drift

- **When**：CLAUDE.md / SKILL.md rule 寫了沒人 enforce、preset YAML 加了不知道有沒有效
- **Do**：故意 break 一條 rule 跑 acceptance gate 看抓不抓得到（chaos test）；`docs/` 當 single source、CLAUDE.md 只當 entry map
- **Concepts**：Failure Injection + System of Record · 📊 圖見 [failure-lifecycle](../../resources/diagrams/failure-lifecycle.png)（F11-F14 進化循環）
- **Read more**：

  | Source | Link |
  |---|---|
  | HumanLayer | [Writing a good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md) |
  | agent-collab-skills | [observed-failure-modes.md](https://github.com/WenyuChiou/agent-collab-skills/blob/main/docs/observed-failure-modes.md) |
  | 內部 | [Stage 7.5 🔁 failure-mode lifecycle](../../stages/07.5-advanced-agentic-concepts.md#-failure-mode-lifecycle產業級-agent-失敗模式怎麼演化成最佳實踐) |

---

→ **7 個 playbook = 7 個 trigger × 12 個 concept ×「對應 reading source」的橋樑**。深挖原理 / 看完整 12 個 concept 跟 8 個 cross-vendor 原則 → [Stage 7.5](../../stages/07.5-advanced-agentic-concepts.md)。

## 🎯 精選 Projects

按用途分 4 類、9 個項目一張表搞定。**挑入口看「適合誰」、想深入細節點連結看 repo**。

> 💡 **要找接日常工具的 MCP**（Notion / Obsidian / Excel / Postgres / Playwright / Slack / Linear / Figma 等）：[`resources/mcp-skills-catalog.md`](../../resources/mcp-skills-catalog.md)——81+ 個分類整理，每個都有 stars / license / 適合誰。下表只列「寫自己 MCP server / 找 reference」用的核心 catalog。

| 分類 | Project | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|---|
| **MCP server collection**<br>（接 CLI 用） | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | ⭐⭐⭐⭐⭐ | 第一個 MCP 從 reference 學起 | 官方 reference servers（現有 7 個：everything / fetch / filesystem / git / memory / sequentialthinking / time；github、sqlite 已移到 `servers-archived`），★ 89k+。詳見 [Stage 5.2](../../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎) |
| | [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) | ⭐⭐⭐⭐ | 想找特定領域的社群 MCP | 社群 MCP catalog、150+ 個依分類整理 |
| **CI 整合 patterns** | [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action) | ⭐⭐⭐⭐⭐ | 第一個 CI workflow 從官方範本起步 | 官方 GitHub Action 範本、PR review / issue triage / 自動 fix |
| | [continuedev/continue](https://github.com/continuedev/continue) | ⭐⭐⭐⭐ | 想把 AI checks 接到 PR pipeline 強制執行 | ★ 35k+。完整介紹見 [`branches/for-developer.md`](../../branches/for-developer.md) |
| **Observability + Cost** | [langfuse/langfuse](https://github.com/langfuse/langfuse) | ⭐⭐⭐⭐⭐ | 想把 trace / cost / session 都接起來 | open source LLM observability，★ 32k+。詳見 [Stage 7 常用推薦](../../stages/07-multi-agent-production.md#-常用-multi-agent--production-工具推薦按用途分類) |
| | [Helicone](https://github.com/Helicone/helicone) | ⭐⭐⭐⭐ | 想要最快的 logging（改 base_url 就好）| proxy-based 監控、改 base_url 就有 logging + caching，★ 6k+ |
| | [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | ⭐⭐⭐⭐⭐ | CLI workflow 升 production 前跑回歸測試 | eval framework，★ 24k+。詳見 [Stage 7 Agent Benchmark Landscape + Reward-Hacking 警告](../../stages/07-multi-agent-production.md#-agent-benchmark-landscape怎麼看不要只看排行榜---reward-hacking-警告) |
| **Production CLI workflow 範本** | [obra/superpowers](https://github.com/obra/superpowers) | ⭐⭐⭐⭐ | 看完整實際在用的 workflow 長什麼樣 | 整套 production-ready skill collection、★ 265k+。看別人怎麼把 CLI workflow 做完整 |
| | [obra/superpowers-marketplace](https://github.com/obra/superpowers-marketplace) | ⭐⭐⭐ | 要把 team 的 CLI workflow 打包共用 | 最簡 marketplace template、★ 1.2k+ |

> 💡 **建議入手路徑**：先從 `modelcontextprotocol/servers` 挑一個 reference MCP 接到 CLI → 用 `claude-code-action` 跑第一個 CI workflow → 加 langfuse 看 trace + cost → production 規模化時把 workflow 打包成 marketplace plugin。

## ✅ Track A 完整通關自我檢查

你能不能：

- [ ] 已有至少 1 個 MCP server 接到你日常 CLI
- [ ] 已有至少 1 個 CI workflow 在自動跑 CLI agent
- [ ] 你能講出某個 task 跑下去的 token 用量、cost、latency 大致範圍
- [ ] 把至少一個 Skill 放進 plugin 的 `skills/<name>/SKILL.md`，並驗證安裝後找得到（即使只有自己用）
- [ ] 知道什麼任務值得加 observability、什麼不值得

如果都可以 → **Track A 完整通關**。建議接著走 [**Stage 8 — Agent Interfaces**](../../stages/08-agent-interfaces.md)（**兩 track 共用 hub**：Computer Use / Browser Use / Code Sandbox，Track A 視角約 1-2 週），或挑一個 [specialized branch](../../README.md#-學習地圖兩條學習路徑) 繼續走（researcher / developer / teacher / knowledge-worker / everyday-users）。

如果想再深入「**怎麼寫自己的 CLI agent**」（不是用現有的）→ 跳到 [Track B Stage 3](../../stages/03-tool-use-and-hello-agent.md) 開始。Track A 跟 Track B 互補。

## 💡 接下來

走完 Track A 你已經是 CLI power user。下一階段選擇：

1. **加深 CLI workflow**（持續優化你的 setup）
   - 訂閱 Anthropic / OpenAI changelog
   - 每季 review 一次 [`resources/cli-agents-guide.md`](../../resources/cli-agents-guide.md) 看新工具
   - 跟你 team 分享 CLAUDE.md / skills

2. **跨到 Track B**（學怎麼寫自己的 agent）
   - Stage 3-4 學 tool use + framework
   - Stage 5 深挖 Claude Code 內部運作
   - Stage 7 寫自己的 multi-agent system

3. **走 specialized branch**（把 CLI 應用在特定領域）
   - 研究人員 / 開發者 / 知識工作者 / 教師 / 日常使用者
   - 各 branch 都會用到 Track A 學的東西
