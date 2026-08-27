# A1 — 選一個 CLI agent，安全地完成第一個小任務

> **繁體中文** | [简体中文](./A1-cli-intro.zh-Hans.md) | [English](./A1-cli-intro.en.md)

> [← 回主路線 README](../../README.md) · **Track A: CLI Power User** 第 1 站 · [下一站：A2](A2-cli-workflow.md)

這一站要把「終端機裡的 AI」說清楚，然後在一個可丟棄的 demo repo（由 Git 管理的練習專案資料夾）裡安全地跑一次。你會先讓工具讀檔、找測試指令、提出計畫；確認計畫後，才做一個可用 `git diff` 看見、也能復原的小改動。

如果你想用現成工具做事，暫時不想自己寫 agent 程式，這一站就是你的入口。

## 你現在只要做這件事

準備一個不含秘密、可以隨時刪除的 demo repo。還沒安裝工具時，先在下面的短表選一個，點官方入口完成安裝與登入；接著送出這段請求：

> 請只讀取目前的 demo repo，說明它的用途、找出測試指令，並提出一個小型文件改動計畫。先不要修改檔案、不要刪除檔案，也不要執行會改變資料的命令。

完成後，你應該看得到 repo 摘要、測試指令、待確認的計畫，以及工具要求權限時的提示。這就是本章的第一個可驗證成果。

## 學習目標

- 分清 LLM、Provider API、Router、coding agent／harness 與 local runtime。
- 依你已有的帳號、provider 或本機環境選入口，不做總排名。
- 在 demo repo 中完成一次「先讀取 → 看計畫 → 確認 → 小改動 → `git diff` → 復原」的循環。

<details markdown="1">
<summary>展開時間、先備條件、帳號與費用</summary>

- **時間**：第一次只讀取與看計畫，通常可在一個短時段完成；CLI-1 至 CLI-4 可以分幾天慢慢做，不必一次做完。
- **先備條件**：會進入資料夾、看 `git status` 和 `git diff`；手邊有一個可丟棄的 demo repo。
- **帳號**：準備一個所選工具支援的登入方式，或把 agent 接到本機模型 runtime。沒有帳號時，先看下方選擇表和官方 Quickstart。
- **費用**：不要猜。開始前看當日官方 pricing／usage 頁；只有整條流程都留在本機時，才不會產生這次練習的模型 API 費用。
</details>

## 五種身分先分開

<table>
<thead>
<tr><th scope="col">種類</th><th scope="col">白話說法</th><th scope="col">例子</th><th scope="col">本章怎麼用</th></tr>
</thead>
<tbody>
<tr><th scope="row">LLM</th><td>產生答案的模型</td><td>Claude、GPT、Gemini</td><td>提供回答；不管理 repo</td></tr>
<tr><th scope="row">Provider API</th><td>通往一家模型服務的門</td><td>Anthropic API、OpenAI API、Gemini API</td><td>提供請求、認證與計費</td></tr>
<tr><th scope="row">Router</th><td>把請求轉給多個 provider 的入口</td><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a></td><td>不是 LLM 或 coding agent</td></tr>
<tr><th scope="row">Coding agent／harness</th><td>在終端機讀檔、改檔、跑命令的工作台</td><td>Claude Code、Codex、OpenCode、Pi</td><td>會操作工作目錄；先用 demo repo</td></tr>
<tr><th scope="row">Local runtime</th><td>在自己電腦上執行模型的引擎</td><td><a href="https://github.com/ollama/ollama">Ollama</a></td><td>可供 agent 呼叫；不是 agent</td></tr>
</tbody>
</table>

## 依現有條件選入口

<table>
<thead>
<tr><th scope="col">你已有的條件</th><th scope="col">可先看的入口</th><th scope="col">先確認什麼</th></tr>
</thead>
<tbody>
<tr><th scope="row">Anthropic 帳號或 API</th><td><a href="https://code.claude.com/docs/en/quickstart">Claude Code</a></td><td>登入與 permission prompt</td></tr>
<tr><th scope="row">ChatGPT 或 OpenAI API</th><td><a href="https://developers.openai.com/codex/cli">Codex CLI</a></td><td>approval、sandbox、工作目錄</td></tr>
<tr><th scope="row">Google 帳號、API 或 Vertex AI</th><td><a href="https://google-gemini.github.io/gemini-cli/">Gemini CLI</a></td><td>認證與 sandbox</td></tr>
<tr><th scope="row">想換 provider 或用本機模型</th><td><a href="https://opencode.ai/docs">OpenCode</a>、<a href="https://block.github.io/goose/">goose</a>、<a href="https://aider.chat/docs/">Aider</a>、<a href="https://pi.dev/docs/latest">Pi</a></td><td>provider 與權限邊界</td></tr>
<tr><th scope="row">想用 Router 或本機 runtime</th><td><a href="https://openrouter.ai/docs/faq">OpenRouter</a> 或 <a href="https://ollama.com/">Ollama</a></td><td>它們需搭配 coding agent</td></tr>
</tbody>
</table>

<a id="cli-1"></a>
### 動手練習 CLI-1：在 demo repo 內先讀取，再做一個可復原的小改動

**成果：** 你能看到 repo 說明、測試指令與待確認計畫，確認後留下可由 `git diff` 檢查的單一小改動。

<details markdown="1">
<summary>展開 CLI-1 的準備、操作與復原步驟</summary>

1. 建立或複製一個可丟棄的 demo repo。只放 README、少量原始碼與測試；不要放 API key、個資、合約或 production 設定。開始前先執行 `git status --short`，確認沒有別人的未完成改動。
2. 先用上面的「只讀取」請求。對照工具列出的檔案、測試指令與計畫；不清楚的地方先問，不要直接核准。
3. 你確認計畫後，只允許一個小文件改動，例如在 `README.md` 增加一段「如何執行測試」。要求工具先展示 diff，再由你核准。
4. 在終端機執行 `git diff -- README.md`，確認只有預期內容。只有在第 1 步已確認檔案原本乾淨時，才執行 `git restore -- README.md`；最後再用 `git status --short` 確認小改動已復原。

若工具沒有 git，仍要保留原檔備份並逐行比較；不要把同一個 demo repo 同時交給兩個會寫檔的 agent。
</details>

<a id="cli-2"></a>
### 動手練習 CLI-2：讓專案規則被正確讀到

**成果：** 你能用一個短規則檔說明專案用途、禁止事項、測試指令與交付格式，並驗證工具有遵守它。

<details markdown="1">
<summary>展開各 CLI 的專案規則位置與驗證方式</summary>

- Claude Code 讀取專案的 `CLAUDE.md`；Codex 使用 `AGENTS.md`。
- OpenCode 使用 `AGENTS.md`，`CLAUDE.md` 是相容 fallback；不要再建立 `OPENCODE.md` 當作通用規則檔。
- Gemini CLI 常用 `GEMINI.md`；goose、Aider、Hermes Agent、Pi 與 Grok Build 的檔名和載入範圍依各自官方文件設定。
- 規則只留下會改變行為的內容：專案用途、不能做的事、測試指令、交付格式。不要把長篇 API 參考資料塞進每次都載入的規則檔。

在 demo repo 內加入一條可觀察規則，例如「先提出計畫，不修改 `data/`」，再提出一個會觸發它的請求。最後檢查 agent 的回應與 `git diff`。
</details>

<a id="cli-3"></a>
### 動手練習 CLI-3：用第二個 harness 重跑同一個請求

**成果：** 你能記錄兩個工具在模型／provider、權限提示、sandbox 與輸出格式上的差異，而不是用主觀分數選贏家。

<details markdown="1">
<summary>展開第二個 CLI 的公平比較步驟</summary>

在同一個乾淨 demo repo、同一份 prompt、同一組檔案上各跑一次。記錄日期、CLI 版本、LLM、provider、登入方式、approval／sandbox 設定、是否實際改檔，以及 `git diff` 結果。不要同時啟動兩個會寫檔的 session；每次完成後復原，再開始下一次。
</details>

<a id="cli-4"></a>
### 動手練習 CLI-4：用假憑證觀察認證失敗

**成果：** 你能區分「登入失敗」「provider API key 失敗」「模型名稱不存在」與「權限／sandbox 阻擋」，且不會把真正的秘密貼進 prompt 或 log。

<details markdown="1">
<summary>展開安全的認證錯誤實驗</summary>

在一次性終端機 session 中使用明確標示為假的值，例如 `not-a-real-key`；不要改動正式的 shell 設定或共享 `.env`。先觀察未登入錯誤，再在已登入的 CLI 中輸入一個官方不存在的模型名稱，記下錯誤類型與補救指引。測試完立刻清除假值，並確認 shell history、工作目錄與 log 沒有真 key。

使用有效憑證的請求可能產生費用；第一次練習可使用本機 Ollama 或 provider 的明確免費額度，並以當日官方價格與實際 usage 為準。
</details>

## 需要完整比較時，再看參考表

A1 只教你安全開始，不在兩個頁面重複維護同一份易變資料。9 個工具的登入、provider、sandbox 與官方來源集中放在 [`CLI Agents 參考指南`](../../resources/cli-agents-guide.md)。官方資料查核日：**2026-08-27 UTC**。

<details markdown="1">
<summary>展開「工具、Router、local runtime」的最短辨識法</summary>

- Claude Code、Codex、Gemini CLI、OpenCode、goose、Aider、Hermes Agent、Grok Build、Pi：會接收任務並操作工作目錄的 CLI agent／harness。
- OpenRouter：替 agent 把請求送到 provider 的 Router，不會替你管理檔案權限。
- Ollama：在本機跑模型的 runtime，不會自己讀 repo；要由支援它的 agent 呼叫。
- 不確定時，只問三句：誰執行模型？誰轉送請求？誰能讀寫我的檔案？
</details>

## 必修閱讀與費用邊界

<details markdown="1">
<summary>展開官方閱讀、帳號與預算說明</summary>

- [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart) 與 [permissions](https://code.claude.com/docs/en/permissions)
- [Codex CLI](https://developers.openai.com/codex/cli)
- [Gemini CLI authentication](https://google-gemini.github.io/gemini-cli/docs/get-started/authentication.html) 與 [sandbox 設定](https://google-gemini.github.io/gemini-cli/docs/get-started/configuration.html)
- [OpenCode 文件](https://opencode.ai/docs) 與 [goose 文件](https://block.github.io/goose/)
- [Aider 文件](https://aider.chat/docs/)、[Hermes Agent 文件](https://hermes-agent.nousresearch.com/docs/)、[Grok Build repo](https://github.com/xai-org/grok-build)、[Pi 文件](https://pi.dev/docs/latest)
- [OpenRouter FAQ](https://openrouter.ai/docs/faq) 與 [Ollama](https://ollama.com/)

每次 cloud 請求的單次費用與本章總費用都會因帳號、provider、模型、輸入輸出 token 與訂閱額度而變動；練習前查當日官方價格或 usage 頁面。只有當 agent 與 provider 都設定成只連本機 Ollama，而且沒有另外呼叫雲端服務時，才不會產生這次練習的模型 API 費用；檔案與命令權限仍要照常檢查。
</details>

## ✅ 進 A2 前的自我檢查

- [ ] 我能用自己的話分清五種身分，知道 OpenRouter 不是 LLM、Ollama 不是 coding agent。
- [ ] 我在 demo repo 完成一次只讀取的說明與計畫，沒有把秘密交給工具。
- [ ] 我確認一個小改動的 diff，並能復原它。
- [ ] 我知道所選 CLI 的登入方式、provider、approval／sandbox 設定。

完成後進入 [A2 — 建立可重複使用的 CLI 工作流程](A2-cli-workflow.md)。想再比較工具的官方狀態，回看 [`resources/cli-agents-guide.md`](../../resources/cli-agents-guide.md)。

> 安全底線：不要在含有秘密或 production 權限的目錄中做第一次實驗；不要使用跳過所有確認的模式；不要把 API key、瀏覽器 token 或 auth 檔貼進 prompt、issue、log 或 git。
