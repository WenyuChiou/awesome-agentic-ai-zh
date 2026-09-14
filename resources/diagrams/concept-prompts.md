# Stage 7.5 概念圖重產規格（2 圖 × 3 語言）

> 2026-09-13 使用 Codex 內建圖片生成工具製作。工具未提供可驗證的引擎版本，
> 所以本紀錄不宣稱使用特定 Image 型號。`NAME.png` 是繁中，`NAME.en.png`
> 是英文，`NAME.zh-Hans.png` 是簡中。

## 共用視覺規格

每次只生成一張圖。英文與簡中必須以通過人工檢查的繁中圖作構圖 reference，
只替換文字，不另行重排。

```text
Create a polished educational infographic for a beginner-friendly Agentic AI
learning roadmap. 1672×941 landscape, warm cream-white background, deep navy
typography, bright coral/blue/green/purple rounded cards, generous whitespace,
crisp flat icons, accessible high contrast, and the same friendly modern style
as the project README diagrams.

Use only the supplied locale text. Do not add vendors, models, dates, rankings,
prices, benchmark numbers, source labels, watermarks, or decorative prose.
Do not mix languages. Keep every arrow in whitespace and prevent text, icons,
arrows, and borders from overlapping.
```

## 圖 A：從失敗證據選一個最小做法

檔案：

- `advanced-agentic-decision-map.png`
- `advanced-agentic-decision-map.en.png`
- `advanced-agentic-decision-map.zh-Hans.png`

固定版面：上方一張「已重現的失敗」卡，中間四張平行概念卡，底部五個較小的
候選模式。四張卡彼此沒有先後箭頭；底部固定提醒「預設先不加，一次只試一個」。

四張平行概念卡依序為：

1. `Evaluator–Optimizer／Agent-as-Judge`：另一個檢查者照規則挑錯。
2. `Failure Injection／Chaos Eval`：故意弄壞一小塊，測停止與復原。
3. `Autonomy Gradients／Trust Layers`：風險越高，自主權越小。
4. `Model–Harness Fit`：用同一組 Eval 決定 Keep／Simplify／Remove。

底部候選模式順序固定為 `Parallel Exploration`、`Hierarchical Delegation`、
`Multi-Agent Handoff`、`Plan–Act–Reflect`、`Dynamic Workflows`。正式英文術語在三語
版本中都保留，不翻成另外一個新名詞。

## 圖 B：Model–Harness Fit

檔案：

- `model-harness-fit.png`
- `model-harness-fit.en.png`
- `model-harness-fit.zh-Hans.png`

固定版面：第一列只有三步，從「選一個 Harness 元件」到「做刪除或簡化測試」，
再到「重跑同一組品質、安全、成本與延遲 Eval」。第二列是三張等大的平行結果卡：

- `KEEP`：拿掉後，可重現的失敗回來。
- `SIMPLIFY`：保護仍有用，但更少步驟就足夠。
- `REMOVE`：品質與安全未退步，成本或延遲相同或更好。

三個判斷是平行結果，不是成熟度階梯，彼此之間不得畫箭頭。底部責任列固定保留
permission、sandbox、audit log、人工核准與 rollback，明確說模型變強不會讓安全邊界
自動過時。

## 驗收清單

- 六張圖都必須是 `1672×941` PNG，bytes 與 hash 各自不同。
- 三語卡片數、位置、icon、顏色、箭頭與閱讀順序相同。
- 繁中不混簡中；英文不混 CJK；簡中不殘留繁體字。
- 圖 A 恰好四張平行概念卡與五個候選模式；圖 B 恰好三步與三個平行結果。
- 正文先解釋名詞，再引用圖；每個語言只引用自己的 locale 圖檔。
- 不放 model ID、版本、價格、stars、benchmark 或 provider 排名。
- 執行 `python scripts/check-image-locale.py`、`python scripts/check-image-delivery.py`
  與 `python -m pytest scripts/test_stage075_content.py -q`。
