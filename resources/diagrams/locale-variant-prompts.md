# 語系變體圖 — 生成流程與教訓

> 姊妹檔：[`concept-prompts.md`](concept-prompts.md)（Stage 7.5 兩組三語概念圖的 Image 2.0 重產規格）。
> 這份記錄的是 **2026-08-02 那批 5 張圖 × 3 語系** 是怎麼產出來的，以及過程中踩到的坑。

## 2026-08-29：Stage 5 的 5.1–5.7 關係與資料流

新增 `claude-code-system-flow.png`、`.en.png`、`.zh-Hans.png`。這組圖補上原本選擇圖沒有回答的問題：各零件如何接進同一次工作。三語都固定使用同一個 16:9 亮色版面與四種線條語意：

- CLAUDE.md 與 Skill 用虛線把 always-on／on-demand context 送進 Agent loop。
- Agent loop 與 MCP 用實線交換 request／result；MCP 是外部工具與資料的連線，不是另一個 agent。
- Hook 以獨立虛線接到 Agent loop 外框，表示符合 lifecycle event 時才執行；它不能貼在 MCP request／result 箭頭上，避免誤教成只檢查 MCP。文字只說可記錄、補充或阻擋，不暗示每種 event／handler 都會阻擋。
- Subagent 用獨立 context 工作，只把摘要送回；Worktree 是可選的檔案樹隔離，不冒充完整 sandbox。
- Plugin 以點線表示它能包裝 Skill、Hook、Subagent 與 MCP 設定，不放進 runtime loop。**Plugin 不連到 Worktree**；Worktree 是另外選用的檔案樹隔離方式，不是 Plugin 內容。

繁中使用 Codex 內建 Image 2.0 產生母版；英文只替換文字，簡中再以英文幾何作母版，避免繁體字形殘留。2026-08-29 再用內建 Image 2.0 移除誤碰 Worktree 的橘色 Plugin 點線，其他文字與幾何不變。三張最終圖皆為 `1672×941`，無模型、版本、價格、排行、benchmark 或 stars。可見底線固定為：Worktree 只隔開檔案；安裝 MCP server 或 Plugin 前仍要查來源、權限與資料流向。

人工逐張驗收標題、八個節點、request／result、summary、optional、Plugin 點線不接觸 Worktree、Hook lifecycle event 線與底部安全邊界。`scripts/test_stage05_content.py` 另鎖住三語引用、尺寸、不同 hash、圖確實位於 5.1 前的未收合區、頁面不混入其他語系版本，以及 `modelcontextprotocol/servers` 第一次正文出現就是官方超連結。

## 2026-08-28：Stage 8 介面選擇圖與四道安全檢查

新增 `interface-choice-map.{png,en.png,zh-Hans.png}`，並原檔名重畫
`agent-guardrail-patterns.{png,en.png,zh-Hans.png}`。兩組都是 16:9 暖白底、亮色卡片、
深藍大字與簡單 icon；每張由 Codex 內建 Image 2.0 生成，再以原尺寸逐字檢查。

介面圖先問「你要做什麼」，再平行分成四張卡：

- 只讀公開資料 → Search／Fetch
- 只操作網頁 → Browser Use
- 跨桌面 App → Computer Use
- 執行程式／改檔 → Sandbox

頂部固定提醒「正式 API／Typed Tool 優先」。四張卡不是 maturity ladder，也不是一定要
由左到右升級；prompt 明確禁止線性階級意象。這讓正文可以用一張圖說清楚「選最小、可檢查
的門」，又不會誤教 Sandbox 是 Computer Use 的下一層。

安全圖把舊的巢狀護盾改成四張獨立卡：隔離、限制、先問、驗證與紀錄。第二張只處理網域、
檔案與動作 allowlist；第四張才處理結果驗證與 log，不再把 destination allowlist 和 output
verification 混成同一件事。箭頭表示每次 action 會依序接受檢查，不表示四種技術彼此包含。

生成順序是繁中母版 → 英語／簡中各自以母版做 text-localization。每次都提供完整逐字文字表，
只保留穩定概念，不放 model ID、版本、價格、stars、benchmark 或 provider 排名。
`scripts/test_stage08_content.py` 鎖住六張 PNG 的最小尺寸、不同 hash 與三語正文引用；
`scripts/check-image-locale.py` 再檢查全站 locale 圖不會串錯。

## 2026-08-28：Stage 7.5 問題分組圖與閱讀決策樹

重畫 `concept-cluster.{png,en.png,zh-Hans.png}` 與
`reading-decision-tree.{png,en.png,zh-Hans.png}`。兩組都採 16:9 暖白底、亮色卡片、
深藍大字與固定三語版面；每張圖都由 Codex 內建 Image 2.0 獨立生成後人工逐字檢查。

概念圖不再把 12 個概念硬塞進 `Service／Repo／Config／Types` 矩陣。那組層級來自
OpenAI 某個 codebase 的架構案例，不是通用 Agent stack。新版只按讀者會遇到的四種問題
分組：邊界與契約、規劃與合作、檢查與學習、控制與復原；每組三張卡，中央提醒每次只選
1–2 個。

決策樹也不再把容易過期的文章名稱與閱讀時間畫進圖裡，只保留五個症狀與兩個入口群組。
正文的官方來源和 24 筆資源可以更新，圖不必跟著每次重畫。舊的 `stack-4layer`、
`failure-lifecycle`、`principle-dependency` 三組共九張圖已完成引用掃描後移除；它們仍可從
Git 歷史復原。

三語圖必須各自引用 locale 檔，並由 `scripts/test_stage075_content.py` 鎖住六張 PNG 的尺寸、
不同 hash 與正文引用。完整文字表與重產限制在 [`concept-prompts.md`](concept-prompts.md)。

## 2026-08-29：Stage 7.5 Model–Harness Fit 判斷圖

新增 `model-harness-fit.png`、`.en.png`、`.zh-Hans.png`。圖先讓一個 Harness 元件跑同一組 Eval，再分成平行的 Keep／Simplify／Remove 三個結果；三者不是成熟度階梯，也不暗示所有元件最後都應移除。底部固定提醒「模型變強不等於安全邊界自動過時」與「一次只改一個元件，再測一次」。

初版繁中圖雖然文字正確，但 imagegen 自行加上紅色印章、山水、竹子與雲紋，不符合技術教材 house style，也違反無 watermark 約束；最終版移除全部裝飾與印章，改用暖白底、細電路線、深藍大字與藍／橘／綠三張平行卡。英語與簡中以通過人工檢查的最終繁中版作構圖 reference，各自換入完整逐字文字表。獨立 review 發現第一張簡中圖仍殘留「保護／步驟」兩個繁體詞，因此重新產圖並逐字複查；最終簡中橘卡人工逐字確認為「保护仍然需要，但步骤可以更少」。PNG 內文目前仍由人工圖文稽核，不能把一般文字檢查誤稱為 OCR。

共同 prompt 約束：

> Show one Harness component, run the same Eval, then branch into three equal
> parallel outcomes: KEEP when removing it restores a repeatable failure,
> SIMPLIFY when the protection still matters but fewer steps are enough, and
> REMOVE when a deletion test passes without quality loss. State that a stronger
> model does not automatically obsolete safety boundaries and that only one
> component changes before retesting. Warm off-white modern technical-textbook
> style, flat vector icons, no arrow between outcomes, no maturity ladder, no
> model/version/price/ranking/vendor fact, no logo, seal, stamp, signature, or
> watermark, and only the supplied locale text.

人工驗收逐張確認：

- 三個結果都從同一個 Eval 分出去，彼此之間沒有箭頭。
- 繁中圖沒有印章或山水裝飾；英語圖沒有中文；簡中圖沒有繁體字。
- 圖沒有把 prompt workaround 與 permission／sandbox／log／Eval／recovery 畫成同一種可隨意刪除的東西。
- 九張 Stage 7.5 圖維持不同 hash，三語正文各自引用 locale 檔。

## 2026-08-28：Stage 6 RAG 與 Memory 三路圖

新增 `rag-memory-map.png`、`.en.png`、`.zh-Hans.png`。三張都使用 16:9 亮色白底卡片，固定畫出三條互不串線的路：文件切成 Chunk、轉成 Embedding 並寫進 Vector Database；問題取回相關片段、經 Reranking 後產生有來源的答案；重要狀態寫進 Memory，下一次再讀回來。每條箭頭只在自己的色框內由左往右，不暗示 Vector Database 會自動寫入 Memory。

用 Codex 內建 image generation 產生三個語系，逐張檢查節點、箭頭、語言與安全提示。獨立 review 抓到第一版有跨色框箭頭，會讓讀者誤以為 RAG 的資料庫與 Memory 是同一條自動流程；最終版改成三個獨立色框，Memory 只保留「這次結果 → 選重要狀態 → 寫入 → 下次讀回」與重複圖示。簡中初稿另在「重要狀態／下次讀回」殘留兩個繁體字；最終版已修成「重要状态／下次读回」。圖片不放固定 chunk size、top-k、價格、benchmark、模型排名或 GitHub stars；底部只保留「只記必要資料」的資料最小化提醒。三語維持相同 icon、配色、節點與閱讀順序，各自使用在地化文字與 alt text。

這組圖固定放在 Stage 6 七個可見核心詞之後。圖的目的不是取代定義，而是讓初學者一眼分清：RAG 是先找外部證據再回答，Memory 是把重要狀態留給下一次使用。

## 2026-08-30：Stage 6 RAG 詳細流水線重畫

重畫 `rag-pipeline-overview.png`、`.en.png`、`.zh-Hans.png`，並放回預設關閉的「RAG 基礎流水線」。舊圖只有兩排方塊與直線箭頭，且沒有正文引用；新圖沿用 `rag-memory-map` 的亮色白底卡片 house style，明確分成「先整理資料」與「問題來了」兩條 lane。Contextualization、query rewrite、fusion 與 reranking 都以虛線和「可選」標籤呈現；候選來源並列 semantic、BM25、SQL／Web，不暗示 vector database 是唯一 retriever。

繁中第一版的 `retrieve` 箭頭錯落在最終答案，視覺檢查後改為從可搜尋資料庫落到「多路找候選」。英語與簡中沿用修正版幾何；簡中初稿 footer 的「記錄」另修成「记录」。三語均不放固定 chunk size、top-k、價格、模型、排名、benchmark、日期或 GitHub stars。

## 2026-08-27：Stage 3 Tool Use 六步圖

新增 `tool-use-loop.png`、`.en.png`、`.zh-Hans.png`。三張都使用 16:9 亮色白底卡片，固定呈現 `模型 → Tool Call → 程式驗證 → 工具執行 → Tool Result → 模型答案`，並用盾牌框住程式驗證與工具執行。底部只保留三個安全提示：allowlist、敏感動作先問人、設定最大輪數。

使用 Codex 內建 image generation 先做繁中母版，再以母版產生英文。簡中直接從繁中母版在地化時，兩次殘留 `請／設`；最終改用英語版作版面母版重新生成，才得到完整簡體字形。三張圖均逐字檢查標題、六步、中心句與三個安全提示；沒有放版本、價格、stars 或其他易變資訊。

最終 prompt 的核心限制是：六張編號卡必須依 `1→2→3→4→5→6` 連接；模型只能提出請求，程式才執行工具；所有文字逐字提供，三語只改文字，不改 icon、箭頭、配色和版面。圖固定放在 Stage 3 八個核心詞之後，先讀定義再看關係。

## 2026-08-27：Stage 2 Prompt Engineering 概念圖

新增 `prompt-engineering-map.png`、`.en.png`、`.zh-Hans.png`。三張皆為 16:9 亮色白底卡片圖，保持同一閱讀順序：

1. Prompt 四部分：目標／資料／規則／輸出
2. Zero-shot／One-shot／Few-shot 的範例數量差別
3. Eval → 修改一處 → 再試一次
4. Chain-of-Thought 只畫成可檢查的編號步驟，不使用「讀取腦內想法」的意象

用 Codex 內建 image generation 先做繁中 canonical，再以同一張圖做英語與簡中在地化。人工校對時抓到初稿把 Few-shot 寫成 `2–5`；由於正文已明確說沒有通用固定數字，三張最終圖全部改成「多個／multiple／多个例子」。另將初稿的腦袋思考泡泡改為 `1／2／3` checklist，避免和「不要索取完整內部思考」的正文衝突。

這組圖固定放在 Stage 2 九個可見核心詞之後。圖片只整理已定義的關係，不代替正文；三語 alt text 也各自描述「四部分、範例數量、檢查迴圈、CoT 的可檢查步驟與隱私邊界」。獨立 review 又抓出兩個視覺問題：英語第二格曾把正文的 `Data` 漂成 `Context`，底部兩段回箭頭也沒有真的從「再試一次」回到 Eval。最終版已把英語欄位改回 `Data`，並以一條由右回左的長箭頭形成單一閉環。

## 這批處理了什麼

`resources/diagrams/` 的慣例是 `NAME.png` = zh-TW、`NAME.en.png`、`NAME.zh-Hans.png`。
處理前有 5 張圖缺 9 個變體，導致 `.en.md` / `.zh-Hans.md` 頁面**alt text 已在地化、圖檔還是繁中**。

| 圖 | 結果 |
|---|---|
| `multi-llm-delegation-composition` | 補上 `.zh-Hans`，忠實比照既有的 `.png` / `.en.png`（深色霓虹＋廠商 logo） |
| `teacher-ai-use-cases-overview` | 三語重產，**升級為 house style**（彩色卡片＋線條 icon） |
| `teacher-ai-classroom-use-cases` | 三語重產，**升級為 house style**（五欄卡片式） |
| `rag-pipeline-overview` | 三語重產，淺色卡片流程圖（**未達 house style**，見下方） |
| `chunking-strategies` | 三語重產，淺色卡片流程圖（**未達 house style**，見下方） |

副檔名同時從 `.jpg` 改為 `.png`（house style 那 20 張都是 png，線條插圖＋密集文字用 jpeg 會有壓縮雜訊），
`stages/06-memory-rag` 與 `branches/for-teacher` 共 12 處引用一併更新。

## 生成方式

**委派 Codex CLI 的內建 image-gen 工具**，不是貼 prompt 到 ChatGPT 網頁。流程：

1. 寫 brief 到 `.ai/codex_task_<NN>_<slug>.md`（`.ai/` 已 gitignore）
2. `bash ~/.claude/skills/codex-delegate/scripts/run_codex.sh --brief-file <path> --repo "$PWD"`
3. brief 裡指定 repo 內的既有圖當**風格參考**（Codex 能直接讀圖檔），並附完整逐字文字表
4. **委派者自己逐張開圖驗收**，不採信 `.result.json` 的 status

風格基準檔：`agent-guardrail-patterns.zh-Hans.png` 與
`teacher-ai-use-cases-overview.png`（本批做得最好的一張，可當樣板）。舊的
`stack-4layer` 已在 Stage 7.5 漸進式重整時移除，不能再當通用 Agent stack 樣板。

## ⚠️ 驗收教訓（這批最值得記的部分）

### 1. delegate 回報 `success` 不等於做對了 —— 這批四次假成功

| 事件 | 實際狀況 |
|---|---|
| `chunking-strategies.zh-Hans` 第 1 次 | 殘留繁體 `種` / `純`，回報 success |
| 同上第 2 次 | 修好 `純`→`纯`，**`種` 仍是繁體**，又回報 success |
| rag/chunking house style 第 3 次 | 修好乾淨度但**整個丟掉 house style** |
| 同上第 4 次 | **根本沒改寫檔案**（時間戳未變），卻列出一串「已執行的驗證指令」 |

**驗收必須是委派者自己看原始產出**，而且要有能分辨的方法。

### 2. CJK 繁簡差異在縮圖尺寸下看不出來

`種`/`种`、`純`/`纯` 只差一個部件。可靠做法：

- 把有疑慮的文字區塊**裁切放大 3–4 倍**
- 拿 repo 裡**已知正確的同一個字**當對照
- 分辨重點在偏旁：`种` = `禾`+`中`、`種` = `禾`+`重`；`纯` = `纟`、`純` = `糸`

### 3. 長寬比是客觀的風格對齊指標

肉眼判斷「風格像不像」不可靠。量長寬比可以抓出版面鬆緊度的偏移——
本批就是這樣抓到 `rag-pipeline` 變體被拉鬆（繁中 3.20、`.en` 2.86、`.zh-Hans` 2.40）。
現在五組圖三語長寬比差異都 < 0.05。

### 4. 「改圖」比「重新生成」更容易失控

要求 Codex 修改既有圖時，它兩次都超出範圍（擅自重新設計節點、改名），
還引入新缺陷（標籤壓框、文字被形狀邊緣裁切）。
**指定重新生成、並附完整規格，比叫它「只修這兩點」可靠。**

## 已退役的舊圖

2026-08-30 全站引用掃描確認下列舊圖已沒有任何頁面使用，因此移除；
`rag-pipeline-overview` 的舊平面箭頭版則由已通過人工檢查的 Image 2.0 三語版本取代並重新上線：

- `chunking-strategies` 三語圖：內容已放入 Stage 6 漸進式文字教學，不再保留素面流程框。
- `reflexion-persistent-memory-loop` 三語圖：內容已整合進 Stage 6 的 RAG／Memory 路線。
- `multi-agent-debate-flow` 三語圖：沒有頁面使用，且深色霓虹風不符合目前主頁式視覺規範。
- `branch-tier-progression.png`：角色入口不是必走的升級階梯，表格比箭頭圖更不容易誤導。

這些圖仍可從 Git 歷史取回。`check-image-locale.py` 現在也會阻擋新的未引用圖檔，避免新版上線後又把舊版留在 repository。

## 重產時的檢查

```bash
python scripts/check-image-locale.py
```

該 gate 把「同語系變體已存在但頁面沒用」當錯誤直接擋，「變體還沒做」則記在它的
`KNOWN_MISSING` 白名單裡——所以**新增一張缺變體的圖會讓 build 失敗**，不會默默累積。
補完變體後記得把對應的 `KNOWN_MISSING` 條目一起移除。

## 2026-08-29：Stage 7 控制問題圖

`agent-engineering-control-questions.{png,en.png,zh-Hans.png}` 取代原本的垂直五層圖。
三張皆以 Image 2.0 產生，固定為和主頁 README 圖相同的 `1672×941` 橫式比例；繁中先定稿，
英語與簡中再以同一母版做文字在地化。視覺基準是主頁 `banner`／`learning-map`：奶油白背景、
深藍字、亮色語意線、圓角卡、簡單線條 icon、充足留白與單一閱讀方向。

共同語意契約：

1. Prompt 與 Context 都進入 Harness，但不是完整 Agent runtime。
2. 上半部只畫一次 Agent run：Harness 內含 model call、tools、state／logs／results、下一步決定與 Agent Loop。
3. 下半部才畫整個長任務：Workflow Graph／Production Orchestration 連接 Goal、Harness run、evidence check、返回路線、human approval 與完成狀態。
4. Loop Engineering 另外明寫 `Goal → Action → Observation → Adjustment`、預算與停止條件；不得和 Harness 內的一次 Agent Loop 混成同一尺度。
5. 圖上以「不是五層」直接阻止嚴格層級誤讀；Harness 包住 Agent Loop，上下兩個尺度分開；不得畫成 Harness 被 Loop 淘汰，也不是章節順序。
6. 三語使用相同尺寸、形狀、箭頭、icon、配色與間距，並各自引用 locale 檔。
7. 箭頭只能走卡片間或專用返回通道；不能穿過文字、icon 或另一個框，arrowhead 也不能壓到無關元素。

人工驗收除了看文字，也逐一確認：

- Prompt 與 Context 都指向 Harness；Harness 內同時畫出 model、tools、state、logs、results、下一步與 Agent Loop。
- 圖用 Harness 包住 Agent Loop 與上下兩個尺度呈現責任重疊；標題「不是五層」不暗示產品世代或 Stage 2→6→7→5→4 的閱讀順序；正文另外提供 Stage 3、4、7 的入門／加深路線。
- 下方 Workflow Graph 保留 Harness run、evidence check、人工核准、完成與失敗返回，沒有把每個節點都畫成 Agent。
- 所有卡片依同一格線對齊；icon 完整留在自己的圓框內；兩條返回箭頭都有獨立留白通道，沒有壓字、穿框或互相交叉。
- 英語圖沒有中文；簡中圖沒有肉眼可見的繁體字；繁中圖沒有簡中用語。

原 `harness-loop-graph-boundary.{png,en.png,zh-Hans.png}` 因把 Harness 縮成「一次執行」且和新圖重複而退役；控制問題 PNG 已吸收正確的責任重疊、內外兩種 loop 與返回路線，不再讓讀者同一章看兩張近似圖。

## 2026-08-29：教師把關循環圖

新增 `teacher-ai-review-loop.png`、`.en.png`、`.zh-Hans.png`，取代會把「即時批改」和學生能力推測畫成可靠功能的舊 `teacher-ai-classroom-use-cases` 三語圖。新圖只保留一條可由教師控制的五步循環：

1. 教師寫清學習目標。
2. AI 只做草稿。
3. 教師檢查隱私、事實與偏見。
4. 學生使用教材。
5. 教師觀察學習情況並修改下一輪設計。

用 Codex 內建 imagegen 先產生繁中母版，再以 text-localization 路徑產生英語與簡中。三張都維持 16:9、亮色白底卡片、同一組 icon、單一路徑與回到第一步的箭頭。人工逐字確認標題、五步與底部「AI 幫忙，教師決定」；不得出現產品 logo、模型名稱、成熟度 badge、分數、診斷、自動評分或自動決策。

共同 prompt 約束：

> Preserve the exact five-step clockwise loop, illustrations, arrows, colors,
> spacing, proportions, and warm off-white background. Use only the supplied
> verbatim locale text. AI drafts; the teacher checks privacy, facts, and bias;
> the teacher observes and revises. No autonomous grading, diagnosis, learner
> score, product logo, badge, extra caption, mixed language, or watermark.

## 2026-08-30：首頁學習路徑 Banner

`banner.png`、`.en.png`、`.zh-Hans.png` 以 Image 2.0 重新產生，取代含固定週數的舊版。
三語共用 `1672×941` 橫式母版、奶油白背景、深藍字、亮藍／橘兩條路、紫色共用 hub、
圓角卡與大留白。路徑固定為：

- 共用基礎 `Stage 0–1–2` 後分流。
- Track A：`A1 → A2 → Stage 5 → A3 → Stage 8`。
- Track B：`3 → 4 → Stage 5 → 6 → 7 → 7.5 → Stage 8`。
- Stage 5 後用上下兩條不交叉的路分開畫 A3 與 6／7／7.5，再於 Stage 8 匯合。
- Stage 8 後才分到研究人員、開發者、教師、知識工作者與日常使用者。

底部只保留三個不會因時間改變的提示：「使用現成 CLI Agent」、「打造自己的 Agent」、
「一站一個小成果」與 repository URL。不得放週數、月份、每週時數、價格、版本、年份、
GitHub stars 或其他容易漂移的指標。箭頭只能落在卡片／節點邊緣；不得穿過文字、icon、
框線或其他箭頭。三語必須使用同一節點、同一方向、同一色彩角色與同一欄位位置。

共同重產 prompt 核心：

> Preserve the wide 1672×941 cream-white README infographic, exact route,
> bright blue/orange paths, purple shared hubs, rounded cards, generous whitespace,
> and locale-specific text. Show Stage 0–1–2, A1–A2, 3–4, Stage 5,
> then separate Stage 5–A3–Stage 8 and Stage 5–6–7–7.5–Stage 8 lanes before
> the five role paths. Replace mutable duration metrics with
> stable Track A, Track B, and one-result-per-stop guidance. Every arrow must land
> on a card or node edge. No text, icon, border, node, or arrow may overlap.
