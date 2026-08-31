> **繁體中文** | [简体中文](./setup-guide.zh-Hans.md) | [English](./setup-guide.en.md)

# 🚀 從零開始 — 給沒有開發背景的設定指南

> [← 回主路線 README](../README.md)

<!-- freshness: canonical=resources/setup-guide.md; verified_on=2026-08-30; scope=install-paths,api-keys,authentication,provider-entrypoints,project-status; max_age_days=90 -->

這一頁不是叫你把所有工具都裝一遍。你只要先選一扇門，完成一個小結果。

已經會用 Python、Git 和 terminal，也知道怎麼保護 **API Key（API 金鑰）**？可以直接去 [Stage 1](../stages/01-llm-basics.md)。

## 📌 這份指南會帶你完成什麼

- 分清 Web Chat、Desktop、IDE、**CLI Agent（命令列代理）** 和 **API（應用程式介面）**，不再把它們當成同一種工具。
- 知道 **API Key（API 金鑰）** 為什麼像密碼，以及不能放在哪裡。
- 用 `uv` 準備 Python 3.12，不必先學一大堆套件管理。
- 複製一份 Python 程式，真的收到模型回覆。
- 知道何時該去 Stage 1，何時該去 Stage 5。

<details markdown="1">
<summary>查看時間、裝置與先備條件</summary>

- 只用 Web Chat：幾分鐘即可開始。
- 完成 API quick start：通常需要約 20–40 分鐘；帳號審核、付款設定與網路狀況可能讓時間變長。
- 需要：可以安裝軟體的 Windows、macOS 或 Linux 電腦，以及可開啟供應商 Console 的帳號。
- 不需要：先會寫程式、先懂 Git branch、先裝完整 IDE。

公司或學校電腦可能禁止安裝程式或建立 API key。遇到這種情況，先問管理員，不要繞過限制。

</details>

## 🚪 先選一扇門

五扇門是平行選擇，不是五個一定要依序完成的等級。

| 你想做什麼 | 這扇門是什麼 | 第一個動作 |
|---|---|---|
| 先和模型聊天 | **Web Chat**：在瀏覽器裡對話 | 開啟 [Claude](https://claude.ai)、[ChatGPT](https://chatgpt.com)、[Gemini](https://gemini.google.com) 或 [Le Chat](https://chat.mistral.ai) |
| 在電腦 App 裡聊天或處理檔案 | **Desktop App**：裝在電腦上的聊天介面 | 從產品的官方下載頁安裝 |
| 寫 code 時請 AI 在旁邊協助 | **IDE Assistant**：住在 editor 裡 | 先看 [開發者路線](../branches/for-developer.md) |
| 讓 Agent 在指定資料夾讀檔、改檔、跑命令 | **CLI Agent**：在 terminal 裡工作 | 先看 [CLI Agents 指南](cli-agents-guide.md) |
| 自己寫程式呼叫模型 | **API**：程式和模型服務說話的入口 | 繼續做下面 A → B → C |

<details markdown="1">
<summary>查看 Web、Desktop、IDE 與 CLI 的完整官方入口</summary>

下表是入口清單，不是排名。推薦度表示「這份學習地圖是否適合拿它當起點」。

<table>
<thead><tr><th scope="col">類型</th><th scope="col">官方入口／專案</th><th scope="col">先知道什麼</th><th scope="col">推薦度</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Web Chat</th><td><a href="https://claude.ai">Claude</a></td><td>雲端聊天介面；方案與功能依帳號、地區而異</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://chatgpt.com">ChatGPT</a></td><td>雲端聊天介面；ChatGPT 訂閱不等於 OpenAI API 額度</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://gemini.google.com">Gemini</a></td><td>雲端聊天介面；連接服務前先看資料權限</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://chat.mistral.ai">Le Chat</a></td><td>Mistral 的雲端聊天介面</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Desktop</th><td><a href="https://claude.com/download">Claude Desktop</a></td><td>Windows、macOS 與 Linux 的現行入口以官方頁為準</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://chatgpt.com/download">ChatGPT Desktop</a></td><td>平台需求以官方下載頁為準</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://gemini.google/mac">Gemini for macOS</a></td><td>目前是 macOS App；其他系統可使用 Web</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://lmstudio.ai/download">LM Studio</a></td><td>本機模型 runtime 與圖形介面；仍要管理模型、硬體與檔案權限</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="5">IDE／Editor</th><td><a href="https://cursor.com">Cursor</a></td><td>AI editor；確認每次修改與 terminal 動作</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://windsurf.com/editor">Windsurf</a></td><td>AI editor；方案與權限以官方文件為準</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://cline.bot">Cline</a></td><td>VS Code coding agent；從低權限開始</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://zed.dev/ai">Zed AI</a></td><td>Zed editor 的 AI 功能</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/features/copilot">GitHub Copilot</a></td><td>可在 GitHub、IDE 與其他介面使用；各介面的權限不同</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="7">CLI Agent</th><td><a href="https://code.claude.com/docs/en/quickstart">Claude Code</a></td><td>先保留 permission prompt；從小資料夾開始</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/openai/codex">OpenAI Codex</a></td><td>coding agent；確認 sandbox、approval 與 diff</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/google-gemini/gemini-cli">Gemini CLI</a></td><td>Gemini 的開源 terminal agent</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/anomalyco/opencode">OpenCode</a></td><td>多 Provider coding agent／harness，不是模型 Router</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/aaif-goose/goose">goose</a></td><td>可連 Provider 與 extensions；先縮小工具權限</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://aider.chat/docs/">Aider</a></td><td>Git-first pair programmer；auto-commit 不代表可跳過 review</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/NousResearch/hermes-agent">Hermes Agent</a></td><td>一般用途 agent；先在隔離環境試小任務</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
</table>

</details>

## 🧩 先分清七個核心詞

- **Chat Surface（聊天介面）**：你打字、貼檔案、看回覆的畫面，例如 Claude.ai。它不是模型 API。
- **API（應用程式介面）**：程式送出請求、拿回結果的入口。人通常不直接在 API 畫面聊天。
- **API Key（API 金鑰）**：讓服務知道「這個程式可以使用哪個帳號」的秘密字串。拿到它的人可能花到你的額度。
- **Environment Variable（環境變數）**：把設定交給程式看的小抽屜。程式可以讀它，不必把秘密寫進 source code。
- **Runtime（執行環境）**：真正把程式跑起來的東西；Python 是一種 runtime，Ollama 是本機模型 runtime。
- **Package Manager（套件管理器）**：幫你安裝與執行別人寫好的套件。這份指南使用 `uv`。
- **CLI Agent（命令列代理）**：在 terminal 裡讀檔、改檔、執行工具的 Agent。它不是 API Provider，也不是單一模型。

## 📚 必讀與官方起點

這五個入口直接保持可見；遇到版本差異時，以官方頁為準。

<table>
<thead><tr><th scope="col">類別</th><th scope="col">官方資源</th><th scope="col">用它解決什麼</th><th scope="col">推薦度</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Claude API</th><td><a href="https://platform.claude.com/docs/en/get-started">Claude API Quickstart</a></td><td>建立 key、送出第一個請求</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://platform.claude.com/docs/en/api/sdks/python">Anthropic Python SDK</a></td><td>確認 Python 需求、環境變數與現行程式形狀</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">Python 工具</th><td><a href="https://docs.astral.sh/uv/getting-started/installation/">uv Installation</a></td><td>依作業系統安裝或更新 uv</td><td>⭐⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">CLI 入門</th><td><a href="https://code.claude.com/docs/en/terminal-guide">Claude Code Terminal Guide</a></td><td>第一次開 terminal、切資料夾與執行命令</td><td>⭐⭐⭐⭐⭐</td></tr></tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">秘密安全</th><td><a href="https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning">GitHub Secret Scanning</a></td><td>了解 secret 為什麼不能進 Git 歷史</td><td>⭐⭐⭐⭐</td></tr></tbody>
</table>

<a id="a--申請第一個-api-key約-10-分鐘"></a>

## 🛠 A — 拿到第一把 API Key

這條 quick start 使用 Anthropic Claude，因為 Stage 1 的 canonical API 路徑也使用它。Claude.ai 訂閱和 Claude API 帳單是兩件事。

1. 開啟 [Claude Console](https://platform.claude.com/)。
2. 進入 **API Keys**，建立一把只給這個練習使用的 key。
3. 若畫面可以選 owner、workspace 或期限，使用最小範圍與最短合理期限。
4. 複製 key，先放進密碼管理器；不要貼到聊天視窗。
5. 先在 Console 查看 billing／usage；若帳戶提供 spend limit 或提醒，把它設在你能接受的小額範圍，再開始呼叫 API。

**API Key 三不規則：**

- **不貼**到 chat、群組、email、issue 或截圖。
- **不寫**進 Python source code，也不進 Git 歷史。
- **不共用**同一把 key 給很多專案；不用時撤銷。

<details markdown="1">
<summary>查看其他 Cloud API 與本機 Runtime</summary>

下表只寫現行官方入口。價格、免費額度與可用模型請點進官方頁查看，不在這份入門指南凍結。

<table>
<thead><tr><th scope="col">類型</th><th scope="col">官方入口</th><th scope="col">Compatibility／限制</th><th scope="col">推薦度</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="7">Cloud API</th><td><a href="https://platform.openai.com/docs/quickstart">OpenAI API</a></td><td>官方 SDK 與 API；ChatGPT 訂閱不等於 API billing</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://ai.google.dev/gemini-api/docs/openai">Gemini API</a></td><td>Google 官方提供 OpenAI libraries compatibility 說明</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://docs.api.nvidia.com/nim/re/reference/llm-apis">NVIDIA NIM</a></td><td>依 endpoint 查看支援的 API shape 與模型</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://api-docs.deepseek.com/">DeepSeek API</a></td><td>官方文件提供 OpenAI-compatible 使用方式</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://platform.kimi.com/docs/api/overview">Kimi API</a></td><td>地區、endpoint 與模型以官方 Console 為準</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://help.aliyun.com/en/model-studio/base-url">Alibaba Model Studio／Qwen</a></td><td>依區域使用對應 base URL；官方提供 OpenAI-compatible endpoint</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://docs.z.ai/api-reference/introduction">Z.ai／GLM API</a></td><td>依官方 reference 使用現行 endpoint</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody><tr><th scope="rowgroup" rowspan="1">本機 Runtime</th><td><a href="https://docs.ollama.com/api/openai-compatibility">Ollama</a></td><td>只相容 OpenAI API 的一部分；需另下載本機模型</td><td>⭐⭐⭐⭐⭐</td></tr></tbody>
</table>

本機推理沒有供應商模型 API 帳單，但硬體、電力、下載時間、裝置安全、檔案與 log 仍由你負責。完整路徑看 [Cookbook 的本機 LLM walkthrough](cookbook.md#6-本機-llm--cli-agent-快速-walkthrough)。

這個 repo 的目前練習標籤是：Stage 1–2 用 `gemma4:e4b`，Stage 3–6 的 Tool Use／ReAct 用 `qwen2.5:3b`，Stage 7 的 Eval／Observability／Streaming／Deploy 用 `qwen3.5:4b`。這是教材預設，不是通用模型排名。

</details>

<a id="b--裝本機環境約-10-分鐘"></a>

## 🛠 B — 裝好 Python 執行環境

這裡用 `uv` 同時管理 Python 與套件。先安裝 `uv`：

macOS、Linux 或 WSL：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows PowerShell：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

關掉並重開 terminal，再依序複製：

```bash
uv --version
uv python install 3.12
uv run --python 3.12 python --version
```

最後一行看到 `Python 3.12`，就完成 B。`uv` 也支援其他 Python 版本；這份教學固定 3.12，減少初學時的套件相容問題。

<details markdown="1">
<summary>安裝失敗時，查看各作業系統替代方式</summary>

- Windows 可使用 `winget install --id=astral-sh.uv -e`。
- macOS 可使用 `brew install uv`。
- 也可以從 [uv 官方安裝頁](https://docs.astral.sh/uv/getting-started/installation/) 下載 release binary。
- 如果公司封鎖安裝 script，停止並請管理員提供核准方式，不要關閉安全軟體硬闖。

已經有 Python 3.10–3.14 也沒關係，`uv` 會尋找可用的 Python；上面的命令只是替這份教學準備一致的 3.12。

</details>

<a id="c--跑第一個-hello-claudepy約-5-分鐘"></a>

## 🛠 C — 跑第一個 `hello-claude.py`

### 1. 建立練習資料夾

PowerShell、macOS 與 Linux terminal 都可以使用：

```bash
mkdir my-first-llm
cd my-first-llm
```

### 2. 先建立 `.gitignore`

建立名為 `.gitignore` 的檔案，貼上：

```gitignore
.env
__pycache__/
*.pyc
```

先排除 `.env`，再建立 secret 檔，可以降低誤加進 Git 的機會。

### 3. 再建立 `.env`

建立名為 `.env` 的檔案。把 placeholder 換成你自己的 key；不要把真 key 貼到這份文件或 commit：

```dotenv
ANTHROPIC_API_KEY=PASTE_YOUR_KEY_HERE
```

### 4. 複製 Python 程式

建立 `hello-claude.py`：

```python
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()  # 從 ANTHROPIC_API_KEY 讀取 key

message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=120,
    messages=[{"role": "user", "content": "請用一句話介紹你自己。"}],
)

for block in message.content:
    if block.type == "text":
        print(block.text)
```

### 5. 直接執行

```bash
uv run --python 3.12 --with anthropic --with python-dotenv python hello-claude.py
```

看到模型印出一句介紹，就代表 Python、套件、API key 與網路都接通了。

<details markdown="1">
<summary>查看常見錯誤與安全復原</summary>

| 你看到什麼 | 通常代表什麼 | 先做什麼 |
|---|---|---|
| `401`／`authentication_error` | key 沒讀到、失效或貼錯 | 撤銷有疑慮的 key；確認檔名是 `.env`，再建立新 key |
| `429`／`rate_limit_error` | 用量、速率或帳戶額度限制 | 停止重試，回 Console 看 usage／billing，再按錯誤訊息等待 |
| `ModuleNotFoundError` | 沒用到這次 `uv run --with ...` 的環境 | 完整複製執行命令，不要只跑 `python hello-claude.py` |
| `uv` 找不到 | 安裝後的 terminal 還沒讀到新 PATH | 關掉並重開 terminal；再看 uv 官方安裝頁 |
| 連線錯誤 | 網路、proxy、防火牆或服務狀態 | 先看供應商 status page；公司／學校網路請問管理員 |

如果 key 曾出現在 Git、聊天、截圖或公開 log，不能只把文字刪掉；請立刻在 Console 撤銷它並建立新 key。

</details>

<a id="d--第一次裝-claude-code約-10-分鐘stage-5--for-developer-會用到"></a>

## 🛠 D — 第一次開 Claude Code

這是 Stage 5 的入口，不是完成 API quick start 的必修。Claude Code 現在優先使用 native installer，不必先裝 Node.js。

macOS、Linux 或 WSL：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell：

```powershell
irm https://claude.ai/install.ps1 | iex
```

安裝後先跑 `claude --version`，再到一個小型練習資料夾執行 `claude`。完整條件與其他安裝法看 [Claude Code Installation](https://code.claude.com/docs/en/installation)。

<details markdown="1">
<summary>查看登入、系統需求與第一份 CLAUDE.md</summary>

Claude Code 目前需要符合官方列出的 Claude plan、Console account 或支援的 cloud provider；免費 Claude.ai plan 不包含 Claude Code。執行 `claude` 後依瀏覽器提示登入，詳細身分差異看 [Authentication](https://code.claude.com/docs/en/authentication)。

官方現行基本需求包含支援的 Windows、macOS 或 Linux、4 GB 以上 RAM、網路連線與可用 shell。Windows 可原生使用 PowerShell；需要 Linux toolchain 或 sandbox 時再考慮 WSL 2。

你可以在 project root 建立 `CLAUDE.md`：

```markdown
# 這個 project 要做什麼
這是一個學習用的小專案。

# 工作規則
- 先說明要改哪些檔案，再開始修改。
- 不要讀取或改寫 `.env`。
- 不要自動 commit；完成後讓我先看 diff。
- 刪檔、安裝套件或連網前先問我。

# 完成條件
- 執行最小相關測試。
- 說明改了什麼、測了什麼、還有什麼風險。
```

`CLAUDE.md` 是 project instructions，不是安全 sandbox。工具權限、approval、版本控制與人工 review 仍要保留。

</details>

<a id="e--第一個-skill-範例約-5-分鐘stage-53-會用到"></a>

## 🛠 E — 建立第一個 Skill

這是 Stage 5.3 的延伸。**Skill（技能包）** 是有名稱、描述與操作指示的可重用資料夾；它不會自動變成安全權限。

第一個動作：建立 `.claude/skills/hello-skill/SKILL.md`。

<details markdown="1">
<summary>查看可直接複製的 SKILL.md</summary>

```markdown
---
name: hello-skill
description: 當使用者明確請你打招呼時，用兩種語言回覆。
---

當使用者請你打招呼時：

1. 用繁體中文說一次 hello。
2. 用英文說一次 hello。
3. 不讀檔、不連網、不執行其他工具。
```

在該 project 開啟 `claude`，輸入「請打招呼」。看到兩種語言，而且沒有多做其他動作，就完成了。

更完整的責任邊界看 [Stage 5.3 — Skills](../stages/05-claude-code-ecosystem.md#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層)，更多範例看 [Cookbook](cookbook.md)。

</details>

## ✅ 完成檢查

做到下面任一條，就可以離開這份指南，不必把所有入口都裝完：

- 我已經能在 Web Chat 完成一次對話，而且知道它不是 API。
- 我完成 A → B → C，看到 `hello-claude.py` 印出模型回覆。
- 我選擇 CLI 路徑，能說出 CLI Agent 的工作資料夾與權限範圍。

還要確認：

- 真正的 API key 沒有出現在 source code、Git、聊天、截圖或 log。
- 我知道如何撤銷 key，也知道 API billing 和聊天訂閱分開。
- 我沒有因為工具能自動執行，就跳過 diff、測試或人工確認。

## 接下來去哪

| 你現在想做什麼 | 下一站 |
|---|---|
| 理解模型、Token、Context Window 與 API | [Stage 1 — LLM 基礎](../stages/01-llm-basics.md) |
| 直接學 Prompt | [Stage 2 — Prompt Engineering](../stages/02-prompt-engineering.md) |
| 用 CLI Agent 工作 | [Track A1 — CLI 入門](../tracks/cli/A1-cli-intro.md) |
| 理解 Claude Code、MCP、Skills、Plugins 與 Subagents | [Stage 5 — Claude Code 生態系](../stages/05-claude-code-ecosystem.md) |
| 使用本機模型 | [Cookbook：本機 LLM walkthrough](cookbook.md#6-本機-llm--cli-agent-快速-walkthrough) |
| 還分不清 OpenRouter、Ollama、OpenCode 或 Pi | [Glossary：先分清五種工具身分](glossary.md#-先分清五種工具身分) |
