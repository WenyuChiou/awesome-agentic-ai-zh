# Cookbook — 把概念變成可執行 recipe

> **繁體中文** | [简体中文](./cookbook.zh-Hans.md) | [English](./cookbook.en.md)

> Stage 5（Claude Code 生態）跟 [`mcp-skills-catalog.md`](mcp-skills-catalog.md) 講「概念」跟「有哪些工具」。這份 cookbook 補中間缺的：「**怎麼動手做出來**」。每個 recipe 是一份 step-by-step + sample code + 常見 pitfall，~30-50 分鐘做完一個。
>
> 不是 reference 也不是 tutorial——是 recipe，挑你需要的那道煮就好。

---

## 📋 目錄

1. [寫你的第一個 Skill（SKILL.md anatomy）](#1-寫你的第一個-skill)
2. [寫你的第一個 MCP server（Python SDK）](#2-寫你的第一個-mcp-server)
3. [Word / Excel / PowerPoint workflow](#3-office-docs-workflow)
4. [NotebookLM workflow](#4-notebooklm-workflow)
5. [Zotero workflow](#5-zotero-workflow)
6. [本機 LLM + CLI Agent 快速 walkthrough](#6-本機-llm--cli-agent-快速-walkthrough)

---

## 1. 寫你的第一個 Skill

> Skill = 一個資料夾含 `SKILL.md`，Claude Code 啟動時自動 discover、按情境自動載入。最小 viable 版本 50 行就能跑。
>
> 📚 **這份是「30 分鐘跑出第一個」實作版。想看「Skill 怎麼寫得好」深度討論** → [Hello-Agents Extra08：如何寫出好的 Skill](https://github.com/datawhalechina/hello-agents/blob/main/Extra-Chapter/Extra08-如何写出好的Skill.md)（中文最完整的 Skill 最佳實踐，討論 description 寫法、references / scripts 設計等）。兩份互補：先用本 recipe 跑出第一個，再讀那份 polish 寫法。

### 為什麼

寫 Skill 跟「在 prompt 裡加幾段 instruction」差別在於：

- Skill 是 **per-domain** 的，不會污染所有 conversation
- 可以打包跨 project / team 共用
- Claude 自己決定何時載入（看 description match 不 match）

### 步驟

#### Step 1：建立 skill 資料夾

兩個位置可以放（看你要 user 級還是 project 級）：

```bash
# user 級（所有 project 共用）
mkdir -p ~/.claude/skills/my-first-skill
cd ~/.claude/skills/my-first-skill

# 或 project 級（只在這個 repo 觸發）
mkdir -p .claude/skills/my-first-skill
cd .claude/skills/my-first-skill
```

#### Step 2：寫 `SKILL.md`

最小可 work 的範本：

```markdown
---
name: my-first-skill
description: When the user asks for [SPECIFIC SITUATION], use this skill to [WHAT IT DOES]. Examples include [2-3 trigger phrases]. Do NOT use for [WHAT IT'S NOT FOR].
---

# My First Skill

You are now in the [domain] context.

## When the user asks X, do these steps:

1. First, [action A]
2. Then, [action B]
3. Verify with [check]

## Don't do:

- [anti-pattern 1]
- [anti-pattern 2]

## Reference

- (optional) link to a doc / paper / API spec
```

具體例子：「整理 Python 程式碼的 import 順序」

```markdown
---
name: python-import-organizer
description: When the user pastes Python code or asks to clean up imports / format code / sort imports, organize the imports following PEP 8 + isort order: stdlib first, then third-party, then local. Do NOT use for non-Python code.
---

# Python Import Organizer

When the user wants Python imports cleaned up:

1. Group imports into 3 sections: stdlib / third-party / local
2. Within each group, sort alphabetically
3. Add a blank line between groups
4. Remove unused imports (only if user explicitly asks; otherwise just sort)

## Don't:
- Don't change function code, only the import block
- Don't auto-remove imports without asking
```

#### Step 3：測試

```bash
# 重啟 Claude Code（讓它重新 discover skills）
# 在 conversation 裡丟一個觸發句
# e.g.「幫我整理一下這段 Python 的 imports」
# 觀察 Claude 有沒有按照 SKILL.md 的步驟做
```

#### Step 4（進階）：加 evals

在 skill folder 內加 `evals/evals.json`：

```json
{
  "evals": [
    {
      "input": "整理一下這段 Python 的 imports: import os\nimport requests\nfrom mypackage import foo",
      "expected_behavior": ["按 stdlib / third-party / local 分組", "alphabetical 排序"]
    }
  ]
}
```

之後可以用 promptfoo 之類工具 batch 跑。

### 常見 pitfall

| 症狀 | 原因 | 解法 |
|---|---|---|
| Claude 從不觸發我的 skill | description 寫得太籠統，匹配不到 user query | description 加 2-3 個具體 trigger phrase（"when the user asks X / Y / Z"） |
| 觸發了但行為不對 | SKILL.md 步驟太抽象 | 改成 numbered list、每步明確動作 |
| 觸發了不該觸發 | description 太寬，匹配到不相關 query | 加 "Do NOT use for X" 收斂 |

### 進一步

- 看 [Stage 5.3](../stages/05-claude-code-ecosystem.md#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層) 的 Skill anatomy 詳解
- 看 [`anthropics/skills`](https://github.com/anthropics/skills) 官方 skill 範本（docx / xlsx / pptx 等）的寫法
- 多個 skill 打包成 plugin → [Stage 5.4](../stages/05-claude-code-ecosystem.md#54--plugins-與-marketplaces)

---

## 2. 寫你的第一個 MCP server

> MCP server = 一個獨立 process，跑起來提供 tool / resource / prompt 給 LLM host（Claude Desktop / Claude Code）。最小可 run 版 < 50 行 Python。

### 為什麼

- Skill 是給 Claude 的「角色 + 規則」；MCP 是給 Claude 的「**外部 function**」
- Skill 不能讀檔、不能呼叫 API；MCP 可以（任何 tool 你寫得出來）
- Skill 只在 Claude Code 跑；MCP 任何 LLM host（包括 Cursor、自寫 agent）都能接

### 步驟

#### Step 1：安裝官方 SDK

```bash
pip install "mcp>=2,<3"
```

> ⚠️ **一定要鎖版本**。官方 Python SDK 於 **2026-07-28 發布 v2.0.0**，是破壞性改版（`FastMCP` 改名 `MCPServer`、低階 `Server` 的 handler 從 decorator 改成建構子參數）。裸寫 `pip install mcp` 會裝到 2.x，**網路上 2025 年寫的 v1 教學會在 import 那行就失敗**。
> 手上有 v1 舊 code 還不想改？鎖 `pip install "mcp>=1,<2"`（v1.x 仍在維護模式、只收安全性修補）。遷移對照表：[官方 migration guide](https://py.sdk.modelcontextprotocol.io/migration/)。

#### Step 2：寫 `server.py`

最小範本——一個會回 echo 的 tool：

```python
# server.py
from mcp.server.mcpserver import MCPServer

app = MCPServer("hello-mcp")

@app.tool()
async def echo(text: str) -> str:
    """Echo the input text back to the user."""
    return f"Echo: {text}"

if __name__ == "__main__":
    app.run(transport="stdio")
```

> 💡 **為什麼這麼短**：v2 從 **type hints 自動產生 inputSchema**（`text: str` → 必填的 string 參數）、用 **docstring 當 tool description**、回傳值也自動包成 MCP content——這三件事在 v1 都要手寫。所以 schema 設計的功夫現在花在「參數命名 + type hint + docstring 寫清楚」上。

#### Step 3：在 Claude Desktop / Code 設定

**Claude Desktop**：編輯 `~/Library/Application Support/Claude/claude_desktop_config.json`（macOS）或 `%APPDATA%\Claude\claude_desktop_config.json`（Windows）：

```json
{
  "mcpServers": {
    "hello-mcp": {
      "command": "python",
      "args": ["/絕對路徑/到/server.py"]
    }
  }
}
```

**Claude Code**：用 `claude mcp add` 指令：

```bash
claude mcp add hello-mcp --scope project -- python /絕對路徑/到/server.py
```

#### Step 4：重啟 Claude Desktop / Code、測試

```
你問：echo "hello world" 給我
Claude 回（會顯示 tool call icon）：Echo: hello world
```

### 常見 pitfall

| 症狀 | 原因 | 解法 |
|---|---|---|
| Claude Desktop 沒看到 tool | server.py 啟動失敗 | terminal 直接 `python server.py` 跑、看 stderr 哪裡爆 |
| tool 列出但 call 失敗 | 參數 type hint 沒寫（v2 靠它產 schema）、或型別對不上 | 每個參數都補 type hint；看 [`schema-design-cheatsheet.md`](schema-design-cheatsheet.md) |
| Claude 不主動叫 tool | docstring（= tool description）太籠統 | docstring 改成「When the user asks X, use this tool」式的具體 trigger |
| `ImportError` / `AttributeError` 在 import 那行 | 混到 v1 寫法（`from mcp.server import Server`、`@app.list_tools()`）跑在 v2 上 | 用上面的 v2 寫法，或鎖 `mcp>=1,<2` 留在 v1 |
| stdio 跟 HTTP 哪個用？ | 本機桌面整合用 **stdio**；遠端用 **Streamable HTTP**（舊的 HTTP+SSE transport 已於 2025-03-26 deprecated、別再用） | 第一個 server 一律用 stdio |
| stdio server 要不要做 OAuth？ | 不用。spec 明寫 authorization 整體是 optional，HTTP transport 才 SHOULD 遵循，**stdio SHOULD NOT 用 authorization** | 憑證從**環境變數**取（例如 `os.environ["API_KEY"]`），不要在 server 裡實作登入流程 |

### 進一步

- 看 [Stage 5.2](../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎) 的 MCP 完整介紹
- 看 [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) 官方 reference server（現有 7 個：everything / fetch / filesystem / git / memory / sequentialthinking / time；github、sqlite 已移到 `servers-archived`）。官方 README 自述這些是 reference implementation、**不是 production-ready**，要找實際能用的 server 走 [官方 Registry](https://registry.modelcontextprotocol.io)（仍在 preview）
- 寫 production server 看 [Stage 5.2「練習：MCP in production」](../stages/05-claude-code-ecosystem.md#52--mcpmodel-context-protocol-基礎) 跟 [`anthropics/claude-code`](https://github.com/anthropics/claude-code) 的 `~/.claude/skills/`

---

## 3. Office Docs Workflow

> 用 Claude 讀寫 Word / Excel / PowerPoint / PDF 不用裝額外 tool——[`anthropics/skills`](https://github.com/anthropics/skills) 官方 repo 已經內建好。

### 為什麼

最常見場景：

- 把 Markdown / 大綱 → 自動生成 Word / PPT
- 讀一堆 PDF / Excel → 整理摘要 / 提取數字
- 改別人傳來的 docx → 加 track changes、或重排格式
- 把表格 cross-reference 寫成報告

不需要自己 parse XML、不需要找 python-docx / openpyxl 教學——anthropics/skills 已經包好。

### 步驟

#### Step 1：安裝 skills

最簡單：clone Anthropic 官方 skills repo 到 user-level skill 目錄：

```bash
# user 級（所有 project 用）
git clone https://github.com/anthropics/skills.git ~/.claude/skills/anthropic-skills
```

或者用 `claude plugin install`（如果有打包成 plugin）。

#### Step 2：重啟 Claude Code

- skills/docx/ → docx 讀寫
- skills/xlsx/ → Excel 讀寫
- skills/pptx/ → PowerPoint 讀寫
- skills/pdf/ → PDF 讀

Claude 會根據 user query 自動載入合適的 skill。

#### Step 3：實用 prompt 範本

**從大綱生 PPT**：
```
讀我寫的 outline.md，照這個結構生一份 PPT：
- 封面 1 頁
- 每個 H2 一頁，bullet points 從 H3 內容濃縮
- 結語 1 頁

存成 ./output/presentation.pptx
```

**讀 Excel 整理數字**：
```
讀 ./data/sales-2023.xlsx 第一張 sheet，把每個 region 的 Q4 總額算出來，
寫進 ./output/q4-summary.md（用 markdown table 格式）。
```

**改 docx**：
```
讀 ./doc/draft.docx，把繁中詞彙轉成簡中（譬如「軟體」→「软件」），
存成 ./doc/draft.zh-Hans.docx，保留原本的 track changes。
```

**讀 PDF 提取資訊**：
```
讀 ./papers/research.pdf，把 abstract、main contributions、limitations
分別寫進三個 markdown section，存到 ./notes/research-summary.md。
```

### 常見 pitfall

| 症狀 | 原因 | 解法 |
|---|---|---|
| skill 沒被觸發 | repo 路徑放錯 | 確認 SKILL.md 在 `~/.claude/skills/anthropic-skills/skills/docx/SKILL.md` 這種層級 |
| pptx 生出來樣式醜 | 沒給設計參考 | prompt 加「參考 ./template.pptx 的樣式」 |
| 大 PDF 讀不完 | context 爆 | 改用 [`SylphxAI/pdf-reader-mcp`](https://github.com/SylphxAI/pdf-reader-mcp)（5-10× 快） |
| Excel 公式被吃掉 | docx skill 不處理 formulas | 開檔前 prompt 明說「保留 formula 不要 hard-code」 |

### 進一步

- catalog 2 [`mcp-skills-catalog.md` 2 辦公文件](mcp-skills-catalog.md#2-辦公文件word--excel--powerpoint--pdf)：補強版 office skill / Excel / PPT 專用 MCP
- 中文圈 office workflow：[`leemysw/feishu-docx`](https://github.com/leemysw/feishu-docx) 飛書 / Lark docs ↔ Markdown

---

## 4. NotebookLM Workflow

> NotebookLM 是 Google 的 RAG-on-your-docs 工具。**Claude Code 沒有官方 NotebookLM 整合**，但社群有 2 個成熟方案。

### 為什麼

NotebookLM 強的地方：

- 上傳 50 份 PDF 自動建索引
- Q&A 帶 citation（每個答案都標出來自哪份文件第幾頁）
- 生成 summary / mind map / podcast-style audio overview

弱點：要在 NotebookLM 網頁裡用，跟你的其他 workflow（Claude Code、Obsidian、Zotero）斷開。

兩個方案橋接：

1. **PleasePrompto/notebooklm-skill**（Skill，browser automation）
2. **teng-lin/notebooklm-py**（Python API + CLI）

### 兩個方案怎麼選

| 場景 | 選哪個 | 為什麼 |
|---|---|---|
| 偶爾從 Claude Code 查一下 NotebookLM | `PleasePrompto/notebooklm-skill` | Claude Code 內 prompt 一句話就跑、setup 簡單 |
| 批次操作（建 100 個 notebook、批次匯入文件） | `teng-lin/notebooklm-py` | Python API，可程式化跑 |
| 不想 Google 政策變動就壞 | （等 Google 出官方 API） | 兩個都是 unofficial、會有風險 |

### 方案 A：PleasePrompto/notebooklm-skill

#### Step 1：clone 到 skills 目錄

```bash
git clone https://github.com/PleasePrompto/notebooklm-skill ~/.claude/skills/notebooklm
```

#### Step 2：第一次跑會要 Google login（瀏覽器自動化）

照 repo README 設定 OAuth / 登入 cookie。

#### Step 3：實用 prompt

```
查我 NotebookLM 內「LLM Agents 2024」這個 notebook，
找出所有提到 "tool use" 的段落，整理成一份比較表，
帶上每個來源文件名跟頁數。
```

### 方案 B：teng-lin/notebooklm-py

```bash
pip install notebooklm-py
```

範例：

```python
from notebooklm import NotebookLM
nlm = NotebookLM() # OAuth 流程

# 建一個 notebook
nb = nlm.create_notebook("My Research")

# 批次匯入 PDF
for pdf in glob.glob("papers/*.pdf"):
    nb.add_source(pdf)

# Q&A
answer = nb.query("What are the main contributions?")
print(answer.text)
print(answer.citations)
```

### 常見 pitfall

| 症狀 | 原因 | 解法 |
|---|---|---|
| 突然不能用 | Google 改了內部 API | 檢查 issue tracker、等社群更新 |
| Q&A 答案模糊 | 上傳文件太多、retrieve 失準 | 拆成幾個 notebook（每個 < 50 source）|
| 中文支援不好 | 預設 UI 設成英文 | NotebookLM 設定改 zh-Hant |

### 進一步

- catalog 1 [`mcp-skills-catalog.md` 1 筆記 / 知識庫](mcp-skills-catalog.md#1-筆記--知識庫)
- 完整 research workspace：用 [`WenyuChiou/research-hub`](https://github.com/WenyuChiou/research-hub) 整合 NotebookLM + Zotero + Obsidian

---

## 5. Zotero Workflow

> Zotero 管文獻，加上 [`WenyuChiou/zotero-skills`](https://github.com/WenyuChiou/zotero-skills) 後 Claude Code 能直接搜 / 加 / 分類 / 標 references。

### 為什麼

研究流程經典痛點：

- 「我那篇 paper 在哪？」——Zotero 有，但要切換視窗
- 「給我所有講 transformer 的 paper 摘要」——要自己 select、export、丟給 LLM
- 「這篇 paper 該打什麼 tag？」——人工

zotero-skills 把這些變成 Claude Code 內一句 prompt 就跑。

### 跟 zotero-gpt 差別

| 工具 | 角色 | 適合 |
|---|---|---|
| [`MuiseDestiny/zotero-gpt`](https://github.com/MuiseDestiny/zotero-gpt) | Zotero plugin（在 Zotero **內部** chat） | 邊讀 paper 邊問 LLM、不切換視窗 |
| [`WenyuChiou/zotero-skills`](https://github.com/WenyuChiou/zotero-skills) | Claude Code skill（從 **外部** 操作 Zotero） | 寫 paper / 整理文獻時，Claude Code 為主 |

互補不衝突，可以兩個都裝。

### 步驟

#### Step 1：開啟 Zotero local API

Zotero 桌面版預設不開 API。打開：

- **Edit → Preferences → Advanced → Config Editor**
- 找 `extensions.zotero.httpServer.enabled`，設 `true`
- 找 `extensions.zotero.httpServer.port`，預設 `23119`

#### Step 2：clone zotero-skills

```bash
git clone https://github.com/WenyuChiou/zotero-skills ~/.claude/skills/zotero-skills
```

照 repo README 設定（包含 API key 給 Web API 寫操作用）。

#### Step 3：實用 prompt

**搜文獻**：
```
搜我 Zotero library 內所有 2023 年之後、跟 multi-agent 相關的 paper，
按 cited count 排序、輸出成 markdown table。
```

**自動分類**：
```
看我 collection "Inbox" 裡的 50 篇 paper，按主題自動建 sub-collection
（譬如 "RAG"、"Tool Use"、"Multi-Agent"），把 paper 移進去。
```

**標 tag**：
```
讀我 Zotero 內這篇 paper（attached PDF 看完），
從 abstract 提取 5 個 keyword 當 tag 加上去。
```

**寫 paper 引用整理**：
```
我的 paper draft 在 ./paper/v3.tex，
找出所有 \cite{} 對應的 BibTeX entry，跟 Zotero library 對比，
把缺的 export 出 .bib 給我。
```

### 常見 pitfall

| 症狀 | 原因 | 解法 |
|---|---|---|
| skill 觸發但 query 失敗 | Zotero 沒在跑 / API 沒開 | 開 Zotero 桌面版 + 確認 port 23119 listening |
| 寫操作（add / move）失敗 | local API 是 read-only，要用 Web API | 設定 Web API key（[zotero.org/settings/keys](https://www.zotero.org/settings/keys)） |
| collection 結構亂 | 自動分類 prompt 沒給目錄結構 | prompt 給 Claude 看現有 collection tree、再決定怎麼分 |

### 進一步

- 完整 research workspace：[`WenyuChiou/research-hub`](https://github.com/WenyuChiou/research-hub) 整合 Zotero + Obsidian + NotebookLM
- 學術論文寫作：[`WenyuChiou/academic-writing-skills`](https://github.com/WenyuChiou/academic-writing-skills)
- 14 個研究流程 skill 集：[`WenyuChiou/ai-research-skills`](https://github.com/WenyuChiou/ai-research-skills)

---

## 6. 本機 LLM + CLI Agent 快速 walkthrough

> 30 分鐘把 Stage 1 的本機模型接到 Stage 5 的 CLI agent：離線、隱私資料、不想用 API 額度時，可以先用這條路線做 end-to-end 驗證。

### 為什麼

Stage 1 教你用 Ollama / llama.cpp / vLLM 跑本機 LLM；Stage 5 教 Claude Code、MCP、Skills、Plugins 的 agent 生態。中間常見的誤會是：**Claude Code 不是本機 LLM runner**。Claude Code 需要 Anthropic OAuth / API key，不能直接把 model endpoint 改成 Ollama 或其他本機 endpoint。

如果目標是「本機 LLM + CLI agent」，選擇支援 BYO LLM 的 CLI 會更直接：**OpenCode / goose / Aider / Hermes Agent** 都能接 OpenAI-compatible endpoint 或 Ollama provider。這個 recipe 用一個短流程讓你先跑通 model、agent、任務三件事。

### 步驟

#### Step 1：Ollama + model（10 分鐘）

```bash
# 安裝 Ollama：https://ollama.com
ollama pull qwen2.5:3b
# RAM 16GB+ 可以改試：ollama pull qwen2.5:7b
ollama serve
```

確認 OpenAI-compatible API 有回應：

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:3b","messages":[{"role":"user","content":"用 3 句話解釋 ReAct agent。"}]}'
```

#### Step 2：選一個 CLI agent 接 Ollama（10 分鐘）

**OpenCode**：適合想切換多 provider、又要接本機模型的人。

```bash
npm install -g opencode-ai
opencode auth login # provider 選 Ollama，endpoint 設 http://localhost:11434/v1
opencode
```

**goose**：內建 Ollama provider，適合先做本機 agent 試跑。

```bash
# 安裝方式看 https://block.github.io/goose
goose configure # provider 選 Ollama，model 設 qwen2.5:3b
goose session start
```

**Aider**：git-native，適合在 repo 內做小型程式碼修改。

```bash
pip install aider-chat
aider --model ollama/qwen2.5:3b --no-show-model-warnings
```

**Hermes Agent**：適合跑在 VPS，讓 Telegram / Slack / Discord 變成 agent 入口。

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes model set ollama:qwen2.5:3b
hermes
```

#### Step 3：跑一個真實小任務（10 分鐘）

不要只問「hello world」。挑一個會碰到檔案、摘要、表格或搜尋的小任務：

- 從 `~/Downloads` 找 5 個 PDF，抽出每篇 paper 的 1 句 summary 與 method。
- 讀 `data.csv` 前 3 欄，輸出 Markdown table 並指出欄位問題。
- 搜 `~/notes/` 裡 7 天內提到 `agent safety` 的段落，整理成 checklist。

觀察三件事：

- **Speed**：本機小模型常比 API 慢 2-5 倍。
- **Quality**：3B / 7B 模型的 reasoning、長 context、複雜程式碼能力通常不如 Claude。
- **Cost**：token 成本是 `$0`，但會吃本機 RAM / VRAM 與電力。

#### Step 4：跟 Claude Code 的差異（5 分鐘）

| 面向 | Claude Code | OpenCode + Ollama |
|---|---|---|
| LLM | Anthropic hosted | 本機模型 |
| 成本 | 訂閱或 per-token | `$0` token cost |
| 速度 | 通常較穩 | 看硬體，常慢 2-5 倍 |
| 隱私 | 內容送 Anthropic | 內容留在本機 |
| Reasoning 上限 | Claude 4.8+ 較強 | 取決於本機模型 |
| 適合 use case | 複雜 codebase、長 context、可靠推理 | 隱私資料、離線 demo、低成本反覆試 |

### 重要限制：Claude Code 不能直接用本機 LLM

Claude Code 目前需要 Anthropic OAuth / API key，沒有官方設定可以把模型切成 Ollama 或本機 endpoint。網路上可能有 proxy 或 API shim 做實驗，但這不是官方支援路徑，穩定性與相容性要自己承擔。

要用本機 LLM，建議把「Claude Code」跟「支援 BYO LLM 的 CLI agent」分開看：Claude Code 用在需要 Claude 品質的工作；OpenCode / goose / Aider / Hermes 用在本機、離線、隱私或低成本實驗。

### 常見 pitfall

| 問題 | 原因 | 解法 |
|---|---|---|
| `connection refused` | Ollama server 沒在背景跑 | 開另一個 terminal 跑 `ollama serve` |
| model output 斷句怪、邏輯弱 | 3B 模型能力有限 | 改用 `qwen2.5:7b` 或 `deepseek-r1:7b` |
| CLI agent 沒改到檔案 | 本機模型太弱，或 prompt 太模糊 | 縮小任務、指定檔案與成功條件 |
| memory / OOM | 模型吃掉 RAM / VRAM | 先用 `qwen2.5:3b`，再升到 7B；必要時開 swap |

### 進一步

- Stage 1 [Local LLM 練習](../stages/01-llm-basics.md#練習-6local-llm)：Ollama / llama.cpp / vLLM 的差異
- [`cli-agents-guide.md`](cli-agents-guide.md)：CLI agent 怎麼選
- Hermes Agent README：多平台 gateway（Telegram / Discord / Slack）與 provider 設定

---

## 找不到你要的 recipe？

- 看 [Stage 5](../stages/05-claude-code-ecosystem.md) 完整概念
- 看 [`mcp-skills-catalog.md`](mcp-skills-catalog.md) 完整工具清單
- 看 [`schema-design-cheatsheet.md`](schema-design-cheatsheet.md) 寫 tool schema 的細節
- 看 [`cli-agents-guide.md`](cli-agents-guide.md) 的 CLI agent 身分與選擇指南

要新 recipe → 開 issue 或直接 PR 一份。recipe 格式：**為什麼 + 步驟 + 範本 prompt + 常見 pitfall + 進一步**。
