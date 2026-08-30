> **繁體中文** | [简体中文](./cli-agents-guide.zh-Hans.md) | [English](./cli-agents-guide.en.md)

# CLI Agents 參考指南

> [← 回主路線 README](../README.md) · [A1：安全地跑第一個小任務](../tracks/cli/A1-cli-intro.md)

這份 reference doc 用「現在要做什麼」和可核對的官方資料整理 9 個 terminal CLI。它不替工具打分，也不以熱門度或主觀排行決定入口；先看身分，再依你的 provider、登入方式與安全邊界選擇。

## 先分清楚：agent 不等於模型或 API

<table>
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

<table>
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

完整表預設收合；展開後請把「查核日」與你的安裝版本一起記下。官方資料查核日：**2026-08-30 UTC**。

<details markdown="1">
<summary>展開 9 個 CLI 的安裝、認證、provider 與安全事實</summary>

<table>
<thead>
<tr><th scope="col">類型</th><th scope="col">工具</th><th scope="col">現在適合誰</th><th scope="col">模型／provider 選擇</th><th scope="col">登入方式</th><th scope="col">安全起手式</th><th scope="col">狀態</th><th scope="col">官方來源</th></tr>
</thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">官方模型生態</th><td>Claude Code</td><td>要在終端機使用 Anthropic 生態的人</td><td>Claude；Anthropic API</td><td>Claude 帳號或 Anthropic API key</td><td>用 demo repo；保留 permission prompt</td><td>Anthropic 官方 terminal、desktop、IDE 與 cloud 介面之一</td><td><a href="https://code.claude.com/docs/en/overview">文件</a> · <a href="https://github.com/anthropics/claude-code">repo</a></td></tr>
<tr><td>Codex CLI</td><td>要在終端機使用 OpenAI／ChatGPT 登入的人</td><td>GPT 系列；OpenAI API</td><td>ChatGPT 登入或 OpenAI API key</td><td>使用預設 approval 與 workspace sandbox；先看 diff</td><td>OpenAI 開源 terminal coding agent</td><td><a href="https://learn.chatgpt.com/docs/codex/cli">文件</a> · <a href="https://github.com/openai/codex">repo</a></td></tr>
<tr><td>Gemini CLI</td><td>已有 Google 認證，想在 terminal 使用 Gemini 的人</td><td>Gemini；Google AI API 或 Vertex AI</td><td>Google 登入、Gemini API key 或 Vertex AI</td><td>使用 approval 模式；需要時明確開啟 `--sandbox`</td><td>Google 開源 terminal agent</td><td><a href="https://google-gemini.github.io/gemini-cli/">文件</a> · <a href="https://github.com/google-gemini/gemini-cli">repo</a></td></tr>
<tr><td>Grok Build</td><td>要試用 xAI Grok terminal TUI 的人</td><td>Grok；xAI 登入或 API key</td><td>首次互動瀏覽器登入；CI 可用 `XAI_API_KEY`</td><td>先用 demo repo；不要複製 `~/.grok/auth.json`</td><td>xAI 官方開源 TUI coding agent</td><td><a href="https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/02-authentication.md">認證</a> · <a href="https://github.com/xai-org/grok-build">repo</a></td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">可換 provider</th><td>OpenCode</td><td>需要在多個 provider 間切換的人</td><td>多 provider；可接 OpenRouter 或相容 endpoint</td><td>依 provider 設定 API key、OAuth 或環境變數</td><td>先檢查 permission 設定；只在 demo repo 試外部目錄</td><td>開源 terminal coding agent；`AGENTS.md` 優先，沒有時才用 `CLAUDE.md` 相容 fallback</td><td><a href="https://opencode.ai/docs/providers/">provider</a> · <a href="https://github.com/anomalyco/opencode">repo</a></td></tr>
<tr><td>goose</td><td>需要 CLI、desktop 或 API，並想接工具與資料來源的人</td><td>15+ provider，包含 Anthropic、OpenAI、Google、Ollama、OpenRouter</td><td>provider API key，或部分既有訂閱的 ACP 登入</td><td>先用低權限 extension 與 sandbox；不連 production 資料</td><td>AAIF 的開源本機 agent，提供 CLI、desktop、API</td><td><a href="https://block.github.io/goose/">文件</a> · <a href="https://github.com/aaif-goose/goose">repo</a></td></tr>
<tr><td>Aider</td><td>希望以 git diff／commit 管理程式修改的人</td><td>多家 cloud API、OpenRouter、OpenAI-compatible endpoint 與本機模型</td><td>provider API key、設定檔或環境變數</td><td>先用乾淨 demo repo；留意 Aider 的 git auto-commit 行為</td><td>開源 terminal pair-programming 工具，官方文件明列 git 整合</td><td><a href="https://aider.chat/docs/">文件</a> · <a href="https://github.com/Aider-AI/aider">repo</a></td></tr>
<tr><td>Pi</td><td>想從小核心開始，用 extensions、skills 或 RPC 擴充的人</td><td>訂閱 provider、API key provider、自訂 provider；可接本機 endpoint</td><td>`/login` 或 provider API key</td><td>Pi 沒有內建 sandbox；用 disposable repo 或容器，並人工審查命令</td><td>可擴充的 minimal terminal coding harness</td><td><a href="https://pi.dev/docs/latest/providers">provider</a> · <a href="https://github.com/earendil-works/pi">repo</a></td></tr>
<tr><td>Hermes Agent</td><td>要在 terminal、desktop 或聊天平台使用同一 agent 的人</td><td>Nous Portal、OpenRouter、Anthropic、Google 與其他 provider</td><td>`hermes model` 設定 API key 或 OAuth；Nous Portal 可用 OAuth</td><td>先在低風險 repo；把 skills、MCP 與 provider 權限逐項開啟</td><td>Nous Research 的開源 agent，文件提供 CLI 與多介面整合</td><td><a href="https://hermes-agent.nousresearch.com/docs/integrations/providers/">provider</a> · <a href="https://github.com/NousResearch/hermes-agent">repo</a></td></tr>
</tbody>
</table>

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
