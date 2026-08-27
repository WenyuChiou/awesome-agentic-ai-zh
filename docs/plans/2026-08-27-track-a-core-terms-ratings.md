# Track A（A1–A3）核心詞、評分與初學者路徑計畫

日期：2026-08-27 UTC
狀態：三語內容已完成；首次獨立 review 的修正已落地，待重跑 gate、重新 review、commit 與 stacked PR

## 這一層要修什麼

2026-08-27 的 A1–A3 重寫已把安全主線與漸進式揭露做好，但也造成四個回歸：

1. `📌`、`📚`、`🛠`、`🎯`、`✅` 路標消失。
2. 原有的五星編輯評分被連同易變的 GitHub stars 一起移除。
3. A1、A2 的核心詞只出現在表格標頭，沒有依全站契約粗體並完整解釋。
4. A3 第一題沒有可直接複製的建立 demo 資料夾指令。

本層只修 Track A 與直接相關的 CLI 指南、glossary、設計規則和 reader-UX gate。Stage 03 另開下一個 stacked PR。

## 初學者主線

每頁不展開任何選單時，讀者都要看見：這一頁解決什麼、學習目標、核心詞、第一個可複製動作、練習成果、精選資源入口與完成檢查。

- **A1**：分清工具身分，選一個 coding agent，在 demo repo 完成可復原的小改動。
- **A2**：分清長期規則、按需 Skill 與單次 prompt，把重複 review 做成可重跑流程。
- **A3**：分清 MCP、CI 與 observability，把一個只讀檢查接到 demo PR。

時間、費用、完整步驟、工具差異、疑難排解與長資源表維持預設收合。既有 CLI-1 至 CLI-12 與 Playbook 4 的標題、anchor 和一句話成果不得移入 `<details>`。

## 核心詞契約

三語使用相同 ID、順序、用途與限制。每個詞第一次出現在可見正文時必須粗體，並在第一個練習前回答「它是什麼、像什麼、本章怎麼用、不是什麼」。

| 頁面 | 核心詞 |
|---|---|
| A1 | LLM、Provider API、Router、Coding agent、Local runtime |
| A2 | Project instructions、Skill、One-off prompt |
| A3 | MCP、CI、Observability |

Glossary 同步補齊 Project instructions、One-off prompt、CI，並把 Skills 的定義從 Claude Code 專屬描述改成跨工具的 `SKILL.md` 行為包；各工具的路徑與權限仍分開說。

## 資源表與五星評分

評分是本學習地圖的編輯建議，不是 GitHub stars 或人氣排名。移除會變動的 `★ 140k+` 之類數字時，不得順手刪除 `⭐⭐⭐⭐⭐` 編輯評分。

- `⭐⭐⭐⭐⭐`：選擇該工具路徑時必讀／必做；不是要求安裝所有五星工具。
- `⭐⭐⭐⭐`：強烈建議優先看。
- `⭐⭐⭐`：完成主線後再比較。
- `⭐⭐`：歷史或少數情境參考。

資源表固定為：

| 頁面 | 筆數 | 分組 `rowspan` | 評分處理 |
|---|---:|---|---|
| A1 | 11 | `4／5／2` | 還原 8 個既有 CLI 與 Ollama 的原評分；Pi、OpenRouter依本章用途補分 |
| A2 | 16 | `4／4／4／2／2` | 原有資源沿用舊分；新官方文件依所選工具路徑標示 |
| A3 | 18 | `4／5／4／3／2` | 原有資源沿用舊分；新增官方安全文件依必要性標示 |

同類型只顯示一次分類欄，每組使用獨立 `<tbody>` 與真正的 `<th scope="rowgroup" rowspan="N">`。三語的 URL、順序、分組與評分完全一致。

## OpenRouter、OpenCode、Pi 與 Ollama

A1 是四者的主要辨識入口，`resources/cli-agents-guide.*` 保存完整比較：

- **OpenRouter** 是 Router：統一 API、帳務與 provider routing；它不讀寫 repo。
- **OpenCode V2** 是 coding agent／harness：它能在授權範圍內讀檔、改檔與執行命令，也能連 OpenRouter 或其他 provider。
- **Pi** 是可擴充的 local coding agent／harness：project trust 只控制專案資源載入，不是 sandbox；真正隔離要靠容器、VM 或 OS 邊界。
- **Ollama** 是 local runtime：它負責在本機跑模型，不會自己管理 repo 或命令權限。

官方查核發現一項現行錯誤：OpenCode V2 只探索 `AGENTS.md`；舊版文件的 `CLAUDE.md` fallback 不適用於 V2。A1、CLI 指南與 developer path 三語都要修正。

主要官方來源：

- [OpenCode V2 Instructions](https://opencode.ai/v2/docs/instructions)
- [OpenCode V2 Skills](https://opencode.ai/v2/docs/skills)
- [OpenRouter FAQ](https://openrouter.ai/docs/faq)
- [Pi Security](https://pi.dev/docs/latest/security)
- [Pi Providers](https://pi.dev/docs/latest/providers)
- [MCP local servers](https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers)
- [Codex GitHub Action](https://learn.chatgpt.com/docs/github-action)
- [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)

## 第一個可複製動作

- A1 把只讀請求改成 `text` code block，讀者可以直接複製給已安裝的 CLI。
- A2 保留完整可複製的最小 project-rules card 與 `SKILL.md`。
- A3 在 CLI-9 可見區同時提供 PowerShell 與 macOS／Linux 建立 `a3-mcp-demo/hello.txt` 的指令；設定差異仍放在收合區。

## 凍結檔案清單

最終 31 個檔案。三語複查發現原 gate 只檢查標題「存在」，沒有檢查可見主線的「順序」，因此在凍結清單中加入 reader-UX checker 與單元測試。Strict anchor gate 隨後證明它不認既有 `<a id="cli-*">` 穩定錨點，因此補上 HTML anchor 支援與 regression。首次獨立 review 再抓出 regex 會把 `data-id` 誤認成 `id`，也會錯把明示 ID slugify；現改用 HTML parser，只接受真正的 `id`／`name` 並以完全相同的 fragment 命中。Review 同時發現 OpenCode V2 舊 fallback 殘留在兩個 A1 鏡像、developer path 三語與先前計畫，因此把這四個直接相依檔案加入凍結清單。恢復 A1 資源列也改變 repo 引用來源，repository snapshot 必須由完整 GitHub API 掃描重建，不能手改引用數字：

- `tracks/cli/A1-cli-intro.*.md` 三語
- `tracks/cli/A2-cli-workflow.*.md` 三語
- `tracks/cli/A3-cli-production.*.md` 三語
- `resources/cli-agents-guide.*.md` 三語
- `resources/glossary.*.md` 三語
- `resources/style-guide.*.md` 三語
- `branches/for-developer.*.md` 三語
- `docs/plans/2026-08-27-track-a-progressive-disclosure.md`
- `scripts/check-anchors.py`
- `scripts/check-reader-ux.py`
- `scripts/reader-ux-pages.yml`
- `scripts/repository-freshness-snapshot.json`
- `scripts/test_check_anchors.py`
- `scripts/test_reader_ux.py`
- `stages/DESIGN.md`
- `CHANGELOG.md`
- 本計畫檔

不修改範例程式、Stage 03、README 或其他 branch 頁面。上述 developer path 三語只修正同一個 OpenCode 規則檔錯誤。本次新增檔案都由失敗 gate 或 reviewer 的直接證據觸發，已在重新 staging 前更新清單；後續若再修改凍結範圍，審查指紋必須作廢重跑。

## Gate 與驗收

`scripts/reader-ux-pages.yml` 新增三頁的 icon、核心詞、可見段落順序、資源分組與 URL→評分鏡像契約。`scripts/check-reader-ux.py` 會阻擋三語把同一批可見段落排成不同順序。A3 只禁止代表 GitHub star 數量的 `★`，不再禁止編輯評分用的 `⭐`。

至少執行：

- `git diff --check`
- `python scripts/check-reader-ux.py`
- `python -m pytest scripts/test_reader_ux.py -q`
- stage template、strict anchors、anchor slug parity、mirror parity、locale links
- zh-Hans 用語、OpenCC、image locale、duplicate repositories
- freshness gate 與相關單元測試
- `python scripts/build-docs-tree.py`
- `python -m mkdocs build`

人工確認三語均符合：核心 icon 存在；核心詞首次粗體且意思一致；不展開仍知道下一步；A1／A2／A3 的資源數量、分組、URL 與評分一致；CLI-1、CLI-5、CLI-9 的第一個動作可直接複製；OpenCode V2 不再沿用舊 fallback；沒有會自然變舊的 GitHub stars 數字。

## Stack 與發布

分支 `codex/track-a-reader-ux` 以 PR #146 的 commit `11a83b82` 為基底。完成後 PR base 指向 `codex/stage02-core-definitions`。不合併、不刪除遠端或本機分支；等使用者明確允許後才按 stack 順序處理。
