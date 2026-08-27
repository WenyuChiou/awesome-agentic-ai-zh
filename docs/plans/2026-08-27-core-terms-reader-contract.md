# 全站核心詞閱讀契約與 Gate 計畫

## 目的

這份學習地圖不能靠讀者猜名詞。從這一層開始，每個完成回溯的章節都要在第一個練習前，放一個預設可見的核心詞區。核心詞第一次出現在可見教學文字時要用粗體，接著用白話解釋，再保留正確技術名稱。

本層只建立規範、設定格式與機器 gate，不順手改寫 Stage 1 或 Stage 2。兩章會各用下一個 stacked PR 加入自己的核心詞，這樣任何一層都能單獨檢查或回退。

## 讀者看到的形狀

每個完成回溯的 Stage／Track 頁面都要依序出現：

1. 這章要解決的問題。
2. `📌` 學習目標。
3. 可見的核心詞區。
4. 第一個可直接複製、貼上或執行的練習。

每個核心詞至少回答四件事：

- **它是什麼**：一句白話定義。
- **它像什麼**：一個不會扭曲概念的生活比喻。
- **這章用它做什麼**：把名詞接回後面的練習。
- **正確術語是什麼**：保留英文名、縮寫或規格名稱，讓讀者之後查得到。

若完整原理很長，可以把更深的補充放進 `<details>`；核心詞名稱與上述最短解釋不得收合。

## Gate 設定

一個完成回溯的頁面在 `scripts/reader-ux-pages.yml` 加入：

```yaml
core_terms:
  section_id: core-terms
  first_exercise_section_id: exercise-1
  min_definition_chars: 20
  terms:
    - id: token
      zh-TW: {term: Token, label: Token（詞元）}
      en: {term: Token, label: Token}
      zh-Hans: {term: Token, label: Token（词元）}
```

`section_id` 與 `first_exercise_section_id` 必須指向同頁既有的 `required_visible_sections`。`id` 決定三語的概念與順序；`term` 是檢查第一次可見用法的精確技術詞；`label` 是核心詞區裡必須出現的粗體定義標籤。

## 阻擋條件

Gate 會阻擋：

- 核心詞區或第一個練習不在可見主線。
- 核心詞區排在第一個練習之後。
- 核心詞區缺少自己的定義，卻借用下一個同級／更高級 section 的標籤或文字補足。
- 技術詞第一次出現在可見教學文字時沒有粗體。
- 核心詞區缺少設定的粗體標籤，或三語詞序不同。
- 標籤後沒有最低限度的解釋文字。
- `id`、locale、term／label 或 section reference 不完整或重複。

機器只能檢查結構，不能判斷比喻是否正確。人工 review 仍要確認四個問題都有回答，而且沒有把每個普通名詞都硬塞成核心詞。

## 首兩個 rollout

1. Stage 1：保留 Token、Context Window、Temperature；統一首次粗體與三語標籤，不改模型事實表。
2. Stage 2：獨立解釋 Prompt、Instruction、Input Data、Example、Eval、Zero-Shot、One-Shot、Few-Shot、Chain-of-Thought；Prompt 定義為送入模型的一組訊息與材料，可包含指令、脈絡／資料、範例與輸出限制，不縮成「一句問題」。

後續每個 phase 的回溯 PR 都要先列出自己的核心詞清單，經人工確認後再加入 gate。

## Stack 與發布規則

- Stack base：`codex/stage00-retro-ux`（PR #143）。
- 本層 branch：`codex/core-terms-reader-contract`。
- 下一層依序為 Stage 1、Stage 2 的核心詞回補。
- 所有 upstream branch、worktree 與 PR 保留。
- 未得到使用者明確「可以合併」前，不 merge、不刪分支、不清 worktree、不 prune。

## 驗收

- 新增正向測試：可見、粗體、依設定順序且有解釋時通過。
- 新增負向測試：首次未粗體、順序交換、解釋過短、核心詞晚於第一個練習都失敗。
- 現有 reader-UX 頁面在尚未 enrollment 前維持通過。
- `git diff --check`、reader-UX unit tests、正式 reader-UX gate 與 MkDocs build 通過。
- 最終 staged diff 交獨立 `code-reviewer`；任何 review 後修改都使 ack 失效。
- PR 只開啟供使用者檢查，不合併。
