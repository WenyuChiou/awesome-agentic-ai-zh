# Cookbook — 把概念變成真的成果

> **繁體中文** | [简体中文](./cookbook.zh-Hans.md) | [English](./cookbook.en.md)

<!-- freshness: canonical=resources/cookbook.md; verified_on=2026-08-30; scope=skills,mcp,documents,gemini-notebook,zotero,local-runtime,cli-tools; max_age_days=90 -->

這份 Cookbook 不要求你一次讀完。先選一個想做的成果，複製它的第一個動作；需要更多步驟時，再打開選單。

如果名詞還不熟，先回 [Stage 5：Claude Code 生態系](../stages/05-claude-code-ecosystem.md)。想比較 OpenRouter、Pi、OpenCode 與 Ollama，直接看[完整 CLI Agent 指南](cli-agents-guide.md)。

## 📌 這份 Cookbook 幫你做什麼

**Recipe（實作配方）**是一條從「我想做什麼」走到「我怎麼知道完成了」的短路線。完成任一份 Recipe，你都會得到一個可以檢查的成果，而不是只看懂一段說明：

- 一張可重複使用的操作卡。
- 一個能被 Agent 呼叫的小工具。
- 一份文件、研究筆記或文獻流程。
- 一個在自己電腦上運作的 CLI Agent。

你還會看到 **Skill（操作卡）**、**MCP Server（工具轉接站）**和 **Coding Agent（程式代理）**。它們分別告訴 Agent 怎麼做、替 Agent 接上工具，以及代替你讀檔、改檔和檢查結果。

## 🎯 先選一份 recipe

| 你想完成什麼 | 從哪裡開始 | 主要風險 |
|---|---|---|
| 讓 Claude 記住固定做法 | [1. 第一個 Skill](#1-寫你的第一個-skill) | 規則寫得太模糊 |
| 讓 Agent 呼叫自己的 Python 工具 | [2. 第一個 MCP server](#2-寫你的第一個-mcp-server) | 把不該開的權限交出去 |
| 產生 Word／Excel／PowerPoint／PDF | [3. Office Docs Workflow](#3-office-docs-workflow) | 沒有打開成品人工檢查 |
| 從自己的資料得到有引用的答案 | [4. Gemini Notebook Workflow](#4-gemini-notebook-workflow) | 社群整合可能突然失效 |
| 從 Zotero 搜尋或整理文獻 | [5. Zotero Workflow](#5-zotero-workflow) | 寫入前沒有預覽變更 |
| 用本機模型協助修改程式 | [6. 本機 LLM＋CLI Agent](#6-本機-llm--cli-agent-快速-walkthrough) | 模型能力或電腦記憶體不足 |

## 🧩 六個核心詞

- **Recipe（實作配方）**：一條從「我想做什麼」走到「我怎麼知道完成了」的短路線。
- **Skill（操作卡）**：放在 `SKILL.md` 裡的可重複指令。Agent 需要時才讀它。
- **MCP Server（工具轉接站）**：把程式、資料或服務包成 Agent 能看懂的 tool、resource 或 prompt。
- **Community Integration（社群整合）**：不是產品官方提供的橋接工具。可以很好用，但上游一改就可能壞。
- **Model Runtime（模型執行環境）**：真正載入並執行模型的程式，例如 Ollama；它不是 Coding Agent。
- **Coding Agent（程式代理）**：讀檔、改檔、跑指令並反覆檢查結果的助手，例如 Claude Code、OpenCode、Pi 或 Aider。

<details markdown="1">
<summary>⏱️ 展開：時間、環境與安全底線</summary>

- 每份 recipe 約 20–50 分鐘；先完成最短路徑，再做進階選項。
- 建議準備 Git、Python 3.11+、Node.js 20+；只有用到對應 recipe 才安裝。
- 練習只用測試資料。不要把密碼、API key、未公開論文或私人文件貼進不信任的工具。
- 任何會刪除、寄送、發布或大量改檔的動作，都要先看 diff 或 preview。

</details>

---

## 1. 寫你的第一個 Skill

**成果：**做出一張專案內可共用的操作卡，並親手觸發一次。

先建立資料夾：

```bash
mkdir -p .claude/skills/summarize-changes
```

<details markdown="1">
<summary>展開完整步驟、測試與常見問題</summary>

建立 `.claude/skills/summarize-changes/SKILL.md`：

```markdown
---
description: Summarize uncommitted changes and flag risks. Use when the user asks what changed or requests a diff review.
---

## Instructions

1. Read the current git diff.
2. Explain the change in three short bullets.
3. List risks, missing tests, and files that should not be committed.
4. If there is no diff, say so. Do not invent changes.
```

啟動 Claude Code 後輸入：

```text
/summarize-changes
```

也可以問「我剛剛改了什麼？」測試自動觸發。Claude Code 會即時偵測既有 skill 目錄裡的 `SKILL.md` 變更，通常不用重啟；只有 session 開始時整個 `.claude/skills/` 尚不存在，才需要重啟一次。

成功標準：回答真的根據目前 diff，而且有說「哪裡可能出錯」。

常見問題：

| 症狀 | 先檢查什麼 |
|---|---|
| `/summarize-changes` 不存在 | 路徑是否正好是 `.claude/skills/summarize-changes/SKILL.md` |
| 常常亂觸發 | `description` 是否清楚寫出「何時使用」 |
| 指令太長 | 把背景資料搬到同資料夾的參考檔，需要時再讀 |

先用 project Skill 最安全：它只跟著這個 repo。確定多個專案都需要同一套做法後，才放到 personal path `~/.claude/skills/<name>/SKILL.md`。

| 容易混淆的東西 | 它解決什麼 | 何時使用 |
|---|---|---|
| 一次性 Prompt | 只交代眼前這一次任務 | 做法不會重複使用 |
| **Skill** | 保存「遇到這種工作要怎麼做」 | 同一做法會在專案裡反覆出現 |
| **MCP Server** | 提供新的 typed tool、資料或服務 | Agent 需要呼叫外部程式或 API |

Skill 可以指揮 Agent 使用既有工具，但 Skill 本身不是新的 API。不要再用「Skill 不能讀檔、MCP 才能讀檔」這種過度簡化來分兩者。

想做正式 eval，可用固定的「應觸發／不應觸發」句子測 description，再檢查回答是否遵守四個步驟。

</details>

---

## 2. 寫你的第一個 MCP server

**成果：**做出一個兩數相加的 MCP tool，並讓 Claude Code 看見它。

先在乾淨的 Python 環境安裝目前穩定的 MCP SDK：

```bash
python -m pip install "mcp>=2,<3"
```

<details markdown="1">
<summary>展開 server 程式、連線方式與錯誤排查</summary>

建立 `server.py`：

```python
from mcp.server import MCPServer

mcp = MCPServer("hello-mcp")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


if __name__ == "__main__":
    mcp.run()
```

這段程式很短，是因為 MCP v2 會從 **type hint** 產生 input schema、把 **docstring** 當成 tool description，並把回傳值包成 MCP content。參數名稱、型別與 docstring 寫錯，Agent 就可能選錯工具或傳錯資料。

把這個本機 stdio server 加進 Claude Code：

```bash
claude mcp add --transport stdio hello-mcp -- python server.py
claude mcp get hello-mcp
```

進 Claude Code 後問：「用 `add` 算 27 + 15。」成功時應得到 `42`，而且你能在 tool call 記錄看見參數。

MCP v2 的高階 class 是 `MCPServer`，正確 import 是 `from mcp.server import MCPServer`。舊的 `FastMCP` 教學與舊 import 路徑不要混用。

安全底線：

- tool 只收完成任務需要的參數。
- 檔案工具限制可讀寫目錄。
- 寫入、付款、寄信或刪除動作先要求人工核准。
- 第三方 MCP server 會接觸你的資料；安裝前先看來源與權限。

| Transport | 適合哪裡 | 驗證提醒 |
|---|---|---|
| **stdio** | 同一台電腦上的 Claude Code／desktop host | 第一個 server 用這條；通常不在 transport 內做 OAuth |
| **Streamable HTTP** | 遠端、多人或服務化部署 | 依現行 MCP authorization 規格設計身份驗證；不要照抄舊 HTTP＋SSE 教學 |

需要 API key 時，從環境變數讀取，不要把 secret 寫進 `server.py`、設定檔範例或 Git。

若 `claude mcp get` 顯示失敗，先直接跑 `python server.py` 看 import error，再確認 `--` 後面的啟動指令與 Python 環境一致。

</details>

---

## 3. Office Docs Workflow

**成果：**用一份測試資料產生文件，再用真正的 Office／PDF 閱讀器打開檢查。

先取得 Anthropic 的官方參考實作：

```bash
git clone --depth 1 https://github.com/anthropics/skills.git anthropic-skills-reference
```

<details markdown="1">
<summary>展開 skill 安裝、範例 prompt 與品質檢查</summary>

`anthropics/skills` 裡的 `docx`、`xlsx`、`pptx`、`pdf` 是 Anthropic 生產環境使用的複雜 skill 參考。這四個資料夾是 **source-available**，不是 Apache-2.0 開源範例；先讀各自授權與 `SKILL.md`。

要在專案內試一個 skill，請把那個 skill 本身放到正確層級，不要把整個 repo 多包一層：

```bash
mkdir -p .claude/skills
cp -R anthropic-skills-reference/skills/docx .claude/skills/docx
```

PowerShell 可改用：

```powershell
New-Item -ItemType Directory -Force .claude/skills
Copy-Item -Recurse anthropic-skills-reference/skills/docx .claude/skills/docx
```

四個資料夾不是同一件事。先只安裝你要練習的那一個：

| Skill | 第一個小任務 | 完成時要檢查 |
|---|---|---|
| `docx` | 把測試資料做成一頁摘要 | 標題、段落、表格與分頁 |
| `xlsx` | 算出一小張表的合計並保留公式 | 公式、儲存格型別與數值 |
| `pptx` | 依 3 點大綱做 3 張投影片 | 文字沒有溢出，圖片與來源正確 |
| `pdf` | 從公開 PDF 摘出 3 個主張 | 頁碼、引用與原文能對上 |

可直接複製的 DOCX 任務：

```text
用我提供的測試資料做一份一頁 DOCX 摘要。
保留標題、三個重點與來源欄；沒有資料就標「待補」，不要猜。
完成後重新打開檔案，確認沒有截字、空白頁或壞掉的表格。
```

檢查順序：內容正確 → 公式／數字正確 → 版面沒有溢出 → 檔案可重新開啟。只看到「檔案已建立」不算完成。

如果 skill 沒出現，確認路徑是 `.claude/skills/docx/SKILL.md`。Claude 產品內建的文件能力與你 clone 下來的參考版本可能不同，所以不要宣稱兩者一定產生完全相同的結果。

</details>

---

## 4. Gemini Notebook Workflow

**成果：**放入自己的來源，取得有引用、可以回頭核對的答案。

Google 已把 NotebookLM 更名為 **Gemini Notebook**；部分套件與網址仍保留舊名。先從官方網頁完成一次：

```bash
python -m webbrowser https://notebooklm.google.com
```

上傳兩份公開文件後問：「這兩份來源同意什麼？不同意什麼？每點附來源。」先點引用確認真的對得上原文，再考慮自動化。

<details markdown="1">
<summary>展開社群 CLI 自動化路徑：notebooklm-py</summary>

Google 目前沒有提供這套自動化的公開官方 API。`notebooklm-py` 是社群專案，使用未公開介面，適合個人研究與 prototype；正式流程要準備它突然失效的替代路徑。

```bash
uv tool install "notebooklm-py[browser]"
notebooklm login
notebooklm auth check --test --json
notebooklm create "My Research"
notebooklm use NOTEBOOK_ID
notebooklm source add ./paper.pdf
notebooklm ask "列出三個主要主張，每點附來源。"
```

要讓 Claude Code 或其他支援 Agent Skills 的工具使用它：

```bash
notebooklm skill install
```

登入會打開瀏覽器並保存驗證狀態。不要把 cookie、token 或個人瀏覽器資料提交進 Git。

</details>

<details markdown="1">
<summary>展開另一個瀏覽器 skill 與排錯提醒</summary>

[`PleasePrompto/notebooklm-skill`](https://github.com/PleasePrompto/notebooklm-skill) 以瀏覽器自動化查詢 notebook。它同樣不是 Google 官方整合，而且必須讓瀏覽器完成登入。

選擇方式：

| 需求 | 較適合的入口 |
|---|---|
| 只想可靠閱讀與人工核對 | Gemini Notebook 官方網頁 |
| 想批次新增來源、問答或匯出 | `notebooklm-py` CLI |
| 已使用 Claude Code，想用 skill 呼叫瀏覽器 | `notebooklm-skill` |

遇到登入失效，先回官方網頁確認帳號能正常使用，再依社群專案自己的 auth 指令重新登入。不要用大量重試繞過 Google 的限制。

</details>

---

## 5. Zotero Workflow

**成果：**從本機 Zotero 找到文獻；需要寫入時，先看到並批准變更。

在 Zotero 開啟「Settings → Advanced → Allow other applications on this computer to communicate with Zotero」，再測試：

```bash
curl http://localhost:23119/api/
```

<details markdown="1">
<summary>展開搜尋、Zotero 10+ 寫入授權與安全做法</summary>

本機 API 在 `http://localhost:23119/api/`，離線可用且沒有 Web API rate limit。Zotero 10+ 的本機 API 支援 `POST`、`PUT`、`PATCH`、`DELETE`；過去把它當成唯讀的教學已不適用。

寫入並不是偷偷打開。應用程式必須先向 `/api/local/authorize` 取得 **local API key**，Zotero 會顯示批准視窗。這個 key 和 zotero.org Web API key 不同，而且能寫入你有權編輯的 library，所以：

1. 第一次只做讀取與搜尋。
2. 寫入前列出預計新增、移動或刪除的項目。
3. 讓使用者在 Zotero 視窗批准。
4. 練習後到 Settings → Advanced 按 **Clear Write Authorizations** 撤銷 remembered key。

配合 [`WenyuChiou/zotero-skills`](https://github.com/WenyuChiou/zotero-skills) 時，可先複製這句：

```text
只搜尋，不要修改：找出我 Zotero 裡 2024 年後與 multi-agent evaluation 有關的文獻。
列出 title、year、DOI 和 Zotero item key；找不到的欄位標「未提供」。
```

第二次才試寫入，而且先要求 preview：

```text
準備把剛才的結果加入「agent-evals」collection。
先列出會移動的 item key，不要執行；等我批准後再寫入。
```

`403` 通常是本機 API 未啟用；`401` 是寫入 key 不存在或失效；`428` 代表寫入缺少正確的 `Zotero-Server-ID`。

</details>

---

## 6. 本機 LLM + CLI Agent 快速 walkthrough

**成果：**讓 Coding Agent 使用你電腦上的模型，完成一個可用 Git 回復的小改動。

先安裝 [Ollama](https://ollama.com/) 並下載目前的輕量模型：

```bash
ollama pull gemma4:e4b
```

先分清它們是什麼：

| 名稱 | 它的工作 | 它不是什麼 |
|---|---|---|
| **Ollama** | 在本機載入並執行模型的 runtime | 不會自己讀 repo、改檔或跑測試 |
| **OpenRouter** | 用一個 API 帳戶路由多家雲端模型與 provider | 不是本機模型，也不是終端機 Coding Agent |
| **OpenCode／Pi／Aider** | 讀檔、改檔、跑指令的 Coding Agent | 本身不是模型；仍要接本機或雲端模型 |
| **Claude Code** | 使用 Claude 的 Coding Agent | 官方路徑不能直接把模型切成 Ollama |

<details markdown="1">
<summary>展開主要路徑：OpenCode＋Ollama</summary>

OpenCode 是會讀檔、改檔與跑指令的 Coding Agent；Ollama 是在本機跑模型的 runtime。先安裝 OpenCode，再用 `opencode` 啟動：

```bash
curl -fsSL https://opencode.ai/install | bash
opencode
```

OpenCode 會自動尋找 `http://127.0.0.1:11434` 的 Ollama。進入 TUI 後選 `ollama/gemma4:e4b`，再到一個已經用 Git 管理的練習 repo，貼上：

```text
只修改 README.md：新增一行「Local agent test」。
先說你要改哪裡；修改後顯示 diff，不要 commit。
```

成功標準：只有 README 被改、diff 符合要求、`git status` 沒有陌生檔案。模型小時，任務也要小；一次只改一件事。

</details>

<details markdown="1">
<summary>展開 Aider 替代路徑、Pi／OpenRouter入口與排錯</summary>

Aider 官方建議使用 `aider-install`，Ollama model prefix 使用 `ollama_chat/`：

```bash
python -m pip install aider-install
aider-install
aider --model ollama_chat/gemma4:e4b
```

其他入口：

- [Pi](https://github.com/earendil-works/pi) 是可擴充的 Agent harness 與 Coding Agent；它預設繼承啟動者權限，敏感專案要另外使用 sandbox 或 container。
- [OpenRouter](https://openrouter.ai/docs/quickstart) 提供多模型統一 API 與 provider routing；它會產生雲端費用，資料政策也取決於所選 provider。
- [完整 CLI Agent 指南](cli-agents-guide.md) 說明何時選 Claude Code、OpenCode、Pi、Aider、OpenRouter 或本機 runtime。

常見問題：

| 症狀 | 先做什麼 |
|---|---|
| 找不到 Ollama model | 跑 `ollama list`，確認 tag 正好是 `gemma4:e4b` |
| 回答很慢或記憶體不足 | 改用 `gemma4:e2b`，並縮小任務與 context |
| Agent 改太多檔案 | 立即停止，查看 `git diff`；把任務縮成一檔一改 |
| tool calling 不穩 | 改用 Stage 3 建議、且確認支援 tool calling 的模型 |

</details>

---

## 📚 必修閱讀

這些是上面指令的事實來源，不需要一次讀完；做哪份 recipe，就先讀那一列。

<small>資料查核：2026-08-30 UTC</small>

| 來源 | 先看什麼 | 編輯評分 |
|---|---|---|
| [Claude Code — Skills](https://code.claude.com/docs/en/slash-commands) | 路徑、觸發方式與 live change detection | ⭐⭐⭐⭐⭐ |
| [MCP Python SDK v2 — What’s new](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/whats-new.md) | `MCPServer` import 與 v1→v2 差異 | ⭐⭐⭐⭐⭐ |
| [Anthropic Skills](https://github.com/anthropics/skills) | Skill 結構與文件 skill 的授權 | ⭐⭐⭐⭐⭐ |
| [Google — NotebookLM is now Gemini Notebook](https://blog.google/innovation-and-ai/products/gemini-notebook/notebooklm-gemini-notebook/) | 產品新名稱與延續關係 | ⭐⭐⭐⭐⭐ |
| [Zotero Local API](https://www.zotero.org/support/dev/web_api/v3/local_api) | 本機 API、寫入授權與撤銷 | ⭐⭐⭐⭐⭐ |
| [OpenCode](https://opencode.ai/docs/) | 安裝、`opencode` 指令與本機模型連線 | ⭐⭐⭐⭐⭐ |
| [Aider＋Ollama](https://aider.chat/docs/llms/ollama.html) | 正確安裝與 `ollama_chat/` prefix | ⭐⭐⭐⭐⭐ |
| [Ollama — Gemma 4](https://ollama.com/library/gemma4) | `e2b`／`e4b` tag 與硬體選擇 | ⭐⭐⭐⭐⭐ |

## ⭐ 精選 Projects 與學習資源

評分是本專案的教學適合度，不是 GitHub stars，也不保證永遠不變。

<table>
  <thead><tr><th scope="col">分類</th><th scope="col">Project／資源</th><th scope="col">適合做什麼</th><th scope="col">限制</th><th scope="col">評分</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">Skills</th><td><a href="https://agentskills.io">Agent Skills standard</a></td><td>理解跨工具共用的 skill 格式</td><td>各產品仍有自己的擴充欄位</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/anthropics/skills">anthropics/skills</a></td><td>閱讀成熟 skill 範例</td><td>文件 skills 是 source-available</td><td>⭐⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">MCP</th><td><a href="https://modelcontextprotocol.io/specification">MCP specification</a></td><td>查 protocol 的正式定義</td><td>入門不用從頭讀完</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/modelcontextprotocol/python-sdk">MCP Python SDK</a></td><td>用 Python 寫 server／client</td><td>注意 v1 與 v2 教學不可混用</td><td>⭐⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">文件</th><td><a href="https://github.com/anthropics/skills/tree/main/skills/docx">Anthropic DOCX skill</a></td><td>學複雜文件 skill 的結構</td><td>使用前確認授權與 runtime</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/anthropics/skills/tree/main/skills/xlsx">Anthropic XLSX skill</a></td><td>學試算表分析與輸出流程</td><td>成品仍要用試算表軟體檢查</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">Gemini Notebook</th><td><a href="https://github.com/teng-lin/notebooklm-py">notebooklm-py</a></td><td>批次來源、問答與 artifact 匯出</td><td>非官方、未公開 API 可能改變</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/PleasePrompto/notebooklm-skill">notebooklm-skill</a></td><td>從 Claude Code 用瀏覽器查 notebook</td><td>非官方且依賴瀏覽器登入</td><td>⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">Zotero</th><td><a href="https://github.com/WenyuChiou/zotero-skills">zotero-skills</a></td><td>從 Agent 搜尋與整理 Zotero</td><td>寫入前一定先 preview</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/WenyuChiou/research-hub">research-hub</a></td><td>串接 Zotero、Obsidian 與研究流程</td><td>比單一 recipe 更進階</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/MuiseDestiny/zotero-gpt">zotero-gpt</a></td><td>在 Zotero 內閱讀時對話</td><td>plugin 路徑和外部 Agent 不同</td><td>⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">本機／CLI</th><td><a href="https://github.com/anomalyco/opencode">OpenCode</a></td><td>連本機或雲端模型改程式</td><td>先檢查 provider 與 permission 設定</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/earendil-works/pi">Pi</a></td><td>可擴充的 coding harness／CLI</td><td>預設沒有內建權限隔離</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/Aider-AI/aider">Aider</a></td><td>以 Git 為中心的結對改程式</td><td>小模型的編碼品質可能不足</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
</table>

## ✅ 完成檢查與下一站

- [ ] 我完成至少一份 recipe，而且能指出產生的檔案、tool 或回答。
- [ ] 我看過成功路徑，也看過一次失敗訊息或錯誤輸出。
- [ ] 我沒有提交 token、cookie、個人文件或未公開資料。
- [ ] 我知道使用的是官方功能還是 Community Integration。
- [ ] 任何寫入或大量改動都有 preview、diff 或人工批准。

接著回 [Stage 5](../stages/05-claude-code-ecosystem.md) 選下一個能力；要找更多工具，進入 [MCP／Skills Catalog](mcp-skills-catalog.md)。
