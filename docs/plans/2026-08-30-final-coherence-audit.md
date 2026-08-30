# 全站連貫性與技術品質稽核（2026-08-30）

## 範圍與證據

- 基準：`610b3a4af7b2c2501c25a52deda104f217b0673a`（Draft PR #203）。
- 範圍：公開入口、Stage／Track 交接、角色路徑、walkthrough、examples index、cookbook／glossary／resource pages、MkDocs 樣式與圖片資產。
- 已執行：Reader UX 26 頁 × 3 語言、相關內容測試 293 passed、`build-docs-tree.py`、三語 `mkdocs build`、產出 HTML 結構檢查、圖片尺寸／容量與引用盤點。
- 限制：此主機沒有 `agent-browser`，因此沒有把「真實手機瀏覽器互動」當成已通過；行動版結論只來自 CSS、HTML 與既有測試。

## Audit Health Score

| # | 面向 | 分數 | 關鍵發現 |
|---|---|---:|---|
| 1 | Accessibility | 3/4 | 結構與替代文字良好，但 `#6366f1` 在白底只有 4.47:1 |
| 2 | Performance | 2/4 | 99 個渲染圖片標籤都沒有 lazy loading；單頁圖片可達 3.95 MiB |
| 3 | Responsive Design | 2/4 | 有手機斷點與可捲動表格意圖，但未經真實手機驗證，小型語言連結也偏小 |
| 4 | Theming | 3/4 | Material 明／暗主題與 token 使用完整；少數顏色、陰影仍硬編碼 |
| 5 | Anti-Patterns | 2/4 | 主站內容克制，但首頁 stats／card grid、Roboto 與四組深色霓虹圖仍像不同模板 |
| **Total** |  | **12/20** | **Acceptable — 內容主線已穩定，技術與資產一致性仍需一輪修正** |

## Anti-Patterns Verdict

**部分未通過。** 主要教學頁已不像一般 AI 產生的卡片牆，且新圖採明亮、直白的說明圖風格；但仍有四個可辨認的模板痕跡：首頁置中的數字條、重複 card grid、Material 預設 Roboto／Roboto Mono，以及 `agent-paradigm`、`multi-LLM delegation`、`power-user workflow` 等深色霓虹圖。這些資產和新的 Stage 2–8 圖不是同一套視覺語言。

## Executive Summary

- Audit Health Score：**12/20（Acceptable）**。
- 問題數：**P0 0、P1 7、P2 5、P3 1**。
- 最先處理：修正公開路線矛盾；把易變事實納入查核；改善圖片載入；補真正的行動版驗收；統一舊圖風格。
- 不應回退的成果：必讀、精選專案、完整五星資源與核心詞目前都有機器 gate 保持可見。

## Detailed Findings by Severity

### [P1] README 漏掉實際存在的 Stage 5.8 選讀入口

- **Location**：`README.md:120` 及兩個語言鏡像；對照 `stages/05-claude-code-ecosystem.md:465` 與 `CAPSTONE.md:20`。
- **Category**：Content integrity / Navigation。
- **Impact**：Stage 5 正文確實有 **5.8 Claude Agent SDK（選修）**，CAPSTONE 也正確說 5.5–5.8 不擋入場；只有 README 寫成 5.5–5.7，讀者會漏掉最後一個選讀入口。
- **Recommendation**：三語 README 統一成 5.5–5.8，並在 site-route gate 鎖住 Track A 核心 5.1–5.4 與選讀 5.5–5.8。
- **Suggested command**：`/clarify`。

### [P1] README 對初學者使用過時且不直白的定位

- **Location**：`README.md:13,31,39,85-86` 及兩個語言鏡像。
- **Category**：Content integrity / UX writing。
- **Impact**：`illustrative`、`USE／BUILD`、`success criteria` 會讓第一次來的人多解一次術語；「每階段 1–5 題」也已被有 6 題的章節推翻。
- **Recommendation**：改成「可直接執行的小練習」、用完整句子說兩條路，刪除易漂移的固定題數；不要刪掉 Ollama／Anthropic 與深度資源定位。
- **Suggested command**：`/clarify`。

### [P1] Stage 設計契約仍保存互相衝突的舊結構

- **Location**：`stages/DESIGN.md:146,151,181,328,391`。
- **Category**：Content integrity / Governance。
- **Impact**：同一份維護契約同時說 Stage 0 有四題、Stage 5 有四個 sub-stage、又說 Stage 5 有 5.1–5.8；後續編輯者無法判斷哪一版才是準則。
- **Recommendation**：Stage 0 固定為一個整合練習；Stage 5 依目前 5.1–5.7 核心內容、5.8 SDK 選修與九個核心詞重寫，不再維護脆弱的數量敘述。
- **Suggested command**：`/distill`。

### [P1] Examples 總入口含大量易變資訊，但沒有 freshness 契約

- **Location**：`examples/README.md` 及鏡像，尤其 85–226 行附近。
- **Category**：Content integrity / Maintenance。
- **Impact**：固定 54 題、模型 tag、下載大小、硬體需求、價格、context 與「production 升級」結論會分別過期；現有 reader-UX／freshness gate 不涵蓋此頁。
- **Recommendation**：用官方來源逐項重查，移除不必要的固定總數，加入三語一致的查核標記與 stale patterns；價格只放仍會影響選擇的欄位。
- **Suggested command**：`/harden`。

### [P1] Agent paradigms 頁把未查核推論寫成確定事實

- **Location**：`resources/agent-paradigms.md:20-24,53,65,80,88,95,110-123` 及鏡像。
- **Category**：Content integrity / Safety。
- **Impact**：`224k+ stars`、`200+ provider`、`$5 VPS`、`€549`、`67 TOPS`、`10× cheaper`、`零 telemetry／完全可審計／0 data exposure` 都會變或需要部署條件。對法律、醫療資料的絕對安全說法尤其容易讓讀者做錯決定。
- **Recommendation**：分清 OpenRouter、OpenCode、Pi／Raspberry Pi、Hermes、OpenClaw 的角色；只保留官方可證明的能力，把安全結論改成「需自行驗證的部署條件」，加入 freshness 標記。
- **Suggested command**：`/harden`。

### [P1] 自訂 accent 對比未達一般文字 WCAG AA

- **Location**：`docs/stylesheets/extra.css:6-10,40-52`。
- **Category**：Accessibility / Theming。
- **Impact**：`#6366f1` 在白底的實測對比為 **4.47:1**，低於一般文字 4.5:1；它會出現在小型語言連結的 hover 狀態。
- **WCAG/Standard**：WCAG 2.2 SC 1.4.3。
- **Recommendation**：將文字 accent 換成較深的 token；裝飾與大面積元件可保留較亮色，但不要共用同一個前景色 token。
- **Suggested command**：`/colorize`。

### [P1] 圖片沒有延遲載入，長頁首屏會下載不需要的資產

- **Location**：建置後三語站共 99 個 `<img>`，`loading="lazy"` 為 0；`stages/07.5-advanced-agentic-concepts.md` 的三張圖合計 3.95 MiB。
- **Category**：Performance。
- **Impact**：手機或慢速網路會先下載頁面下方圖片；Stage 5–8、README 與資源頁多在 2–4 MiB，延後第一個可操作內容。
- **Recommendation**：首張有意義的 hero 可 eager，其餘圖加 lazy loading；在不改視覺的前提下做 PNG lossless／near-lossless 壓縮並設容量 gate。
- **Suggested command**：`/optimize`。

### [P2] Walkthrough 在 Stage 7 後沒有把讀者送回 Stage 7.5／8

- **Location**：`walkthroughs/build-first-agent-in-7-steps*.md` 結尾。
- **Category**：Navigation / UX writing。
- **Impact**：讀者完成部署後只看到延伸點子，不知道主路線還有進階概念與介面安全兩站；約 300 行的固定描述也容易漂移。
- **Recommendation**：加入三語可見的「下一站」連結到 Stage 7.5 與 Stage 8；移除固定行數，保留它是跨章整合範例的定位。
- **Suggested command**：`/clarify`。

### [P2] ROADMAP 把已完成的首頁重畫仍列為未來工作

- **Location**：`ROADMAP.md:27`、`ROADMAP.en.md:25`、`ROADMAP.zh-Hans.md:25`。
- **Category**：Content integrity。
- **Impact**：貢獻者會重做已完成工作，也會懷疑目前圖片是否只是暫稿。
- **Recommendation**：移到「最近完成」，並在 roadmap stale gate 阻擋同一句再出現。
- **Suggested command**：`/polish`。

### [P2] 行動版表格與小型語言連結缺少真實瀏覽器證據

- **Location**：`docs/stylesheets/extra.css:40-47,87-97`。
- **Category**：Responsive / Accessibility。
- **Impact**：語言連結以 `.72rem` 搭配很小的垂直 padding，觸控目標可能不足；`overflow:auto` 設在 `<table>` 本體，是否能在各瀏覽器穩定橫向捲動尚未驗證。
- **WCAG/Standard**：WCAG 2.2 SC 2.5.8（Target Size）。
- **Recommendation**：補 320／375／768／1440px 的瀏覽器驗收，量測 touch target、表格 scrollWidth 與正文溢位。
- **Suggested command**：`/adapt`。

### [P2] 三語建置警告太多，真實錯誤容易被淹沒

- **Location**：`mkdocs.yml` 的 i18n 建置與 `build-docs-tree.py` 產出。
- **Category**：Maintenance / Navigation。
- **Impact**：目前建置成功，但 contextual language switcher 與 `navigation.instant` 的相容性警告，以及大量跨語言相對連結警告，讓 CI 無法用「新警告」辨認新缺陷。
- **Recommendation**：分類預期警告、建立 baseline 或改寫生成樹連結；另以瀏覽器驗證語言切換是否留在同一頁。
- **Suggested command**：`/harden`。

### [P2] 舊圖與新圖不是同一套視覺語言

- **Location**：`resources/diagrams/agent-paradigm-decision-tree*.png`、`multi-llm-delegation-composition*.png`、`power-user-multi-type-workflow*.png`、`add-branch-decision-flow.png`、`teacher-ai-use-cases-overview*.png`。
- **Category**：Anti-Pattern / Theming。
- **Impact**：深色霓虹圖與偏簡報模板的教師圖，會讓讀者以為跳到另一個專案；小字在手機上也更難讀。
- **Recommendation**：以現有 README／Stage 2–8 的明亮、留白、短句風格重畫；三語一次交付，確認無箭頭或圖示重疊後刪除舊資產。
- **Suggested command**：`/quieter`。

### [P3] 首頁仍有常見文件模板痕跡

- **Location**：`docs/stylesheets/extra.css:14-83` 與建置後首頁。
- **Category**：Anti-Pattern。
- **Impact**：置中 hero、四格 stats、相同 card grid 與 Roboto 讓首頁容易和一般 Material 範本混在一起，但不妨礙使用。
- **Recommendation**：完成內容正確性後再評估；不要為了「更設計」犧牲目前清楚的路線順序。
- **Suggested command**：`/shape`。

## Patterns & Systemic Issues

1. **路線事實重複維護**：README、CAPSTONE、ROADMAP、DESIGN 各自手寫 Stage 5 範圍，已產生 5.7／5.8 漂移。應用同一份 machine-readable route contract 驗證。
2. **freshness 覆蓋不完整**：Stage 與核心資源已有 gate，但 examples 總入口、agent paradigms、walkthrough 等公開頁仍可保存價格、型號與能力斷言而不被攔住。
3. **圖片只有引用 gate，沒有體驗 gate**：能確認圖片存在與語言對應，卻沒有容量、lazy loading、手機可讀字級與風格一致性條件。
4. **成功建置不等於零警告**：目前 build 會成功，但 warning 數量高，無法直接證明三語站內導航完全正常。

## Positive Findings

- Reader UX 已保護 26 頁 × 3 語言：核心詞、必讀、精選專案、完整星等資源保持可見，次要內容才收合。
- 相關內容與結構測試 293 passed；Stage 0–8、A1–A3、五條角色路徑與核心資源已具三語鏡像。
- 生成 HTML 有 skip link、語意 heading、原生 `<details>`／`<summary>`；抽查圖片都有描述性 alt，未找到空 alt 或空連結。
- Material 同時配置明／暗主題，自訂 CSS 多數使用 Material token，沒有覆蓋 focus 或移除鍵盤輪廓。
- 新版 Prompt、Tool Use、Framework、RAG、Stage 7／7.5／8 圖沒有明顯箭頭或圖示重疊，且教學順序比舊圖清楚。

## Recommended Actions

1. **[P1] `/clarify`** — 修正 README、DESIGN、ROADMAP 與 walkthrough 的公開路線和初學者文字。
2. **[P1] `/harden`** — 對 examples index 與 agent paradigms 建立官方來源 fact pack、freshness 標記與回歸 gate。
3. **[P1] `/optimize`** — 圖片 lazy loading、容量壓縮與 page-weight gate。
4. **[P2] `/adapt`** — 用真實瀏覽器驗證 320／375／768／1440px、語言切換、觸控目標與表格溢位。
5. **[P2] `/quieter`** — 將深色霓虹與教師舊圖重畫成專案的明亮、簡單、直白風格。
6. **[P3] `/polish`** — 最後再處理首頁模板痕跡與剩餘建置警告。

You can ask me to run these one at a time, all at once, or in any order you prefer.

Re-run `/audit` after fixes to see your score improve.
