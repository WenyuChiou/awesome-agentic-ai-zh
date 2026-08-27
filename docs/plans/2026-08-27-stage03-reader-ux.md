# Stage 03 工具使用與第一個 Agent 重整計畫

> - 狀態：PR 03A 已開啟且 CI 全綠；PR 03B 正在補齊六題可執行資料夾與安全回歸測試
> - 查核日期：2026-08-27 UTC
> - 工作分支：`codex/stage03-reader-ux`
> - 堆疊基底：`codex/track-a-reader-ux`（PR #147）
> - 發布規則：只建立堆疊 PR；未經使用者明確同意，不合併、不刪分支、不清理 worktree。

## 這一章真正要教什麼

Stage 03 是讀者第一次把「只會回答文字的模型」接到程式。讀者要看懂一個完整來回：

1. 程式把可用工具和輸入形狀告訴模型。
2. 模型回傳一張結構化的工具請求。
3. 程式檢查請求並執行真正的函式。
4. 程式把結果送回模型。
5. 模型用結果回答，或再呼叫下一個工具。

本章不把 LLM 說成會自行執行程式。對 client-executed tool 而言，模型只提出請求；真正執行、驗證、權限與錯誤處理都由應用程式負責。

## 已確認的缺陷

- 繁中頁面約 23,855 個非空白字元，七個 `<details>` 中一個預設展開；第一眼同時出現概念、十多筆導讀、六題程式、反思、專案與檢查表。
- 六個練習雖然存在，長程式與補充觀念仍和主線同一層；初學者不容易知道第一個動作。
- 缺少第一題前的可見核心詞區。`ReAct`、`Structured Output` 等詞先出現，後面才解釋。
- 第一題示範只取得 tool call，沒有真的執行工具、送回 tool result、取得最後答案；與「完整工具迴圈」的敘述不符。
- 把 `LLM + tools + loop` 寫成唯一的 Agent 定義；本章應明說這是學習地圖採用的工作定義。
- 圖片把 LLM 簡化成只有 text-in/text-out，並用同一張混合語言圖承擔三語概念；現況已不準確。
- 把 ReAct 寫成需要顯示思維鏈。可觀察的工具迴圈可以是 ReAct-inspired，但不應要求或洩漏私人 chain-of-thought。
- 結構化輸出被寫成「保證正確」。Schema 可以限制外形，仍需處理 refusal、截斷、語意錯誤與供應商差異。
- 錯誤處理教讀者把 retry 全交給模型。正式應用仍須捕捉 transport、解析、schema 與工具執行錯誤，設定有限重試和停止條件。
- 固定預算數字互相矛盾，也沒有輸入／輸出 token 假設。`$0 local` 只代表沒有 API 費，不能代表硬體與電力完全免費。
- 多處用單次觀察宣稱某模型「幾乎一定錯」或另一模型「較穩」，但沒有 eval；改成要求同一題、同一 schema、同一評分重跑。
- 精選資源表仍是 Markdown 空白分類格，混入會過期的 GitHub star 數字。
- `jxnl/instructor` 已由 GitHub 重新導向到 `567-labs/instructor`，應使用 canonical repository 名稱。
- Stage 03 範例的 SDK 範圍仍是 `openai>=1.50,<2.0`、`anthropic>=0.40,<1.0`；目前 PyPI 分別已到 OpenAI 3.x 與 Anthropic 1.x。這項程式層更新另放在下一層 PR，避免文件重整和 30 個範例檔一次混在一起。

## 讀者不展開選單時看到的主線

1. 一句話說明：工具像模型可以填寫的工作單；真正做事的是程式。
2. `📌` 四到五個可驗證的學習目標。
3. 第一題前可見的八個核心詞，首次正文出現加粗：
   - Tool Use
   - Function Calling
   - Tool Schema
   - Tool Call
   - Tool Result
   - Agent Loop
   - ReAct
   - Structured Output
4. 一張短表分清「直接回答、結構化輸出、工具呼叫」何時使用。
5. 五條可見安全底線：允許清單、參數驗證、最小權限、高風險確認、有限迴圈。
6. 六個練習的標題、既有 anchor、成果、第一個可複製動作。
7. 一個推薦小專案：安全的天氣小幫手。
8. `✅` 短版自我檢查與 Stage 04 入口。

核心詞不是八個同義詞。每個詞都要說明它是什麼、像什麼、在本章做什麼，以及不能混淆的限制。

## 預設收合內容

- 時間、先備知識、環境、模型與費用估算。
- `📚` 必修閱讀的閱讀順序與完整說明；標題仍保持可見。
- AI／LLM／Agent 的補充框架與本章工作定義。
- 六題完整程式、Path A／Path B、逐步解說與排錯。
- Structured Output 的供應商差異與 strict-mode 限制。
- Reflection、Reflexion、Self-Refine、CoT、Planning 的關係與後續路由。
- 完整精選資源表與其他專案靈感。

所有 `<details>` 預設關閉。練習標題、成果與第一步不得藏入選單。

## 六個練習的角色

1. **Function Calling**：完成一次 schema → call → execute → result → final answer。
2. **多工具選擇**：讓模型在數個安全工具中選一個；程式仍以 allowlist 派發。
3. **ReAct from scratch**：不用 framework 寫有限次數的工具迴圈。
4. **多步任務**：用同一個 loop 完成兩個以上互相依賴的工具步驟。
5. **錯誤處理**：分開處理程式錯誤與可回傳給模型的語意錯誤；不做無限 retry。
6. **Schema 設計**：比較壞 schema 與好 schema，使用固定 eval，不做無來源的模型排名。

練習 2–6 保留既有 `examples/stage-3/` 入口。練習 1 的 inline 範例保持可直接複製，範例硬化 layer 另補上 `examples/stage-3/01-function-calling/` 的雙路徑完整 round trip、README 與離線測試。

範例資料夾入口加入可見主線後，三語未展開實測為 `4,315／8,090／4,381` 個非空白字元；reader-UX 上限只保留 50 字餘量，調成 `4,365／8,140／4,431`。這是讓讀者可以直接開檔執行的必要導航，不以刪掉入口來維持舊門檻。

## 2026-08-27 官方事實包

來源優先順序是供應商正式文件、正式 SDK／PyPI、原始論文、官方或專案 model card；社群 repo 只證明教學內容與維護狀態。

1. [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling)：function calling 是模型與外部系統互動的結構化介面；應用程式執行函式。OpenAI strict mode 要求物件 `additionalProperties: false`，且 properties 全部列入 `required`。這不是所有 OpenAI-compatible endpoint 的通用保證。
2. [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)：schema 能限制外形，但仍要處理 refusal、截斷與語意品質；以 eval 驗證 schema 設計。
3. [Anthropic How Tool Use Works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)：client tool 的標準迴圈是 `tool_use` → 應用程式執行 → `tool_result`；非 `tool_use` 的 stop reason 也必須明確處理。
4. [Anthropic Handle Tool Calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)：每個 tool use 都要有對應 result；錯誤用 `is_error: true`。工具結果可能含 prompt injection，應視為不可信資料。
5. [Anthropic Prompt Injection Guidance](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)：工具輸入與輸出都要驗證，正式上線前要用惡意內容 red-team。
6. [Gemini Function Calling](https://ai.google.dev/gemini-api/docs/function-calling)：模型產生函式名稱與參數，應用程式負責執行並回傳結果；可有平行與連續呼叫。
7. [Ollama Tool Calling](https://docs.ollama.com/capabilities/tool-calling)：官方示範 single、parallel、multi-turn agent loop。專案仍依使用者已驗證的安裝保留 `qwen2.5:3b`，但不再宣稱它永遠穩定。
8. [Ollama OpenAI Compatibility](https://docs.ollama.com/api/openai-compatibility)：本章 Path A 是 OpenAI Python SDK 連到 Ollama 的 compatible endpoint；要明說不是呼叫 OpenAI 雲端服務。
9. [ReAct paper](https://arxiv.org/abs/2210.03629)：原論文交錯 reasoning traces 與 actions；本章只教可觀察的 action／observation loop，不要求模型輸出私人推理。
10. [Anthropic PyPI](https://pypi.org/project/anthropic/) 與 [OpenAI PyPI](https://pypi.org/project/openai/)：2026-08-27 查核時最新 major 已分別為 1.x 與 3.x，Python 需求皆至少 3.10；舊範例 pins 另案更新。

## 精選資源表

三語使用相同順序、URL、狀態與推薦度。表格使用六個 `<tbody>`，分類欄以 `rowspan` 合併。推薦度是本 Stage 的學習優先順序，不是 GitHub stars：

| 分組 | 筆數 | 用途 |
|---|---:|---|
| 官方核心文件 | 6 | 先建立正確工具迴圈、schema、安全與 ReAct 定義 |
| 官方課程與範例 | 4 | 跟著 notebook 或可部署範例學 |
| 從零實作 | 4 | 看懂 framework 藏起來的 loop |
| Framework／CodeAct 對照 | 3 | 完成本章後再比較抽象 |
| 中文章節式教材 | 2 | 需要長篇中文路線時深入 |
| Structured Output 工具 | 2 | 需要 typed／constrained output 時使用 |

總計 21 筆。移除所有 `★ 13k+` 類易變人氣數字；保留 `⭐⭐⭐⭐⭐` 到 `⭐⭐` 的編輯推薦度。停滯專案明標「教學玩具／歷史參考」，不包裝成 production 選擇。

## 圖片處理

三張 `ai-ml-llm-agent-hierarchy*.png` 只被 Stage 03 三語引用，沒有產生器、導覽或其他文件引用。它們混合語言、文字太密，且把 LLM 限定成 text-only。這一層移除三張圖及引用，改成可搜尋、可翻譯、可被螢幕閱讀器讀取的短文字流程；不另外新增另一張容易過時的點陣圖。

## 兩層 stacked PR

### PR 03A：Stage 03 讀者路徑

**Branch:** `codex/stage03-reader-ux`，base 為 PR #147。

預計檔案：

- 三語 `stages/03-tool-use-and-hello-agent*`
- 三語 `resources/glossary*`
- 三語 `resources/schema-design-cheatsheet*`（主章直接連出的規格補充）
- 三語根目錄 `README*`（Stage 03 練習數 5 → 6 的直接一致性修正）
- `stages/DESIGN.md`
- `scripts/reader-ux-pages.yml`
- `scripts/freshness-models.yml`（Stage 03 官方事實包與 90 天三語 marker）
- `scripts/repository-freshness-snapshot.json`
- `scripts/test_stage03_snippets.py`（直接執行三語 Markdown 內的參數 guard regression）
- 本計畫
- `CHANGELOG.md`
- 刪除三張過時階層圖

凍結候選清單為 22 個檔案。2026-08-27 重新掃描全部 298 個 repo 後，snapshot 確實有變更：Stage 03 已改用 `567-labs/instructor` 的正式網址，因此不再保留舊的 redirect key。第一次 review 又證明 AST 能 parse 不代表參數安全，因此新增一個只針對 Stage 03 Markdown 程式的 regression。任何其他依賴必須先寫入本計畫並重新計數，不能用 `git add .` 補進去。

全站掃描也找到 27 個既有錯誤，主要是其他章節的舊 repo 名稱與 Stage 06／08 的授權標示。這些不是 Stage 03 新造成的問題，會在對應章節 PR 修正；本 PR 的要求是 snapshot 涵蓋全部 298 個連結，且 Stage 03 自己沒有 redirect、license mismatch 或遺漏。

### PR 03B：Stage 03 範例硬化

**Branch:** `codex/stage03-example-hardening`，base 為 PR 03A。

- 新增 `01-function-calling/`：Ollama／Anthropic starter、兩個離線測試、requirements 與三語 README，共八個檔案；Stage 3 六題因此全部有獨立可執行資料夾。
- 六個資料夾的 SDK 範圍更新為 2026-08-27 PyPI 已查核的 OpenAI 3.x／Anthropic 1.x，Python 最低需求皆為 3.10；Anthropic starter 使用固定 `claude-haiku-4-5-20251001`。
- 六題都把模型產生的工具名稱與參數當成不可信資料：先做 allowlist、JSON／物件／必要欄位檢查，再執行；解析、未知工具與參數錯誤都變成可觀察結果，不讓 Python 直接 crash。
- Exercise 3–5 的多輪路徑明分正常完成與 `length`／`max_tokens`／其他停止原因，並保留 `max_iter`；Anthropic 的失敗結果帶原 call ID 與 `is_error: true`。
- 12 個既有 starter、10 個既有 mock tests、15 份既有 README、五個 requirements 全部對齊；新增一個結構 regression，鎖住六資料夾、雙路徑、SDK major、固定模型、PowerShell、查核日期與 starter 自我檢查。
- 三語範例索引改為 `folder 6`，Stage 03 第一題直接連到相同語言 README；DESIGN 與 style guide 同步留下日後章節可複用的安全範例契約。
- README 保持走查用途，不擴成另一章；深入內容仍路由到官方 Function Calling／Tool Use 文件。

PR 03B 的驗收不是「舊測試仍綠」而已。每個 starter 至少有兩個執行時 assert；12 個資料夾測試入口都要逐一跑，另在乾淨 Python 3.10+ 環境安裝當次 requirements，確認目前 SDK major 可以 import 與執行 mock。三語 README 必須同 URL、同模型 ID、同價格公式、同查核日，且不能殘留 Unix-only 第一指令、浮動 Haiku alias、無 token 假設的固定價格或沒有 eval 的速度／品質排名。

兩層都只開 PR，不合併。這能讓內容設計與可執行程式各自回朔，也讓 review 的 staged fingerprint 保持可理解。

## 驗收標準

- 不展開任何選單，讀者仍能說出工具迴圈五步並開始練習 1。
- 八個核心詞在第一題前可見、首次正文使用粗體，三語順序與意思一致。
- `📌`、`📚`、`🛠`、`🎯`、`✅` 全部保留。
- 六個練習標題、anchor、成果與第一步保持可見；沒有預設展開的 `<details>`。
- 第一題示範真的完成 tool call → 執行 → tool result → final answer。
- 沒有把 private chain-of-thought 當必要輸出；ReAct、CoT、Reflection、Reflexion、Self-Refine 與 Planning 均保留並正確路由。
- 沒有無限 retry、未驗證參數、任意函式派發或「模型自己執行工具」的錯誤教學。
- Ollama weather guard 會實際拒絕非物件、缺欄位、多欄位、數字／空白 city 與非 celsius unit；Anthropic 路徑同樣拒絕空白 city。
- 本機路徑明說 API 費 `$0`，但不宣稱硬體與電力零成本；雲端費用使用公式與當次價格來源。
- 21 筆資源三語同 URL、同順序、同評分、六個 rowgroup，`rowspan` 總和為 21。
- 無 volatile GitHub stars；redirect、停滯與授權狀態依 2026-08-27 API metadata 標示。
- 三張被刪圖片沒有孤兒引用。
- reader-UX、strict anchors、anchor slug parity、mirror parity、locale links、Hans、image locale、duplicate repositories、freshness、docs tree 與 MkDocs build 全通過。
- 最終穩定 staged diff 只做一次獨立 `code-reviewer`；任何 review 後修改都使 ack 失效。
- commit、push、開 PR 後停下；未經使用者明確同意，不 merge、不 retarget、不清分支。

## 本層驗證紀錄

- 三語未展開量測：繁中 `4,237`、英文 `7,975`、簡中 `4,295` 個非空白字元；各有 12 個 `<details>`、0 個預設展開。
- 三語各有 21 筆資源；rowspan 固定為 `6/4/4/3/2/2`，URL 順序與逐列推薦度一致。
- stage template、strict anchors、anchor slug parity、mirror parity、locale links、Hans、image locale、duplicate repositories、freshness、reader-UX 與 298-repo snapshot coverage 通過。
- `python -m pytest scripts -q`：312 passed，其中 6 條直接執行 Stage 03 三語 snippet guard。
- Stage 03 的 10 個 mock test 入口逐一執行，全部通過；因每個資料夾都使用同名 `test.py`／`test_anthropic.py`，不能用單一 pytest collection 當作同一個 package 收集。
- 三語頁面的 9 個 Python fenced blocks 全部通過 `ast.parse`。
- `python scripts/build-docs-tree.py` 與 `python -m mkdocs build` 通過；build 只留下專案既有 warning，沒有 Stage 03 新錯誤。
