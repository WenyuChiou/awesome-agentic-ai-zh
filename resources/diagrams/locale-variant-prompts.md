# 語系變體圖 — 生成流程與教訓

> 姊妹檔：[`concept-prompts.md`](concept-prompts.md)（Stage 7.5 那 3 張概念圖的 ChatGPT prompt）。
> 這份記錄的是 **2026-08-02 那批 5 張圖 × 3 語系** 是怎麼產出來的，以及過程中踩到的坑。

## 2026-08-28：Stage 6 RAG 與 Memory 三路圖

新增 `rag-memory-map.png`、`.en.png`、`.zh-Hans.png`。三張都使用 16:9 亮色白底卡片，固定畫出三條互不串線的路：文件切成 Chunk、轉成 Embedding 並寫進 Vector Database；問題取回相關片段、經 Reranking 後產生有來源的答案；重要狀態寫進 Memory，下一次再讀回來。每條箭頭只在自己的色框內由左往右，不暗示 Vector Database 會自動寫入 Memory。

用 Codex 內建 image generation 產生三個語系，逐張檢查節點、箭頭、語言與安全提示。獨立 review 抓到第一版有跨色框箭頭，會讓讀者誤以為 RAG 的資料庫與 Memory 是同一條自動流程；最終版改成三個獨立色框，Memory 只保留「這次結果 → 選重要狀態 → 寫入 → 下次讀回」與重複圖示。簡中初稿另在「重要狀態／下次讀回」殘留兩個繁體字；最終版已修成「重要状态／下次读回」。圖片不放固定 chunk size、top-k、價格、benchmark、模型排名或 GitHub stars；底部只保留「只記必要資料」的資料最小化提醒。三語維持相同 icon、配色、節點與閱讀順序，各自使用在地化文字與 alt text。

這組圖固定放在 Stage 6 七個可見核心詞之後。圖的目的不是取代定義，而是讓初學者一眼分清：RAG 是先找外部證據再回答，Memory 是把重要狀態留給下一次使用。

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

風格基準檔：`stack-4layer.zh-Hans.png`、`agent-guardrail-patterns.zh-Hans.png`、
`teacher-ai-use-cases-overview.png`（本批做得最好的一張，可當樣板）。

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

## 已知未竟事項

`rag-pipeline-overview` 與 `chunking-strategies` 這兩組（共 6 張）**視覺等級不如 teacher 兩組**——
是乾淨、文字正確、三語一致的淺色卡片流程圖，但沒有線條 icon、配色也弱。
四次嘗試都在「有 house style 但有瑕疵」與「乾淨但退回素面」之間擺盪。

要再挑戰的話，建議：
- 以 `teacher-ai-use-cases-overview.png` 為唯一視覺樣板，把它的構圖元素逐項拆解寫進 brief
- 或改用 `--model` 指定不同模型重試
- 原始 `.jpg`（2026-05 版）仍在 git 歷史中，必要時可還原

## 重產時的檢查

```bash
python scripts/check-image-locale.py
```

該 gate 把「同語系變體已存在但頁面沒用」當錯誤直接擋，「變體還沒做」則記在它的
`KNOWN_MISSING` 白名單裡——所以**新增一張缺變體的圖會讓 build 失敗**，不會默默累積。
補完變體後記得把對應的 `KNOWN_MISSING` 條目一起移除。
