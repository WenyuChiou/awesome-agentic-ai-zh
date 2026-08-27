# A3 — 把 CLI agent 接進安全的團隊流程

> **繁體中文** | [简体中文](./A3-cli-production.zh-Hans.md) | [English](./A3-cli-production.en.md)

> [← A2 — 讓 CLI agent 每次都照同一套方法做事](A2-cli-workflow.md) · **Track A: CLI Power User** 第 3 站（最後）

這一站只做一件事：**讓 CLI agent 在測試用 PR 做一個只讀檢查。它可以提出意見，但不能自己合併、部署或取得多餘權限。**

## 學習目標

完成後，你可以：

- 只把一個安全範圍交給 MCP server。
- 讓 CI 在 PR 自動產生一份可檢查的建議。
- 看懂一次執行留下的 usage、時間與結果。
- 把 A2 的 Skill 交給隊友，並讓對方安全地重跑。

## 三個詞先分清

| 詞 | 白話說法 | 正確意思 |
|---|---|---|
| **MCP** | 像轉接頭 | 讓 agent 連到外部工具或資料；能碰什麼取決於你給的權限 |
| **CI** | 像每次交作業都會出現的檢查站 | push 或 PR 發生時，自動執行固定工作 |
| **Observability** | 像收據加行車紀錄 | 留下做了什麼、花了多少、哪裡失敗的紀錄 |

三個詞會一起出現，但不是同一件事：MCP 負責「接工具」，CI 負責「何時自動跑」，observability 負責「跑完留下什麼證據」。

## 先走安全階梯

1. **只讀**：先讓 agent 看資料，不讓它改資料。
2. **最小權限**：只開這次需要的資料夾、repo、tool 或 token scope。
3. **demo repo**：先在可丟棄的練習環境測試。
4. **人工 review**：人決定要不要採用 agent 的建議。
5. **最後才考慮寫入**：auto-merge、push、deploy 不屬於這一站。

<details markdown="1">
<summary>展開時間、先備條件、環境與費用</summary>

- **時間**：先完成四個最小成果，通常可拆成數次短練習；不要為了趕時間一次接很多服務。
- **先備條件**：完成 [A1](A1-cli-intro.md) 與 [A2](A2-cli-workflow.md)，並能看懂 `git status`、PR 與 GitHub Actions 的基本畫面。
- **環境**：一個沒有真實 secrets 的 demo repo；第一輪使用 GitHub-hosted Linux runner，較容易套用 sandbox。
- **費用**：GitHub Actions、CLI 訂閱與模型 API 可能分開計費。執行前先看自己使用的方案，不要把別人的價格當成自己的價格。

如果 A2 的 `review-changes` Skill 還不能穩定輸出 `PASS` 或具體問題，先回去修好再進 A3。
</details>

<details markdown="1">
<summary>展開必讀資料與閱讀順序（查核於 2026-08-27 UTC）</summary>

1. 先看 [MCP Connect to local servers](https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers)，知道 server 只能拿到你交給它的路徑。
2. 再看 [GitHub Actions Security Hardening](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)，先理解 least privilege 與不可信 PR。
3. 選一條 CI 路徑：
   - Claude Code：[官方 GitHub Actions 文件](https://docs.anthropic.com/en/docs/claude-code/github-actions)
   - Codex：[官方 GitHub Action 文件](https://developers.openai.com/codex/github-action)
4. 需要 trace、eval 或完整 production 理論時，再進 [Stage 7](../../stages/07-multi-agent-production.md) 與 [Stage 7.5](../../stages/07.5-advanced-agentic-concepts.md)。

查核日期只代表上面資料在當天已檢查，不代表它們永遠不會改。
</details>

## 動手練習

<a id="cli-9"></a>
### 動手練習 CLI-9：只連一個 MCP server

**成果：** agent 能讀到一個新建的 demo 資料夾，但沒有取得整個 home、磁碟、真正專案或 secrets。

先建立空的 `a3-mcp-demo` 資料夾，裡面放一個 `hello.txt`。把官方 filesystem reference server 接到你的 CLI 時，**只傳入這個資料夾的絕對路徑**。

成功時，agent 能讀出 `hello.txt`；要求它讀取範圍外的檔案時，應該失敗或要求你重新授權。

<details markdown="1">
<summary>展開 CLI-9 的安裝、權限測試與 GitHub MCP 延伸</summary>

1. 依你主用 CLI 的官方 MCP 文件開啟設定；不同 CLI 的設定檔與指令不一定相同。
2. 使用官方 package `@modelcontextprotocol/server-filesystem`，arguments 只放 `a3-mcp-demo` 的絕對路徑。不要填 `~`、home、磁碟根目錄或整個工作區。
3. 重新啟動 CLI，請它列出 demo 資料夾，再讀取 `hello.txt`。
4. 請它讀 demo 範圍外的一個普通檔名。正確結果是拒絕或先要求新增授權；不是偷偷讀取。
5. 練習後移除 server 設定，確認 CLI 已不能再使用它。

要讀 PR 或 issue 時，改看 GitHub 官方的 [`github/github-mcp-server`](https://github.com/github/github-mcp-server)。先使用 `--read-only`，再用 toolsets 或 tools allow-list 只開需要的能力。若使用 PAT，放在安全的 secret／環境變數，授予最少 scope，練習後撤銷；能用 OAuth 時依 host 官方流程設定。

[`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) 適合讀 reference implementation，但官方說明它們不是 production-ready。舊 `github` reference server 已移到歷史集合，不要再用它當現行 GitHub 入口。

**費用提醒：** 本機 filesystem server 通常不另外收費，但 CLI／模型仍可能計費。遠端 MCP 也可能有自己的方案。
</details>

<a id="cli-10"></a>
### 動手練習 CLI-10：讓 PR 多一個只讀檢查員

**成果：** 測試用 PR 會留下 review 結果；人仍決定是否修改、合併或部署。

選 Anthropic 的 [`claude-code-action`](https://github.com/anthropics/claude-code-action) 或 OpenAI 的 [`codex-action`](https://github.com/openai/codex-action)。第一輪只在自己控制的 demo repo 與 branch 執行，沿用 A2 的 [`review-changes` Skill](A2-cli-workflow.md#動手練習-cli-6把重複-review-做成-skill)。

成功標準不是「幾分鐘內完成」，而是 workflow 成功結束，並以 PR comment、job summary 或 artifact 留下可閱讀的結果。

<details markdown="1">
<summary>展開 CLI-10 的安全設定與驗證步驟</summary>

1. 從供應商的官方範例建立 workflow，不要複製來源不明的 YAML。
2. API key 放入 GitHub Actions secret。不要寫進 workflow、prompt、repo 或 log。
3. `GITHUB_TOKEN` 從 `contents: read` 起步。只有需要貼 PR comment 時，才對該 job 增加必要的 pull-request 權限。
4. Codex 的只讀工作使用目前官方 action 支援的 `permission-profile: ":read-only"`；不要同時設定互斥的 legacy sandbox 欄位。Claude Code 依官方 action 的 permissions／allowed tools 限制可用能力。
5. prompt 只要求讀 diff、列問題、輸出 `PASS` 或具體建議。明寫：不得 edit、commit、push、merge、deploy 或傳送額外訊息。
6. 先用自己建立的 same-repo test branch。不要用 `pull_request_target` checkout 不可信 PR code；這可能讓不可信內容接觸 secrets 或寫入權限。
7. 檢查 Actions log、review 結果與 repo diff。任何 secret 外洩跡象都要立即刪除 log、撤銷並輪替 secret。

GitHub 建議 production workflow 把第三方 Action pin 到完整 commit SHA，因為 tag 可能移動。官方文件中的 `@v1`／`@v5` 適合辨認產品版本；正式落地時再查證並固定當下可信的完整 SHA。

**費用提醒：** 設定 job timeout 與 concurrency，避免卡住或重複觸發。模型 API、供應商方案與 GitHub Actions minutes 要分開看。
</details>

<a id="cli-11"></a>
### 動手練習 CLI-11：看一次執行的收據

**成果：** 你留下 provider／model、input usage、output usage、時間與結果；資料拿不到的欄位會清楚寫「未確認」，不會猜。

先分清你用的是訂閱方案，還是按 API usage 計費。若官方提供 token 與單價，成本才用這個算式：

`input tokens × input price + output tokens × output price`

<details markdown="1">
<summary>展開 CLI-11 的記錄卡、停止規則與 observability</summary>

先用一個小 task 填這張卡：

| 欄位 | 要記什麼 |
|---|---|
| Task | 這次請 agent 做什麼 |
| Provider／model | 實際使用的供應商與型號；拿不到就寫未確認 |
| Usage | input／output usage；不要只寫模糊的「總 token」 |
| 時間 | workflow 或 CLI 顯示的實際耗時 |
| 結果 | `PASS`、問題清單或失敗原因 |
| 成本 | 只有能對到官方單價時才計算；否則寫計費方式或未確認 |

再設一個工具真的支援的停止規則，例如 job timeout、最大重試、provider spend limit，或每次進入付費步驟前人工確認。不要發明一個工具不會讀的「通用成本設定」來製造安心感。

要比較多次執行時，可選 [Langfuse](https://github.com/langfuse/langfuse)、[Phoenix](https://github.com/Arize-ai/phoenix)、[Helicone](https://github.com/Helicone/helicone) 或 [promptfoo](https://github.com/promptfoo/promptfoo)。先確認資料會送去哪裡、是否含原始 prompt／code／PII，再決定能不能接。

Prompt caching 的 TTL、資格與價格依 provider／model 而變。Anthropic 目前文件同時提供預設 5 分鐘與可選 1 小時 TTL；把它當作要查的產品設定，不要當成所有 CLI 的固定規則。
</details>

<a id="cli-12"></a>
### 動手練習 CLI-12：把 Skill 安全交給隊友

**成果：** 第二個乾淨 demo repo 能找到 `review-changes` Skill；執行後沒有非預期修改。

把 A2 的 `review-changes` Skill 放進可版本控制的 team repo，附上四件事：安裝位置、需要的權限、測試方法、移除方法。Claude Code 可再依官方 plugin 格式打包；其他 CLI 依各自 Skill 文件安裝。

<details markdown="1">
<summary>展開 CLI-12 的分享、安裝與撤銷步驟</summary>

1. 分享前讀完 `SKILL.md` 與附帶 scripts，確認沒有下載陌生程式、讀取 secrets 或改變外部系統。
2. 保留 plugin 根目錄的 `skills/review-changes/SKILL.md`；不要把專案自己的 `CLAUDE.md`、`AGENTS.md` 或 secrets 一起打包。
3. 在第二個乾淨 demo repo 依工具文件安裝。Claude Code 可參考 [Plugins 文件](https://code.claude.com/docs/en/plugins)與 [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official)。
4. 做一個小文件 diff，執行 Skill，再用 `git status --short` 確認它只 review、沒有改檔。
5. 記錄版本或 commit SHA。更新前先看 diff；不再使用時，依文件移除 plugin／Skill，並確認 agent 找不到它。

Skill 的核心意思可以共用，但資料夾、權限、frontmatter 與安裝方式不一定相同。不要把某一家工具的 plugin 格式說成所有 CLI 都通用。

**費用提醒：** 分享檔案本身通常不收模型費，但每位隊友執行 Skill 時可能使用自己的訂閱或 API 額度。
</details>

## 只記得這個 production 安全迴圈

`圈定範圍 → 只讀執行 → 留下紀錄 → 人工判斷 → 能夠復原`

如果沒有範圍、證據或復原方法，就先不要提高權限。這比背很多工具名稱更重要。

### 📋 Playbook 4：派遣 subagent 跑獨立任務

**成果：** 先列出目前工具真的提供哪些 agent，再把獨立、可驗證的工作交出去；不要假設每台電腦都有同名 agent。

<details markdown="1">
<summary>展開 Playbook 4 與其餘六個進階 playbook</summary>

**Playbook 4 — subagent：** subagent 是主 session 派出去的獨立小幫手。Claude Code 目前有 `Explore`、`Plan`、`general-purpose` 等 built-in subagent；可用清單仍會受版本、session 與設定影響。`code-reviewer` 是官方文件提供的**自訂範例**，不是每個安裝都固定存在。先執行工具的 agent list，再選 read-only agent 或建立受限 reviewer。

其餘情況只記一個動作，理論放在 [Stage 7.5](../../stages/07.5-advanced-agentic-concepts.md)：

- **範圍不清：** 明寫可動與不可動的路徑，先要求計畫，不先改檔。
- **多人／多 agent 平行：** 分開 ownership 與 commit，最後再整合；不要同時改同一批檔案。
- **Review agent 輸出：** reviewer 只提供證據，不取代測試、branch protection 或人類判斷。
- **在 CI 跑 agent：** 從只讀與可信 trigger 開始；模型 fallback 必須明確設定並重新驗證，不能偷偷換。
- **控制成本：** 用實際 usage、timeout、重試與 provider limit；拿不到資料就說拿不到。
- **防止規則 drift：** 故意做一個安全的小失敗，確認 gate 真的會擋；規則文字本身不是證據。

延伸閱讀：[`resources/subagent-cookbook.md`](../../resources/subagent-cookbook.md)與 [Stage 5.5](../../stages/05-claude-code-ecosystem.md#55--subagentsclaude-code-原生-multi-agent-機制-2025-新功能)。這些頁面之後會在自己的 layer 重新查證；使用 agent 名稱前仍以你當下的官方文件與實際清單為準。
</details>

## Track A 完成檢查

- [ ] MCP 只拿到 demo 資料夾或最小 read-only toolset。
- [ ] PR workflow 只提出意見，沒有 auto-merge、push 或 deploy。
- [ ] secrets 不在 repo、prompt 或 log；workflow 使用最小權限。
- [ ] 我能指出一次執行的結果與 usage；拿不到的資料沒有亂猜。
- [ ] 隊友能在乾淨 demo repo 執行 Skill，之後 `git status` 沒有非預期修改。

五項都做到，就完成 Track A。接著依目的選路：想做應用，回到 [Stage 3](../../stages/03-tool-use-and-hello-agent.md)；想研究 production 系統，進 [Stage 7](../../stages/07-multi-agent-production.md)；想理解更深的 agent 概念，再讀 [Stage 7.5](../../stages/07.5-advanced-agentic-concepts.md)。

<details markdown="1">
<summary>展開完整學習資源表（18 筆，查核於 2026-08-27 UTC）</summary>

<table>
<thead>
<tr><th scope="col">類型</th><th scope="col">資源</th><th scope="col">先看什麼</th><th scope="col">何時使用</th><th scope="col">來源</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">安全連接 MCP</th><td>MCP Connect to local servers</td><td>allowed directories 與明確授權</td><td>第一次接本機 server</td><td><a href="https://modelcontextprotocol.io/docs/2026-07-28/develop/connect-local-servers">官方文件</a></td></tr>
<tr><td>MCP Security Best Practices</td><td>least privilege、scope 與 token handling</td><td>要連帳號或遠端服務前</td><td><a href="https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices">官方文件</a></td></tr>
<tr><td><code>github/github-mcp-server</code></td><td><code>--read-only</code>、toolsets 與 tools allow-list</td><td>要讀 GitHub PR／issue</td><td><a href="https://github.com/github/github-mcp-server">GitHub repo</a></td></tr>
<tr><td><code>modelcontextprotocol/servers</code></td><td>reference implementation 與非 production-ready 警告</td><td>學協定或讀範例程式</td><td><a href="https://github.com/modelcontextprotocol/servers">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">CI 與 PR review</th><td>GitHub Actions Security Hardening</td><td>最小權限、不可信輸入、pin SHA</td><td>寫任何有 secrets 的 workflow 前</td><td><a href="https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions">官方文件</a></td></tr>
<tr><td>Claude Code GitHub Actions</td><td>官方 setup、permissions 與 troubleshooting</td><td>使用 Claude Code 跑 CI</td><td><a href="https://docs.anthropic.com/en/docs/claude-code/github-actions">官方文件</a></td></tr>
<tr><td><code>anthropics/claude-code-action</code></td><td>官方範例與 action inputs</td><td>從可執行範本開始</td><td><a href="https://github.com/anthropics/claude-code-action">GitHub repo</a></td></tr>
<tr><td>Codex GitHub Action</td><td>permission profile、trigger 與輸出</td><td>使用 Codex 跑 CI</td><td><a href="https://developers.openai.com/codex/github-action">OpenAI 官方文件</a></td></tr>
<tr><td><code>openai/codex-action</code></td><td><code>:read-only</code> 與 safety strategy</td><td>核對最新 inputs 與範例</td><td><a href="https://github.com/openai/codex-action">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">觀察與評估</th><td><code>langfuse/langfuse</code></td><td>traces、usage 與 eval</td><td>想把多次執行放在一起看</td><td><a href="https://github.com/langfuse/langfuse">GitHub repo</a></td></tr>
<tr><td><code>Arize-ai/phoenix</code></td><td>tracing 與 evaluation</td><td>想用開放原始碼觀察 AI 系統</td><td><a href="https://github.com/Arize-ai/phoenix">GitHub repo</a></td></tr>
<tr><td><code>Helicone/helicone</code></td><td>proxy／gateway 的資料流與隱私邊界</td><td>想從 gateway 收集 request 紀錄</td><td><a href="https://github.com/Helicone/helicone">GitHub repo</a></td></tr>
<tr><td><code>promptfoo/promptfoo</code></td><td>eval cases 與 CI regression</td><td>要比較改動前後是否退步</td><td><a href="https://github.com/promptfoo/promptfoo">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="3">分享 Skill／plugin</th><td>Claude Code Plugins</td><td>plugin 結構、安裝與 marketplace</td><td>要替 Claude Code 打包</td><td><a href="https://code.claude.com/docs/en/plugins">官方文件</a></td></tr>
<tr><td><code>anthropics/claude-plugins-official</code></td><td>官方管理的 plugin 目錄</td><td>找可讀的正式範例</td><td><a href="https://github.com/anthropics/claude-plugins-official">GitHub repo</a></td></tr>
<tr><td><code>obra/superpowers-marketplace</code></td><td>最小 marketplace 外殼</td><td>理解 curator-only 結構</td><td><a href="https://github.com/obra/superpowers-marketplace">GitHub repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">目錄與完整範例</th><td><code>wong2/awesome-mcp-servers</code></td><td>先分類，再逐一查來源與權限</td><td>官方資源沒有需要的 server 時</td><td><a href="https://github.com/wong2/awesome-mcp-servers">GitHub repo</a></td></tr>
<tr><td><code>obra/superpowers</code></td><td>Skill、規則與 workflow 如何組在一起</td><td>完成最小流程後看完整例子</td><td><a href="https://github.com/obra/superpowers">GitHub repo</a></td></tr>
</tbody>
</table>

目錄只幫你「找到候選項」，不替候選項保證安全。安裝任何 MCP、Action、Skill 或 plugin 前，都要再看 source、權限、最近維護狀態與移除方法。
</details>
