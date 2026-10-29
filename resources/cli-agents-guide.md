> **繁體中文** | [简体中文](./cli-agents-guide.zh-Hans.md) | [English](./cli-agents-guide.en.md)

# CLI Agents 參考指南

> [← 回主路線 README](../README.md) · [A1：安全地跑第一個小任務](../tracks/cli/A1-cli-intro.md)

這份 reference doc 用「現在要做什麼」和可核對的官方資料整理 9 個 terminal CLI。它不替工具打分，也不以熱門度或主觀排行決定入口；先看身分，再依你的 provider、登入方式與安全邊界選擇。

## 先分清楚：agent 不等於模型或 API

<table align="center">
<thead>
<tr><th scope="col">種類</th><th scope="col">它負責什麼</th><th scope="col">例子</th><th scope="col">不要混淆</th></tr>
</thead>
<tbody>
<tr><th scope="row">LLM</th><td>產生文字、程式碼或工具呼叫</td><td>Claude、GPT、Gemini</td><td>模型不自動擁有你電腦的檔案權限</td></tr>
<tr><th scope="row">Provider API</th><td>提供某家模型的請求、認證與計費</td><td>Anthropic API、OpenAI API、Gemini API</td><td>API 不是 terminal 工作台</td></tr>
<tr><th scope="row">Router</th><td>把請求轉接到多家 provider</td><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a></td><td>Router 不會代替 agent 管理檔案或命令權限</td></tr>
<tr><th scope="row">Coding agent／harness</th><td>在終端機讀檔、編輯、執行命令並回報結果</td><td>Claude Code、Codex、OpenCode、Pi</td><td>它的 approval、sandbox 與 project trust 要另外查</td></tr>
<tr><th scope="row">Local runtime</th><td>在本機載入並執行模型</td><td><a href="https://ollama.com/">Ollama</a></td><td>它可供 agent 呼叫，但本身不是 coding agent</td></tr>
</tbody>
</table>

## 用情境找入口

<table align="center">
<thead>
<tr><th scope="col">你的條件</th><th scope="col">先查哪一類</th><th scope="col">要記錄的差異</th></tr>
</thead>
<tbody>
<tr><th scope="row">已有一家模型服務的帳號</th><td>該生態的 CLI，例如 Claude Code、Codex 或 Gemini CLI</td><td>登入流程、approval、sandbox、用量頁面</td></tr>
<tr><th scope="row">需要更換 provider</th><td>OpenCode、goose、Aider、Hermes Agent 或 Pi</td><td>支援的 endpoint、模型 ID、API key 儲存位置</td></tr>
<tr><th scope="row">想集中轉接多個 provider</th><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a> 搭配一個 agent</td><td>實際路由到的 provider、資料政策、usage 與 billing</td></tr>
<tr><th scope="row">想在本機練習</th><td><a href="https://ollama.com/">Ollama</a> 搭配支援相容 API 的 agent</td><td>模型是否在本機、agent 是否仍可執行 shell／寫檔</td></tr>
</tbody>
</table>

## 9 個 CLI 工具

以下工具資料直接展開。請把「查核日」與你的安裝版本一起記下。官方資料查核日：**2026-08-30 UTC**。

> **穩定通道與局部查核（2026-10-11 UTC）：** 新手基準優先選官方 stable release。只有驗證特定功能時，才在隔離 demo repo 試用 alpha、preview 或 nightly；
> 先讀 release notes、固定 exact version，並保留回退方式。官方發布頁將 [Codex CLI `0.163.0-alpha.5`](https://github.com/openai/codex/releases/tag/rust-v0.163.0-alpha.5)
> 與 [Gemini CLI `0.65.0-nightly.20261010.g9b6e0265d`](https://github.com/google-gemini/gemini-cli/releases/tag/v0.65.0-nightly.20261010.g9b6e0265d) 標記為 pre-release，
> 兩者都不作為穩定的新手入門基準。此處僅局部查核發布通道；整張表最後一次完整查核仍為 2026-08-30 UTC。

<div class="reader-resource-catalog" role="region" tabindex="0" aria-label="CLI 工具與學習資源">
<table align="center">
<thead><tr><th scope="col">分類</th><th scope="col">專案／文件</th><th scope="col">評分</th><th scope="col">用途</th><th scope="col">限制</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4" align="center" valign="middle" width="80">官方模型生態</th><td><div data-field="entry"><strong>Claude Code</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>現在適合誰：</strong> 要在終端機使用 Anthropic 生態的人</div><div data-field="models"><strong>模型／provider 選擇：</strong> Claude；Anthropic API</div></td><td><div data-field="auth"><strong>登入方式：</strong> Claude 帳號或 Anthropic API key</div><div data-field="safety"><strong>安全起手式：</strong> 用 demo repo；保留 permission prompt</div><div data-field="status"><strong>狀態：</strong> Anthropic 官方 terminal、desktop、IDE 與 cloud 介面之一</div><div data-field="sources"><strong>官方來源：</strong> <a href="https://code.claude.com/docs/en/overview">文件</a> · <a href="https://github.com/anthropics/claude-code">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>Codex CLI</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>現在適合誰：</strong> 要在終端機使用 OpenAI／ChatGPT 登入的人</div><div data-field="models"><strong>模型／provider 選擇：</strong> GPT 系列；OpenAI API</div></td><td><div data-field="auth"><strong>登入方式：</strong> ChatGPT 登入或 OpenAI API key</div><div data-field="safety"><strong>安全起手式：</strong> 使用預設 approval 與 workspace sandbox；先看 diff</div><div data-field="status"><strong>狀態：</strong> OpenAI 開源 terminal coding agent</div><div data-field="sources"><strong>官方來源：</strong> <a href="https://learn.chatgpt.com/docs/codex/cli">文件</a> · <a href="https://github.com/openai/codex">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>Gemini CLI</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>現在適合誰：</strong> 已有 Google 認證，想在 terminal 使用 Gemini 的人</div><div data-field="models"><strong>模型／provider 選擇：</strong> Gemini；Google AI API 或 Vertex AI</div></td><td><div data-field="auth"><strong>登入方式：</strong> Google 登入、Gemini API key 或 Vertex AI</div><div data-field="safety"><strong>安全起手式：</strong> 使用 approval 模式；需要時明確開啟 <code>--sandbox</code></div><div data-field="status"><strong>狀態：</strong> Google 開源 terminal agent</div><div data-field="sources"><strong>官方來源：</strong> <a href="https://google-gemini.github.io/gemini-cli/">文件</a> · <a href="https://github.com/google-gemini/gemini-cli">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>Grok Build</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>現在適合誰：</strong> 要試用 xAI Grok terminal TUI 的人</div><div data-field="models"><strong>模型／provider 選擇：</strong> Grok；xAI 登入或 API key</div></td><td><div data-field="auth"><strong>登入方式：</strong> 首次互動瀏覽器登入；CI 可用 <code>XAI_API_KEY</code></div><div data-field="safety"><strong>安全起手式：</strong> 先用 demo repo；不要複製 <code>~/.grok/auth.json</code></div><div data-field="status"><strong>狀態：</strong> xAI 官方開源 TUI coding agent</div><div data-field="sources"><strong>官方來源：</strong> <a href="https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/02-authentication.md">認證</a> · <a href="https://github.com/xai-org/grok-build">repo</a></div></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5" align="center" valign="middle" width="80">可換 provider</th><td><div data-field="entry"><strong>OpenCode</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>現在適合誰：</strong> 需要在多個 provider 間切換的人</div><div data-field="models"><strong>模型／provider 選擇：</strong> 多 provider；可接 OpenRouter 或相容 endpoint</div></td><td><div data-field="auth"><strong>登入方式：</strong> 依 provider 設定 API key、OAuth 或環境變數</div><div data-field="safety"><strong>安全起手式：</strong> 先檢查 permission 設定；只在 demo repo 試外部目錄</div><div data-field="status"><strong>狀態：</strong> 開源 terminal coding agent；<code>AGENTS.md</code> 優先，沒有時才用 <code>CLAUDE.md</code> 相容 fallback</div><div data-field="sources"><strong>官方來源：</strong> <a href="https://opencode.ai/docs/providers/">provider</a> · <a href="https://github.com/anomalyco/opencode">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>goose</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>現在適合誰：</strong> 需要 CLI、desktop 或 API，並想接工具與資料來源的人</div><div data-field="models"><strong>模型／provider 選擇：</strong> 15+ provider，包含 Anthropic、OpenAI、Google、Ollama、OpenRouter</div></td><td><div data-field="auth"><strong>登入方式：</strong> provider API key，或部分既有訂閱的 ACP 登入</div><div data-field="safety"><strong>安全起手式：</strong> 先用低權限 extension 與 sandbox；不連 production 資料</div><div data-field="status"><strong>狀態：</strong> AAIF 的開源本機 agent，提供 CLI、desktop、API</div><div data-field="sources"><strong>官方來源：</strong> <a href="https://block.github.io/goose/">文件</a> · <a href="https://github.com/aaif-goose/goose">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>Aider</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>現在適合誰：</strong> 希望以 git diff／commit 管理程式修改的人</div><div data-field="models"><strong>模型／provider 選擇：</strong> 多家 cloud API、OpenRouter、OpenAI-compatible endpoint 與本機模型</div></td><td><div data-field="auth"><strong>登入方式：</strong> provider API key、設定檔或環境變數</div><div data-field="safety"><strong>安全起手式：</strong> 先用乾淨 demo repo；留意 Aider 的 git auto-commit 行為</div><div data-field="status"><strong>狀態：</strong> 開源 terminal pair-programming 工具，官方文件明列 git 整合</div><div data-field="sources"><strong>官方來源：</strong> <a href="https://aider.chat/docs/">文件</a> · <a href="https://github.com/Aider-AI/aider">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>Pi</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>現在適合誰：</strong> 想從小核心開始，用 extensions、skills 或 RPC 擴充的人</div><div data-field="models"><strong>模型／provider 選擇：</strong> 訂閱 provider、API key provider、自訂 provider；可接本機 endpoint</div></td><td><div data-field="auth"><strong>登入方式：</strong> <code>/login</code> 或 provider API key</div><div data-field="safety"><strong>安全起手式：</strong> Pi 沒有內建 sandbox；用 disposable repo 或容器，並人工審查命令</div><div data-field="status"><strong>狀態：</strong> 可擴充的 minimal terminal coding harness</div><div data-field="sources"><strong>官方來源：</strong> <a href="https://pi.dev/docs/latest/providers">provider</a> · <a href="https://github.com/earendil-works/pi">repo</a></div></td></tr>
<tr><td><div data-field="entry"><strong>Hermes Agent</strong></div></td><td align="center" valign="middle">—</td><td><div data-field="audience"><strong>現在適合誰：</strong> 要在 terminal、desktop 或聊天平台使用同一 agent 的人</div><div data-field="models"><strong>模型／provider 選擇：</strong> Nous Portal、OpenRouter、Anthropic、Google 與其他 provider</div></td><td><div data-field="auth"><strong>登入方式：</strong> <code>hermes model</code> 設定 API key 或 OAuth；Nous Portal 可用 OAuth</div><div data-field="safety"><strong>安全起手式：</strong> 先在低風險 repo；把 skills、MCP 與 provider 權限逐項開啟</div><div data-field="status"><strong>狀態：</strong> Nous Research 的開源 agent，文件提供 CLI 與多介面整合</div><div data-field="sources"><strong>官方來源：</strong> <a href="https://hermes-agent.nousresearch.com/docs/integrations/providers/">provider</a> · <a href="https://github.com/NousResearch/hermes-agent">repo</a></div></td></tr>
</tbody>
</table>
</div>

<details markdown="1">
<summary>OpenRouter 與 Ollama 的補充說明</summary>

### OpenRouter 與 Ollama 放在哪裡？

OpenRouter 是 Router，不列入上表的 9 個 coding CLI；它提供統一 API、provider routing 與集中用量。Ollama 是 local runtime，不是 agent；它可在 `http://localhost:11434/v1` 提供相容 API，供 OpenCode、goose、Aider 或其他 client 使用。兩者都不能取代 agent 的檔案權限與 sandbox 設計。
</details>

## Prompt 跨 CLI 搬移時保留四件事

1. 寫清楚檔案路徑、允許的範圍與「先列計畫、確認後再改」的順序。
2. 把模型、provider、API key、approval／sandbox 設定分開記錄；不要假設換 CLI 後相同。
3. 用一般文字描述目標；`/login`、`/permissions` 等斜線指令只在對應工具的區塊使用。
4. 要求輸出 `git diff`、測試結果與未完成項目，並在另一個 CLI 前先復原工作樹。

<details markdown="1">
<summary>展開規則檔、sandbox 與常見問題</summary>

- Claude Code 的專案規則是 `CLAUDE.md`；Codex 使用 `AGENTS.md`。OpenCode 以 `AGENTS.md` 優先，沒有時才使用 `CLAUDE.md` 相容 fallback；不要把不存在的 `OPENCODE.md` 當共通格式。
- Gemini CLI 的專案上下文與 `.gemini/` 設定依官方文件；`--sandbox`、approval mode 與 `--yolo` 的風險不同，第一次不要跳過確認。
- Pi 的 project trust 不是 sandbox，官方安全文件明確提醒它依啟動使用者權限執行；需要隔離時改用容器或其他 OS 層邊界。
- Aider 官方文件說明編輯後的 git 整合與 auto-commit；先在乾淨 demo repo 觀察，確認 commit 內容再帶入工作 repo。
- goose、Hermes Agent 與其他可接 MCP／extension 的 agent，先開一個低權限、只讀取的整合；不要以 Gmail、Slack 或 production DB 作第一個外部連線。
- API key 只放在官方支援的 credential store 或環境變數；不進 repo、不進 prompt、不進截圖與 issue。費用按當日官方價格和實際 usage 計算，不按模型名稱猜測。

#### 官方查核入口（2026-08-30 UTC）

- [Claude Code overview](https://code.claude.com/docs/en/overview) · [permissions](https://code.claude.com/docs/en/permissions)
- [OpenAI Codex CLI](https://learn.chatgpt.com/docs/codex/cli)
- [OpenCode](https://opencode.ai/docs/) · [canonical repository](https://github.com/anomalyco/opencode)
- [Gemini CLI](https://google-gemini.github.io/gemini-cli/)
- [goose](https://block.github.io/goose/) · [canonical repository](https://github.com/aaif-goose/goose)
- [Aider](https://aider.chat/docs/)
- [Hermes Agent](https://hermes-agent.nousresearch.com/docs/)
- [Grok Build](https://github.com/xai-org/grok-build)
- [Pi](https://pi.dev/docs/latest) · [canonical repository](https://github.com/earendil-works/pi)
- [OpenRouter FAQ](https://openrouter.ai/docs/faq) · [Ollama](https://ollama.com/)
</details>

## 回到 Track A

- 要第一次安全操作：回到 [A1](../tracks/cli/A1-cli-intro.md)。
- 要把規則檔與重複流程固定下來：進入 [A2](../tracks/cli/A2-cli-workflow.md)。
- 要做 MCP、CI 與 usage trace：進入 [A3](../tracks/cli/A3-cli-production.md)。

> 維護原則：工具、登入、價格、sandbox 與 provider 都會變動；每次改表前重查官方文件，並更新查核日。這份表保持事實欄位，不維護熱門度或主觀評分。
