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

- `License`（SPDX ID 或標註例外，見 5）
- `推薦度`（⭐ × N，見 2）
- `教什麼`、`適合誰`

### 必填欄位（非 repo entry：article / course / video / protocol / documentation）
某些 entry 不是 GitHub repo 而是文章、影片、官方文件、catalog hub。對這類：

- `推薦度`（必填）
- `教什麼`、`適合誰`（必填）
- `形式`（必填，標明是 `文章` / `影片` / `課程` / `精選清單` / `規格文件` 等）

範例：`Anthropic — Building Effective Agents` 部落格文章用 `形式 = 文章` + 推薦度，不需要 repo 的 License 欄位。

### 全站資源選擇規則

推薦度是每筆 entry 必填的編輯判斷。

- 用現行官方文件、規格與 model card 查證事實。
- 用知名或廣泛使用、可實作的 repo，給讀者一條動手的路。
- 人氣只用來找候選，不能取代維護、License、安全或相關性檢查。
- 每個 project 都要說明它教什麼、適合誰，以及目前狀態或限制。

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

這是編輯評分，不是 GitHub stars。只有資源用途、品質或維護狀態的查證結果改變時，才能連同理由調整評分。

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
| Gemini Notebook-like 工具 | 類 Gemini Notebook 的工具 / 類似 Gemini Notebook 的工具 |
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

## 🧩 先認識核心詞

### **正確術語（需要時附中文）**
一句白話定義。再給一個不會扭曲概念的生活比喻，並說明後面的哪個練習會用到它。

## 🚪 進入條件（Stage 1+ 才需要）
<details markdown="1">
<summary>⏱ 開始前先看：時間、先備工具與預算</summary>

**時間估算**：N-M 週（約 X-Y 小時）

你應該已經：
- ...

</details>

## 📚 必修閱讀
先列出 1–3 個完成眼前練習真的會用到的來源。這些連結保持可見，不能只藏在收合區。

1. [必要連結](url) — 會在哪一步用到
2. ...

<details markdown="1">
<summary>展開：完整閱讀順序與延伸來源</summary>

1. [延伸連結](url) — 描述
2. ...

</details>

## 🛠 動手練習（不是看過就好）

### 練習 N：標題
一句話描述完成後會看到什麼。標題留在 details 外，讓深連結可見。

<details markdown="1">
<summary>展開詳細步驟</summary>

時間、費用、程式碼、預期輸出與疑難排解。

</details>

可執行資料夾必須先提供可直接複製的 PowerShell 指令，再用預設收合的 `<details>` 提供 macOS/Linux 替代指令；同時提供 Path A 與 Path B 腳本，以及不打 API 的 offline mock tests。SDK 依賴要限制 major version，cloud model 要使用釘住的 model ID；執行前必須驗證不受信任的工具名稱與參數。Cloud 成本寫成 token 公式並標示核對日期，不要假設一個固定金額。不同 framework 的範例各自建立 Python 3.11 `.venv`，不要合併 requirements。測試必須走過核心行為；只驗 import 成功不算通過。

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

練習標題、成果和第一步保持可見。次要 `<details>` 預設不加 `open`。雙路徑練習仍以 Ollama Path A 為主要路徑，但不是看到 Path A 就一律展開：只有它是讀者眼前唯一要做的事，而且展開後內容很短時才可加 `open`。長程式碼與疑難排解預設收合；Anthropic Path B 也預設收合。不要把可被連結的 heading 包進 `<details>`，也不要用三層以上的巢狀收合。

若一個進階主題已大到有自己的必讀、核心詞、練習與精選資源表，建立可獨立閱讀的三語頁面，不要把整章塞進 Stage 的長 `<details>`。Stage overview 必須提供可見入口；獨立頁的頁首與頁尾都要回到同語言 Stage。被搬出的重要名詞、必讀與五星資源仍直接可見，只有安裝、成本、替代方案與排錯收合。舊深連結留在語意相符的可見 gateway，不能讓 anchor 落入關閉內容。

### 全站白話規則（ELI5）

這份規則適用整個學習地圖。目標是讓五歲小孩也能跟得上「現在要做什麼」，但不能犧牲技術正確性。

- 技術詞第一次出現在可見教學文字時，要用**粗體**標出；接著先說白話用途，再保留正確術語。例如：「讓程式拿資料的入口（**API**）」。H1 可以直接使用章名，但正文第一次使用仍要套用這條規則。
- 一句只講一件事，一個步驟只要求一個主要動作。看見長句、縮寫或 jargon，先拆開或補一句定義。
- 指令、檔名、錯誤碼、模型名稱、價格、數字與安全提醒必須保持精確。
- 不展開任何 `<details>` 時，讀者仍要知道下一步要做什麼，以及完成時會看到什麼。
- Review 時抽查可見主線：第一次來的讀者若無法用自己的話說出下一步，就先改寫；需要多段的原理移入預設收合內容。

### 核心詞寫法

- 每個完成回溯的 Stage／Track，都要在第一個練習前放一個可見核心詞區。核心詞名稱與最短解釋不能放進 `<details>`。
- 每個核心詞獨立回答四件事：**它是什麼**、**它像什麼**、**這章用它做什麼**、**正確術語是什麼**。需要更深原理時，再把補充放進預設收合區。
- 只收後文、練習或 self-check 真的會用到的關鍵概念。不要把每個普通名詞拉出來湊數，也不能用「太細」當理由刪掉 Zero-Shot、Token、MCP 等必要術語。
- 三語的概念、順序、用途與限制一致；英文名、縮寫、指令與規格名稱保持精確。
- `scripts/reader-ux-pages.yml` 的 `core_terms` 會記錄核心區、第一個練習、三語 term／label、順序與最低解釋長度。加入後只能維持或加強，不能靜默移除。

### 概念圖寫法

- 先在正文用白話定義核心詞，再用圖整理它們的關係；不要讓圖成為讀者第一次遇到術語的地方。
- 預設參考主頁 README：奶油白底、深藍主字、少量亮色、圓角卡、簡單線條 icon、充足留白與一個主要閱讀方向。每張圖只回答一個核心問題；資訊太多時拆成兩張，不縮字硬塞。
- 新畫或重畫的概念圖以 Image 2.0 產出 PNG，不用臨時 SVG 代替；舊圖輪到該章重畫時才套用，不一次改壞全站歷史。
- 三語圖保持同一畫布比例、構圖、共同格線、順序、數字與限制，並各自提供正確語系的圖檔與 alt text。卡片位置、外距、內距與同層高度要一致。
- 圖裡的精確數字也要有官方依據。沒有固定通則時，寫「多個」「依模型而異」等誠實文字，不要為了好看造出範圍。
- 箭頭只走留白通道，不穿過文字、icon 或其他卡片；arrowhead、icon、標籤與框線不得互相重疊。同層卡片使用共同格線、等高與一致內距。
- 逐張以原尺寸檢查安全邊界、文字、繁簡字形、箭頭、共同格線與對比；任何文字、icon、箭頭或框線重疊都視為失敗。最後跑 image-locale gate 與三語 MkDocs build。
- 文件站會自動替非首屏教學圖加入 lazy loading、async decoding 與可鍵盤操作的「開啟原圖」入口；README 頂端 banner 保持 eager，不要在各章重複手寫這些 HTML。新增或替換圖檔要通過 `scripts/check-image-delivery.py` 的單圖、單頁、總量與建置後 HTML ratchet，並以 320／375／768／1440 px 人工確認 caption、表格、觸控目標與圖中文字真的讀得到。

### Reader UX ratchet

- 章節完成三語遷移與人工複查後，才加入 `scripts/reader-ux-pages.yml`。這是逐章收緊，不要求尚未整理的頁面一次全部通過。
- `scripts/check-reader-ux.py` 使用保守的 source-level proxy，計算第一次開頁時可見 Markdown 的非空白字元。預設展開內容與可見 fenced code 算入；HTML comment 與收合內容不算。這是可重複的 ratchet，不是瀏覽器 DOM 字數。
- 設定檔會保存三語各自的字數上限、允許預設展開的數量、必須保持可見的精確 heading／anchor、核心詞契約，以及資源表的分組列數。沒有重新審查，不得調高上限或刪除保護項目。
- 自動 gate 只能防止已知結構倒退。人工 review 仍要確認：不展開任何選單時，讀者知道要做什麼，也知道成功會看到什麼。

### 分組資源表

- 同一分類連續出現兩列以上時，改用 HTML `<table>`，並以 `<th scope="rowgroup" rowspan="N">` 合併分類欄。
- 每個 `<thead>` 欄位標題 `<th>` 都要加 `scope="col"`。
- 每個分類使用一個獨立的 `<tbody>`；分類的第一列保留 `<th scope="rowgroup" rowspan="N">`。
- 只合併真正共用的分類。不同分類不可因狀態、Context 或其他文字剛好相同而跨組合併。
- 轉換後保留原有資源數量、順序、連結與三語對應，並用 MkDocs 檢查實際渲染。
- 沒有重複分類的短表格繼續使用 Markdown，避免為了格式增加維護成本。

含模型、價格、context、授權或生命週期狀態的頁面，把可見查核日期用小字放在受影響的表格或段落附近。只有該內容本身是補充資料時，日期才跟著收合；頁首只保留不顯示的機器 marker：

```markdown
<small>資料查核：YYYY-MM-DD UTC</small>

<!-- freshness: canonical=stages/0N-slug.md; verified_on=YYYY-MM-DD; scope=models,pricing,availability,deprecations; max_age_days=90 -->
```

日期只寫查核範圍與日期，不重複加入「資料不會永久正確」等通用提醒。三語 marker 必須完全一致；`canonical` 一律指向繁中主頁。官方沒有公布的欄位寫「官方未公布」，不要從第三方榜單反推；第三方 benchmark 只能教讀者怎麼自己評測。

**Stage 0 例外**：可以省略 `精選 Projects`、`進入條件`，因為它是 prerequisite gateway。可見主線依序保留 skip 判斷、4 個學習目標、1 個整合練習、18 筆五星學習資源與短版完成檢查；時間、環境、補充練習與名詞預設收合。

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

### 角色路線頁

完成回溯並加入 `scripts/reader-ux-pages.yml` 的角色頁，三語都保留可見主線 `📌 → 🎯 → 🧩 → 🛠 → 📚 → ✅`：先說這條路解決什麼，再列學習目標、粗體核心詞、可直接複製的小任務、入口與完成檢查。先用白話定義核心詞，再保留正確英文術語；不能因為簡化而刪除後文會用到的技術詞。

第一個任務必須小、可測、可回復。若任務會改檔案，要明寫 read-only plan、人工批准、diff、test、rollback，以及 agent 不得自行 push／merge／deploy。必修閱讀、精選專案、完整五星學習資源與安全警告保持可見；替代方案、費用、進階流程與排錯才放進預設關閉的 `<details markdown="1">`。專門的大型 catalog 可讓每個分類入口與安全邊界可見，再讓讀者按分類展開其中上百筆項目。既有深連結的空 anchor 放在語意相符的新 heading 或 summary 旁，並保留可見的回主路線連結。

工具的核心身分和 surface 分開寫。IDE、CLI、desktop、cloud、CI、SDK 可以同時出現，不能當成互斥分類。OpenRouter 是 Provider／Router，Ollama 是 Model／Runtime，coding agent／harness 是另一個身分軸。

角色頁的分組資源表遵守上面的 `rowspan` 規則。三語須保留相同 URL 順序、狀態、授權、限制與穩定的編輯評分（⭐⭐⭐–⭐⭐⭐⭐⭐）；不寫易變的 GitHub stars。ELI5 白話仍須保留等價語意、技術名詞與安全限制。

### Cookbook

Cookbook 的用途、選擇表、核心詞、六份 recipe 標題、成果、第一個可複製動作、必修閱讀、精選資源與完成檢查保持可見；九個完整步驟／替代方案／排錯區塊預設收合且不加 `open`。每個核心詞第一次出現就用粗體白話定義，不能把可執行命令或產品名稱翻成另一個東西。

完整資源表固定使用六個獨立 `<tbody>`，以 `scope="rowgroup"` 和 `rowspan` 合併分類欄。三語的 URL、命令、日期、授權、安全限制與編輯評分一致；社群整合明標非官方、可能失效與官方 fallback。易變事實附查核日期，但不加入「永遠最新」之類的保證。

### Resources 工具櫃入口

`resources/README*` 先問讀者卡在哪裡，再用粗體白話定義 Reference、Guide、Cookbook、Catalog 與 Glossary。11 份 reference 的入口、用途、限制與回主線連結保持可見；只有分檔理由與 maintainer 規則收合。不要加會漂移的行數、GitHub stars 或把舊產品名稱寫成現行名稱。

完整入口表固定使用五個獨立 `<tbody>`，分類列數為 `4／2／2／2／1`。同類型只在第一列出現一次，使用 `scope="rowgroup"` 與真正 `rowspan`；不可用重複文字或空白儲存格假裝合併。三語檔名依 locale 指向自己的 mirror，順序與語意一致。

### Glossary 查字入口

Glossary 的快速地圖、工具身分表、每個詞的 heading 與一句白話定義保持可見；不能把最短答案藏進 `<details>`。只有 maintainer 完整分類表、來源與查核說明預設收合。第一次出現的核心詞照全站規則用**粗體**標出，並保留正確英文術語。

工具身分表要直接分清 Provider API、Router、Model Runtime、Coding Agent／Agent Harness 與 Agent Framework。型號、價格、context、固定 token 換算等易變快照不要複製到 Glossary；改連到有 freshness gate 的章節或官方文件。

### 內部連結
- Stage 之間：相對路徑 `[Stage 4](04-agent-frameworks.md)`
- Branch ↔ README：`[← 回主路線](../README.md)`
- 跨 stage 引用同一 repo：用全名 + 連結，不要只寫「之前提過」

### 外部連結
- GitHub repo：`https://github.com/owner/repo` ✓ 不加 trailing slash
- 文章 / 部落格：完整 URL，標題用粗體
- 商業產品（Cursor、Make.com 等）：用官方網址，不是 affiliate
- 正文第一次提到 repo、規格或官方工具時，就加上超連結；不要讓初學者看到裸露的 `owner/repo` 後還要自己搜尋。完整資源表再補狀態、授權、限制與評分。

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

這份指南本身也歡迎 PR。修改前請先開 Issue 討論——術語決策會影響三語的許多 entry。

當前 maintainer：[@WenyuChiou](https://github.com/WenyuChiou)。
