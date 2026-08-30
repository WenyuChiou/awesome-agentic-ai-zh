# 開發者延伸路線（For Developers）

> **繁體中文** | [简体中文](./for-developer.zh-Hans.md) | [English](./for-developer.en.md)

[← 回主路線](../README.md)

<!-- freshness: canonical=branches/for-developer.md; verified_on=2026-08-29; scope=coding-agents,tool-identity,permissions,sandboxing,project-status; max_age_days=90 -->

<a id="使用情境開發場景-ai-怎麼幫"></a>

## 📌 這條路幫你做什麼

AI 程式助手像一位會讀檔案、改程式、跑指令的隊友。它做得快，也可能做錯。這條路教你先把任務縮小，再看懂每個改動，最後由人決定要不要留下。

建議路線：`A1 → A2 → Stage 5 的 5.1–5.4 → A3`。可以從 [A1](../tracks/cli/A1-cli-intro.md)、[A2](../tracks/cli/A2-cli-workflow.md)、[Stage 5](../stages/05-claude-code-ecosystem.md) 和 [A3](../tracks/cli/A3-cli-production.md) 依序前進；[Stage 8](../stages/08-agent-interfaces.md) 建議完成，但不擋你先開始這條路。已走 Track B 的讀者，可以先讀 [Stage 7](../stages/07-multi-agent-production.md)。

## 🎯 學習目標

完成這一頁後，你可以：

1. 分清工具本身是什麼，以及你從哪個畫面或入口使用它。
2. 先限制檔案、指令與網路，再讓工具動手。
3. 用差異、測試、人工檢查與回復管理一次小改。
4. 分開檢查程式品質、代理行為與正式環境記錄。

<a id="coding-agents"></a>

## 🧩 八個核心詞

- **IDE／Surface（整合開發環境／操作介面）**：IDE 是寫程式的工作桌；Surface 是你操作工具的入口，例如 CLI、IDE、desktop 或 cloud。同一個工具可以有很多 Surface，所以「看起來像 IDE」不代表它只能在 IDE 裡工作。
- **Coding Agent／Harness（程式代理／代理執行框架）**：Coding Agent 會讀 code、使用工具、修改檔案並依結果繼續。Harness 是把模型、工具、規則與執行循環接在一起的外殼。兩者常放在同一產品裡，但不是同一個意思。
- **Provider／Router（供應商／路由器）**：Provider 提供模型服務；Router 把請求送到一個或多個 Provider。Router 不是模型，也不會替你管理 repo 權限。
- **Model／Runtime（模型／執行環境）**：Model 產生下一步內容；Runtime 讓模型在本機或服務中執行。本機 Runtime 不等於會改程式的代理。
- **Sandbox（沙箱）**：把程式關在有限範圍裡，像只讓小孩在安全遊戲區活動。它能縮小出錯範圍，但不是百分之百保證。
- **Approval（人工批准）**：高風險動作前，由人清楚說可以。Test 通過不代表工具自動取得 push、merge 或 deploy 權限。
- **Diff／Rollback（差異／回復）**：Diff 告訴你改了什麼；Rollback 只退回不想要的那次改動。先看 Diff，才知道 Rollback 應該碰哪些檔案。
- **Eval／Observability（評測／可觀察性）**：Eval 用固定案例測品質；Observability 保存執行中的 trace、log、成本與錯誤。前者像考試，後者像行車記錄器。

### OpenCode、Pi、OpenRouter、Ollama 差在哪裡？

| 名稱 | 核心身分 | 白話說法 |
|---|---|---|
| OpenCode | Coding Agent／Harness | 會在程式專案裡讀、改、測 |
| Pi | Coding Agent／Harness | 從小核心加 extensions、skills 或 RPC |
| OpenRouter | API Router | 把模型請求送到 Provider；不會替你改 repo |
| Ollama | Local Model Runtime | 在本機提供模型執行與 API；本身不是 Coding Agent |

記法很簡單：**OpenCode／Pi 負責做事，OpenRouter 負責帶路，Ollama 負責讓本機模型跑起來。**

<a id="code-review"></a>

## 🛠 第一個練習：完成一次可回復的小改

請在可丟棄的 demo repo 或新 branch 操作。直接把下面這段貼給 Coding Agent：

```text
先做 read-only plan，不要修改任何檔案。

任務：找出 README.md 裡一個可以說得更清楚、但不改變技術意思的句子。
請先回報：
1. 你要改哪一句。
2. 為什麼這是小範圍改動。
3. 我應該執行哪個 test 或文件檢查。
4. rollback 方法。

在我明確人工批准前，不要寫檔。批准後只准修改 README.md。
完成後顯示 git diff -- README.md，並回報 test 結果。
不要 push、merge 或 deploy。
```

收到 plan 後，由 Human／人工讀完再批准。修改完成後，自己執行：

```powershell
git diff -- README.md
# 接著執行這個 repo 的文件 test 或最小相關 test
```

如果改動不是你要的，先看 `git status`，確認 `README.md` 沒有別人的工作，再只 Rollback 這次練習產生的改動。不要用會清掉整個工作區的指令。

<a id="推薦工具"></a>
<a id="tier-升級路徑"></a>

## 📚 先選一個入口

| 你現在想做的事 | 先看什麼 | 為什麼 |
|---|---|---|
| 學完整的 permission 與 sandbox 流程 | [Claude Code](https://code.claude.com/docs/en/overview) | 文件把權限、隔離與多種 Surface 分開說清楚 |
| 使用 app、CLI、IDE 或 cloud 工作 | [OpenAI Codex](https://github.com/openai/codex) | 同一個 Coding Agent 可以在多個入口工作 |
| 把 GitHub issue 交給 cloud agent | [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent) | 可以看懂 cloud agent 與 IDE agent mode 的差別 |
| 使用開源、可換 Provider 的工具 | [OpenCode](https://github.com/anomalyco/opencode) | 適合把 Coding Agent、Provider 與 Router 分開理解 |
| 從 IDE 開始並逐步批准 | [Cline](https://github.com/cline/cline) | 可以練習逐步批准工具、檔案與 browser 操作 |

不要只問「哪個最強」。先問：它能看到哪些檔案、能跑哪些命令、是否能連網、誰批准高風險動作，以及失敗時怎麼回復。

## 📖 必修閱讀

按順序讀，每篇只要先回答一個問題：

1. [Claude Code permissions](https://code.claude.com/docs/en/permissions)：`allow`、`ask`、`deny` 各代表什麼？
2. [OpenAI Codex agent approvals & security](https://learn.chatgpt.com/docs/agent-approvals-security)：Sandbox、Approval 與網路控制怎麼一起工作？
3. [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent)：Cloud agent 和 IDE agent mode 在哪裡執行？
4. [Pi — Permissions & Containerization](https://github.com/earendil-works/pi#permissions--containerization)：沒有內建 permission sandbox 時，責任落在哪裡？
5. [OpenRouter provider selection](https://openrouter.ai/docs/guides/routing/provider-selection)：Router 如何選 Provider？
6. [Ollama docs](https://docs.ollama.com/)：Local Model Runtime 提供什麼，又沒有提供什麼？

<a id="精選-projects"></a>
<a id="社群備註"></a>

## ⭐ 精選工具與專案

<small>工具身分、Surface、授權與 repository 狀態於 2026-08-29 UTC 依官方文件與 GitHub API 查核。推薦度是本學習地圖的編輯評分，不是 GitHub stars 或效能排名。</small>

<table>
<thead><tr><th scope="col">分類</th><th scope="col">官方工具／專案</th><th scope="col">核心身分</th><th scope="col">主要 Surface</th><th scope="col">適合做什麼</th><th scope="col">狀態、授權與限制</th><th scope="col">推薦度</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">官方／商業 Coding Agents</th><td><a href="https://code.claude.com/docs/en/overview">Claude Code</a></td><td>coding agent</td><td>CLI／IDE／desktop／cloud</td><td>學 permission、sandbox、project rules 與完整 workflow</td><td>商業；permission prompt 要保留，先從小 repo 開始</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/openai/codex">openai/codex</a></td><td>coding agent</td><td>app／CLI／IDE／cloud</td><td>比較同一代理在本機與遠端的不同工作方式</td><td>活躍；repo 程式碼為 Apache-2.0，app／cloud 依服務條款；不要關掉必要 Approval 或放大 workspace 權限</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent">GitHub Copilot</a></td><td>coding agent／code assistant</td><td>GitHub／IDE／CLI／app</td><td>從 IDE 協作走到 issue、branch 與 PR</td><td>商業；Cloud agent 與 IDE mode 權限不同，產出仍需人工 review</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://cursor.com/docs">Cursor</a></td><td>coding agent + AI editor</td><td>IDE／CLI／cloud／SDK</td><td>比較 editor、background agent 與其他 Surface</td><td>商業；每個 Surface 的權限與資料邊界要分開確認</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="6">開源 Coding Agents／Harnesses</th><td><a href="https://github.com/anomalyco/opencode">anomalyco/opencode</a></td><td>coding agent／harness</td><td>terminal／desktop</td><td>切換 Provider 或相容 endpoint</td><td>活躍；MIT；<code>AGENTS.md</code> 優先，缺少時才用 <code>CLAUDE.md</code></td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/earendil-works/pi">earendil-works/pi</a></td><td>coding agent／harness</td><td>terminal／SDK／RPC</td><td>從小核心加 extensions、skills 與自訂流程</td><td>活躍；MIT；沒有內建 sandbox，要自行隔離</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/Aider-AI/aider">Aider-AI/aider</a></td><td>coding agent／pair programmer</td><td>CLI</td><td>用 Git diff、commit 與 undo 管理小改</td><td>活躍；Apache-2.0；auto-commit 不代表可以跳過 hook</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/aaif-goose/goose">aaif-goose/goose</a></td><td>coding／general agent</td><td>CLI／desktop／API</td><td>連接 Providers、MCP 與 extensions</td><td>活躍；Apache-2.0；先從低權限 extension 開始</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/cline/cline">cline/cline</a></td><td>coding agent</td><td>IDE／CLI／SDK</td><td>逐步批准工具、檔案與 browser 操作</td><td>活躍；Apache-2.0；IDE Surface 本身不是安全保證</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/OpenHands/OpenHands">OpenHands/OpenHands</a></td><td>software-development agent platform</td><td>web／CLI／SDK／cloud</td><td>在隔離環境中處理較完整的 issue</td><td>活躍；MIT；任務越大越需要 checkpoint 與人工 review</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Workflow 支援</th><td><a href="https://github.com/obra/superpowers">obra/superpowers</a></td><td>workflow collection</td><td>agent plugin／skills</td><td>參考 planning、TDD、debug 與 review 流程</td><td>活躍；MIT；模板仍要配合自己的 repo gate</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/yamadashy/repomix">yamadashy/repomix</a></td><td>repo context packer</td><td>CLI／MCP</td><td>整理一次性的 codebase context</td><td>活躍；MIT；輸出前仍要排除 secret 與不必要檔案</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">維護／歷史</th><td><a href="https://github.com/continuedev/continue">continuedev/continue</a></td><td>coding agent</td><td>CLI／VS Code／JetBrains</td><td>閱讀開源 editor-agent 整合的歷史設計</td><td>read-only；Apache-2.0；官方 2.0.0 是最後版本，不再積極維護</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/RooCodeInc/Roo-Code">Roo Code</a></td><td>coding agent</td><td>VS Code extension</td><td>閱讀多 mode 代理的設計歷史</td><td>已封存；Apache-2.0；新專案請改用仍在維護的工具</td><td>⭐⭐⭐</td></tr>
</tbody>
</table>

<a id="也適用其他分支"></a>

## ✅ 完成檢查與下一站

- [ ] 我能說出 Coding Agent／Harness、Router 與 Local Model Runtime 的差別。
- [ ] 工具先給 read-only plan，得到人工批准後才改一個檔案。
- [ ] 我讀過完整 Diff，也真的執行了對應 Test。
- [ ] 我知道如何只 Rollback 這次改動，而且工具沒有 push、merge 或 deploy。

下一站：要設計 Skills／MCP，走 [Stage 5](../stages/05-claude-code-ecosystem.md)；要做 Eval、Observability 與 production gate，走 [Stage 7](../stages/07-multi-agent-production.md)；要比較 CLI agents，打開 [CLI agent 指南](../resources/cli-agents-guide.md)。

<details markdown="1">
<summary>⏱ 展開：時間、環境、費用與 secret 邊界</summary>

第一個練習約需 20–40 分鐘。使用可丟棄 repo 或新 branch，先看 `git status`，不要把同事或另一個工具正在修改的檔案交給代理覆蓋。

- API key 放環境變數或工具支援的 secret store，不貼進 prompt、README 或 commit。
- 先關閉不需要的網路、外部目錄與 shell 權限。
- 費用依 Model、Provider、輸入量與重試次數變動；不要保存固定單次價格猜測。
- Sandbox 只能縮小爆炸範圍；外部服務、credential 與人工批准仍要分開保護。

</details>

<a id="必練流程按使用頻率"></a>
<a id="3-個具體-workflow-recipe"></a>

<details markdown="1">
<summary>🧪 展開：從每日小改走到團隊 workflow</summary>

### 每日開發

`plan → 人工批准 → 小改 → diff → test → review → commit`。每一步都能停下來，才容易找到錯在哪裡。

### PR review

把代理意見當成候選 finding。要求它指出檔案、行為、重現方式與建議 Test；沒有證據的猜測不能直接變成阻擋理由。

### CI

CI agent 使用唯讀 token、最小 repository 權限與固定輸入。Issue、PR 或網頁文字不能直接變成可執行命令。發布、merge 與 secrets 保留額外批准。

### 批次重構

先建立基準測試，再按模組分批。每批都有 checkpoint、Diff 與 Rollback；不要因為工具能改很多檔案，就一次交出整個 repo。

</details>

<a id="常見踩坑anti-patterns"></a>

<details markdown="1">
<summary>🧯 展開：常見錯誤、替代方案與 rollback</summary>

| 問題 | 改成什麼 |
|---|---|
| 看到 IDE 畫面就以為工具只能在 IDE 用 | 分開看核心身分與所有 Surface |
| 把 OpenRouter、Ollama、OpenCode 當同一類 | Router、Runtime、Coding Agent 分開選 |
| 工具說 Test 綠就直接接受 | 自己讀 Diff、確認 Test 覆蓋需求，再人工批准 |
| 用固定行數判斷安全 | 看範圍、可測性、可回復性與 Diff 是否可讀 |
| Aider 自動 commit 就跳過 hook | 明確啟用 repo 需要的 verify／hook，再走正常 review gate |
| 多個工具同時改同一檔案 | 分清 ownership、使用獨立 worktree，最後人工整合 |

Rollback 前先看 `git status` 和 Diff。只回復已確認的目標，不要用 broad reset 清掉別人的工作。

</details>
