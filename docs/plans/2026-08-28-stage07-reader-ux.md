# Stage 07 三語閱讀體驗與現行資訊計畫

- 日期：2026-08-28 UTC
- Branch：`codex/stage07-reader-ux`
- 基底：`codex/stage06-reader-ux`

## 目標

讓第一次接觸 production Agent 的讀者，不展開任何選單也能：

1. 先判斷是否真的需要 Multi-Agent。
2. 說清七個核心詞。
3. 看懂 Prompt／Context／Harness／Loop／Graph 的分工。
4. 用 Harness 八項檢查表找出缺口。
5. 直接跑五個現有練習的離線測試。
6. 不被靜態排行榜、GitHub stars 或工具名稱混淆。

敘述採「先白話、再保留正確術語」，但不刪掉 Handoff、Eval、
Observability、Guardrail、Idempotency、Reward hacking 等必要概念。

## 可見主線

1. 單一 Agent／Multi-Agent 選擇。
2. `📌` 五個學習目標。
3. 七個粗體核心詞。
4. `🚪` 最短進入條件。
5. `📚` 三份必讀入口。
6. 五層工程分工與亮色三語圖。
7. Harness 八項 production 檢查。
8. OpenRouter／Pi／OpenCode／Orca／QM 角色辨識。
9. 五題 heading、成果與第一個 `python test.py`。
10. execution receipt 小專案。
11. Benchmark／Reward hacking 閱讀紀律。
12. `🎯` 精選資源與 `✅` 自我檢查。

## 預設收合

- 時間、環境、費用與敏感資料提醒。
- 完整閱讀順序。
- Loop／Graph／Multi-Agent 的選擇細節。
- 回饋、復原、冪等、成本與 tracing 細節。
- 五題的付費路徑與觀察步驟。
- Benchmark 連結。
- 20 筆完整資源表。

所有 `<details markdown="1">` 預設關閉。既有五層、Harness 八元件、
五題練習、Benchmark 警告與 Projects 深連結保持可見。

## 事實與來源

優先採供應商正式文件與 canonical repo：

- OpenAI Agents SDK：manager／handoff orchestration、tracing、testing utilities。
- Anthropic：Building Effective Agents、evaluation、prompt caching。
- Microsoft Agent Framework：sequential、concurrent、handoff、group chat、human approval。
- OpenTelemetry：獨立 GenAI semantic-conventions repo；規格仍在演進。
- GitHub canonical owner：Terminal-Bench／Harbor、Pi、OpenCode、Orca、QM、
  LangGraph、crewAI、promptfoo、OpenTelemetry GenAI、Langfuse、Phoenix、Opik、
  Claude Agent SDK、DeepSeek Harness、Grok Build、NemoClaw、BentoML、
  LongHorizon-Harness、Edict。

不保留固定 SOTA 分數、模型名次、GitHub star 數或「prompt caching 一定省 90%」。
Preview、Alpha、best-effort、新專案與已封存狀態放在限制欄。

## 舊元素落腳

| 舊內容 | 新位置／處理理由 |
|---|---|
| 「真的需要 Multi-Agent 嗎？」 | 移到頁首選擇表，先做決策再學工具。 |
| 回饋迴路、復原、冪等與成本 | 合併進 Harness 八元件後的收合實作重點。 |
| 參考實作與常用工具推薦 | 依用途合併進 20 筆資源表；OpenRouter／Pi／OpenCode／Orca／QM 另有可見角色表。 |
| Exercise 6：Cost Optimization | 舊頁只有標題、沒有第六個範例資料夾；成本量測保留在 Harness 細節與 Exercise 4，不再假裝有可執行第六題。 |
| 固定 SOTA 分數表 | 刪除易過期數字；Benchmark 名稱放進收合入口，Task／Environment／Grader／Trajectory／Hold-out 五個判讀問題保持可見。 |
| 「接下來」 | 合併到短版自我檢查後的 Stage 7.5／8 入口。 |

外部實際引用的五層、Harness、八元件、Benchmark 警告與 Projects heading
維持原本可解析的文字與 anchor；strict anchor gate 逐一驗證。

## 資源表

20 筆、四組：

- Orchestration／Workflow：4。
- Eval／Observability：6。
- Harness／Sandbox／Deploy：5。
- Multi-Agent 案例：5。

每組一個 `<tbody>`；分類使用
`<th scope="rowgroup" rowspan="N">`，欄位使用 `scope="col"`。
三語 URL、順序、五星編輯評分與限制一致。

## 圖

保留既有檔名以保護引用：

- `agent-engineering-5layer.{png,en.png,zh-Hans.png}`
- `inside-a-graph.{png,en.png,zh-Hans.png}`

六張圖由暗色霓虹改為暖白底、亮色卡片與深藍文字。繁中、英語、簡中分開產出；
mirror 頁不得再引用繁中 base 圖。圖只整理正文已定義的關係，不加入模型、
版本、價格、排行榜或時間估算。

## Stacked 邊界

本層只處理三語教材、規範、freshness／reader-UX gate、圖與內容測試。

下一層 `stage07-example-hardening` 才處理五個 `examples/stage-7/`：

- `qwen2.5:3b` 等模型與 SDK 更新。
- 直接 copy／run／change-one-thing 教學。
- Ollama／Anthropic 雙路徑。
- 固定價格／延遲敘述。
- 離線 behavior tests 與安全邊界。

未經使用者明確同意，不合併 PR、不刪遠端 branch、不清理 worktree。

## 驗收

- `python scripts/check-reader-ux.py`
- `python -m pytest scripts/test_stage07_content.py -q`
- strict anchors、anchor slug parity、locale links。
- mirror parity、Hans 字元、image locale。
- freshness gate 與相關單元測試。
- `python scripts/build-docs-tree.py`
- `python -m mkdocs build`
- `git diff --check`

目前鎖定：

- 三語可見字元：`5,770／9,925／5,863`。
- 七個預設關閉 details。
- 五個真實練習；沒有虛構 Exercise 6。
- 20 筆資源、四個 rowgroup，rowspan 合計 20。
- 六張不同的三語亮色 PNG。
