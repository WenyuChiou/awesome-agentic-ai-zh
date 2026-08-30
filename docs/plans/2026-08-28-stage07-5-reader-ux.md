# Stage 07.5 進階概念地圖漸進式重整計畫

- 日期：2026-08-28 UTC
- Branch：`codex/stage07-5-reader-ux-stack`
- 基底：`codex/stage07-examples-stack`（建立時為 `8e07e76674d11819f22d9eaeed3e7fe67ec9da5d`）
- 定位：Stage 07 content + example-hardening 之上的單層 stacked PR

## 目標

Stage 07.5 不是再塞一章理論，而是一張「遇到問題時知道去哪找答案」的地圖。
第一次閱讀、不展開任何選單時，讀者要能：

1. 知道這章不用把 12 個概念一次學完。
2. 用白話說清楚六個會反覆出現的核心詞。
3. 依自己遇到的問題，從 12 個概念中挑 1–2 個先讀。
4. 寫出一張很短的工作邊界卡，說清楚 agent 能做什麼、不能做什麼、怎樣算完成。
5. 知道下一篇該讀什麼，以及什麼資訊仍會隨產品更新。

敘述採「先白話、再保留正確術語」。不能為了縮短頁面刪掉既有 12 個概念、
Harness、Eval、Dynamic Workflows、Model–Harness Fit 或重要 research 名詞。

## 基線診斷

| 指標 | 繁中 | English | 简中 |
|---|---:|---:|---:|
| 行數 | 638 | 636 | 636 |
| H2／H3 | 7／22 | 7／22 | 7／22 |
| Markdown 連結 | 93 | 93 | 93 |
| 表格列 | 92 | 92 | 92 |
| `<details>` | 0 | 0 | 0 |

主要缺陷不是「概念太多」，而是所有層級同時出現：

- 頁首先給 8 區塊目錄、10 個縮寫、4 層 stack、5 個 failure cases、12 個概念、
  4 類原則和 5 個 OpenAI 原則；讀者看不出第一步。
- 同一件事以「四層工作邊界」「四類 Harness 原則」「五個 OpenAI 原則」重複分類，
  但三套分類不是同一種座標。
- 五張圖都留在第一遍；圖很亮，但文字密、分類互相依賴，不能代替定義。
- 38 個 unique URL 被重複插入正文，沒有真正的分組資源表。
- 多個固定數字被寫成通則：70% production、200k context、500 行、80% reader、
  3.5 PR/day、分數差一倍、10% variance、75% reward hacking。這些數字不是都適合當教材規則。
- `Replit Agent 2024 incident` 與正文 2025-07 自相矛盾；Voyager 年份也要按 paper／repo 重查。
- AutoGen 已進入 maintenance mode，新專案應導向 Microsoft Agent Framework；現頁仍把
  AutoGen 當現行首選。
- OpenAI 的 `Types → Config → Repo → Service` 是其特定 codebase 架構片段，不能寫成
  所有 agent 系統的通用四層真理。
- 「透明」應教可觀察的 plan、action、receipt 與結果，不要求模型公開私人 Chain-of-Thought。
- LLM-as-judge 不能單獨當真相來源；要和固定 rubric、deterministic checks、抽樣人工檢查配合。

## 可見主線

1. `🎯` 這一關在解什麼問題：進階概念很多，但每次只挑跟眼前問題有關的 1–2 個。
2. `📌` 四個學習目標。
3. `🚪` 最短進入條件：完成 Stage 07，或已做過一個有工具、Eval 與停止條件的 Agent。
4. 六個粗體核心詞：
   - **Work Boundary（工作邊界）**：像地上的線，先說哪裡可以碰、哪裡不能碰。
   - **Contract（契約）**：像交作業規則，輸入、輸出與完成條件要寫清楚。
   - **Reflection（反思／回看）**：做完先看證據，再決定要不要修一次。
   - **Autonomy（自主權）**：agent 可以自己決定到哪一步。
   - **Budget Gate（預算閘門）**：錢、token、時間或輪數到上限就停。
   - **Graceful Degradation（平穩降級）**：最好路徑壞掉時，改走較簡單但安全的路。
5. 一張亮色三語「問題 → 概念群 → 安全 gate」概念圖。
6. 12 個概念的四組地圖；每列只留白話定義與「什麼時候用」。
7. 五種常見卡關的選擇表：越界、交接漏資料、反覆失敗、成本失控、服務壞掉。
8. `🛠` 三分鐘工作邊界卡：直接複製四行，填入 `可以做／不能做／完成證據／停止條件`。
9. `🎯` 五筆精選閱讀入口。
10. `📚` 24 筆完整學習資源、限制與五星編輯評分。
11. `✅` 短版自我檢查與 Stage 08 入口。

## 12 個概念全部保留

改成四個問題群組，分類欄用真正 `rowspan`，不再用來源專案的 code layer 當通用座標：

| 群組 | 保留概念 | 初學者先問的問題 |
|---|---|---|
| 邊界與契約（3） | Work Boundary、Contract-driven Hand-offs、Spec-driven Development | 誰能動什麼？交出去的東西長什麼樣？ |
| 規劃與合作（3） | Speculative／Parallel Exploration、Hierarchical Task Decomposition、Self-organizing Teams | 工作怎麼拆？真的需要多人嗎？ |
| 檢查與學習（3） | Agent-as-Judge／Constitutional Review、Plan-Act-Reflect、Failure Injection／Chaos Eval | 怎麼知道它做對？失敗後怎麼學？ |
| 控制與復原（3） | Autonomy Gradients、Cost-aware Budget Gates、Graceful Degradation | 怎麼限制風險？壞掉時怎麼安全退一步？ |

Constitutional AI、ReAct、Reflexion、Self-Discover、CAMEL、Voyager、Bitter Lesson、
Model–Harness Fit 仍保留正確名稱與來源；不把它們全部拉進頁首核心詞。

## 預設收合

- 時間、先備條件與完整閱讀方式。
- 三個 incident case study；修正年份並區分官方說明、當事人記錄與媒體報導。
- 12 個概念的完整原理、限制與 canonical source。
- Harness Engineering 的 cross-vendor 整理；明寫這是編輯整理，不是假裝供應商共用同一套命名。
- OpenAI Harness Engineering codebase case study，包括該專案的 layer 架構。
- Coding-agent harness、Eval rigor、Dynamic Workflows、Model–Harness Fit、分工研究。
- 完整 reading decision tree。

所有 `<details markdown="1">` 預設關閉。Dynamic Workflows 的標題、既有 legacy anchor、
一句話定位與查核日期留在 `<details>` 外，確保既有深連結落在可見位置。

## 事實更新與來源規則

來源優先順序：

1. 供應商正式文件與 release notes。
2. canonical GitHub repo／model card。
3. 原始 paper 或作者頁。
4. 事故資料庫與媒體只用於事件脈絡，不能證明產品目前狀態。

目前已確認的更新：

- Claude Code Dynamic Workflows：現行文件要求 v2.1.154+，適用範圍、16 concurrent／
  1,000 total、`ultracode`、`/workflows` 與版本差異以官方 docs 為準；2026-05-28 與
  Opus 4.8 同日發布只作歷史背景，不再放進標題或暗示模型綁定。
- OpenAI Agents SDK Sandbox Agents 仍是 Beta；workspace、session、manifest、snapshot、
  approval 與 sandbox client 是正式文件中的現行概念，但不能寫成已 GA。
- AutoGen 已是 maintenance mode／community-managed；新讀者導向 production-ready 的
  Microsoft Agent Framework，AutoGen 留在歷史／遷移欄。
- Anthropic 2026 的 Context Engineering、Demystifying Evals、long-running harness 等新資料
  加入；Building Effective Agents 保留為 foundation，不獨占最新實務。
- `70% planning／80% execution` 只保留在收合研究案例，清楚寫成 Anthropic 對特定
  Claude Code 使用資料的平均觀察，不寫成所有人與所有 agent 的規則。
- 所有年份、版本、Preview／Beta／maintenance 狀態在編輯前與 staging 前各查一次。

三語頁加入同一個 90 天 freshness marker：

`scope=agent-patterns,harnesses,evals,dynamic-workflows,framework-status,research`

## 學習資源表

24 筆、五組，直接放在可見主線：

- 基礎設計與 context：5。
- Orchestration／Contracts：5。
- Eval／Resilience：5。
- Research patterns：5。
- 中文／動手入口：4。

每組一個 `<tbody>`；分類用 `<th scope="rowgroup" rowspan="N">`，欄位用
`scope="col"`。三語 URL、順序、限制與五星編輯評分一致。不放 GitHub star 數、
固定排行榜或「最強」結論。

候選現行專案與入口包括 Microsoft Agent Framework、LangGraph、OpenAI Agents SDK、DSPy、
Deep Agents、tau2-bench、SWE-bench、datawhalechina/hello-agents 與李宏毅課程；逐一用
GitHub API／官方 docs 驗證 owner、archive、maintenance、release 與文件入口。

## 圖片決策

現有五組三語圖都已在地化，但一頁五張仍過重；部分圖把編輯分類畫成通用事實。

- 重畫並保留 `concept-cluster.{png,en.png,zh-Hans.png}`：改成四個問題群組，少字、亮色、
  每組三概念，圖片只整理正文已先定義的關係。
- 重畫並保留 `reading-decision-tree.{png,en.png,zh-Hans.png}`：改成「我卡在哪裡 → 先讀
  哪一組 → 做哪個小檢查」，移除固定分鐘數。
- `stack-4layer`、`failure-lifecycle`、`principle-dependency` 三組不再嵌入正文；掃完引用後
  刪除九張 orphan 圖，並同步刪改 prompt 素材。Git commit 本身保留完整回溯。
- 使用 image 2.0 分別產出繁中、English、简中，不以同一張圖混放兩種語言。

## 舊元素落腳

| 舊內容 | 新位置／處理理由 |
|---|---|
| 10 個縮寫表 | 只保留後文真的需要的縮寫；放進時間／閱讀收合區。 |
| Types → Config → Repo → Service | 移到 OpenAI codebase case study，標成特定架構，不再當整章主軸。 |
| Failure-mode lifecycle | 事件例子放進收合 case study；刪除「事故必然自動消除」的過度結論。 |
| 12 概念 skeleton | 全數保留，改成四個問題群組與真正合併分類欄。 |
| 五個 OpenAI 原則 | 合併成 cross-vendor harness lessons；原文數字與 quote 僅在需要時短引。 |
| Coding-agent harness | 收合專題，連回 Stage 05／07／08，不和 12 概念搶主線。 |
| Eval rigor | 保留 pass^k、重跑、固定環境、hold-out、reward-hacking 警告；刪除無法當通則的百分比。 |
| Dynamic Workflows | 保留可見 heading／legacy anchor／一句話定位；完整版本與限制收合。 |
| Model–Harness Fit／Bitter Lesson | 保留為「工具會過期」收合提醒，不另造無來源定律。 |
| 分工研究 | 保留裝潢比喻；數字標示資料範圍，不外推。 |
| Self-quiz prompt | 改成可直接複製的短版問題卡，不要求建立空白檔案。 |

## Stacked 邊界與預計檔案

本層只處理 Stage 07.5：

- 三語 Stage 07.5。
- `stages/DESIGN.md`、`docs/TESTING_PLAN.md`、`CHANGELOG.md`。
- Final review 發現的直接全站矛盾：Stage 04 三語 AutoGen 狀態與三語 catalog 的 production
  推薦改成 Microsoft Agent Framework；不藉此改寫其他 Stage 04／catalog 內容。
- Stage 07.5 reader-UX／content／freshness 測試與設定。
- 六張重畫圖、九張 orphan 圖刪除、直接相關 diagram prompt 文件。

不修改 Stage 08、README、ROADMAP、glossary 或可執行 examples；它們在各自 layer 處理。
若 strict anchor 或直接引用真的失效，只納入最小相依修正並列入凍結清單。

使用者已同意把完成的小層逐步 push 並開 PR；未經再次明確同意，不合併、不刪遠端
branch、不清理 worktree。

## 驗收

- 三語 12 個概念全部存在、順序與語意一致。
- 六個核心詞第一次可見使用時粗體並有白話定義。
- 至少六個預設關閉 `<details>`，不得有 `open`。
- 不展開時仍看得懂選路、三分鐘工作邊界卡、自我檢查與 Stage 08 入口。
- 24 筆資源、五個 rowgroup，`rowspan` 合計 24；URL、評分、限制三語一致。
- Dynamic Workflows legacy anchors 仍可見；AutoGen 明標 maintenance，MAF 為現行入口。
- 三語 freshness marker 日期一致，無未限定的過期產品狀態。
- Stage 04 與 catalog 不再把 maintenance-mode AutoGen 當新 production 專案入口。
- 六張亮色圖是六個不同檔案；三語各自引用自己的版本。
- 被刪圖沒有引用、產生器、prompt 或 `.gitignore` orphan。
- `python scripts/check-reader-ux.py`
- Stage 07.5 content tests、freshness tests。
- strict anchors、anchor slug parity、mirror parity、locale links、Hans／OpenCC、image locale、
  duplicate repos、catalog counts、repository snapshot。
- `python scripts/build-docs-tree.py`
- `python -m mkdocs build`
- `git diff --check`
- 最終 staged fingerprint 的獨立 `code-reviewer` ACK；任何後續修改都使 ACK 失效。

## 執行結果與證據

### 讀者體驗

- 三語頁都由 `638／636／636` 行整理為 299 行，12 個概念仍完整保留。
- 後續依全站規則把完整資源表移出選單；每頁現有 8 個預設關閉的
  `<details markdown="1">`，沒有 `open`。包含 24 筆資源的可見主線實測為
  `10,288／14,772／10,328` 個非空白字元。
- 六個核心詞、四行工作邊界卡、12 概念四組 `3／3／3／3`、24 筆資源五組
  `5／5／5／5／4`、Dynamic Workflows legacy anchors 與 Stage 08 入口都通過專屬測試。
- 所有分類欄使用真正的 HTML `rowspan`；三語 URL、評分與順序由測試鎖定，限制欄則由
  人工語意鏡像 review 複查。

### 事實與資源

- 查核日統一為 2026-08-28 UTC。AutoGen 明標 maintenance mode，現行入口改為
  Microsoft Agent Framework；OpenAI Sandbox Agents 保留 Beta；Dynamic Workflows 的版本、
  concurrency、run 上限與現行指令依官方文件限定，不外推成通則。
- 全站 GitHub snapshot 於 `2026-08-28T11:12:11Z` 重建，覆蓋 261 個實際 repo 引用。
  Stage 07.5 新增的 `SWE-bench/SWE-bench` 已納入，`verify-snapshot` 通過。
- 完整掃描另外找出 16 個不屬於本層的既有問題：10 個 repo canonical redirect，以及
  Stage 08 三語共 6 處把 OmniParser 的 `CC-BY-4.0` 誤寫為 Apache 2.0。它們已記為
  Stage 08／全站 freshness 後續工作，沒有混進本層偷偷修正。
- 第一輪獨立 review 另抓到 AutoGen 的跨頁狀態矛盾、英文概念表三個「何時使用」翻譯
  漂移，以及資源測試把第一語言誤當 oracle。三項都已修正；24 組 URL＋評分現在使用
  明確常數，三語一起漂移也會失敗。

### 圖片與孤兒清理

- Image 2.0 分別產出繁中、English、简中兩組共六張 `1672×941` 亮色圖；六個檔案
  bytes／hash 均不同，並由三語頁各自引用自己的版本。
- `concept-cluster` 只畫四個問題群；`reading-decision-tree` 只畫五種卡關如何選 1–2 組。
  圖中不放價格、版本、排行或固定效能數字。
- 引用掃描後刪除 `stack-4layer`、`failure-lifecycle`、`principle-dependency` 三組共九張
  orphan 圖，並同步縮減 generation prompts；Git history 仍可完整回復。

### 驗證紀錄

- `python -m pytest scripts -q`：435 passed。
- `python -m pytest scripts/test_stage075_content.py -q`：22 passed。
- reader UX、freshness strict、strict anchors、mirror parity、locale links、Hans 字元、
  zh-Hans localize、image locale、duplicate repos、catalog counts、repository snapshot、
  stage template required sections 與 `git diff --check` 全部通過。
- `python scripts/build-docs-tree.py`：staged 7 dirs + 29 root pages。
- `python -m mkdocs build`：exit 0。`python -m mkdocs build --strict` 仍因全站既有的
  i18n sibling／nav／`${CLAUDE_SKILL_DIR}` 等 warnings exit 1；本層不把既有 warning debt
  偽裝成成功，也不在 Stage 07.5 混修全站建置設定。
- 依使用者授權，final review 通過後 push 並建立以上游 Stage 07 examples branch 為 base
  的 stacked PR；不合併、不刪 branch、不清理 worktree。最終 staged fingerprint 與
  `code-reviewer` verdict 記錄在 commit body 與交付說明；review ACK 後不再修改本檔，
  避免讓已審 fingerprint 過期。
