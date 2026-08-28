# Stage 04 Agent 框架閱讀體驗與範例現代化 Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use `writing-plans` to keep this plan current, then execute each task through the repository review and verification gates.

**Goal:** 讓第一次接觸 Agent framework 的讀者，不展開任何選單也能分清 workflow、agent、framework 與 orchestration，選出合適路線並開始第一題；同時把三語框架資料與五組可執行範例更新到 2026-08-27 的官方現況。

**Architecture:** 使用兩層 stacked PR。PR 04A 只處理三語教材、概念圖、事實包、資源表與閱讀體驗 gate；PR 04B 疊在 04A 上，只處理五個範例資料夾、依賴、雙路徑與測試。每層獨立 review、commit、push、開 PR，未經使用者明確同意不合併、不清理。

**Tech Stack:** Markdown、MkDocs、Python 3.11、LangGraph 1.x、CrewAI 1.x、Smolagents 1.x、Pydantic AI 2.x、OpenAI Python SDK 3.x、Anthropic Python SDK 1.x、PyYAML、pytest、Pillow。

---

## 狀態與邊界

- 查核日期：`2026-08-27 UTC`。
- 04A 進度：Task 1–4 已完成；Task 5 第一次 review 擋下 Stage 7／8 同源過時主張、乾淨 checkout 未先裝 requirements、簡中 switcher 與台灣用語，舊 fingerprint 已作廢。修正後正在重跑 gate 與第二次 review。
- 目前三語未展開可見字元：繁中 `5,230`、英文 `10,190`、簡中 `5,244`；各自上限只多 `50` 字。
- 目前三語皆為 `8` 個關閉 `<details>`、`0` 個預設展開；18 筆資源與 `4／6／4／3／1` rowgroup、35 個外部 URL 和五題練習均通過 reader-UX parity。
- Image 2.0 已產生並人工檢查三張同構亮色圖：`agent-framework-choice-map.png`、`.en.png`、`.zh-Hans.png`。
- Staging 前複查：GitHub API 時間為 `Thu, 27 Aug 2026 21:15:53 GMT`；PyPI 仍為 LangGraph `1.2.11`、CrewAI `1.15.18`、Smolagents `1.26.0`、Pydantic AI `2.35.1`、Agent Framework `1.15.0`、Strands Agents `1.54.0`、Deep Agents `0.7.9`、AutoGen AgentChat `0.7.5`。
- 本機證據：reader UX 9 pages × 3 locales、strict anchors、mirror、locale、Hans、image、duplicate repo、freshness、298-link snapshot 與 MkDocs build 通過；`python -m pytest scripts -q` 為 `319 passed`。英文 Stage 5.5 舊 fragment 在本輪被 gate 擋下並已修正。
- PR 04A branch：`codex/stage04-reader-ux`。
- PR 04A base：`codex/stage02-prompt-map`（PR #150）。
- PR 04B branch：完成 04A 後建立 `codex/stage04-example-hardening`，base 指向 04A。
- 04B 候選已完成五個 current-major 範例與三語 README。每個資料夾都用獨立 Python 3.11 環境驗收；乾淨的 Exercise 2 環境實際抓出並修正 `crewai[anthropic]` extra 遺漏，五組 `pip check` 與 11 個直接執行的離線入口均通過。
- CodeAct 的離線測試已驗 AST allowlist、JSON tool 邊界、loopback 控制埠與 Docker 資源限制；`network_mode="none"` 會切斷 Smolagents 的 host → Jupyter 控制通道，而 internal bridge 在現行 Docker 也不能可靠支援這條 published-port 路徑。因此範例使用一般 bridge、只把控制埠綁到 `127.0.0.1`，並明說容器仍可能連網、不是 production sandbox。另增 `test_docker_smoke.py` 實測 executor 與實際 port binding；本機 Docker client 存在但 daemon 未啟動，因此不宣稱 live 容器已跑過。
- 主工作區有 Claude 的 `stages/01-llm-basics.md` 修改；本計畫只使用隔離 worktree，不切換、不覆蓋。
- 本次不修改 Stage 05 正文。只允許修正 Stage 07／07.5／08 指向 Stage 04 的既有 anchor 或同源過時敘述；若能保留原 anchor，就不改後續章節結構。
- 不合併 PR、不刪 branch、不清 worktree。只有使用者明確說可以合併時才執行安全合併流程。

## 已確認的大問題

### 閱讀形狀

- 三語頁面都是 `0` 個 `<details>`；時間、先備知識、三份必讀、四象限、五種 multi-agent pattern、Claude Code 比較、tool pattern、五題練習與 18 筆專案同時展開。
- 繁中約 `17,386` 字元、英文約 `28,013`、簡中約 `18,948`；初學者看不到「現在先做哪一步」。
- 沒有第一題前的可見核心詞區。頁首叫讀者自行查 glossary，`orchestration`、`state`、`checkpoint`、`handoff`、`HITL` 等詞先出現才解釋。
- `📌`、`📚`、`🛠`、`🎯`、`✅` 路標目前存在，重整時必須保留。
- Stage 03 已有六題，Stage 04 仍寫成「跑完全部 5 個 hello-X projects」。
- `async Python` 被寫成硬性門檻，但本章第一輪練習不需要讀者先精通 async；應改成「之後會有幫助」，並提供可跳過的補充。

### 事實與定位

- 「Anthropic 與 Cognition 說 90% 用例不該用 multi-agent」沒有來源支持。Anthropic 的 `90.2%` 是特定 research eval 的相對提升，不是一般用例比例。
- 「multi-agent 通常 3–10× token」不是通則。Anthropic 只報告其 Research 系統約使用 chat 的 `15×` tokens，並明說結果依任務而異。
- 「平行就會 wall-clock 1/N」忽略最慢分支、整合、重試與 rate limits。
- `tools <20–30`、`>30 tools` 是沒有官方依據的硬門檻；應改成看工具描述是否塞滿 context、選錯率是否上升，再用 eval 決定。
- 「進階 tool patterns 都需要 framework」不正確。Framework 可以減少重複程式，但 raw SDK 也能做 routing、composition 與 retrieval。
- CrewAI 已支援 Flow persistence、resume 與 human feedback；「長 workflow 沒 checkpointing」已過時。
- OpenAI Swarm 官方 README 已明說由 Agents SDK 取代，只適合教育用途，不能再給 production 星等。
- Microsoft Agent Framework 已在 `2026-04-02` 發布 Python `1.0.0` stable，現有內容仍把它寫成剛合併的後繼概念。AutoGen 與 Semantic Kernel 仍可用，但 Microsoft 已提供遷移到 Agent Framework 的正式指南。
- OpenAI Agents SDK 的 Sandbox Agents 是 beta；不能寫成「production coding agent 首次 architecturally sound」這類沒有可驗證標準的結論。
- Strands 舊 repo `strands-agents/sdk-python` 已導向 `strands-agents/harness-sdk`。
- Deep Agents 現行 PyPI 是 `0.7.9`，不是頁面寫的 `0.6.12`；它的官方定位是 agent harness，不只是一般 framework。
- Pydantic AI 已到 `2.35.1`，有 multi-agent 與 harness 文件；「較新、只做 typed output」的描述太窄。
- Eve 是 `2026-06-17` 開放 public preview，應清楚標示 Preview，不把新專案當成成熟預設。
- 18 筆表格使用空白儲存格假裝合併，且混入 GitHub stars。編輯星級要保留，人氣星數要移除。

### 可執行範例

- 五份 requirements 都排除目前 major：LangGraph `<1.0`、CrewAI `<1.0`、Pydantic AI `<2.0` 等。
- 2026-08-27 PyPI 查核：`langgraph 1.2.11`、`crewai 1.15.18`、`smolagents 1.26.0`、`pydantic-ai 2.35.1`、`pydantic 2.13.4`、`litellm 1.98.0`。
- CrewAI `1.15.18` 要求 Python `>=3.10,<3.14`；本機 Python 3.14 不能作為它的驗收環境。本層統一用 Python 3.11 clean venv。
- 若框架 API 改變，部分測試會印出「跳過」後成功；這會把破壞變成綠燈，必須改成真正失敗。
- 練習 3 的 `starter_anthropic.py` 只是概念文字，不是可執行 Anthropic Path B。
- 五題都必須符合 repo contract：Ollama Path A、Anthropic Path B、雙離線 mock tests、明確預算、至少兩個自我驗證 assert。

## 讀者不展開選單時看到的主線

1. 一句話問題：framework 像積木盒，幫你少寫重複程式；不是每個任務都需要它。
2. `📌` 四個可驗證學習目標。
3. `🧩` 八個主核心詞，第一次可見教學使用粗體：
   - **Framework（框架）**
   - **Workflow（工作流程）**
   - **Agent（代理程式）**
   - **Orchestration（編排）**
   - **State（狀態）**
   - **Checkpoint（檢查點）**
   - **Handoff（交接）**
   - **Human-in-the-loop（HITL，人在迴圈中）**
4. 一張亮色三語概念圖：固定路線／動態路線 × 單一 agent／多個 agent；箭頭最後進入「先用最簡單能完成任務的形狀」。
5. 一張短版選擇表：raw SDK、LangGraph、CrewAI、OpenAI Agents SDK、Microsoft Agent Framework 各適合什麼。
6. 五種協作 pattern 的名稱與一句話用途。**Supervisor** 與 **Worker** 在第一次出現時另外粗體解釋。
7. `📚` 必修閱讀標題與一句閱讀目的；完整連結清單收合。
8. `🛠` 五題的標題、既有 anchor、成果、第一個可複製指令與預算提醒。
9. 練習 4 前明確解釋 **CodeAct**；練習 5 前明確解釋 **Type-safe**，並提醒 Stage 03 的 Structured Output。
10. `🎒` 一個推薦小專案：有人工批准的研究摘要工作流。
11. `🎯` 精選 Projects 標題與一個推薦入口；完整 18 筆表格預設收合。
12. `✅` 短版自我檢查與 Stage 05 入口。

## 預設收合內容

- 時間、先備知識、Python 版本、環境與完整預算公式。
- 四份必修閱讀與建議順序。
- workflow／agent × single／multi 的完整四象限說明。
- Anthropic／Cognition 的 multi-agent 取捨與限制。
- 五種 pattern 的完整比較、論文、Claude Code subagent 對照。
- Dynamic tool selection、tool composition、tool-augmented retrieval 的深度說明。
- 五題完整程式、Path A／Path B、macOS/Linux 替代指令與排錯。
- 18 筆框架／harness／基礎設施表。
- 歷史與遷移說明：OpenAI Swarm、AutoGen、Semantic Kernel。

所有 `<details>` 預設關閉；不使用 `open`。可被其他頁面深連結的 heading 留在外面，必要時加穩定 HTML anchor。

## 18 筆資源表

保留現有 18 筆與編輯評分，但把分類改成真正的 HTML rowgroup。三語 URL、順序、狀態與評分完全一致。

| 分組 | 筆數 | 定位 |
|---|---:|---|
| Production orchestration | 4 | LangGraph、Semantic Kernel、Agno、Microsoft Agent Framework |
| 快速雛形／多 Agent | 6 | CrewAI、AutoGen、OpenAI Agents SDK、Deep Agents、Swarm、Strands |
| 特殊路線 | 4 | Smolagents、Pydantic AI、Letta、Eve |
| 特化 | 3 | LlamaIndex、AgentScope、LangChain |
| 基礎設施 | 1 | LiteLLM |

固定 `rowspan`：`4／6／4／3／1`，總和 `18`。OpenAI Swarm 只保留教育評分，不再列 production 星等。AutoGen、Semantic Kernel 的評分可保留，但用途欄必須寫現行／遷移定位。所有 `★ 39k+` 類數字移除。

## 2026-08-27 官方事實包

資料優先順序：正式文件／release notes → 官方 repository／PyPI → 原始論文。第三方比較文不證明版本、可用性或 production 定位。

1. [Anthropic — Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)：workflow 是預先定義的 code path；agent 由模型動態決定過程。先用最簡單可行方案，framework 可能遮住 prompt 與 response。
2. [Anthropic — Multi-agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)：適合 breadth-first、可平行的研究；特定系統約使用 chat `15×` tokens。共享 context、強依賴任務與多數 coding 工作不一定適合。
3. [Cognition — Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents)：主要風險是 context fragmentation；文章沒有「90%」通則。
4. [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)、[Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)、[Workflows and Agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)：LangGraph 是低階 orchestration runtime；checkpoint 支援 persistence、HITL、fault tolerance 與 time travel。
5. [CrewAI Flows](https://docs.crewai.com/en/concepts/flows)：Flows 支援 persistence、resume 與 human feedback；刪除「沒有 checkpointing」說法。
6. [OpenAI Agents SDK orchestration](https://openai.github.io/openai-agents-python/multi_agent/)、[handoffs](https://openai.github.io/openai-agents-python/handoffs/)、[tracing](https://openai.github.io/openai-agents-python/tracing/)：manager-as-tools 與 handoff 是不同模式；SDK 內建 tracing。
7. [OpenAI Sandbox Agents](https://openai.github.io/openai-agents-python/sandbox/guide/)：Sandbox Agents 是 beta；隔離邊界、manifest、session 與 approval 分層描述。
8. [OpenAI Swarm](https://github.com/openai/swarm)：官方標示 experimental／educational，已由 Agents SDK 取代。
9. [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)、[Migration Guide](https://learn.microsoft.com/en-us/agent-framework/migration-guide/)：Python `1.0.0` 於 2026-04-02 stable；官方提供 AutoGen／Semantic Kernel 遷移路徑。
10. [AutoGen](https://microsoft.github.io/autogen/)：現行 package 是 `autogen-agentchat 0.7.5`；舊 0.2 tutorial 不可當現行 API。
11. [Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview)：官方定位是建在 LangGraph 上的 agent harness，包含 planning、filesystem、subagent、memory、permissions 與 HITL。
12. [Strands Agents](https://strandsagents.com/docs/user-guide/quickstart/overview/)：Python／TypeScript SDK；canonical monorepo 是 `strands-agents/harness-sdk`。
13. [Smolagents](https://huggingface.co/docs/smolagents/index)、[secure code execution](https://huggingface.co/docs/smolagents/tutorials/secure_code_execution)：CodeAgent 執行模型產生的程式，必須清楚說明本機執行風險與 sandbox 選項。
14. [Pydantic AI Agent](https://pydantic.dev/docs/ai/core-concepts/agent/)、[Output](https://pydantic.dev/docs/ai/core-concepts/output/)、[Multi-agent](https://pydantic.dev/docs/ai/guides/multi-agent-applications/)：typed output 使用 schema／validation，validation failure 可以重試，但不能保證答案語意正確。
15. [Agno](https://docs.agno.com/)：目前定位是 AgentOS 平台，原生支援 agents、teams、workflows，也能包裝其他 framework。
16. [Vercel Eve](https://vercel.com/blog/introducing-eve)：filesystem-first TypeScript durable-agent framework，2026-06-17 public preview，包含 durability、sandbox、HITL、subagents 與 evals。
17. GitHub repository snapshot：18 筆 repo 的 canonical URL、archived、last push、release 與 license 在 staging 前重掃；API `NOASSERTION` 只代表 GitHub 無法分類，不能直接宣稱沒有授權。
18. PyPI JSON：所有教學範例依賴在 04B staging 前再查一次；版本變動就更新 requirements、三語日期與 review fingerprint。

## Task 1：建立 Stage 04 事實與錨點基線

**Files:**

- Inspect: `stages/04-agent-frameworks.md`
- Inspect: `stages/04-agent-frameworks.en.md`
- Inspect: `stages/04-agent-frameworks.zh-Hans.md`
- Inspect: `stages/07-multi-agent-production*.md`
- Inspect: `stages/07.5-advanced-agentic-concepts*.md`
- Modify: `scripts/freshness-models.yml`

**Steps:**

1. 記錄三語可見字數、heading、anchor、URL、資源順序與評分。
2. 掃描所有指向 Stage 04 fragment 的 inbound links。
3. 保留三組既有 canonical anchor：四象限、何時需要 multi-agent、精選 Projects。若 heading 改寫，放相同語系的顯式 `<a id="...">`。
4. 在 `freshness-models.yml` 加入 `stage04_fact_pack` 與 `verified_pages`：scope 固定為 `frameworks,releases,maintenance,licenses,security`，`max_age_days=90`。
5. 重新執行 freshness tests，先讓缺 marker 的預期失敗證明 gate 已覆蓋 Stage 04，再進入正文修改。

## Task 2：先完成繁中 Stage 04 主線

**Files:**

- Modify: `stages/04-agent-frameworks.md`
- Modify: `stages/DESIGN.md`
- Modify: `scripts/reader-ux-pages.yml`

**Steps:**

1. 把時間、進入條件與環境放進第一個關閉 `<details>`。
2. 保留四個可衡量目標，修正 Stage 03 六題與 async 門檻。
3. 在第一題前新增八個可見核心詞；每詞回答「是什麼、像什麼、這章拿來做什麼、限制」。
4. 加入短版選擇表與五種 pattern；刪掉假門檻和假精確數字。
5. 把必修閱讀改成官方來源；heading 與目的可見，連結清單收合。
6. 五題保留原 heading／anchor，加入一句成果、可複製 PowerShell 指令與預算提醒。完整步驟連到同語系 example README 並收合。
7. 加入推薦小專案、短版 self-check 與 Stage 05 入口。
8. 把 18 筆表轉成五個 `<tbody>`、真實 `rowspan=4/6/4/3/1`，保留評分、移除 GitHub stars、修正現況與 canonical URL。
9. 加入可見查核日期與三語共用 freshness marker。
10. 在 DESIGN 寫下 Stage 04 固定主線、核心詞、圖、五題、18 筆 rowgroup、歷史框架標示與兩層 PR 邊界。
11. 在 reader-UX YAML 先只設定繁中候選結構，執行 targeted gate；完成三語前不宣稱 parity 通過。

## Task 3：生成並人工檢查三語亮色概念圖

**Files:**

- Add: `resources/diagrams/agent-framework-choice-map.png`
- Add: `resources/diagrams/agent-framework-choice-map.en.png`
- Add: `resources/diagrams/agent-framework-choice-map.zh-Hans.png`
- Modify: `stages/04-agent-frameworks*.md`

**Steps:**

1. 使用 Image 2.0 生成同構亮色圖，不放版本、價格、stars 或沒有通則的數字。
2. 圖中只使用正文已先解釋的詞：Workflow、Agent、Single、Multi、Orchestration、Checkpoint、Handoff、HITL。
3. 三張各用正確語系；繁中／簡中不得混字，英文不得混入中文句子。
4. 逐張用原尺寸檢查文字、箭頭、對比、裁切與字形。
5. 三語 Markdown 各自使用正確圖檔與在地化 alt text；圖片不能取代可搜尋正文。
6. 執行 image locale gate 與三語 MkDocs build。

## Task 4：建立英文與簡中鏡像

**Files:**

- Modify: `stages/04-agent-frameworks.en.md`
- Modify: `stages/04-agent-frameworks.zh-Hans.md`
- Modify: `scripts/reader-ux-pages.yml`

**Steps:**

1. 以繁中定稿為 canonical，逐段翻譯，不用機械繁簡轉換取代內容審查。
2. 鎖住八個核心詞的 concept ID、順序、用途與限制。
3. 鎖住五題 heading、成果、PowerShell 指令、預算公式、官方 URL、18 筆表格與評分。
4. 確認歷史／Preview／遷移狀態三語一致。
5. 在 `reader-ux-pages.yml` 正式加入 Stage 04：
   - visible section order
   - `max_open_details: 0`
   - 八個 core terms
   - 五題 heading／anchor
   - `resource_group_rowspans: [4, 6, 4, 3, 1]`
   - ordered URL、URL/rating、日期／狀態 literals parity
6. 字數上限只比實測各多 50 字，不先猜一個寬鬆上限。

## Task 5：PR 04A 驗證、review 與未合併 PR

**Files:**

- Modify: `CHANGELOG.md`
- Modify: `docs/plans/2026-08-27-stage04-reader-ux-and-framework-examples.md`
- Potentially modify: `scripts/repository-freshness-snapshot.json`

**Steps:**

1. staging 前重新查官方 docs、PyPI 與 18 筆 repo metadata；變動就更新三語與 fact pack。
2. 對最終 diff 更新 CHANGELOG，日期取 GitHub API UTC，不憑記憶。
3. 執行：
   - `git diff --check`
   - `python scripts/check-reader-ux.py`
   - strict anchors、anchor slug parity、mirror parity、locale links、Hans、image locale、duplicate repos、freshness strict gate
   - `python -m pytest scripts -q`
   - `python scripts/build-docs-tree.py`
   - `python -m mkdocs build`
   - 英文／簡中 MkDocs build
4. 人工驗收：不展開能選路線、開始第一題、看懂成功條件；重要詞沒有被收合或刪除。
5. 逐檔 `git add <path>`；列出 expected file freeze list，斷言 staged count 完全相符。
6. 記錄 staged tree/fingerprint，執行一次獨立 `code-reviewer`。
7. reviewer 後任何修改都重新跑相關 gate、重新 stage、重新 fingerprint、重新 review。
8. commit：`content(stage4): make framework choices clear`。
9. push 並開 PR，base 指向 PR #150 的 branch；等待 checks 全綠後停下，不合併。

## Task 6：建立 PR 04B 範例層

**狀態：完成候選實作。** 保留五份原有深度閱讀與延伸段落，沒有再接受 delegate 的過度壓縮稿；requirements、雙路徑、行為測試、三語 PowerShell／macOS/Linux 指令、成本公式與安全邊界已同步。等待 Task 7 的全站 gate、獨立 review、commit 與未合併 stacked PR。

**Files:**

- Modify: `examples/stage-4/01-same-agent-two-frameworks/**`
- Modify: `examples/stage-4/02-multi-agent-roles/**`
- Modify: `examples/stage-4/03-graph-workflow/**`
- Modify: `examples/stage-4/04-codeact-vs-json-tool/**`
- Modify: `examples/stage-4/05-typed-agent/**`
- Modify: `examples/README*.md`
- Add or modify: `scripts/test_stage04_examples.py`
- Modify: `stages/DESIGN.md`
- Modify: `resources/style-guide*.md`
- Modify: `CHANGELOG.md`
- Modify: this plan

**Steps:**

1. 從 04A head 建立 `codex/stage04-example-hardening` 隔離 worktree。
2. 用 Python 3.11 建 clean venv；重新查 PyPI，requirements 鎖 current major，不鎖死 patch。
3. 每題提供：
   - `starter.py`：Ollama Path A
   - `starter_anthropic.py`：Anthropic Path B
   - `test.py`：Path A offline mock
   - `test_anthropic.py`：Path B offline mock
   - 三語 README：PowerShell first、macOS/Linux 收合、成本公式、查核日、成功輸出、安全提醒
4. 練習 1：同一任務用 LangGraph 與 CrewAI；比較抽象和 trace，不用行數宣稱勝負。
5. 練習 2：CrewAI 角色協作；輸入、handoff 結果與停止條件可觀察。
6. 練習 3：LangGraph branching、checkpoint 與 HITL；Anthropic path 必須真的可執行，不保留概念 placeholder。
7. 練習 4：Smolagents CodeAct 與 JSON tool；模型生成 code 視為不可信，只在明確 sandbox／受限 mock 中執行，不能直接 `exec` 任意輸出。
8. 練習 5：Pydantic AI `output_type`／validation；驗證外形不代表語意正確，加入不合法 confidence 與 sources regression。
9. 所有 starter 加最小權限、有限迴圈／timeout、明確錯誤；每檔至少兩個自我驗證 assert。
10. 移除所有「API 變了就 skip」分支；不支援的 API 必須讓測試失敗。
11. `scripts/test_stage04_examples.py` 鎖住五資料夾、十個入口、requirements major、Python 範圍、model ID、PowerShell、成本、查核日期、雙路徑與 README URL parity。
12. 在 clean venv 安裝每組 requirements，逐一執行十個 mock test 入口；不能只靠 pytest collection，避免同名 `test.py` 衝突。

## Task 7：PR 04B 驗證、review 與未合併 PR

**狀態：進行中。** 五個獨立 clean-env installs、`pip check`、11 個離線入口、compileall、Stage 4 結構 gate、323 個 scripts tests、locale／Hans／mirror／freshness 檢查與三語 MkDocs build 已通過；只剩 staged fingerprint、獨立 reviewer、commit 與未合併 stacked PR。

1. 執行 04A 全套內容 gate，再加：
   - clean Python 3.11 dependency installs
    - 十一個 Stage 04 offline mock entrypoints
   - starter `ast.parse`
   - `scripts/test_stage04_examples.py`
2. 重新查 PyPI、Anthropic model ID 與價格；三語 README 同步。
3. 對最終 diff 寫 CHANGELOG，逐檔 stage，斷言 freeze list 和 count。
4. 穩定 staged diff 執行一次獨立 `code-reviewer`；修正後舊 ack 作廢。
5. commit：`fix(stage4): modernize framework examples`。
6. push 並開 stacked PR，base 指向 PR 04A branch；等待 checks 全綠後停下，不合併。

## 驗收標準

- 三語 `0` 個預設展開 `<details>`。
- `📌`、`📚`、`🛠`、`🎯`、`✅` 在可見主線。
- 八個主核心詞在第一題前可見、第一次教學使用粗體、三語順序一致。
- Supervisor、Worker、CodeAct、Type-safe 在第一次可見使用時粗體並有白話定義。
- 五題 heading、anchor、成果、第一步與預算提醒可見。
- 不再出現 `90% use cases`、通用 `3–10×`、`wall-clock 1/N`、`tools >30` 等假通則。
- CrewAI persistence、Swarm replacement、Microsoft Agent Framework stable／migration、Sandbox beta、Strands canonical repo 等資訊正確。
- 18 筆資源、18 個 URL、五個 `<tbody>`，rowspan `4/6/4/3/1`；三語 URL、狀態與評分一致。
- 所有 volatile GitHub stars 移除；編輯星級保留。
- 三張亮色概念圖同構、三語在地化、原尺寸人工檢查通過。
- freshness marker 三語同日、同 scope、同 canonical，fact pack 有官方 URL。
- 五個範例各有真正的 Ollama／Anthropic 路徑與兩個 offline tests；沒有 placeholder 或 API-drift skip。
- CrewAI 用 Python 3.11 驗收，不把 Python 3.14 不相容誤判成框架程式錯誤。
- 生成程式碼不在 host 上無限制執行；高風險操作有 sandbox／allowlist／HITL 邊界。
- 04A 與 04B 各自可回溯、各自 review、各自開 PR；未經許可不合併、不清理。

## 刻意不做

- 不把 18 個 framework 都做成教學；本章教選擇與五個代表練習，深度導向官方 docs。
- 不用 benchmark 或 GitHub stars 宣稱哪個「最強」。
- 不把 multi-agent 當成預設，也不把 single-agent 說成落後。
- 不在 Stage 04 重寫 Stage 05 Claude Code subagent、Stage 06 memory 或 Stage 07 production 全章。
- 不在同一 PR 混入 Stage 05 正文、README 全站重整或其他章節的資源汰換。
