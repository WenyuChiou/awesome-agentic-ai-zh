# Stage 08 Agent Interfaces 漸進式重整 Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: use verification-before-completion and execute this plan task-by-task in the dedicated Stage 08 worktree.

**Goal:** 把 Stage 08 從一頁同時攤開的產品清單，整理成初學者能先選對介面、做安全小練習，再按需要展開 Computer Use、Browser Use、Sandbox 與 benchmark 細節的三語學習地圖。

**Architecture:** 繁中是 canonical；先用測試鎖住可見主線、八個核心詞、舊錨點、21 筆資源與時效性事實，再重寫繁中，最後建立 English 與简中語意鏡像。所有高變動資料進入 90 天 freshness 契約；兩組圖只整理正文已先定義的關係，不承載價格、排行或版本號。

**Tech Stack:** Markdown、MkDocs Material、Python／pytest 內容契約、YAML reader-UX／freshness 規則、GitHub API repository snapshot、Image 2.0 三語圖。

---

## 定位與邊界

- 日期：2026-08-28 UTC。
- Branch：`codex/stage08-reader-ux-stack`。
- 基底：`codex/stage07-5-reader-ux-stack`（建立時為 `87a036fdf0a01befb9d40e5335c8b0ebebacba6a`）。
- 本層只處理 Stage 08 與直接相依的 glossary、DESIGN、測試、freshness、圖片及 CHANGELOG。
- README、首頁、PROGRESS、研究人員／開發者／教師／知識工作者路徑留到全站連貫性 layer；本層只記錄它們的後續需求，不混進 Stage 08 diff。
- 不新增章節型教科書或大型 executable example。依 repo 定位保留一頁 roadmap、兩個安全的小練習，深度實作導向 canonical quickstart／repo。
- 使用者已同意把完成的小層逐步 push 並開 PR；未經再次明確同意，不合併、不刪 branch、
  不清理 worktree。

## 基線診斷

| 指標 | 繁中 | English | 简中 |
|---|---:|---:|---:|
| 行數 | 547 | 547 | 547 |
| H2／H3 | 16／33 | 16／33 | 16／33 |
| Markdown 連結 | 89 | 89 | 89 |
| unique 外部 URL | 44 | 44 | 44 |
| `<details>` | 0 | 0 | 0 |
| 未展開可見字元 | 24,296 | 35,266 | 22,023 |

主要缺陷：

- 進入條件、六筆必讀、產品排行榜、benchmark、sandbox 供應商、法律事件、四個練習、17 筆 Projects 與 Voice／VLA 全部同時可見，讀者不知道第一步。
- `Agent Interface`、`Accessibility Tree`、`Approval Gate`、`Prompt Injection` 等關鍵詞沒有在第一次使用前用白話定義。
- Computer Use 與 Browser Use 被簡化成「像素 vs DOM」，但現行 Browser Use 可同時用 accessibility tree、元素引用與像素回退；Computer Use 也不是模型直接控制真實電腦，應用程式仍負責執行動作。
- OpenAI 舊 `computer-use-preview` 已 deprecated；現行 GA 工具是 `computer`。官方同頁不同段落仍出現不同模型例子，因此教材不把單一模型 ID 寫成永久入口。
- Anthropic 現行 `computer_toolset_20260801` 與 `browser_toolset_20260801` 是 client toolsets；應用程式執行每個 call。Browser Use 是本章目前缺少的重要正式介面。
- OpenAI Agents SDK Sandbox Agents 仍是 Beta；Windows 應使用 Docker 或 hosted provider，不能把 Unix local client 當跨平台隔離方案。
- Gemini in Chrome 仍逐步開放，不能寫成所有平台與所有使用者已普遍可用。
- 既有練習要求直接碰 Excel、Slack、真實帳號，且以「沒有 API」概括 Excel／Slack；不適合第一個安全練習。
- 固定 GitHub stars、`5／10 行`、`<90ms`、`唯一 GPU sandbox`、`Top 5`、`4 強`、固定平台／價錢及「首次／最強」結論都容易過期或缺乏可比較範圍。
- OmniParser repo 是 CC-BY-4.0；現頁三語共六處誤寫 Apache-2.0。`icon_detect_v3` 採 MIT 授權的 YOLOv9 實作，較早的 Ultralytics detectors 保留 AGPL，caption models 採 MIT；不能混成一種授權。
- Comet prompt injection 與 Amazon injunction 的時間、來源與範圍被壓成廣泛結論；若保留，必須放進收合安全案例並說清楚程序狀態與受保護帳戶範圍。
- 既有安全圖把四種防護畫成必然巢狀，並把 output filter 與 destination allowlist 混在一起，需要重畫。

## 可見主線

讀者不展開任何選單時依序看到：

1. `🎯` 這關解決的問題：先選最小、最安全、最容易驗證的介面，不是看到 GUI 就用 Computer Use。
2. `📌` 五個學習目標。
3. `🚪` 最短進入條件：已會 Stage 03 的 tool loop；Track A 只需會使用一個 agent，Track B 需能讀短 Python。
4. `📚` 必修閱讀標題與一句選路提醒；完整順序放在關閉選單。
5. `🔑` 八個粗體核心詞，先白話再保留正確術語：
   - **Agent Interface（Agent 操作介面）**：agent 用來看見、操作或執行工作的門。
   - **Browser Use（瀏覽器操作）**：工作都在網頁內時，用頁面結構、元素與必要的畫面座標完成。
   - **Computer Use（電腦操作）**：工作跨桌面 app 時，看截圖並提出滑鼠／鍵盤動作，由執行器真正操作。
   - **Sandbox（沙箱）**：把程式關在獨立工作房間，限制它能看到與碰到的東西。
   - **Accessibility Tree（無障礙樹）**：瀏覽器整理給輔助工具的頁面文字、按鈕與表單地圖。
   - **Harness（執行框架）**：接收模型動作、執行、回傳結果、限制輪數並留下紀錄的外層程式。
   - **Approval Gate（批准閘門）**：付款、登入、刪除或難以回復之前一定停下來問人。
   - **Prompt Injection（提示注入）**：網頁裡的壞指令假裝成任務，想騙 agent 改變原本規則。
6. `🧭` 最小介面選擇表與亮色三語圖：
   - 只找／讀公開資料 → Web Search／Fetch。
   - 任務只在網頁內 → Browser Use。
   - 任務跨整個桌面 → Computer Use。
   - 要執行模型產生的 code／改檔 → Sandbox。
   - 有正式 API／typed tool 時優先使用它，GUI 是必要時的 fallback，不是預設捷徑。
7. `🛡️` 四道安全檢查與重畫圖：隔離環境、範圍 allowlist、重大動作 approval、結果／紀錄驗證。四道檢查是並列責任，不畫成錯誤的固定巢狀架構。
8. `🛠` 兩個可直接複製的安全練習：
   - Track A：在新瀏覽器 profile／隔離環境只開 `example.com`，回報 title、final URL 與 screenshot；不登入、不下載、不離開 allowlist，遇到要求即停。
   - Track B：複製一個小型 policy／executor 練習，對 domain、action 與 high-impact 動作做 allowlist／approval 檢查，再以 assertions 驗證拒絕路徑。程式本身不連外、不碰真實帳戶。
   - 每題保留 `$0` 本地路徑與 API／受管環境可能另計費的預算提醒；不要求先建立空白文字檔。
9. `🎯` 五筆可先選一筆的精選入口，以及直接可見的完整 21 筆五星資源表。
10. `✅` 短版自我檢查與專門路徑入口，不虛構尚不存在的 Stage 9。

## 預設收合

共 9 個 `<details markdown="1">`，全部預設關閉：

1. 時間、環境、進入條件與完整必修閱讀順序。
2. Computer Use 的 screenshot → action → executor → result loop、Anthropic／OpenAI 現行 tool shape 與 legacy migration。
3. OSWorld 1／2 benchmark discipline；保留 108 long-horizon workflows、約 1.6 小時 human median、特定 harness 的 tool-call 與 score，但不外推成模型永久排行。
4. Browser Use 深入：DOM、Accessibility Tree、element reference、pixel fallback、Playwright MCP、browser-use。
5. Sandbox 深入與小辭典：Container、microVM、Firecracker、gVisor、cold start、workspace、session、snapshot；說清楚隔離邊界而不把供應商行銷數字當通則。
6. Track A 的產品／操作路線與 availability 限制。
7. Track B 的 canonical quickstarts、executor 與 sandbox 路線；不放未驗證或已過時的 SDK code。
8. Comet／indirect prompt injection／Amazon case study；區分 Brave research、Perplexity response、法院命令與目前程序狀態。
9. Voice agents／VLA 作為未來介面方向；只給少量入口，不聲稱有 Stage 9。

所有舊 H2／H3 slug 先建立清單；被重新命名的 public deep link 以空 `<a id="...">` 落在對應的新可見標題或收合區前。glossary 現有四個 Stage 08 deep links 必須繼續有效，並同步改掉「4 強／5 強／7 強」等過期描述。

## 事實來源與 freshness 契約

來源優先順序：

1. 供應商正式產品／API 文件。
2. 供應商 release notes、官方 help center。
3. canonical GitHub repo、model／dataset card。
4. benchmark 首頁、paper 與資料集。
5. 安全研究原文、當事人回應、法院文件；媒體只做線索，不證明產品現況。

三語使用同一 marker：

`<!-- freshness: canonical=stages/08-agent-interfaces.md; verified_on=2026-08-28; scope=computer-use,browser-use,sandboxes,availability,benchmarks,security; max_age_days=90 -->`

需鎖定的現行事實：

- Anthropic `computer_toolset_20260801` 與 `browser_toolset_20260801` 是 client toolsets；應用程式執行每個 call。Computer Use 適合跨桌面，Browser Use 適合全部留在網頁內的任務。
- OpenAI 新實作使用 GA `computer` tool；`computer-use-preview`／`computer_use_preview` 只能出現在明確的 deprecated／legacy migration 說明。
- OpenAI 官方 Computer Use 頁不同段落可能使用不同模型例子；正文不把 model ID 寫成介面定義，也不把當日 sample model 當永久推薦。
- OpenAI Sandbox Agents 保留 `Beta`，並說清楚 `SandboxAgent`、`Manifest`、`SandboxRunConfig`、workspace／session／snapshot 的分工。
- Gemini in Chrome 標為 gradual rollout／不是每位使用者都可用；不把 Incognito、OS 或行動平台支援外推。
- OSWorld 2.0 數字一律附 benchmark、metric、step budget 與 model／harness 範圍；不能拿舊 OSWorld 與 2.0 的百分比直接做能力上升／下降結論。
- OmniParser repo license 是 CC-BY-4.0；`icon_detect_v3` 採 MIT 授權的 YOLOv9 實作，較早的 Ultralytics detectors 保留 AGPL，caption models 採 MIT。
- `★ 108k`、`5 行`、`10 行`、`<90ms`、`唯一 GPU sandbox`、`Top 5`、`4 強`、`7 強`、`2026-05 snapshot` 與無範圍的 `60% latency` 全部禁止或只能在有來源的歷史限制句中出現。

編輯前已完成 2026-08-28 官方查證；staging 前重查同一組 URL。任何 availability、tool type、Beta／GA、license 或 benchmark 變動都使舊 review fingerprint 失效。

## 21 筆學習資源與評分

完整表固定五組 `5／5／4／5／2`；每組一個 `<tbody>`，分類使用 `<th scope="rowgroup" rowspan="N">`，欄位使用 `scope="col"`。三語 URL、順序、限制與五星編輯評分一致；不顯示 GitHub stars。

### 官方介面文件（5）

1. Anthropic Computer Use tool — ⭐⭐⭐⭐⭐。
2. Anthropic Browser Use tool — ⭐⭐⭐⭐⭐。
3. OpenAI Computer Use guide — ⭐⭐⭐⭐⭐。
4. OpenAI Agents SDK Sandbox guide — ⭐⭐⭐⭐（Beta）。
5. Google Chrome Help: Gemini in Chrome — ⭐⭐⭐（逐步開放）。

### Hands-on executor／framework（5）

6. `anthropics/claude-quickstarts` — ⭐⭐⭐⭐⭐；取代 redirect 的 `anthropic-quickstarts`。
7. `browser-use/browser-use` — ⭐⭐⭐⭐⭐。
8. `microsoft/playwright-mcp` — ⭐⭐⭐⭐⭐。
9. `trycua/cua` — ⭐⭐⭐⭐。
10. `bytedance/UI-TARS-desktop` — ⭐⭐⭐⭐。

### Sandbox／runtime（4）

11. `e2b-dev/E2B` — ⭐⭐⭐⭐⭐。
12. `cloudflare/sandbox-sdk` — ⭐⭐⭐⭐；Apache-2.0，Beta，API 在 v1.0 前可能改變。
13. Modal Sandboxes docs — ⭐⭐⭐⭐。
14. Vercel Sandbox docs — ⭐⭐⭐⭐。

### GUI parsing／benchmark／dataset（5）

15. `microsoft/OmniParser` — ⭐⭐⭐⭐；附 CC-BY-4.0／weights 授權邊界。
16. OSWorld 2.0 — ⭐⭐⭐⭐⭐。
17. `xlang-ai/OSWorld` — ⭐⭐⭐⭐⭐。
18. `web-arena-x/webarena` — ⭐⭐⭐⭐。
19. `OSU-NLP-Group/Mind2Web` — ⭐⭐⭐⭐。

### 安全研究與回應（2）

20. Brave: indirect prompt injection systematic risk — ⭐⭐⭐⭐。
21. Perplexity BrowseSafe response — ⭐⭐⭐。

既有 Atlas、Dia、ColPali 不列為 Stage 08 現行核心推薦：Atlas 若確有停運資料只留歷史說明；Dia 不是本章核心 agent interface；ColPali 是文件 retrieval，回到 Stage 06 較合適。這是位置校正，不是刪除核心名詞。

## 圖片決策

使用 Image 2.0 分別產出繁中、English、简中，六個檔案必須 bytes／hash 不同：

- 新增 `interface-choice-map.{png,en.png,zh-Hans.png}`：四條選路（Search／Fetch、Browser Use、Computer Use、Sandbox）加「正式 API 優先」提示。亮色、少字、不放型號與排行。
- 重畫 `agent-guardrail-patterns.{png,en.png,zh-Hans.png}`：四道並列檢查（isolate、allowlist、approval、verify／log），不再使用巢狀盒子，也不把 output filter 等同 destination allowlist。
- 圖前先有文字定義，圖後有可搜尋的 localized caption；圖不是唯一資訊來源。
- 更新 `resources/diagrams/locale-variant-prompts.md`，移除把舊 guardrail 圖當正確語意樣板的敘述，保留視覺 house style 指引。
- 生成後逐張用 original resolution 驗收 CJK、英文、箭頭、順序、重複字與語意；不能只信生成工具回報。

## Task 1：先寫失敗的 Stage 08 內容契約

**Files:**

- Create: `scripts/test_stage08_content.py`
- Modify: `scripts/reader-ux-pages.yml`

**Steps:**

1. 從現有三語 headings 產生並人工核對 legacy anchor oracle。
2. 在新測試明列八個 core labels、21 組 URL／rating、五個 rowgroup、兩組三語圖、freshness marker 與禁止詞。
3. 測試可見 section 順序、核心詞第一次可見使用粗體、兩個 copy-ready exercises、四題標題與成果、Stage 7.5 返回連結、四道 guardrail、Stage 9 不存在、不准空引號 `""`／`“”`；直接執行 policy 範例，確認 mixed case、前後空白、未知 action、非 HTTPS、userinfo 與非 allowlist host 都採 fail-closed。
4. 測試 9 個 closed details、零個 `open`、完整資源表位於選單外、舊 anchor 仍落地、三語 external URL／resource rating 一致。
5. 測試現行事實：Anthropic toolsets、OpenAI `computer`／deprecated preview、Sandbox Beta、Gemini rollout、OmniParser weights 的逐模型授權、Cloudflare Sandbox SDK Beta／v1.0 前可能變更、OSWorld 2.0 範圍。
6. 在 `reader-ux-pages.yml` 加入 Stage 08 ratchet；先設定目標可見字元 `5,500／9,000／5,600`，完成正文後只可向下收緊。
7. 執行 `python -m pytest scripts/test_stage08_content.py scripts/test_reader_ux.py -q`；預期 Stage 08 新契約因舊頁結構而 FAIL，reader checker 自身測試保持 PASS。

## Task 2：重寫繁中 canonical page

**Files:**

- Modify: `stages/08-agent-interfaces.md`
- Modify: `resources/glossary.md`

**Steps:**

1. 依可見主線重寫頁首、五個學習目標、八個核心詞與 selector；先白話、後術語。
2. 建立兩個安全、可直接複製的練習與預算提醒；不操作真實 Slack／Excel／帳戶。
3. 把完整 Computer Use、Browser Use、Sandbox、benchmark、產品 availability、安全案例與 Voice／VLA 移入 9 個 closed details；完整資源表保持可見。
4. 寫 21 筆真正 rowgroup 的 HTML resource table；合併重複「推薦工具」與「精選 Projects」。
5. 為舊 headings 加 explicit anchor aliases；同步更新 glossary 四個 Stage 08 link label／anchor。
6. 執行繁中專屬 Stage 08 測試、strict anchors、`python scripts/check-reader-ux.py`；修到繁中主線能在不展開時完成 selector 與第一個練習。

## Task 3：建立 English 與简中語意鏡像

**Files:**

- Modify: `stages/08-agent-interfaces.en.md`
- Modify: `stages/08-agent-interfaces.zh-Hans.md`
- Modify: `resources/glossary.en.md`
- Modify: `resources/glossary.zh-Hans.md`

**Steps:**

1. 以定稿繁中結構逐段建立 English，保留 exact product／API terms、數字、URL、ratings 與安全邊界。
2. 以同一 canonical 結構建立简中，不做只換字的機械翻譯；修正語序與專業用語。
3. 逐列比對 21 筆資源、五組 rowgroup、9 個 details、八個核心詞、兩個 exercises、legacy anchors 與 glossary links。
4. 執行 mirror parity、locale links、Hans／OpenCC、English CJK residual、Stage 08 tests；任何三語事實差異都回到正文修正。

## Task 4：產生並驗收兩組三語圖

**Files:**

- Create: `resources/diagrams/interface-choice-map.png`
- Create: `resources/diagrams/interface-choice-map.en.png`
- Create: `resources/diagrams/interface-choice-map.zh-Hans.png`
- Modify: `resources/diagrams/agent-guardrail-patterns.png`
- Modify: `resources/diagrams/agent-guardrail-patterns.en.png`
- Modify: `resources/diagrams/agent-guardrail-patterns.zh-Hans.png`
- Modify: `resources/diagrams/locale-variant-prompts.md`

**Steps:**

1. 先讀 imagegen skill，使用 Image 2.0 分別生成三語 choice map。
2. 分別重畫三語 guardrail 圖，不沿用錯誤巢狀關係。
3. 逐張 original-resolution 人工驗收並記錄尺寸、SHA-256、文字語言與圖中順序。
4. 把 localized alt／caption 加入三語頁，執行 image locale gate 與 Stage 08 image contracts。

## Task 5：加入 freshness、維護文件與 snapshot

**Files:**

- Modify: `scripts/freshness-models.yml`
- Modify: `scripts/repository-freshness-snapshot.json`
- Modify: `stages/DESIGN.md`
- Modify: `docs/TESTING_PLAN.md`
- Modify: `CHANGELOG.md`

**Steps:**

1. 新增 Stage 08 stale patterns：preview tool 無 legacy qualifier、Sandbox GA、Gemini blanket availability、OmniParser Apache、volatile stars／排行／行數／cold-start／GPU uniqueness。
2. 更新 DESIGN：Stage 08 可見主線、八核心詞、兩個安全練習、10 details、`5／5／4／5／2` 資源表、兩組圖與 90 天 freshness。
3. 更新 TESTING_PLAN 說清楚自動檢查能證明什麼，以及安全案例語意／法院範圍仍需人工 review。
4. 以 GitHub API 重建 repository snapshot；斷言新增／改名 repo 全被追蹤、redirect 已消失、archive／owner／license 狀態有記錄。
5. 對最終 diff 寫 CHANGELOG，不憑記憶；包含基線／結果數字、查核日、移動／歷史化項目、OmniParser 修正與刻意未改 README／paths。

## Task 6：三層驗證、review 與本地 commit

**Steps:**

1. staging 前重新查驗所有高變動官方 URL；若資料變更，三語一起修正。
2. 執行機器 gate：
   - `git diff --check`
   - `python -m pytest scripts -q`
   - `python scripts/check-reader-ux.py`
   - strict anchors、anchor slug parity、mirror parity、locale links。
   - Hans／OpenCC、image locale、duplicate repositories、freshness strict、repository snapshot。
   - `python scripts/build-docs-tree.py`
   - `python -m mkdocs build`
3. 執行元素落腳審計：逐項確認舊 heading、17 個舊 resource／product、四個 exercises、兩個安全 case、Voice／VLA、三語圖與 glossary deep links 的新位置或移除理由。
4. 執行三語語意鏡像 review：tool type、availability、Beta／GA、license、benchmark metric、numbers、ratings、safety instruction 不可漂移。
5. 逐檔 `git add <path>`；將 staged file count 與凍結清單比較，記錄 staged fingerprint。
6. 對穩定 staged diff 執行一次獨立 `code-reviewer`。任何後續修改都必須重新跑受影響 gate、重新 stage、重新 review；禁止 `--no-verify`。
7. 使用單一 Stage 08 local commit：`content(stage8): choose safe agent interfaces progressively`。commit body 記錄前後可見字元、details／resource／diagram 數、查核日、已知 strict-build warning debt、review fingerprint 與未 push／未 merge 邊界。

## 驗收標準

- 不展開時，讀者能說出四種選路、完成 Track A 第一練習、知道四道安全檢查。
- 八個核心詞第一次可見使用粗體、有足夠白話定義，且都在第一個練習前。
- Computer Use、Browser Use、Sandbox、DOM、Accessibility Tree、Container、microVM、Firecracker、gVisor、Harness、Approval Gate、Prompt Injection 等重要名詞沒有因精簡而消失。
- 三語各 9 個 closed details，沒有 `open`；包含完整資源表的可見字元依實測 ratchet 鎖定。
- 21 筆資源、五組 `5／5／4／5／2`，`rowspan` 合計 21；URL、順序、限制與評分三語一致，無 volatile star count。
- Anthropic Computer／Browser toolsets、OpenAI GA computer／deprecated preview、Sandbox Beta、Gemini rollout、OSWorld 2.0 metric 與 OmniParser license 全部正確且有官方來源。
- 舊 Stage 08 headings／glossary deep links 仍落地；沒有虛構 Stage 9。
- 六張圖為六個不同檔案；三語各自引用自己的圖，圖中不承載時效性數字。
- 所有被移動／替換／歷史化元素都有明確新位置或理由。
- 完整 tests、content gates、MkDocs build 與獨立 review 通過後才可 commit。
- Final review 通過後，依使用者授權 push 並建立以 Stage 07.5 branch 為 base 的 stacked PR；
  未經再次明確同意，不 merge 或清理 branch／worktree。

## 候選實作證據（review 前凍結）

- 後續依全站規則把完整資源表移出選單；三語各 9 個 closed details、0 個 `open`，
  四題標題、成果與舊深連結都留在可見主線。包含 21 筆資源的可見字元實測為
  `8,931／12,471／9,016`，對應 ratchet 為 `8,981／12,521／9,066`。
- 21 筆 URL／評分依 `5／5／4／5／2` 五個真正 rowgroup 排列；三語來源順序一致。
- `interface-choice-map` 與重畫的 `agent-guardrail-patterns` 共六張 `1672×941` PNG，
  六個 SHA-256 均不同，三語頁各自引用自己的 locale 圖。
- Stage 08／reader 契約 70 passed；全套 `python -m pytest scripts -q` 為 457 passed。
- strict anchors、anchor slug parity、mirror、locale、Hans、image、duplicate repo、freshness、
  reader UX、catalog counts 與 260-repo snapshot coverage 通過；MkDocs 三語 build 成功。
- GitHub API snapshot 於 `2026-08-28T13:10:44Z` 重建。Stage 08 引用的 12 個 repo 均 verified、
  未封存、無 redirect；全站另有 9 個其他章節既有 canonical redirect，留給最終整合層。
- Stage template 的 REQUIRED sections 通過；Stage 06／07／08 仍有不阻擋的自然命名 EXPECTED warnings。
- Stage 08 專屬契約為 27 passed；`python -m pytest scripts -q` 為 462 passed。三語 MkDocs
  build 均為 exit 0，既有全站 nav／locale warning 未在本層擴大。
- 全站 527 個 URL 的額外人工掃描發現 Stage 06 三語沿用的 Chroma 舊網址已成 404；
  官方新入口已確認為 `https://docs.trychroma.com/docs/overview/getting-started`。這不是
  Stage 08 新增連結，依小型可回溯 PR 原則留給下一個獨立 stacked link-fix，不混進本層。
- 最終 staged diff 取得獨立 reviewer ACK 後才 commit、push 與建立 stacked PR；`main`、
  上游 branch 與既有 PR 不直接修改，也不在本層 merge 或清理。
