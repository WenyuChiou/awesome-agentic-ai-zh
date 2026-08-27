> **繁體中文** | [简体中文](./style-guide.zh-Hans.md) | [English](./style-guide.en.md)

# `awesome-agentic-ai-zh` 風格指南

這份指南是這份 catalog 的**單一真實來源**——術語、entry 結構、license 標註、寫作風格、禁用詞，全部以這份文件為準。

PR 之前請先讀完本文。專案維護者也會用這份指南做 review。

---

## 📋 目錄

- [1. 專案 entry schema](#1-專案-entry-schema)
- [2. 推薦星等定義](#2-推薦星等定義)
- [3. 禁用詞與替代](#3-禁用詞與替代)
- [4. 可保留的英文名詞](#4-可保留的英文名詞)
- [5. License 標註慣例](#5-license-標註慣例)
- [6. Stage 頁面模板](#6-stage-頁面模板)
- [7. Branch 頁面模板](#7-branch-頁面模板)
- [8. 寫作風格規範](#8-寫作風格規範)
- [9. 連結與引用](#9-連結與引用)

---

## 1. 專案 entry schema

每個 project entry 統一格式如下：

```markdown
### [Repo Name](https://github.com/owner/repo) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| 語言 | Python |
| Stars | ★ 12k+ |
| License | MIT |
| 推薦度 | ⭐⭐⭐⭐ |

**教什麼**：1-2 句話，這個 project 在這個 stage 教什麼具體的東西。

**適合誰**：1 句話，誰應該讀這個、為什麼。

**備註**：1-3 句個人評價。哪裡好、哪裡弱、哪裡可以跳。（可省略）

**怎麼跑**：
\`\`\`bash
# 最小安裝指令、第一次跑該執行什麼
\`\`\`
```

### 必填欄位（GitHub repo entry）
對「真實 GitHub repo」的 entry：

- `Stars`（★ Xk+ 格式，無千位逗號）
- `License`（SPDX ID 或標註例外，見 5）
- `推薦度`（⭐ × N，見 2）
- `教什麼`、`適合誰`

### 必填欄位（非 repo entry：article / course / video / protocol / documentation）
某些 entry 不是 GitHub repo 而是文章、影片、官方文件、catalog hub。對這類：

- `推薦度`（必填）
- `教什麼`、`適合誰`（必填）
- `形式`（必填，標明是 `文章` / `影片` / `課程` / `精選清單` / `規格文件` 等）
- `Stars` / `License` 可省略（沒有 GitHub repo 對應）

範例：`Anthropic — Building Effective Agents` 部落格文章用 `形式 = 文章` + 推薦度，不需要 Stars / License。

### 選填欄位
- `語言` — 主要程式語言（Python / TypeScript / 中文 等）
- `最後更新` / `狀態` — 已停滯或維護放緩時加註
- `備註`、`怎麼跑`

### 標題格式
- Stage 1-4 / 6 用 `### [Repo](url)`
- Stage 5 / 7 / branches 用 `#### [Repo](url)`（已有上層 H3 分類時）
- 標題後可接星等：`### [Repo](url) ⭐⭐⭐⭐⭐` 或副標：`### [Repo](url) ⭐ 官方`

---

## 2. 推薦星等定義

| 星等 | 含義 | 何時用 |
|---|---|---|
| ⭐⭐⭐⭐⭐ | 必讀 / 必做 | 該 stage 不讀這個會卡住 |
| ⭐⭐⭐⭐ | 強烈建議 | 深入學該主題的好材料 |
| ⭐⭐⭐ | 紮實範例 | 值得跑一遍、互相對照 |
| ⭐⭐ | 有用參考 | 有興趣再看 |
| ⭐ | 利基 / 進階 / 為了完整性 | 多數讀者可跳 |

**準則**：

- 同一個 repo 出現在不同 stage / branch 時，**星等應一致**（除非有明確 audience-specific 理由，且註明在備註）
- 不要因為「想要看起來推薦」就給高星等。誠實 > 客氣
- 商業產品（Cursor、LangSmith 等）也照同一套標準

---

## 3. 禁用詞與替代

這份文件以**繁體中文（zh-TW，台灣慣例）** 為準。下表列出常見的 zh-Hans 用詞與替代。

> 📌 **語言代碼慣例（BCP 47 / W3C i18n）**：repo 用 `.zh-Hans.md`（不是 `.zh-CN.md`）標記簡體中文檔。`Hans` / `Hant` 是 [BCP 47 script subtag](https://www.w3.org/International/articles/language-tags/)，跟地區解耦——簡體中文不只用在中國大陸（也用在新加坡、馬來西亞），用 `Hans` 比 `CN` 更準確。canonical README 的內容是 **zh-Hant-TW**（繁體中文，台灣慣例），但檔名保持無 suffix 的 `README.md` 作為 GitHub 預設首頁。未來若要分地區可再擴成 `zh-Hans-CN` / `zh-Hant-HK` 等。感謝 [@xfq](https://github.com/xfq)（W3C i18n lead）在 [#9](https://github.com/WenyuChiou/awesome-agentic-ai-zh/issues/9) 指出這個問題。

### 繁簡用詞替換

| 禁用（zh-Hans） | 改用（zh-TW） |
|---|---|
| 教程 | 教學 / 課程 / 導讀 |
| 視頻 | 影片 |
| 軟件 | 軟體 |
| 文件（指 file 時） | 檔案 |
| 文档 / 文件（指 docs 時） | 文件 / 文件（這個保留） |
| 代碼 | 程式碼 / 原始碼 |
| 用戶 | 使用者 |
| 網絡 | 網路 |
| 接口 | 介面 |
| 默認 | 預設 |
| 函数 | 函式 |
| 算法 | 演算法 |
| 程序（指程式時） | 程式 |
| 質量（指品質時） | 品質 |
| 信息 | 資訊 |
| 數據 | 資料 |
| 內存 | 記憶體 |

### Overclaim（誇大）用語禁用

| 禁用 | 改用 |
|---|---|
| 全世界最好的 / 業界最強 | 完整的 / 知名的 / 廣泛使用的 |
| production-grade（描述教材時） | 教學導向 / 用來學 production pattern 的教材 |
| 首選 / 唯一選擇 | 不錯的選項 / 入門選擇之一 |
| 最緊迫 / 最重要 | （直接不要修飾） |
| 權威參考（除非真的是官方 spec） | 重要參考實作 / 官方範本 |
| 沒問題（法律或 license 判斷時） | 使用前先讀條款 / 條款還是要自己看過 |

### 中夾英（English-in-Chinese）禁用句型

| 禁用 | 改用 |
|---|---|
| follow 條款 | 遵守條款 |
| ready-made 教材 | 現成可改的教材 |
| NotebookLM-like 工具 | 類 NotebookLM 的工具 / 類似 NotebookLM 的工具 |
| 視覺化 node-based | 視覺化節點式 |
| Anthropic host 的 server | Anthropic 維護的 server |
| coding 流程 | 開發流程 / 程式開發流程 |

---

## 4. 可保留的英文名詞

技術寫作中**保留英文**比硬翻譯讀起來更自然的詞：

- `LLM`、`API`、`SDK`、`MCP`
- `agent`、`tool use`、`function calling`、`prompt`、`prompt caching`
- `framework`、`library`、`repo`、`commit`、`PR`、`branch`
- `RAG`、`embedding`、`vector DB`、`retrieval`、`chunk`、`token`
- `streaming`、`async`、`batch`、`webhook`
- `marketplace`、`plugin`、`skill`、`hook`
- `project`、`repo` （可保留也可改用「專案」）
- `production`（指「正式環境」時）— 但本 catalog 多數場合刻意避免（見 3）
- `動手練習`、`hello-world` — 保留

**判準**：技術文件圈讀者習慣的英文術語就保留，避免「太政治正確的中文化」。

---

## 5. License 標註慣例

### 常見 license 直寫
- `MIT`
- `Apache-2.0`
- `BSD-3-Clause`
- `GPL-3.0`
- `LGPL-3.0`

### 需要加註的特殊情況

| 情況 | 寫法 |
|---|---|
| 上游無 SPDX | `NOASSERTION（上游未提供 SPDX；使用前請讀 LICENSE）` |
| AGPL（傳染性） | `AGPL-3.0` + 備註：`AGPL-3.0 license（傳染性開源）— 修改後散布的衍生產品需遵守條款。` |
| 自訂非商用 | `NOASSERTION（自訂非商用）` + 備註：`License 是自訂非商用條款，使用前請先讀原始條款。` |
| 多元 license（每個 plugin 自己有） | `NOASSERTION（每個 plugin 獨立 license，請看各自目錄）` |
| Creative Commons | 直寫 `CC-BY-4.0`、`CC-BY-NC-SA-4.0` 等 |

**規則**：**永遠不要**把 license 解讀成法律建議。「研究 / 個人使用沒問題」這種句子禁用。改成「使用前先讀原始條款」。

---

## 6. Stage 頁面模板

> 同一個模板適用於兩個位置：
> - `stages/0X-*.md` — 共用基礎（0-2）+ Track B（Stage 3-8）
> - `tracks/cli/AX-*.md` — Track A（A1-A3）的 sub-stage，也照同一模板，只是 cross-link 比例較高（多數 entry 引用既有 Stage 5 / 7 / cli-agents-guide）

每個 stage（Stage 0 除外）都應該有：

```markdown
# Stage N — 主題

> [English](./0N-slug.en.md) | **繁體中文**

[1-2 句話描述這個 stage 的核心問題]

## 📌 學習目標
- bullet 1
- bullet 2
...

## 🚪 進入條件（Stage 1+ 才需要）
<details markdown="1">
<summary>⏱ 開始前先看：時間、先備工具與預算</summary>

**時間估算**：N-M 週（約 X-Y 小時）

你應該已經：
- ...

</details>

## 📚 必修閱讀
這些資料會在練習中用到；需要時再展開。

<details markdown="1">
<summary>展開 3-5 個必讀來源</summary>

1. [連結](url) — 描述
2. ...

</details>

## 🛠 動手練習（不是看過就好）

### 練習 N：標題
一句話描述完成後會看到什麼。標題留在 details 外，讓深連結可見。

<details markdown="1">
<summary>展開詳細步驟</summary>

時間、費用、程式碼、預期輸出與疑難排解。

</details>

[3-5 個動手練習 items]

## 🎯 精選 Projects

### [Project Name](url) ⭐⭐⭐⭐
[entry schema 見 1]

[N 個 entries]

## ✅ 進 Stage N+1 前的自我檢查
你能不能：

- [ ] ...
- [ ] ...

如果可以 → 進 Stage N+1。
如果不行 → ...

## 💡 接下來（選填，多在最後一個 stage 用）
```

次要 `<details>` 預設不加 `open`。唯一通例是雙路徑練習的主要 Ollama Path A；Anthropic Path B 仍預設收合。不要把可被連結的 heading 包進 `<details>`，也不要用三層以上的巢狀收合。

含模型、價格、context、授權或生命週期狀態的頁面，在資料附近加入可見查核日期與機器 marker：

```markdown
> 資料查核：YYYY-MM-DD UTC。價格與可用性之後可能改變，使用前請再看官方頁面。

<!-- freshness: canonical=stages/0N-slug.md; verified_on=YYYY-MM-DD; scope=models,pricing,availability,deprecations; max_age_days=90 -->
```

三語 marker 必須完全一致；`canonical` 一律指向繁中主頁。官方沒有公布的欄位寫「官方未公布」，不要從第三方榜單反推；第三方 benchmark 只能教讀者怎麼自己評測。

**Stage 0 例外**：可以省略 `精選 Projects`、`進入條件`，因為它是 prerequisite gateway。

---

## 7. Branch 頁面模板

```markdown
# 給 [audience] — 專業分支

> [English](./for-X.en.md) | **繁體中文**

> [← 回主路線 README](../README.md) · 從 Stage 7 結尾分支出來

## 使用情境
- bullet 1
- bullet 2

## 精選 Projects

### 子分類 1
#### [Project](url) ⭐⭐⭐⭐
[entry]

### 子分類 2
...

## 必修閱讀
1. ...

## 必練流程
- bullet 1
- bullet 2
```

Branch 的 entry 格式可以比 stage 簡潔（不一定要完整 schema 表格），但連結 + 星等 + 1-2 句描述是最低門檻。

---

## 8. 寫作風格規範

### 句長
- **單句不超過 60 字**（中文標點計入）
- 太長就斷成兩句
- 英文 rhythm 強迫塞進中文 = 翻譯腔，要避免

### 標點
- **中文用全形**：，。：；「」（）
- **句中夾英文**時，英文前後可以留空格也可以不留，但全文要一致
- **避免 ASCII 逗號 `,`** 在中文句中（會中夾英）

### 主動 vs 被動
- 偏好主動句：「Claude 呼叫工具」 ✓
- 避免被動句：「工具被 Claude 呼叫」 ✗

### 「你」 vs 「我們」
- **「你」優先**——這是給讀者的學習材料
- 「我」用於作者發表意見時：「我建議...」
- 避免「我們」（除了合著者實際存在的場合）

### 連接詞
- 偏好簡單：「但、所以、因為、不過」
- 避免：「然而、因此、由於、之所以」

---

## 9. 連結與引用

### 內部連結
- Stage 之間：相對路徑 `[Stage 4](04-agent-frameworks.md)`
- Branch ↔ README：`[← 回主路線](../README.md)`
- 跨 stage 引用同一 repo：用全名 + 連結，不要只寫「之前提過」

### 外部連結
- GitHub repo：`https://github.com/owner/repo` ✓ 不加 trailing slash
- 文章 / 部落格：完整 URL，標題用粗體
- 商業產品（Cursor、Make.com 等）：用官方網址，不是 affiliate

### 連結文字慣例
- Repo entry 標題：`[owner/repo](url)` 或 `[Project Name](url)`
- 句中引用：`[Repo Name](url)` 或 `\`owner/repo\``（短引用用 inline code）
- 連結文字**避免**「點這裡」、「按這個」

---

## 相關內部設計文件

這份 style-guide 講「entry 怎麼寫」。為什麼分這 5 個 branch、為什麼是 8 個 stage 這類**設計理由**，見：

- [`branches/DESIGN.md`](../branches/DESIGN.md)——branch 設計筆記（為什麼這樣切、entry 該放哪）
- [`stages/DESIGN.md`](../stages/DESIGN.md)——stage 設計筆記（為什麼這結構、動手練習 怎麼挑）
- [`cli-agents-guide.md`](cli-agents-guide.md)——cross-cutting CLI agent 比較指南

## 修改本指南

這份指南本身也歡迎 PR。修改前請先開 Issue 討論——術語決策影響 100+ 個 entry。

當前 maintainer：[@WenyuChiou](https://github.com/WenyuChiou)。
