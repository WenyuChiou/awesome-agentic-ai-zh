# Track A（A1–A3）漸進式重整計畫

> 查核基準：`origin/main` at `4ebb3a8940fbc8edf684226833feb59c73f68f3c`
> 官方資料與 GitHub API 查核日：2026-08-27 UTC
> 原則：先完成每章計畫，再改繁中；繁中定稿後才同步英語與簡中。

## 1. 成功長什麼樣

讀者第一次打開頁面，不需要展開任何選單，就能回答三個問題：

1. 這一章要幫我做什麼？
2. 我現在只要做哪一件事？
3. 做對了會看到什麼？

「五歲也看得懂」在這裡是清楚度標準，不是幼兒語氣。第一次出現的名詞先用一句白話說明，再保留正確術語、命令、檔名、安全限制與官方來源。

所有完整工具表與資源表都使用語意化 HTML table。相同分類只顯示一次，使用 `<tbody>`、`scope="rowgroup"` 與真正的 `rowspan`；不以空白儲存格假裝合併。

## 2. 已確認的問題

| 頁面 | 目前未展開可見字元 | `<details>` | 核心問題 |
|---|---:|---:|---|
| A1 | 4,243 | 0 | 工具身分混在一起；四個練習與完整排行一次攤開 |
| A2 | 5,285 | 0 | 舊 command 格式、錯誤的截斷說法、資源與主練習混在一起 |
| A3 | 11,667 | 0 | 四個練習、七個 playbook、九個專案全部可見 |
| CLI 指南 | 5,555 | 0 | 主觀排行、易變 stars、舊 repo 路徑與未證實的精確數字太多 |

事實缺陷：

- OpenCode 的 canonical repo 是 `anomalyco/opencode`；專案規則使用 `AGENTS.md`，`CLAUDE.md` 是相容 fallback，不是 `OPENCODE.md`。
- goose 的 canonical repo 是 `aaif-goose/goose`，不應繼續連到搬遷前路徑。
- Claude Code 已把 custom commands 併入 Skills；`.claude/commands/` 仍相容，但新教學應使用 `.claude/skills/<name>/SKILL.md`。
- `CLAUDE.md` 不會因超過 100 行就截斷。官方目前建議每份維持在 200 行內，並強調具體、簡短、可驗證。
- Pi 現在有正式文件與 canonical repo；它是可擴充的 terminal coding harness，不是模型、API provider 或 OpenRouter 的別名。
- `examples/README.*` 宣稱 Track A 有 CLI-9／CLI-10 兩個資料夾，但 repo 裡沒有 `examples/track-a/`；必須改成事實。
- A2、A3 的英語與簡中缺少完整「進入條件」，現有 mirror 不是語意等價。

## 3. 先把五種東西分清楚

A1 用同一張短表建立全站共用心智模型：

| 種類 | 白話說法 | 例子 | canonical home |
|---|---|---|---|
| LLM | 會產生答案的腦 | Claude、GPT、Gemini | Stage 01 |
| Provider API | 直接通往模型公司的門 | Anthropic API、OpenAI API、Gemini API | Stage 01／setup guide |
| Router | 一個入口，替你轉接多家模型 | OpenRouter | A1；Stage 07 講 production routing |
| Coding agent / harness | 在終端機讀檔、改檔、跑命令的工作台 | Claude Code、Codex、OpenCode、Pi | A1–A3 |
| Local runtime | 在自己電腦上把模型跑起來的引擎 | Ollama | Stage 01 |

身份表保持可見；各產品的安裝、計費、provider、sandbox 與限制放進預設收合的詳表。

## 4. PR 切法

不用一條跨 A1–A3 的長 stack。A1、A2 各自合併並驗 main CI；A3 因內容量與安全風險較高，使用兩層短 stack。

```text
A1 身分與第一次安全操作
  ↓ main CI 綠
A2 可重複規則與第一個 Skill
  ↓ main CI 綠
A3a MCP／CI／成本的最小安全主線
  ↓ dependent PR
A3b playbook、資源與進階查證
```

每個 PR 都能單獨 revert。下層 merge 後，dependent branch 重新基於最新 `origin/main`，以 `--force-with-lease` 更新並重跑全部 gate。

## 5. A1：先認東西，再安全地跑一次

### 不展開時看見

1. 這條 Track 適合誰。
2. 三個學習目標。
3. 上面的五種身分短表。
4. 「依你已經有什麼」的短選擇表，不做總排名。
5. CLI-1：在測試資料夾或 demo repo 內完成一次讀取型任務。
6. CLI-2 的標題、錨點與一句話成果。
7. 三項成功檢查與 A2 入口。

CLI-1 不再用「整理 Downloads 並移動檔案」當第一個任務。第一步改成讓工具說明 demo repo、找出測試指令、提出計畫；讀者確認後，才做一個可由 `git diff` 看見、可復原的小改動。

### 預設收合

- 時間、先備條件、費用與帳號。
- CLI-2 詳細步驟。
- CLI-3 第二工具比較與 CLI-4 認證錯誤實驗。
- 指向 CLI 指南完整九工具事實表的閱讀入口。
- 完整學習資源與疑難排解。

CLI-1 至 CLI-4 的標題、錨點與一句話成果都留在 `<details>` 外，避免既有深連結失去落腳點。

### 工具表規則

- 不顯示 stars，也不用五顆星評分。
- 欄位固定為：`類型｜工具｜現在適合誰｜模型／provider 選擇｜登入方式｜安全起手式｜狀態｜官方來源`。
- 狀態只描述官方可證實的現況，不把「最新」「最強」「社群最快」當事實。
- A1 只保留短選擇表與身分辨識；9 個現行 CLI 的完整事實表只在 CLI 指南維護，避免兩頁同步漂移。
- 完整表只保留兩個真正共用的分類，使用 `rowspan` 合併：官方模型生態（4）、可換 provider（5）。Pi 的 minimal 特性與 Hermes 的多介面特性放在各自內容欄，不再為單筆資料製造分類儲存格。
- Pi 列為 minimal／extensible；OpenRouter 放在 Router、Ollama 放在 local runtime，兩者都不列成 CLI agent。

### 直接一致性範圍

- A1 三語。
- CLI 指南三語。
- glossary 的五種身分三語。
- 直接寫死舊 OpenCode／goose 路徑或固定「8 家」的入口文字，改成不易漂移的「CLI 工具比較」。
- `examples/README.*` 的 Track A 現況改成 12 個 inline 練習、沒有獨立資料夾。
- `CLAUDE.md` 與 `docs/TESTING_PLAN.md` 的 Track A 現況列，移除已失真的行數與 8-CLI 說法。
- reader-UX config 與測試、CHANGELOG。

## 6. A2：把重複交代變成一張規則卡

### 不展開時看見

1. 一句目標：讓工具每次進 repo 都先知道同一套規則。
2. 三個詞：project instructions、Skill、單次 prompt。
3. CLI-5：寫一份最小規則檔，只含專案用途、不能做的事、測試指令、交付格式。
4. CLI-6：用目前推薦的 `SKILL.md` 格式做一個可重複 review Skill。
5. 成功檢查與 A3 入口。

### 預設收合

- 時間與進入條件。
- 各 CLI 的規則檔位置對照。
- legacy `.claude/commands/` 相容說明。
- CLI-7 任務拆解與 CLI-8 portable prompt 詳細步驟。
- multi-agent 延伸、完整資源表、替代工具與常見坑。

### 事實修正

- 移除 30–50、50、100 行等無官方依據的硬門檻；只保留官方「每份建議低於 200 行」與「只留下會改變行為的規則」。
- 不再教新手先做 legacy command；改教 Skill，並用一句話說舊 command 仍可運作。
- 不宣稱一份文字可原封不動跨所有 CLI；清楚區分共用內容與工具專屬檔名／權限。
- A2 三語補齊進入條件並做語意鏡像比對。

本輪仍不新增 `examples/track-a/`。現有 repository contract 明確說 Track A 保持 inline；若 Stage 05 重整後要新增一個靜態範例包，先另作設計決定，不在 A2 偷渡。

## 7. A3a：先完成一個小而安全的 production loop

### 不展開時看見

1. 一句目標：讓團隊能看見 agent 做了什麼，並在危險動作前停下來。
2. 三個詞：MCP、CI、trace。
3. 一個整合小專案：選一個低權限 MCP、在 PR 上跑一個只讀／建議型檢查、記錄一次 token 與費用。
4. CLI-9 至 CLI-12 的標題、錨點與一句話成果。
5. 最小 production checklist。

### 預設收合

- 時間、完整先備條件與必修閱讀。
- CLI-9 至 CLI-12 的 provider-specific 詳細步驟。
- Secrets、權限、fork PR、提示注入、預算上限與失敗復原。
- 完整工具比較表。

### 安全底線

- 第一個 MCP 使用最小權限；不以 Gmail、Slack、production DB 作新手第一步。
- GitHub Actions 範例不把未信任 PR 內容與高權限 secret 放在同一個 job。
- 不承諾固定「1–2 分鐘」會出現 review comment。
- 不教用模型名稱硬寫「便宜／昂貴」；費用以當日官方價格與實際 usage 計算。
- CLI-9／CLI-10 不存在範例資料夾的說法修正為 inline exercise。

## 8. A3b：把七個 playbook 變成查問題的工具

不把七個 playbook 連續攤開。可見區只留一張「你遇到什麼問題？」表：

| 問題 | 先看哪個 playbook |
|---|---|
| 任務越做越大 | Scope |
| 多個 agent 互相撞檔 | Isolation／reconciliation |
| 不敢相信輸出 | Review／eval |
| CI 太自由 | Approval／sandbox |
| 帳單失控 | Budget／cache |
| 規則慢慢失效 | Drift／failure injection |

完整 playbook、來源與專案表放進預設收合區。相同來源類別合併；第三方文章只作延伸閱讀，不用來證明工具目前的認證、價格、權限或功能狀態。

## 9. 每個 PR 的查核流程

1. 編輯前重查官方文件與 GitHub API UTC 日期；全量 repo snapshot 以整批掃描完成後取得的官方時間作 `checked_at`，不能把掃描期間的新資料標成更早已確認。
2. 繁中先完成主線、事實、錨點、表格與 `<details>`。
3. 主代理檢查「不展開也能開始」後，才同步英語與簡中。
4. 三語逐項比對工具名稱、命令、路徑、數字、狀態、警告與 URL。
5. 跑 reader-UX、template、anchor、mirror、locale、Hans、freshness、docs tree 與 MkDocs gates。
6. 逐檔 stage，記錄檔案數與 staged fingerprint。
7. 最終穩定 diff 只跑一次獨立 `code-reviewer`；任何修改都讓 ack 失效。
8. commit、PR、全綠後安全 merge；再驗 main 對應 SHA 的 CI。

## 10. 驗收標準

- A1、A2、A3 三語都加入 reader-UX ratchet；所有 `<details>` 預設關閉。
- 不展開仍看得到本章目的、第一個行動、完成條件與下一章入口。
- CLI-1 至 CLI-12 與七個 playbook 的既有深連結仍有可見落腳點。
- OpenRouter、OpenCode、Pi、Ollama 不再被放在同一產品類型。
- 所有資源表同類欄位真正合併，沒有空白分類格與重複分類字樣。
- Stage pages 不再維護 stars；完整表每列有官方來源與 2026-08-27 查核日。
- 三語沒有不同的登入、sandbox、secret、費用或安全指引。
- `examples/README.*` 不再宣稱不存在的 Track A 資料夾。

## 11. 官方事實來源

- [OpenRouter FAQ](https://openrouter.ai/docs/faq)
- [OpenCode documentation](https://opencode.ai/docs)
- [Pi documentation](https://pi.dev/docs/latest)
- [Claude Code documentation](https://code.claude.com/docs/en/overview)
- [OpenAI Codex documentation](https://developers.openai.com/codex/cli)
- [Gemini CLI documentation](https://google-gemini.github.io/gemini-cli/)
- [goose documentation](https://block.github.io/goose/)
- [Aider documentation](https://aider.chat/docs/)
- [Hermes Agent documentation](https://hermes-agent.nousresearch.com/docs/)
- [Grok Build repository and documentation](https://github.com/xai-org/grok-build)
