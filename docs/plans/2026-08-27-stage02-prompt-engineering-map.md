# Stage 02 Prompt Engineering 概念圖計畫

## 目的

用一張五歲程度也能循序看懂的圖，整理 Stage 02 已經在正文定義的關係。圖片不能取代核心詞，也不能把已撤掉的錯誤規則重新畫回教材。

## Stacked PR 邊界

- branch：`codex/stage02-prompt-map`
- base：`codex/stage02-core-definitions`（PR #146）
- 不修改 Stage 03、範例程式、模型 freshness 或其他章節
- 未獲使用者明確同意，不 merge、不清理 branch／worktree

## 固定位置與閱讀順序

圖放在三語 Stage 02 的核心詞與一句口訣之後、進入條件之前。讀者先從正文認識 Prompt、Eval、Zero-Shot、One-Shot、Few-Shot 與 Chain-of-Thought，再用圖複習：

1. 目標／資料／規則／輸出組成 Prompt。
2. 可以不給、給一個、或給多個範例。
3. 用固定題目 Eval，修改一處，再試一次。
4. CoT 是把工作拆成可檢查步驟，不是要求模型公開完整內部想法。

## 三語與圖像規格

- `resources/diagrams/prompt-engineering-map.png`
- `resources/diagrams/prompt-engineering-map.en.png`
- `resources/diagrams/prompt-engineering-map.zh-Hans.png`
- 16:9、亮色、白底、清楚卡片與箭頭；三語構圖與語意一致
- Few-shot 不使用 `2–5` 等沒有官方通則的固定數字
- 每個頁面使用自己的語系圖檔與在地化 alt text

## Reader UX ratchet

加入完整圖片 alt text 與一句操作圖說後，三語未展開實測為 `3,320／6,659／3,386` 個非空白字元。新上限只保留 50 字餘量：`3,370／6,709／3,436`。這是刻意新增的可見教學與無障礙文字，不以刪掉必要說明來維持舊門檻。

## 驗收

- 原尺寸人工檢查三張圖的文字、繁簡字形、箭頭、對比與固定數字
- `git diff --check`
- reader UX、strict anchors、slug parity、mirror parity、locale links、image locale
- `python scripts/build-docs-tree.py`
- `python -m mkdocs build`
- 對最終 staged fingerprint 執行一次獨立 `code-reviewer`
