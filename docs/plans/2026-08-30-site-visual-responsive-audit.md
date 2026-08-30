# 全站圖表、手機閱讀與載入體驗稽核（2026-08-30）

## 範圍與證據

- 基準：`212b86004a294353f995b71ce62325c772d45151`（Draft PR #205 的 head）。
- 範圍：三語 MkDocs 站、67 張 PNG 圖、圖表所在頁面、手機表格、觸控目標、明／暗主題與圖片載入方式。
- 內容基準：完整測試 `894 passed`；`build-docs-tree.py` 與三語 `mkdocs build` 成功。
- 瀏覽器實測：Chromium 的 320×720、375×812、768×1024、1440×900，共 5 頁 × 4 viewport；另以 375×812 抽查 3 頁深色模式。
- 圖片證據：67 張 PNG 共 78.72 MiB；建置後 96 個 `<img>`，`loading="lazy"` 與 `decoding="async"` 都是 0。
- 可及性證據：所有 Markdown 圖片都有非空 alt；20 組頁面／viewport 都沒有整頁水平溢出，需橫向捲動的表格皆可操作。

## Audit Health Score

| 面向 | 分數 | 關鍵發現 |
|---|---:|---|
| Accessibility | 3/4 | alt、heading、原生 details 良好；小型語言按鈕與部分 summary 未達 44 px，亮色 accent 對比只有 4.47:1 |
| Performance | 2/4 | 沒有 lazy loading／async decoding；單頁圖檔可達 4.00 MiB，也沒有 page-weight gate |
| Responsive Design | 2/4 | 版面與表格不會爆版，但 1672 px 圖在 320 px 手機只顯示 273 px，圖中文字難讀 |
| Theming | 3/4 | 明／暗模式正常；舊深色霓虹圖與新亮色教學圖仍不一致 |
| Anti-Patterns | 2/4 | 新主線圖已克制；仍有固定模型職位、密集三欄卡與內部決策樹等舊模板痕跡 |
| **Total** | **12/20** | **Acceptable：內容主線可用，但圖的交付方式與幾張舊圖仍需修正** |

## Executive Summary

- 問題數：**P0 0、P1 3、P2 5、P3 1**。
- 手機版真正的問題不是 overflow，而是圖中文字縮得太小，讀者也沒有明顯的點按放大入口。
- 最先做的應是「圖片交付」小 PR：延遲載入、非同步解碼、點按看原圖、容量 gate、觸控尺寸與文字色對比。
- 舊圖不能一律重畫。有些圖只重複旁邊文字，移除比再製造三張語言版本更清楚、更容易維護。
- **必修閱讀、精選 Projects、完整五星學習資源與安全提醒仍保持可見；本輪不把它們收進 details。**

## Detailed Findings

### [P1] 所有教學圖都會立即下載

- **Location**：`scripts/mkdocs_hooks.py:48-54`、建置後全站 96 個 `<img>`。
- **Evidence**：`loading="lazy"` 0 個、`decoding="async"` 0 個；Stage 7.5 三張圖合計 3.89–4.00 MiB，首頁三張圖合計 3.36–3.52 MiB。
- **Impact**：讀者還沒滑到頁尾，手機就先下載下方圖片；慢速網路會延後第一個可操作內容。
- **Recommendation**：在 MkDocs HTML 階段為正文圖加入 lazy loading 與 async decoding；只有真正的首屏 hero 才保留 eager。新增 hook 單元測試與每頁／單圖容量 gate。
- **Suggested command**：`/optimize`。

### [P1] 圖表會縮進手機，但文字已小到不適合閱讀

- **Location**：Stage 5–8、Stage 7.5、角色頁與資源頁中的 16:9 圖。
- **Evidence**：1672×941 圖在 320 px viewport 顯示約 273×154（16.3%）；教師 1920×1080 圖在收合區約 247×139（12.9%）。375 px viewport 也只有約 328×185。
- **Impact**：圖沒有超出螢幕，卻失去「看一眼就懂」的作用；字多的三欄圖尤其嚴重。
- **Recommendation**：每張教學圖提供可鍵盤操作的「開啟原圖」連結；手機可點按看大圖。重畫時限制一張圖只說一個關係，必要時拆成兩張，不用再把更多字塞進 16:9 畫布。
- **Suggested command**：`/adapt`。

### [P1] Subagent 三模式圖與正文已落後現行官方產品形狀

- **Location**：`resources/subagent-advanced.md:104-165` 及兩個語言鏡像；`subagent-composition-patterns*.png`。
- **Evidence**：頁面把選項固定成 Parallel／Pipeline／Meta-Agent，並宣稱「90%」及「Anthropic 官方範例都不這樣用」，但沒有來源。現行官方文件改以 Subagents、Agent view、Agent teams、Dynamic workflows 四種入口比較，且 Agent teams 明確標示 experimental；subagent 的背景執行與訊息能力也已更新。
- **Official sources**：[Run agents in parallel](https://code.claude.com/docs/en/agents)、[Create custom subagents](https://code.claude.com/docs/en/sub-agents)、[Agent teams](https://code.claude.com/docs/en/agent-teams)。
- **Impact**：只換亮色背景仍會留下錯的心智模型，讀者也會把社群偏好誤認成 Anthropic 官方規則。
- **Recommendation**：另開三語內容 PR，先重寫選擇方式與限制，再以 Image 2.0 生成明亮、短句、無重疊的新圖；移除無證據的百分比與官方背書說法。
- **Suggested command**：`/harden` + `/quieter`。

### [P2] 小型互動目標與 accent 文字對比不足

- **Location**：`docs/stylesheets/extra.css:6-10,40-52`。
- **Evidence**：首頁語言按鈕在 320 px 約 77–88×31 px；部分 `<summary>` 高 36 px。`#6366f1` 在白底對比為 4.467:1，低於一般文字 4.5:1。
- **Impact**：手指較難準確點擊；hover／focus 的小字對部分讀者不夠清楚。
- **Recommendation**：把主要觸控目標提高到至少 44 px；將文字 accent 換成 `#4f46e5` 或更深 token，亮紫色只留給裝飾與非文字狀態。
- **Suggested command**：`/adapt` + `/colorize`。

### [P2] Multi-LLM 圖仍把模型名稱畫成固定職位

- **Location**：`resources/mcp-skills-catalog.md:1003-1019` 及鏡像；`multi-llm-delegation-composition*.png`。
- **Evidence**：正文已正確提醒「不要把模型名稱當固定職位」，舊圖卻仍以 Claude／Codex／Gemini 和易變能力固定分工，且使用黑底霓虹風格。
- **Impact**：圖和同頁文字互相打架，也會隨模型能力與產品名稱漂移。
- **Recommendation**：這一節已在收合的 maintainer 自家專案 catalog，旁邊文字足以說清楚；優先刪圖而不是重畫。若未來確實需要圖，只畫 Planner／Executor／Reviewer 與共同 acceptance gate，不放供應商名稱。
- **Suggested command**：`/distill`。

### [P2] 教師使用情境總覽有圖示壓線，而且沒有增加新資訊

- **Location**：`branches/for-teacher.md:141-161` 及鏡像；`teacher-ai-use-cases-overview*.png`。
- **Evidence**：橘色卡右上圖示壓到邊框；圖只重複下方「備課／課堂／行政」三段短文。相較之下，可見的 `teacher-ai-review-loop*.png` 步驟單純、易懂，可保留。
- **Impact**：違反無 overlap 的圖表規則，也讓收合補充區多載入一張不必要圖片。
- **Recommendation**：移除使用情境總覽三語圖；保留五步人工審查圖。若日後使用情境變複雜，再依新內容重畫。
- **Suggested command**：`/distill`。

### [P2] Branch 決策樹是維護文件，不需要保存一張會過時的大圖

- **Location**：`branches/DESIGN.md:135-147`；`add-branch-decision-flow.png`。
- **Evidence**：深色霓虹圖含固定 branch 數量與門檻；下方兩個文字案例已能解釋判斷方式。
- **Impact**：維護規則變動時容易只改文字、忘記重畫圖片；它也不是一般讀者的教學主線。
- **Recommendation**：刪除圖片，改用可 diff、可搜尋的短版文字檢查表；不要為內部治理流程再生一張裝飾圖。
- **Suggested command**：`/distill`。

### [P2] 圖片 gate 只檢查存在與語言，沒有檢查體驗

- **Location**：`scripts/check-image-locale.py`、`scripts/test_image_locale.py`。
- **Evidence**：目前能阻擋錯語言與孤兒圖，但不限制單圖容量、單頁總量、lazy／async 屬性、原圖入口或圖中 overlap 的人工驗收紀錄。
- **Impact**：三語圖可以形式正確，卻同時太重、太小或視覺不一致。
- **Recommendation**：新增 machine gate 檢查位元組、頁面總圖重與必要 HTML 屬性；風格、文字可讀性與 overlap 保留為 PR 人工 checklist，不能假裝能完全自動判斷。
- **Suggested command**：`/harden`。

### [P3] 首頁仍有常見文件模板痕跡

- **Location**：`docs/stylesheets/extra.css:14-83`。
- **Evidence**：置中 hero、四格 stats、同形 card grid 與 hover 浮起效果都很常見。
- **Impact**：不妨礙理解，也不是目前阻塞；過早重畫可能破壞已清楚的入口順序。
- **Recommendation**：完成圖片交付與舊圖清理後再做小幅 polish，不先大改首頁資訊架構。
- **Suggested command**：`/polish`。

## Positive Findings

- 20 組頁面／viewport 實測沒有整頁水平 overflow；Material 的 table wrapper 能讓所有過寬表格左右滑。
- 深色模式在抽查頁面正確使用 `slate`，正文、表格與目前新圖沒有消失或超出 viewport。
- 所有 Markdown 圖都有描述性 alt；沒有空 alt，也沒有語言圖片錯配。
- Stage 2–8 的新版亮色圖未見箭頭或 icon overlap，且正文先定義、圖再整理，沒有讓圖片取代解釋。
- 必修閱讀、精選專案、完整星等資源和第一個可複製動作已有 reader-UX gate 保持可見。

## 建議的 stacked PR 順序

1. **Image delivery**：lazy／async、點按看原圖、44 px 觸控目標、accent 對比、圖片容量 gate。只改站點交付與測試，不重畫內容圖。
2. **Subagent refresh**：以官方現行四種入口重寫三語頁面，再用 Image 2.0 生成同風格三語圖。
3. **Old visual retirement**：刪除 Multi-LLM、教師使用情境與 Branch 決策樹的多餘舊圖；保留真正能幫助理解的教師審查圖。
4. **Final visual polish**：重新量測手機與深色模式，最後才評估首頁 stats／card 是否需要降低模板感。

每個 PR 都疊在 #205 之後並維持 Draft；完成 review 與 CI 後仍不自動合併，等使用者檢查與明確同意。
