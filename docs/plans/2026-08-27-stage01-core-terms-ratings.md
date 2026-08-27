# Stage 01 核心詞與學習資源評分回補計畫

## 目的

Stage 1 已有 Token、Context Window、Temperature 三個核心詞，但正文第一次使用沒有粗體，三個定義也沒有明說「這章會拿它做什麼」。前次漸進式重整還保留了 17 筆延伸資源，卻拿掉整個推薦度欄位；讀者看得到入口，卻不知道先後次序。

本層只修這兩個回溯缺口，不重查或改寫 15 家模型事實表。模型、價格、context 與 availability 仍使用 2026-08-27 的既有 freshness fact pack；Stage 2 的 Prompt 定義留給下一層。

## 核心詞形狀

三語在第一個練習前固定保留相同順序：

1. **Token（詞元）**：模型讀寫與 API 計價的小單位；積木比喻；接到練習 2 的 usage 與成本。
2. **Context Window（上下文視窗）**：一次請求可處理的 token 空間；桌面比喻；提示與歷史先占位、答案也要留空間；另查最大輸出上限；接到長文件分批。
3. **Temperature（溫度）**：抽樣變化程度；從候選積木挑下一塊的比喻；接到輸出穩定度，不宣稱增加知識或保證重現。

本章目的中的第一次正文使用先以粗體標出。核心詞標籤、用途、比喻與限制保持可見，不放進 `<details>`。

`scripts/reader-ux-pages.yml` 為 Stage 1 加入 `core_terms`，並鎖住核心詞 heading、練習 1 heading、三語 term／label、順序與最低解釋長度。

## 17 筆資源評分

17 筆入口、五組順序與 `4/4/2/4/3` rowspan 全部保留。新增「推薦度」欄，不恢復會變動的 GitHub stars。

既有歷史版本曾使用 5 顆星，但現在 style guide 明定 `⭐⭐⭐⭐⭐` 代表「跳過會卡住」。這 17 筆都位於選讀區，因此不假標必修五星：

- `⭐⭐⭐⭐`：10 筆，與本章 API、本機路徑或核心原理高度相關。
- `⭐⭐⭐`：6 筆，有用但較進階、平台限定或更新較慢。
- `⭐⭐`：1 筆，`karpathy/LLM101n` 已封存，只作歷史參考。
- `⭐⭐⭐⭐⭐`：0 筆；真正必修入口已在本章 `📚 必修閱讀` 區。

三語每一列的 URL→推薦度必須完全一致；reader-UX config 同時啟用 `ordered_external_urls` 與 `resource_url_ratings`。

## 來源查核

- GitHub API snapshot 於 `2026-08-27T12:37:04Z` 覆蓋表內 13 個 repositories；除 `karpathy/LLM101n` 已封存外，其餘均未封存、未搬家。
- 17 個入口在 2026-08-27 UTC 全部可取得 HTTP 200。
- Anthropic Quickstart 的舊網址會轉到 `https://platform.claude.com/docs/en/get-started`，本層改用最終官方網址。
- Hugging Face LLM Course 入口會轉到 `https://huggingface.co/learn/llm-course/chapter1/1`，本層改用最終課程入口。
- CHANGELOG 日期以 staging 前重查的 GitHub API header `Thu, 27 Aug 2026 13:40:14 GMT` 決定。

## Stack 與邊界

- Stack base：`codex/core-terms-reader-contract`（PR #144）。
- Branch：`codex/stage01-core-terms-retro`。
- 不修改 Stage 0、Stage 2、模型 freshness tooling、模型事實表或 README。
- 未獲使用者明確同意前，不 merge、不刪 branch、不移除 worktree、不 prune。

## 驗收

- 三語第一次正文使用的三個核心詞都是粗體。
- 三個定義逐詞回答定義、比喻、本章用途與限制。
- core-term gate 通過，且核心詞區早於練習 1。
- 必要解釋加入後，三語可見非空白字元實測為 `6,721／10,248／6,714`；ratchet 只保留 50 字緩衝，設為 `6,771／10,298／6,764`，不以刪除核心觀念換取舊門檻綠燈。
- 三語各有 17 筆 URL、17 個推薦度，分布固定為 `10／6／1／0`（四／三／二／五星）。
- 五個 rowgroup 仍為 `4/4/2/4/3`，每列 URL→推薦度一致。
- `git diff --check`、reader-UX tests／formal gate、anchors、mirror、locale、Hans、freshness、MkDocs build 全部通過。
- 最終 staged diff 經獨立 code-reviewer；PR 只開啟供檢查，不合併。
