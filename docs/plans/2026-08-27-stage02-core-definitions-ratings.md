# Stage 02 核心定義、練習校正與資源評分計畫

> - 狀態：內容已實作並通過最終 staged-diff review
> - 查核日期：2026-08-27 UTC（GitHub API `Date`：2026-08-27 14:04:07 GMT）
> - 工作分支：`codex/stage02-core-definitions`
> - 堆疊基底：`codex/stage01-core-terms-retro`（PR #145）
> - 發布規則：建立獨立堆疊 PR；未經使用者明確同意，不合併、不刪分支、不清理 worktree。

## 這次要修什麼

Stage 02 已有簡短主線、三個練習與 18 筆資源，但目前有四個會讓初學者誤會的問題：

1. `Prompt` 沒有完整定義，讀者容易以為它只是一句問題。
2. `Instruction` 被寫成 `system / developer message`，把「信封裡的內容」與「信封的角色」混成同一件事。
3. 練習 1 稱為 `System Prompt`，程式卻把整份 prompt 放進 `user` message；標題與實作互相矛盾。
4. 術語表把 Few-shot 寫死成 2–5 個例子；官方文件只說少量／一小把例子，沒有通用固定數字。

此外，完整資源表缺少專案既有的五星推薦欄，讀者無法快速判斷先後順序。

## 讀者不展開選單時要看到的主線

1. 一句話說明本關目的，並立即定義 **Prompt（提示）**。
2. 保留 `📌` 學習目標。
3. 在第一個練習前，依固定順序看懂九個核心詞：
   - Prompt
   - Instruction
   - Input Data
   - Example
   - Eval
   - Zero-Shot
   - One-Shot
   - Few-Shot
   - Chain-of-Thought
4. 每個詞都提供：白話定義、生活比喻、本章用途、必要限制；正確術語第一次出現時加粗。
5. 另外用短 callout 分清 **Message Role（訊息角色）** 與 **Instruction（指令）**：角色是容器與優先順序，指令是容器裡的要求；各供應商的角色名稱不一定相同。
6. 保留 `📚`、`🛠`、三個練習、推薦小專案、`🎯`、`✅`。
7. 練習 1 改名為「Prompt 四格」，但保留舊 `System Prompt` HTML anchor，避免外部深連結失效。
8. 練習 3 改成可直接複製的結果紀錄，不要求讀者先抄一張空表。

時間、工具、閱讀清單細節、程式碼、補充練習、18 筆完整資源與進階分層維持預設收合；重要定義、第一步與完成條件不得藏起來。

## 事實包與衝突處理

本次以 2026-08-27 重新開啟的官方文件為準：

- [OpenAI Prompt Engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)：developer／user 是訊息角色與優先順序；few-shot 是 prompt 裡的一小把 input/output examples。
- [OpenAI Evals](https://developers.openai.com/api/docs/guides/evals)：eval 至少要有代表性測試資料與明確判分條件。
- [OpenAI Reasoning Best Practices](https://developers.openai.com/api/docs/guides/reasoning-best-practices)：推理模型宜先用簡短直接 prompt；要求 `think step by step` 可能無益甚至有害，先試 zero-shot，再按需要加 few-shot。
- [Anthropic Prompt Engineering Overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)：先定成功條件、可重複測試與第一版 prompt；不是每個失敗 eval 都該靠改 prompt 解決。
- [Anthropic Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)：模型特定的 thinking 建議不能當成所有模型的通則。
- [Google Prompt Design Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies)：清楚 instruction、zero/few-shot examples、固定格式與反覆測試。

若供應商建議互相不同，正文不宣稱「永遠要加例子」或「永遠不要加例子」；本章教讀者先定 eval，再用同一組題目比較。

## 18 筆資源的評分

評分代表本 Stage 的建議閱讀優先順序，不是 GitHub stars，也不是永久品質排名：

- `⭐⭐⭐⭐⭐`：不做會卡住本 Stage。
- `⭐⭐⭐⭐`：很適合本 Stage，建議優先。
- `⭐⭐⭐`：有特定需求再用。
- `⭐⭐`：歷史背景或只適合少數情境。

本表位於選修工具箱，因此不把任何一筆硬標成五星。三語固定為：

- 10 筆 `⭐⭐⭐⭐`：Anthropic tutorial、Anthropic courses、三家官方 prompting 文件、三家官方 cookbook、DAIR guide、promptfoo。
- 7 筆 `⭐⭐⭐`：Google Cloud generative-ai、PromptingGuide.ai、NirDiamant、李宏毅 2025 Fall、Promptflow、DSPy、Inspect AI。
- 1 筆 `⭐⭐`：已封存的 Microsoft Prompt Engine。
- 0 筆 `⭐⭐⭐⭐⭐`。

李宏毅資源保留並明標「2025 Fall 課程」，不把它包裝成最新模型文件；Microsoft Prompt Engine 保留在歷史區，不推薦新專案使用。

## 凍結檔案清單

預計正好九個檔案：

1. `stages/02-prompt-engineering.md`
2. `stages/02-prompt-engineering.en.md`
3. `stages/02-prompt-engineering.zh-Hans.md`
4. `resources/glossary.md`
5. `resources/glossary.en.md`
6. `resources/glossary.zh-Hans.md`
7. `scripts/reader-ux-pages.yml`
8. `docs/plans/2026-08-27-stage02-core-definitions-ratings.md`
9. `CHANGELOG.md`

不修改 Stage 03、README、範例程式、圖片或 freshness tooling；它們依既定章節順序另開 PR。

## 驗收與發布

1. 繁中先通過人工主軸、官方事實、Markdown、錨點與 reader-UX gate。
2. 英文與簡中依同一九詞順序、同一資源 URL、同一評分同步；主代理逐列複查。
3. 機器驗收至少包含：
   - `git diff --check`
   - reader-UX formal gate 與單元測試
   - Stage template、strict anchors、anchor slug parity、mirror parity、locale links
   - Hans 字元、image locale、duplicate repositories、freshness strict gate
   - `python scripts/build-docs-tree.py`
   - `python -m mkdocs build`
4. 結構斷言：九詞三語順序一致、全部在第一題之前且位於 `<details>` 外；18 URL 與 18 評分逐列一致；rowspan 固定 `5/4/4/4/1`；所有 `<details>` 預設關閉。
   - 最終未展開字元實測：繁中 `3,135`、英文 `6,282`、簡中 `3,189`；門檻只各留 50，為 `3,185／6,332／3,239`。
5. CHANGELOG 只依最終 diff 與 API UTC 日期撰寫。
6. 逐檔 stage，斷言正好九個檔案，記錄 staged fingerprint。
7. 最終穩定 diff 交獨立 `code-reviewer`；任何修改都使 ack 過期，必須重跑相關 gate 與 review。
8. 單一 commit 後推送並建立以 #145 為 base 的堆疊 PR。只建立，不合併。

## 候選版本驗證結果

- multi-locale acceptance preset：PASS；三語行數 `321／320／320`、H2 `9／9／9`、table `2／2／2`，禁止詞 0。
- reader-UX：7 頁 × 3 語 PASS；相關單元測試 `43／43`，合併執行的結構／鏡像／錨點／locale／Hans／freshness 測試 `155／155`。
- Stage template、strict anchors、mirror parity、locale links、image locale strict、duplicate repositories、OpenCC Hans residue、model freshness、site-anchor parity：全部 PASS。
- `python scripts/build-docs-tree.py` 與 `python -m mkdocs build`：退出碼 0；既有 MkDocs warning 保留，未由本層新增阻擋錯誤。
- 獨立 `code-reviewer`：APPROVE，無可執行 finding；review 後沒有再修改正文、規則、CHANGELOG 或翻譯內容。
