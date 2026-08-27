# Track A3 漸進式重整、安全自動化與事實更新計畫

## 目標

讓第一次把 CLI agent 接進團隊流程的讀者，只先完成一件事：

> **把一個只讀檢查放進測試用 PR；它可以提出意見，但不能自己合併、部署或取得多餘權限。**

讀者不展開任何選單，也能分清 MCP、CI、observability，完成 CLI-9 至 CLI-12 的最小成果，並知道何時必須停下來請人檢查。文字使用沒有軟體背景的人也能讀懂的短句；技術名稱、檔名、命令、權限與安全限制保持精確。

## 現況診斷

查核日：**2026-08-27 UTC**（GitHub API response date：`Thu, 27 Aug 2026 10:37:10 GMT`）。

| 項目 | 繁中 | 英文 | 簡中 | 問題 |
|---|---:|---:|---:|---|
| 未收合非空白字元 | 11,785 | 15,811 | 11,966 | 所有補充理論與資源一起攤開，第一遍找不到主線 |
| `<details>` | 0 | 0 | 0 | 時間、閱讀、四個練習細節、七個 playbook 與資源全都可見 |
| H2／H3 | 8／11 | 8／11 | 8／11 | 章節層級看似整齊，但同時承擔實作與 Stage 7.5 理論 |
| 外部連結 | 26 | 26 | 26 | 多個連結嵌在零碎 mini-table，缺少依用途整理的閱讀順序 |
| 資源表 | 9 筆／4 類 | 9 筆／4 類 | 9 筆／4 類 | 分類欄用空白假裝合併，另有主觀星等與即時 stars |

已確認的內容缺陷：

- `modelcontextprotocol/servers` 的 `github` reference server 已移到歷史封存集合；現行 GitHub MCP 應指向 `github/github-mcp-server`。官方 reference servers 也明示不是 production-ready。
- 原文把 filesystem MCP 說成「讀指定目錄外的檔案」，方向與最小權限相反。初學者應只授權一個可丟棄的 demo 資料夾。
- `1–2 分鐘出現 PR comment` 是不可靠的速度承諾；成功標準應是 workflow 完成並留下可檢查的結果。
- GitHub Actions 的 `pull_request_target` 搭配 checkout 不可信 PR code 可能暴露 secrets 或寫入權限；原文沒有說明這條重要邊界。
- `code-reviewer` 是官方文件中的自訂 subagent 範例，不是每個 Claude Code 安裝都固定存在的內建 agent。現行內建核心包括 `Explore`、`Plan`、`general-purpose`，而且會隨版本與 session 設定改變。
- `plan.yml`／`max_cost_usd` 沒有跨 Codex、Claude Code、Gemini CLI、OpenCode 的通用規格，不能當成可直接照做的成本控制方法。
- Prompt caching 目前不是只有單一「五分鐘 reuse window」：Anthropic 文件同時說明預設 5 分鐘與可選 1 小時 TTL。A3 不應把供應商細節寫成永久規則。
- 「Opus 掛了就 fallback Haiku」不是可靠的通用 production 策略。模型切換可能改變能力、價格、權限與輸出，必須由使用者明確設定並重新驗證。
- CLI-11 的成本算式表達不清。input 與 output token 要分別乘各自單價；訂閱方案、API 計費與工具顯示的 usage 也不能混為一談。
- 七個 playbook 全部可見，卻又聲稱「其餘折疊」，而且重複 Stage 7.5。A3 應教可執行的安全流程，再把理論導回 Stage 7.5。
- 簡中下一步把 repo 規則檔寫成 `CLAUDE.zh-Hans.md`；專案實際載入的 canonical 名稱仍是 `CLAUDE.md`。

## 章節形狀

### 不展開時看見

1. 一句話目標：先讓 agent 在測試用 PR 做一個只讀檢查。
2. 四個學習目標。
3. 三個核心詞的短表：
   - **MCP**：像轉接頭，讓 agent 使用外部工具；轉接頭能碰什麼，取決於你給的權限。
   - **CI**：像每次交作業都會自動出現的檢查站。
   - **Observability**：像收據與行車紀錄，告訴你做了什麼、花了多少、哪裡失敗。
4. 一條可見安全階梯：`只讀 → 最小權限 → demo repo → 人工 review → 才考慮寫入`。
5. CLI-9 至 CLI-12 的標題、固定 anchor、成果與最低完成條件。
6. 一個短版 production 安全迴圈：先界定範圍、執行、留紀錄、人工判斷、可復原。
7. 保留可見的 `Playbook 4：派遣 subagent 跑獨立任務` 標題與一句話成果，避免三個既有 cookbook 深連結落入收合區。
8. Track A 完成檢查與下一條路徑選擇。

目標：三語未收合正文各降到目前約三分之一；繁中以 **3,600 字元以下**為 ratchet 起點，英文 **5,800**、簡中 **3,700**。字數只是防回退門檻，仍要人工確認能從上往下完成任務。

### 預設收合

- 時間、先備條件、環境、費用與方案差異。
- 必修閱讀與「先讀哪一份」順序。
- CLI-9 的 filesystem MCP、GitHub MCP 與權限測試步驟。
- CLI-10 的 Claude Code／Codex 官方入口、workflow 權限、安全事件與疑難排解。
- CLI-11 的 usage 記錄、成本計算、訂閱與 API 計費差異、observability 延伸。
- CLI-12 的 Skill repo／plugin 分享方式與工具差異。
- 七個 playbook 的完整解釋與 Stage 7.5 對照；Playbook 4 的標題留在外面，細節收合。
- 完整學習資源表、替代工具與下一步說明。

所有 `<details>` 預設關閉，不使用 `open`。任何會直接決定安全、完成條件或下一步的句子不得藏入選單。

## 練習設計

### CLI-9：只連一個、只開一個資料夾

主線使用官方 filesystem reference server，但只讓它接觸新建的 demo 資料夾。成功標準是讀出 demo 資料夾內的檔案，並確認沒有把 home、整顆磁碟、真正的專案或 secrets 一起授權。

GitHub MCP 放在進階步驟，改用 `github/github-mcp-server`。第一次只開讀取 PR／issue 所需能力；若工具支援 toolset 或 scope 限制，就從最小集合開始。`modelcontextprotocol/servers` 只當協定學習範例，不描述成可直接部署的 production server。

### CLI-10：讓 PR 多一個只讀檢查員

讀者選一條官方路徑：Anthropic `claude-code-action` 或 OpenAI `openai/codex-action@v1`。第一輪只在自己控制的測試 branch／demo repo 執行；最小 `GITHUB_TOKEN` 權限、API key secret、trigger 與 sandbox 分開說明。

成功標準改為：workflow 成功結束，並以 PR comment、job summary 或 artifact 留下 review 結果。結果只供人閱讀；不得 auto-merge、push fix 或 deploy。清楚禁止 `pull_request_target` checkout 不可信 PR code，並提醒所有第三方 Action 應依 GitHub 安全建議固定到完整 commit SHA；教學中的簡短 tag 只能標成易讀起點，不宣稱是最高安全設定。

### CLI-11：先看收據，再定停止規則

先分清目前使用的是訂閱方案還是 API 計費，再記錄一個真實 task 的 provider／model、input usage、output usage、時間與結果。能取得單價時，使用：

`input tokens × input price + output tokens × output price`

若工具沒有提供精確 usage 或該方案不是按 token 計費，就明寫「這一欄無法由本次執行確認」，不要猜。停止規則使用工具真正支援的 spend limit、timeout、最大重試或人工 gate；不再虛構通用 `plan.yml`。

### CLI-12：把操作卡交給另一個人

把 A2 的 `review-changes` Skill 放進一個可版本控制的 team repo，附上安裝位置、需求、權限與驗證步驟。Claude Code 使用者可再依官方 plugin 文件打包；其他工具依各自 Skill 路徑安裝。成功標準是第二個乾淨 demo repo 能找到 Skill，跑完仍沒有非預期修改。

`CLAUDE.md`／`AGENTS.md` 等 project instructions 留在專案；它們不是所有工具都能通用安裝的 plugin 內容。

## Playbook 收斂

- 第一遍只教一個安全迴圈，不要求先理解十二個抽象概念。
- Playbook 1–3、5–7 收進「需要時再看」；移除每節重複的小型兩欄表，改成短列點與單一來源連結。
- Playbook 4 標題與原有三語 slug 保持可見；正文改成：內建 agent 名稱會依工具與版本不同，先列出目前可用 agent，再選只讀或自訂 reviewer。`code-reviewer` 只稱為官方文件提供的自訂範例。
- 多 agent、fallback、成本 gate、failure injection 的完整理論都導回 Stage 7.5，不在 A3 重寫第二份。

## 學習資源表

完整表預設收合，改用 HTML `<table>`、五個 `<tbody>` 與真正 `rowspan`。欄位固定為：

`類型｜資源｜先看什麼｜何時使用｜來源`

分組與順序固定為 **4／5／4／3／2，共 18 筆**：

1. **安全連接 MCP（4）**
   - MCP 官方「Connect to local servers」
   - MCP 官方 Security Best Practices（2026-07-28 revision）
   - `github/github-mcp-server`
   - `modelcontextprotocol/servers`（只標為 reference／非 production-ready）
2. **CI 與 PR review（5）**
   - GitHub Actions Security Hardening
   - Anthropic Claude Code GitHub Actions 文件
   - `anthropics/claude-code-action`
   - OpenAI Codex GitHub Action 文件
   - `openai/codex-action`
3. **觀察與評估（4）**
   - `langfuse/langfuse`
   - `Arize-ai/phoenix`
   - `Helicone/helicone`
   - `promptfoo/promptfoo`
4. **分享 Skill／plugin（3）**
   - Anthropic Plugins 官方文件
   - `anthropics/claude-plugins-official`
   - `obra/superpowers-marketplace`
5. **目錄與完整範例（2）**
   - `wong2/awesome-mcp-servers`
   - `obra/superpowers`

移除 `continuedev/continue` 的「CI pattern」定位；它是活躍且有價值的專案，但目前這一列不能直接證明 A3 的最小 PR review 流程。移除 stars、主觀星等、排行榜與會自然變舊的數量。所有 repo 已於查核日確認 public、未 archived、未 disabled；新增的 `openai/codex-action` 必須加入 repository freshness snapshot。

## 官方事實基線

編輯前與 staging 前各重查一次：

- [MCP Connect to local servers](https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers)
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)
- [MCP Registry About](https://modelcontextprotocol.io/registry/about)（目前 preview；metadata 與 namespace 驗證不等於替 server code 背書）
- [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- [Claude Code GitHub Actions](https://docs.anthropic.com/en/docs/claude-code/github-actions)
- [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)
- [Anthropic Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
- [OpenAI Codex GitHub Action](https://developers.openai.com/codex/github-action)
- [OpenAI Codex GitHub integration](https://developers.openai.com/codex/integrations/github)

易變事實只放在需要它的收合區，並顯示 **2026-08-27 UTC** 查核日期。查核日只代表當天已檢查，不保證永久最新。

## 預計修改範圍

- A3 三語正文。
- `stages/DESIGN.md`：記錄 A3 的固定閱讀形狀、安全階梯、深連結與 18 筆合併資源表規則，並把舊的「多 CLI／plugin 打包」定位改回 A1／A2 與工具專屬延伸。
- `scripts/reader-ux-pages.yml`：加入 A3 visible-path ratchet、CLI-9 至 CLI-12、Playbook 4 與完成檢查的可見斷言、資源 rowspans。
- reader UX tests：加入 A3 的 18 筆資源、五個 rowgroup、全關閉 details、安全禁語與三語 URL／數字一致性。
- `scripts/repository-freshness-snapshot.json`：由既有更新器完整重查 297 個 tracked repo，納入本層新增的 `openai/codex-action`，並讓所有列共用同一次批次完成時間；不手寫 API 欄位。
- `CHANGELOG.md`：依最終 diff 記錄實際移動、刪除與事實修正。
- 本計畫檔。

不在 A3 層直接改寫 Stage 5、Stage 7、Stage 7.5、subagent cookbook 或 README。已發現的「內建 agent 清單」「`max_cost_usd`」「MCP production 定位」會在對應章節 layer 重新查證；A3 只修讀者此刻會直接照做的內容。若 A3 的新連結使 strict anchor 或直接入口失效，只做最小相依修正並列入凍結清單。

## 驗收

### 機器檢查

- `git diff --check`
- strict anchors、anchor slug parity、mirror parity、locale links。
- zh-Hans 字元、image locale、duplicate repositories。
- repository freshness strict gate 與相關單元測試。
- `python scripts/build-docs-tree.py`
- `python -m mkdocs build`
- A3 結構斷言：
  - 三語 details 數量一致、全部預設關閉。
  - CLI-9 至 CLI-12 與 Playbook 4 標題、anchor、成果留在可見區。
  - 資源表正好 18 筆、5 個 rowgroup、`rowspan` 總和 18，三語 URL 與順序一致。
  - 不得出現 `plan.yml`、`max_cost_usd`、固定 1–2 分鐘承諾、把 `code-reviewer` 稱為固定內建 agent、把 archived `github` reference server 當現行入口、`CLAUDE.zh-Hans.md`、stars 或主觀星等。
  - 安全階梯、禁止 auto-merge／deploy、最小權限與不可信 PR 警告三語語意一致。

### 人工檢查

- 不展開選單，讀者能用自己的話分清 MCP、CI、observability。
- 不展開也能開始 CLI-9，知道只授權 demo 資料夾，而不是整台電腦。
- CLI-10 先產生只讀建議；人類仍掌握 merge、push、deploy。
- CLI-11 不猜 usage、價格或「便宜／昂貴」模型；資料拿不到就明說拿不到。
- CLI-12 不把某一家工具的 plugin 格式講成所有 CLI 通用。
- 每段先講「現在做什麼」，再補原因；第一次出現的技術詞有一句白話解釋。
- 同類資源真正合併；沒有重複分類、空白分類格、散落 mini-table 或相互打架的推薦路徑。
- 三個 cookbook 深連結仍抵達可見的 Playbook 4。

## Git 與發佈

- A3 維持獨立、可回退的 stacked layer：`codex/track-a3-reader-ux`，base 為已合併 A2 的 `origin/main@9f561ab6d5c941b9ebe297e569a7203e1e60f14c`。
- 先完成繁中內容與事實 gate，再同步英文與簡中；主代理逐欄比對，不以翻譯成功代替語意檢查。
- 逐檔 stage，凍結清單與 staged 檔數必須一致。CHANGELOG 只對最終 diff 寫。
- 穩定 staged fingerprint 執行一次獨立 `code-reviewer`；任何修改都使舊 ack 失效。
- 所有 PR checks 全綠才安全合併；零 checks、PENDING、空狀態或失敗都停止。
- 合併後驗證 main 對應 SHA 的 CI，再清理 A3 worktree／branch。Claude 若同時改到相同檔案，先整合最新 main，不覆蓋對方修改，並使既有 fingerprint 與 review ack 失效。
