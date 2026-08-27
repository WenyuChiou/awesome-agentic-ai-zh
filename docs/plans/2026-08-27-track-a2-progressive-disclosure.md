# Track A2 漸進式重整與事實更新計畫

## 目標

讓第一次接觸 CLI agent 的讀者，先看懂三件事：

1. **專案規則**像貼在工作室牆上的共同守則，每次進來都要看。
2. **Skill**像放在工具箱裡的操作卡，需要做那件事時才拿出來。
3. **單次 prompt**像今天臨時交代的一句話，用完不必留下。

讀者不展開任何選單，也能完成 CLI-5、CLI-6，知道自己是否可以進 A3。技術名稱、檔名、命令與安全限制保持精確；白話說明要讓沒有軟體背景的人一次讀懂。

## 現況診斷

查核日：**2026-08-27 UTC**。

| 項目 | 繁中 | 英文 | 簡中 | 問題 |
|---|---:|---:|---:|---|
| 未收合非空白字元 | 5,295 | 8,086 | 5,505 | 第一遍閱讀負擔過高 |
| `<details>` | 0 | 0 | 0 | 時間、閱讀、資源與進階練習全部攤開 |
| 資源列 | 7 | 7 | 7 | 分類欄以空白代替真正合併，另有 2 個工具散在表外 |
| 練習 | CLI-5 至 CLI-8 | CLI-5 至 CLI-8 | CLI-5 至 CLI-8 | 沒有顯式 anchor；舊 slash command 仍是主教學 |

已確認的內容缺陷：

- `CLAUDE.md` 的 30–50、50、100 行門檻不是跨工具的官方規則。Anthropic 目前只對自己的 `CLAUDE.md` 建議每份低於 200 行；Codex `AGENTS.md` 使用的是可設定的 byte 上限，不能混成同一條規則。
- Claude Code 已把 custom commands 併入 Skills；`.claude/commands/` 仍相容，但新手主線應改用 `.claude/skills/<name>/SKILL.md`。
- Codex、Claude Code、Gemini CLI、OpenCode 都支援 Skill，但原生搜尋位置與額外 frontmatter 不完全相同。只能說「核心 `SKILL.md` 內容可共用」，不能說整個資料夾可原封不動跨所有工具。
- OpenCode V2 目前只把 `AGENTS.md` 當作 project instructions；舊版 `CLAUDE.md` fallback 說明不能寫成所有版本都成立。
- 現有「同一 prompt 在每個 CLI 都能通」說法太強。檔名、權限、sandbox、tool 名稱與啟用方式都可能不同。
- 英文的 self-check 有語法錯誤；三語大量中英混排，且 A3 的進入條件仍要求舊 slash command。
- stars、五顆星評分與「90% 都通」「必備 daily driver」屬於易變或主觀資訊，移除。

## 章節形狀

### 不展開時看見

1. 一句話目標：讓 CLI agent 每次進 repo 都先讀到同一套規則，重複工作則放進 Skill。
2. 三個核心詞的「白話說法／正確術語／何時使用」短表。
3. 三個學習目標。
4. CLI-5 的標題、成果與最小規則卡。
5. CLI-6 的標題、成果與最小 review Skill。
6. CLI-7、CLI-8 的標題、固定 anchor 與一句話成果。
7. 短版成功檢查與 A3 入口。

目標：三語各自的未收合正文控制在目前約一半以下；不以硬字數代替人工可讀性檢查。

### 預設收合

- 時間、先備條件、環境與費用。
- 必修閱讀與建議順序。
- 四個 CLI 的 project-instructions／Skill 位置對照。
- CLI-5、CLI-6 的完整步驟與驗證方法。
- CLI-7 任務拆解與 CLI-8 portable prompt 的詳細步驟。
- Claude Code legacy `.claude/commands/` 相容說明。
- multi-agent 延伸、替代工具、疑難排解與完整資源表。

所有 `<details>` 預設關閉，不使用 `open`。練習標題、anchor、成果與最低完成條件留在外面。

## 練習設計

### CLI-5：做一張最小專案規則卡

讀者只放四類內容：

- 這個專案做什麼。
- 哪些事情不能做。
- 用哪一條命令驗證成果。
- 完成時要回報什麼。

不再要求「角色扮演」，也不預設一定要 commit。讀者先用自己的主工具原生檔名；完整對照表放在收合區。

### CLI-6：把重複檢查做成 Skill

主線使用 `SKILL.md`，做一個只讀的 `review-changes` Skill：讀取目前 diff、列出風險、回報 `PASS` 或具體問題，不自動 commit、push 或部署。

範例只使用各家共同的最小 frontmatter：`name`、`description`。工具專屬欄位放在補充說明，避免製造「全部通用」的錯覺。

### CLI-7：把大任務切成看得見的小步驟

保留標題、anchor 與一句話成果；完整比較流程收合。例子縮小為可復原的文件任務，不要求一次翻譯 50 個檔案。

### CLI-8：分開共用內容與工具差異

讓讀者把需求、範圍、成功條件寫成共用核心，再另外記錄檔名、權限、sandbox、命令等工具差異。不承諾零修改搬家。

## 表格規則

- Markdown 表格若同一分類跨多列，不用空白儲存格假裝合併；改用 HTML `<table>` 與真正的 `rowspan`。
- 第一遍只顯示「專案規則／Skill／單次 prompt」三列短表，不把完整工具矩陣放在主線。
- 完整資源表預設收合，欄位固定為：`類型｜資源｜先看什麼｜適合何時使用｜官方／repo 來源`。
- 分組固定為：官方專案規則（4）、官方 Skill 文件（4）、標準與可讀範例（4）、索引與 prompt 練習（2）、repo-context 工具（2）。三語 rowgroup 數量、順序與 URL 完全一致。已搬家的 `f/awesome-chatgpt-prompts` 不留在 A2，改用未封存的 Anthropic 官方互動式 prompt 教學。
- 不顯示 stars、主觀星等、排行榜或會自然過期的數字。

## 官方事實基線

執行前與 staging 前各重查一次：

- [Codex：`AGENTS.md`](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Codex／ChatGPT：Build skills](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code：`CLAUDE.md`](https://code.claude.com/docs/en/memory)
- [Claude Code：Skills 與 legacy commands](https://code.claude.com/docs/en/slash-commands)
- [Gemini CLI：`GEMINI.md`](https://geminicli.com/docs/cli/gemini-md/)
- [Gemini CLI：Agent Skills](https://geminicli.com/docs/cli/using-agent-skills/)
- [OpenCode V2：Instructions](https://opencode.ai/v2/docs/instructions)
- [OpenCode V2：Agent Skills](https://opencode.ai/v2/docs/skills)
- [Agent Skills 開放標準](https://agentskills.io/specification)

若 V1／V2 或不同產品文件衝突，正文只教目前正式版本；舊版行為放入清楚標示的相容說明，不混寫成一般規則。

## 直接一致性範圍

本層預計修改：

- A2 三語正文。
- A3 三語的進入條件與直接接續步驟：由 legacy slash command 改為 CLI-5 規則卡、CLI-6 Skill，以及 plugin-root 的 `skills/<name>/SKILL.md`。
- README 三語的 A2 摘要：改成 project instructions、Skill、任務拆解。
- Glossary 三語與 `docs/TESTING_PLAN.md` 的直接相依敘述：舊 `.claude/commands/` 只標成相容路徑，新範例使用 Skill。
- Track A 設計計畫與必要的 reader-UX 結構斷言。
- 最終 diff 對應的 CHANGELOG。

不在本層改寫 Stage 05、Stage 07.5、cookbook 或 glossary 的長篇內容；只修會讓 A2 讀者立刻走回舊格式的直接相依句子。其餘盤點到的過期行數規則與 Skill 說明會登記給各自章節處理，避免 A2 PR 失控。

## 驗收

### 機器檢查

- `git diff --check`
- strict anchors、anchor slug parity、mirror parity、locale links。
- zh-Hans 字元、image locale、duplicate repositories。
- freshness gate 與既有單元測試。
- `python scripts/build-docs-tree.py`
- `python -m mkdocs build`
- 新增 A2 結構斷言：三語 details 數量一致且全關閉；CLI-5 至 CLI-8 anchor 可見；資源表 16 筆、5 個 rowgroup、`rowspan` 總和 16；三語 URL／命令／數字一致；不得出現舊的 30–50／50／100 行硬門檻。

### 人工檢查

- 不展開任何選單，讀者能說出 project instructions、Skill、單次 prompt 的差別。
- 不展開也能開始 CLI-5，並知道 CLI-6 的成果長什麼樣。
- 每段先說「要做什麼」，再補「為什麼」；一句只交代一件事。
- 技術詞第一次出現時有白話說法，但命令、檔名與安全邊界不模糊。
- 同類表格欄位真正合併；沒有重複分類、空白分類格或散落在表外的同類清單。
- 四家工具的規則檔、Skill 路徑與相容限制有官方來源，三語沒有講成不同的事。
- A3、glossary 與測試計畫不會把讀者帶回 legacy `.claude/commands/`；新流程統一使用 Skill，plugin 只打包 plugin-root 內的 `skills/<name>/SKILL.md`。

## Git 與發佈

- A2 保持單獨、可回退的 stacked layer：`codex/track-a2-reader-ux`。
- 只逐檔 stage；凍結清單與 staged 檔數必須一致。
- 穩定 staged diff 執行一次獨立 `code-reviewer`；任何修改使 ack 失效。
- 所有 checks 全綠才安全合併；零 checks、PENDING、空狀態或失敗都停止。
- Claude 若同時改到相同檔案，先重新整合最新 main，不覆蓋對方內容，並重跑全部相關 gate。
