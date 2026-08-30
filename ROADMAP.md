# 路線圖 / Roadmap

> **繁體中文** | [简体中文](./ROADMAP.zh-Hans.md) | [English](./ROADMAP.en.md)

這份文件只回答兩件事：**現在已經能用什麼？接下來還要補什麼？** 它不是發行日期，也不承諾完成時間。

**狀態圖例**：🟢 正在做／隨時可貢獻 · 🟡 已知缺口 · 🔵 想法 · ✅ 最近完成

---

<a id="近期想補的缺口"></a>
<a id="進行中--隨時可貢獻"></a>
<a id="-動手練習覆蓋補齊"></a>
<a id="-audience-branch-深化"></a>
<a id="-stage-2--stage-3-2026-freshness-小修"></a>

## 🟢 現在正在做

### 1. 把整站接成同一條路

文字路線統一為：

- 共用基礎：`Stage 0 → Stage 1 → Stage 2`
- Track A：`A1 → A2 → Stage 5 → A3 → Stage 8`
- Track B：`Stage 3 → Stage 4 → Stage 5 → Stage 6 → Stage 7 → Stage 7.5 → Stage 8`

Track A 做完 A3 就能開始 Capstone；Stage 8 建議完成，但不擋入場。首頁學習地圖、文字與測試現在使用同一條路線；之後改順序時，三者要一起更新。

### 2. 整理五條角色路徑

研究人員、開發者、教師、知識工作者與日常使用者都會補上「今天先做什麼」。第一個動作留在畫面上；完整專案表、替代方案與疑難排解預設收合。重要名詞與五星編輯推薦度不會因為縮短頁面而消失。

### 3. 整理 setup、courses、cookbook、glossary 與 catalog

- Setup 先幫讀者選 Web、Desktop、IDE、CLI 或 API，再展開安裝細節。
- Cookbook 先顯示成果、第一個可複製動作與成功條件。
- Glossary 的名詞和短定義保持可搜尋；長例子才收合。
- MCP／Skills catalog 保持可搜尋，增加分類導航與維護狀態，不把每一列拆成一個選單。

### 4. 持續檢查 repository 與易變資訊

每週 workflow 逐一檢查 canonical GitHub repo、redirect、archive、license metadata、release 與最近活動。較久沒 push 只會產生 warning，不會自動刪除穩定且仍有教學價值的專案。模型、價格、API 與產品能力仍要回官方文件逐章查證。

---

<a id="基礎建設maintainer-進行中"></a>

## ✅ 最近完成

- Stage 0–8 與 A1–A3 已完成第一輪漸進式揭露、三語一致性、核心詞與資源表整理。
- Stage 2 保留 zero-shot、one-shot、few-shot、Chain of Thought 等必要名詞，並加入三語 Prompt Engineering 概念圖。
- Stage 3 用三語圖教第一個 Agent Loop；Stage 4 用 framework 教 Workflow Graph；Stage 7 以 Agent Production Engineering 整合 Harness、Loop 與 Graph。Stage 6 重畫兩條路的 RAG pipeline；Stage 8 補上介面選擇與安全檢查圖。
- Stage 0 有整合練習；Stage 7.5 本來就是 reading map，不強迫新增程式資料夾；Stage 8 已有可複製的安全練習，獨立 end-to-end 範例仍可貢獻。
- MkDocs build、三語 mirror／anchor／locale gate、reader-UX gate、freshness gate 與 repository snapshot 都已納入維護流程。

---

## 🟢 很適合貢獻的小任務

- 回報過時事實或失效連結，附官方新來源。
- 替一個練習補上更清楚的「怎麼跑」與成功條件。
- 修順一段英文或簡中鏡像，但不要改變原意、數字、URL 或安全規則。
- 替 role path 補一個真實情境，說清楚輸入、輸出、人工檢查與隱私邊界。
- 替穩定專案補 status／license／限制；不要只用 stars 或最近 push 日期下結論。

先看 [`CONTRIBUTING.md`](CONTRIBUTING.md)；想長期維護一章，再看 [`CONTRIBUTORS.md`](CONTRIBUTORS.md)。

---

<a id="想法箱待討論還沒承諾"></a>

## 🔵 還在討論

- 是否需要第三條正式軌道，例如 no-code／web-only 路線；目前日常使用者可直接走 role path，不必先多造一條主幹。
- 是否加入最小影音 walkthrough；需要先衡量字幕、三語同步與長期維護成本。
- Voice Agent 與 VLA 應放在既有 Stage 8／研究或開發者延伸，還是需要新的專題頁；先避免為新名詞增加主線負擔。

要提想法請開 [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions)；issue 留給缺陷、過時資訊或明確的新資源。
