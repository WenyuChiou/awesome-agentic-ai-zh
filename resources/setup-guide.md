> **繁體中文** | [简体中文](./setup-guide.zh-Hans.md) | [English](./setup-guide.en.md)

# 🚀 從零開始 — 給沒有開發背景的設定指南

> [← 回主路線 README](../README.md)

> 預估時程：30-45 分鐘。你會申請第一個 API key、裝好 Python / uv，並跑出第一個 LLM hello world。
> 這份文件寫給「想學 AI agent，但還沒寫過 code」的人。已經熟 Python / git / CLI 的開發者，可以直接跳 [Stage 1](../stages/01-llm-basics.md)。

## 先選你的入門方式

依「想花多少時間 setup」由淺到深排序。**完全沒接觸過 LLM 直接從 1️⃣ 開始就好**。

### 1️⃣ 網頁版（最簡單，免費可試，零 setup）

打開瀏覽器就能用，**第一次接觸 LLM 最推薦這條**。免費 tier 通常夠你試一個禮拜。

| 服務 | 網址 | 備註 |
|---|---|---|
| **Claude** | https://claude.ai | Anthropic 官方。免費 tier 每天額度有限，付費版 $20/月 |
| **ChatGPT** | https://chatgpt.com | OpenAI 官方。免費可用 GPT-5.5 Instant（有用量限制），付費 $20/月升 Plus 解鎖 Thinking/Pro |
| **Gemini** | https://gemini.google.com | Google 官方。免費 tier 寬鬆，整合 Google 服務 |
| **Le Chat** | https://chat.mistral.ai | Mistral（歐洲開源 LLM）。免費、隱私導向 |

### 2️⃣ 桌面 App（免費，跨應用整合更好）

跑在你電腦上的原生 app——比網頁多了系統 shortcut、跟剪貼簿 / 截圖整合、可以拖拉檔案。

| App | 下載 | 平台 |
|---|---|---|
| **Claude Desktop** | https://claude.ai/download | macOS / Windows |
| **ChatGPT Desktop** | https://openai.com/chatgpt/download | macOS / Windows |
| **Gemini** | 暫無原生 desktop app | （用網頁版即可） |
| **LM Studio** | https://lmstudio.ai | macOS / Windows / Linux — 跑本機 LLM 的桌面 app，零成本但要 GPU/RAM |

### 3️⃣ IDE 內建 AI（在 code editor 裡邊寫 code 邊有 AI 助手）

跑在 IDE / code editor 裡——你正常寫 code，AI 在旁邊 suggest、修改、回答問題。**已經有寫 code 習慣、想把 IDE 升級成 AI-native 的人這條最順**。

| 工具 | 下載 | 形態 |
|---|---|---|
| **Cursor** | https://cursor.com | 獨立 IDE（VS Code fork） |
| **Windsurf** | https://codeium.com/windsurf | 獨立 IDE（Codeium 出） |
| **Cline** | https://cline.bot | VS Code extension（agentic 風格） |
| **Continue** | https://continue.dev | VS Code / JetBrains extension（開源） |
| **Roo Code** | https://github.com/RooCodeInc/Roo-Code | VS Code extension（Cline fork）；⚠️ **repo 已封存 2026-05（read-only）** |
| **Zed** | https://zed.dev | 獨立 editor，內建 AI assistant |
| **GitHub Copilot** | https://github.com/features/copilot | VS Code / JetBrains 等多 IDE extension |

→ 詳細比較 → [`branches/for-developer.md`](../branches/for-developer.md)

### 4️⃣ CLI Agent（terminal，能讀寫檔案、跑指令、操作 git）

裝在 terminal 的 agent——你下一個 prompt（譬如「重構這個 module」），agent 自己讀檔、改檔、跑指令、commit。**比 IDE 模式更自主、可以處理多步驟任務**，但 setup 稍複雜（需要先有 Node.js 或 Python，看下面 B / D）。

| CLI Agent | 安裝 / 文件 | 主要 LLM |
|---|---|---|
| **Claude Code** | https://code.claude.com/docs/en/quickstart | Claude |
| **Codex CLI** | https://github.com/openai/codex | GPT 系列 |
| **Gemini CLI** | https://github.com/google-gemini/gemini-cli | Gemini |
| **OpenCode** | https://github.com/anomalyco/opencode | 任意（多 provider） |
| **goose** | https://block.github.io/goose | 任意 |
| **Aider** | https://aider.chat | 任意（git-native） |
| **Hermes Agent** | https://github.com/NousResearch/hermes-agent | 200+（model-neutral） |

→ 想看 CLI agent 身分與選擇指南 → [`cli-agents-guide.md`](cli-agents-guide.md)
→ Claude Code 第一次裝的詳細步驟 → 本指南 [D](#d--第一次裝-claude-code約-10-分鐘stage-5--for-developer-會用到)

> 💡 **IDE-based 跟 CLI agent 怎麼選？** 邊寫 code 邊要 AI 幫忙 → IDE；下單一 prompt 讓 agent 自己跑完一整個任務 → CLI。兩個可以並用。

### 5️⃣ API + 自己寫 code（最進階，能 batch、整合任何工具）

想自己寫 Python script、跑 batch job、把 LLM 接到自己的 app／automation？接下來的 A-C 就是給你的。

> 💡 **API key 是什麼**：簡單講就是「讓程式呼叫模型的密碼」。請把它當成信用卡資料一樣保管。

---

## A — 申請第一個 API key（約 10 分鐘）

### Anthropic Claude（推薦第一次）

1. 開 https://console.anthropic.com/
2. 用 Google、GitHub 或 email 註冊。
3. 進帳號後找到 **API Keys**，按 **Create Key**。
4. **立刻複製顯示出的 key**。多數平台只會顯示一次。
5. 先放在本機密碼管理器，或短暫放在本機文字檔；下一節會移到 `.env`。

> ⚠️ **API key 三不規則**
> - **不貼**到 chat 視窗、群組、email 或截圖。
> - **不上傳**到 git；GitHub 可能掃到後自動撤銷。
> - **不放**雲端硬碟純文字檔；同步到其他裝置等於多一份風險。

### 其他 LLM 選項

#### 西方 cloud（美區友善、英文場景）

- **OpenAI**：https://platform.openai.com/api-keys
  ChatGPT Plus 和 API key 是兩件事；訂閱 Plus 仍要另外申請 API key。

- **Google AI Studio**：https://aistudio.google.com/
  適合先試 Gemini API，免費額度會依地區和帳號狀態不同。

- **NVIDIA NIM**：https://build.nvidia.com/
  **托管多個開源 model（Llama / Mistral / DeepSeek / Qwen / Gemma 等）、OpenAI-compatible API、新帳號送 1000 credits**。適合「想試多個 open-source model 但沒 GPU」的情境。`base_url=https://integrate.api.nvidia.com/v1`。

#### 中國 / 中文場景（地區友善、價格極便宜）

> 中國大陸使用者連 Anthropic / OpenAI 有困難、或想試中文 native 模型，從這邊開始。**這些 API 都 OpenAI-compatible**、改 `base_url` 跟 model name 就能跑同一份練習。

- **DeepSeek**：https://platform.deepseek.com/
  web 版 https://chat.deepseek.com 完全免費（含深度思考模式）。API 價格極便宜（**$0.14 input / $0.28 output per 1M token**、比 haiku 便宜約 7 倍）。Code / 推理都很強。
  `base_url=https://api.deepseek.com/v1`、`model=deepseek-v4-flash` 或 `deepseek-v4-pro`。

- **Moonshot Kimi**：https://platform.moonshot.cn/ (中國)、https://platform.moonshot.ai/ (海外)
  web 版 https://kimi.com 免費、**1M token context** 是賣點（很大檔案 / 長對話）。API 約 $5-15/1M input、按 context size 階梯計費。
  `base_url=https://api.moonshot.cn/v1` (中國) / `https://api.moonshot.ai/v1` (海外)、`model=kimi-k3` 等。

- **通義千問 Qwen（Alibaba）**：https://dashscope.console.aliyun.com/
  web 版 https://chat.qwen.ai 免費。API 走 Alibaba Cloud DashScope、有 **OpenAI-compatible endpoint**（[文件](https://help.aliyun.com/zh/dashscope/developer-reference/compatibility-of-openai-with-dashscope/)）。**同樣的 Qwen 模型也能用 Ollama 在本機跑**（`ollama pull qwen2.5:3b`）——cloud 跟 local 兩條路徑都通。

- **智譜 GLM（ZhipuAI）**：https://open.bigmodel.cn/ (中國) / https://z.ai/ (海外)
  web 版 https://chatglm.cn 免費、有 GLM-4.5、GLM-4-Plus。API 有 free tier、學生申請可額外領 credit。

#### 本機（沒有供應商模型 API 帳單；下載後可離線推理）

- **Ollama 本機模型**：不用 API key。走本機路線請看 [Cookbook Recipe 6](cookbook.md#6-本機-llm--cli-agent-快速-walkthrough)。
  本 repo 的「Path A」預設就是 Ollama：Stage 1–2 用 `gemma4:e4b`，Stage 3–6 的 tool use／ReAct 題用 `qwen2.5:3b`，Stage 7 的辯論、評測、觀測、串流與部署機制用 `qwen3.5:4b`。本機推理不會產生供應商模型 API 帳單，但硬體、電力、下載與等待時間仍有成本。

> 💡 **怎麼挑第一個**：
> - 想學 agent / production、**美區帳號OK** → **Anthropic Claude**（curriculum canonical）
> - 想學 agent / production、**中國地區**或想試中文模型 → **DeepSeek**（最便宜 cloud option、OpenAI-compat、中文很強）
> - 想試多個 model 但沒 GPU → **NVIDIA NIM**（送 1000 credit、托管 10+ open model）
> - 想把資料留在本機 / 中國大陸無 cloud → **Ollama**（仍要保護裝置、檔案、log 與存取權限）

---

## B — 裝本機環境（約 10 分鐘）

### 裝 Python 3.10+

- **macOS**：開 Terminal，輸入 `brew install python@3.12`。如果還沒有 Homebrew，先看 https://brew.sh。
- **Windows**：到 https://www.python.org/downloads/ 下載 installer，安裝時一定要勾 **Add Python to PATH**。
- **Linux**：Ubuntu 用 `sudo apt install python3 python3-venv`，Fedora 用 `sudo dnf install python3`。
- **驗證**：macOS / Linux 輸入 `python3 --version`；Windows 輸入 `py --version`。看到 `Python 3.10` 以上即可。

### 裝 uv

uv 是 Python 套件管理工具。你可以把它想成「幫你臨時裝好需要套件再執行」的工具。

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
irm https://astral.sh/uv/install.ps1 | iex
```

驗證：

```bash
uv --version
```

### 建立第一個 `.env` 檔

在你要跑 script 的資料夾裡，建立一個檔名叫 `.env` 的檔案：

```bash
ANTHROPIC_API_KEY=sk-ant-...貼上你剛才複製的 key
```

`.env` 是專門放本機祕密資訊的檔案。程式會讀它，但你不應該把它上傳到 GitHub。

### 加上 `.gitignore`

同一個資料夾建立 `.gitignore`：

```gitignore
.env
__pycache__/
*.pyc
```

這樣 git 就不會把 `.env` 收進版本紀錄。

---

## C — 跑第一個 `hello-claude.py`（約 5 分鐘）

建立 `hello-claude.py`：

```python
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic() # 自動讀取 ANTHROPIC_API_KEY

msg = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello, who are you?"}],
)

print(msg.content[0].text)
```

執行：

```bash
uv run --with anthropic --with python-dotenv python hello-claude.py
```

看到 Claude 回覆自我介紹，就代表你的 API key、Python、套件都通了。

### 常見錯誤

| 錯誤訊息 | 常見原因 | 解法 |
|---|---|---|
| `401 Unauthorized` | API key 沒讀到或打錯 | 回 A 重新複製，確認 `.env` 檔名和內容 |
| `429 Rate limit` | 太快送太多請求 | 等幾秒或幾分鐘再跑 |
| `connection refused` | 連線或防火牆問題 | 確認網路、公司或學校防火牆 |
| `ModuleNotFoundError` | 套件沒有被安裝 | 確認執行的是上面的 `uv run --with ...` 指令 |

---

## D — 第一次裝 Claude Code（約 10 分鐘；Stage 5 / for-developer 會用到）

### 先裝 Node.js

> 💡 **Node.js 是什麼**：跑 JavaScript 的 runtime（類似 Python interpreter 但是給 JS 用）。**`npm`** 是它附帶的「套件管理器」（package manager）—— 跟 Python 的 `pip` 同角色、用來安裝別人寫好的工具（如下面的 Claude Code）。`npm install -g X` 表示「全域裝 X、之後在任何資料夾都能用」。

- **macOS / Linux**：`brew install node`，或從 https://nodejs.org 下載。
- **Windows**：從 https://nodejs.org 下載 installer。
- **驗證**：輸入 `node --version`，看到 v18 以上即可。

### 裝 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### 第一次認證

```bash
claude
```

第一次啟動時通常會讓你選：

- **Claude subscription**：用 Claude.ai 帳號登入，對初學者最省事。
- **API key**：貼上 A 申請到的 key。

### 建立第一份 `CLAUDE.md`

在你的 project 根目錄建立 `CLAUDE.md`。Claude Code 啟動時會讀它，理解你希望它怎麼協助。

```markdown
# 你是誰
我是 [你的名字]，[你的領域，例如：教師 / 研究者 / 寫作者]。

# Code style
- 註解用繁體中文寫，code 用英文
- 寫 function 時優先加 type hint
- 不要主動 commit；改完讓我手動 git add

# 不准做的事
- 不要連網查資料，除非我明確說可以
- 不要動 `.env` 或 `.gitignore`
- 不要刪資料夾，包括子資料夾
```

---

## E — 第一個 Skill 範例（約 5 分鐘；Stage 5.3 會用到）

Skill 是 Claude Code 的「可重用 prompt 包」。當你的訊息符合描述，Claude Code 會自動載入那份指示。

建立 `.claude/skills/hello-skill/SKILL.md`：

```markdown
---
name: hello-skill
description: 第一個 hello skill。當使用者說「請打招呼」或「say hi」時觸發。
---

當使用者請你打招呼時，回三件事：

1. 用繁體中文跟英文各說一次 hello
2. 提現在的日期（用 system 時間）
3. 給一個今日小提醒（隨機選健康 / 學習 / 心情建議）
```

跑 `claude`，輸入「請打招呼」。如果 Claude 回覆三件事，就代表 Skill 被載入了。

> 想看更完整的 Skill 設計：看 [Stage 5.3 — Skills](../stages/05-claude-code-ecosystem.md#53--skillsclaude-code-的行為層-claude-code-生態最關鍵的一層)。
> 想看可以照做的範例：看 [Cookbook](cookbook.md)。

---

## 接下來去哪

| 你現在的狀態 | 下一步 |
|---|---|
| 想正式理解 LLM、API、token | [Stage 1 — LLM 基礎](../stages/01-llm-basics.md) |
| 想直接挑身分分支 | [日常使用者](../branches/for-everyday-users.md) / [教師](../branches/for-teacher.md) / [知識工作者](../branches/for-knowledge-worker.md) / [研究者](../branches/for-researcher.md) / [開發者](../branches/for-developer.md) |
| 想看 Claude Code 完整生態 | [Stage 5 — Claude Code 生態系](../stages/05-claude-code-ecosystem.md) |
| 想本機 LLM、不用雲端 key | [Cookbook Recipe 6](cookbook.md#6-本機-llm--cli-agent-快速-walkthrough) |
| 想比較 CLI agent | [CLI Agents 比較指南](cli-agents-guide.md) |
| 不懂某個用詞 | [Glossary](glossary.md) |
