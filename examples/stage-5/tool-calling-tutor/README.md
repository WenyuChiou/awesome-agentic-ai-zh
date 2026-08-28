<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# tool-calling-tutor — Claude Code skill

> Skill 用途：當你卡在 tool calling（LLM 不呼叫、args 錯、ReAct loop 跑不停、schema 不知道怎麼寫），可直接輸入 `/tool-calling-tutor` 開啟；在相關情境中也可能自動載入，帶你走完 4-symptom 診斷與 5-step 修法。

對應 [Stage 3 — Tool Use & Agent 入門](../../../stages/03-tool-use-and-hello-agent.md)，同時是 [Stage 5 — Claude Code Ecosystem](../../../stages/05-claude-code-ecosystem.md) 5.3 的**自帶 skill 範例**。

## 為什麼這個 skill 存在

Tool calling 是整個 curriculum 最陡的學習曲線——schema 設計、SDK response shape、ReAct loop 三個 mental model 疊在一起。Stage 3 doc 已經把概念講清楚，但**遇到「我這份就是不會跑」的時候、需要互動式 debug**。

這個 skill 補的就是這塊缺：

| 已有資源 | 不足 | 這個 skill 補的 |
|---|---|---|
| `stages/03-tool-use-and-hello-agent.md` | 講 6 個練習、不互動 | 互動式 triage：你卡哪個 symptom？ |
| `resources/schema-design-cheatsheet.md` | 5 條規則 + 5 anti-pattern、prescriptive | 走步驟版：bad → good schema 怎麼 4 步改 |
| `resources/glossary.md` 2 | 1 行定義 | 不重複定義、引用為主 |
| `examples/stage-3/02-06/` | 完整可跑 starter | Skill 指過去當 fork template |

## 雙重用途

1. **學習者用**：安裝後當 personal debug 助手。直接輸入 `/tool-calling-tutor` 開啟；相關問題也可能讓 skill 自動載入。
2. **Stage 5 5.3 meta-example**：學 SKILL.md 怎麼寫的時候，直接看這份。包含完整 frontmatter（含 trigger phrases + Do NOT use for）、`references/` 設計、`evals/evals.json` 範例。

## 怎麼安裝

以下命令都從這個 repository 的根目錄執行。

### Option A：user 級（所有 project 共用）

```powershell
$repoRoot = Get-Location
$skillSource = Join-Path $repoRoot "examples\stage-5\tool-calling-tutor"
$skillTarget = Join-Path $env:USERPROFILE ".claude\skills\tool-calling-tutor"
New-Item -ItemType Directory -Force -Path $skillTarget | Out-Null
Copy-Item -Force -LiteralPath (Join-Path $skillSource "SKILL.md") -Destination (Join-Path $skillTarget "SKILL.md")
Copy-Item -Recurse -Force -LiteralPath (Join-Path $skillSource "references") -Destination $skillTarget
Copy-Item -Recurse -Force -LiteralPath (Join-Path $skillSource "evals") -Destination $skillTarget
```

English 請改複製 `translations/SKILL.en.md`；簡體中文請改複製 `translations/SKILL.zh-Hans.md`。

### Option B：project 級（只在這個 repo 觸發）

```powershell
$repoRoot = Get-Location
$skillSource = Join-Path $repoRoot "examples\stage-5\tool-calling-tutor"
$skillTarget = Join-Path $repoRoot ".claude\skills\tool-calling-tutor"
New-Item -ItemType Directory -Force -Path $skillTarget | Out-Null
Copy-Item -Force -LiteralPath (Join-Path $skillSource "SKILL.md") -Destination (Join-Path $skillTarget "SKILL.md")
Copy-Item -Recurse -Force -LiteralPath (Join-Path $skillSource "references") -Destination $skillTarget
Copy-Item -Recurse -Force -LiteralPath (Join-Path $skillSource "evals") -Destination $skillTarget
```

<details markdown="1">
<summary>macOS/Linux 指令</summary>

```bash
skill_source="examples/stage-5/tool-calling-tutor"
mkdir -p ~/.claude/skills/tool-calling-tutor
cp "$skill_source/SKILL.md" ~/.claude/skills/tool-calling-tutor/SKILL.md
cp -R "$skill_source/references" "$skill_source/evals" ~/.claude/skills/tool-calling-tutor/

mkdir -p .claude/skills/tool-calling-tutor
cp "$skill_source/SKILL.md" .claude/skills/tool-calling-tutor/SKILL.md
cp -R "$skill_source/references" "$skill_source/evals" .claude/skills/tool-calling-tutor/
```
</details>

### 驗證安裝

在 Claude Code 中輸入：

```
/tool-calling-tutor
```

預期：skill 會開啟，並詢問或確認對應的 symptom 路線。這是確定的安裝檢查。自動載入會受上下文影響，不能當作安裝成功的證明。

Claude Code 會在目前 session 偵測既有 personal 或 project skills 目錄中的變更。只有在 session 開始時頂層 skills 目錄不存在，才需要重啟。

## 包含什麼

```
tool-calling-tutor/
├── SKILL.md # 主 skill 檔（zh-TW canonical）
├── README.md / .en.md / .zh-Hans.md # 你正在看的這份
├── references/
│ ├── debug-flowchart.md # 4-symptom 診斷流程
│ ├── schema-evolution.md # bad → good schema 4-step worked example
│ └── sdk-diff.md # Anthropic vs OpenAI-compat 並排對照
│ （以上每份都有 .en.md / .zh-Hans.md 翻譯）
├── translations/
│ ├── SKILL.en.md # SKILL.md 英文版（給英語使用者裝）
│ └── SKILL.zh-Hans.md # SKILL.md 簡體版
└── evals/
    ├── evals.json # 5 個離線 contract case
    └── check_evals.py # 不呼叫 model 的檢查器
```

## 跑 evals（選擇性）

```powershell
python evals/check_evals.py
```

這是五個 case 的**離線 contract 檢查**：不問 model，只檢查每條約定是否寫完整、連結是否能找到。`evals.json` 不是 promptfoo 設定檔。若日後要加入 model-graded eval，[promptfoo](https://github.com/promptfoo/promptfoo) 是一個常見的可選路徑；本範例沒有提供 provider 設定，也沒有品質分數。

## 跟其他資源的關係

```
        ┌─────────────────────────────────┐
        │ Stage 3 doc + 練習 1-6 inline │
        │ (學 tool calling 概念) │
        └────────────────┬─────────────────┘
                         │
                         ▼
        ┌─────────────────────────────────┐
        │ examples/stage-3/02-06/ │
        │ (完整可跑 starter + test) │
        └────────────────┬─────────────────┘
                         │ fork template
                         ▼
        ┌─────────────────────────────────┐
        │ 你的 tool-calling agent │
        │ ❓ 卡住了 │
        └────────────────┬─────────────────┘
                         │ 載入
                         ▼
        ┌─────────────────────────────────┐
        │ tool-calling-tutor skill (這個) │
        │ → 4-symptom triage │
        │ → references/ deep dive │
        │ → 路由到 cookbook / Stage 4/7 │
        └─────────────────────────────────┘
```

## 不處理什麼

| 情境 | 路 |
|---|---|
| LangChain / LangGraph / CrewAI / Pydantic AI | Stage 4 |
| 寫 MCP server / client | `resources/cookbook.md` 2 |
| Production observability / cost tracking | Stage 7 |
| 一般 prompt engineering | Stage 2 |

## 延伸

- **改 trigger phrases**：在 SKILL.md frontmatter `description` 加你自己常用的觸發句
- **加你的 case 到 references/**：debug-flowchart 裡開新 Section、把你碰到的 weird case 記下來
- **fork 成你的版本**：這個 skill 設計就是 Stage 5 5.3 的 meta-example、歡迎 fork

<details markdown="1">
<summary>目前來源</summary>

簡短的目前參考（檢查於 2026-08-28 UTC）：[Claude Code skills](https://code.claude.com/docs/en/skills)、[Agent Skills](https://agentskills.io)、[Anthropic skills](https://github.com/anthropics/skills) 與 [promptfoo](https://github.com/promptfoo/promptfoo)。
</details>

## License

跟 repo 一致（MIT）。Skill body 改寫、fork、商用都 OK。
