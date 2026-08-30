<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# `examples/` — 可以直接執行的小練習

> [← 回主路線 README](../README.md)

<!-- freshness: canonical=examples/README.md; verified_on=2026-08-30; scope=example-inventory,local-model-tags,download-sizes,sdk-entry-points; max_age_days=90 -->

Stage 章節先告訴你「這個觀念是什麼」；這個資料夾讓你真的跑一次。第一次不用把所有模型都裝好，也不用先讀完整份程式。

## 📌 先分清五個詞

| 核心詞 | 五歲也能懂的說法 | 正確意思 |
|---|---|---|
| **Example（範例）** | 已經拼好的小積木 | 可以直接執行、觀察結果的示範程式 |
| **Starter（起始程式）** | 留幾塊給你自己拼 | 練習用的最小程式入口，通常是 `starter.py` |
| **Path（路徑）** | 到同一個終點的不同條路 | 本專案用 Path A／B／C 表示不同執行方式 |
| **Mock（模擬答案）** | 先用玩具電話練習 | 不連真實模型，先檢查程式邏輯 |
| **Live call（真實呼叫）** | 真的把電話打出去 | 連本機或雲端模型，結果、時間與費用都可能改變 |

## 🎯 你會學會什麼

- 先用 **Mock** 找程式錯誤，再做 **Live call** 看模型行為。
- 知道 Ollama、Anthropic API 與測試各自負責什麼。
- 從 Stage 索引找到正確資料夾，不用猜檔名。
- 看懂測試結果、diff 與限制，不把「有輸出」誤認成「已經正確」。

## 📚 必讀閱讀

1. [安裝與環境設定](../resources/setup-guide.md)：先讓 Python、Git 與選用的模型路徑能工作。
2. [Stage 1：LLM 基礎](../stages/01-llm-basics.md)：選模型、看費用與理解 Context。
3. [CLI Agents 指南](../resources/cli-agents-guide.md)：分清 Coding Agent、Router 與 Local Runtime。

## 🛠 第一次執行：先跑不花模型費的測試

以下範例有完整的 `test.py`。先複製這三行：

```powershell
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
python test.py
```

看到通過訊息，代表程式的固定邏輯能工作；它還沒有證明任何模型一定會答對。接著再選一條真實模型路徑。

| 路徑 | 誰真的產生答案 | 先做什麼 | 適合什麼時候 |
|---|---|---|---|
| **Path C：Mock** | 固定的假答案 | `python test.py` | 第一個步驟；先找程式錯誤 |
| **Path A：Ollama** | 你電腦上的模型 | 安裝 Ollama、pull 該題指定模型 | 練習真實模型行為，不產生供應商模型 API 帳單 |
| **Path B：Anthropic** | Anthropic 雲端模型 | 設定 `ANTHROPIC_API_KEY` | 想用同一題比較雲端品質時 |

<details markdown="1">
<summary>展開 Path A／B 的完整命令、環境與費用提醒</summary>

### Path A：Ollama

```powershell
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

本機執行不會產生供應商模型 API 帳單，但仍會使用下載空間、記憶體、電力與時間。檔案、log 和工具權限仍要保護。

### Path B：Anthropic API

```powershell
$env:ANTHROPIC_API_KEY = "your-key"
python starter_anthropic.py
```

雲端呼叫可能使用額度或產生費用。執行前看當日官方 pricing／usage 頁，設定自己能接受的上限；不要把 key 寫進程式或 commit。

</details>

## 🧭 依 Stage 找範例

這裡只列實際存在的資料夾；短練習仍會直接放在 Stage 章節中。

| Stage | 這一關在學什麼 | 可執行資料夾 |
|---|---|---|
| [Stage 1](../stages/01-llm-basics.md) | LLM 基礎與錯誤處理 | `stage-1/`：2 個 |
| [Stage 2](../stages/02-prompt-engineering.md) | Prompt 設計與小型評測迴圈 | `stage-2/`：1 個 |
| [Stage 3](../stages/03-tool-use-and-hello-agent.md) | **工具使用與第一個 Agent Loop** | `stage-3/`：6 個 |
| [Stage 4](../stages/04-agent-frameworks.md) | **Workflow Graph 與 Agent 框架** | `stage-4/`：5 個；各用自己的 Python 3.11 環境 |
| [Stage 5](../stages/05-claude-code-ecosystem.md) | Claude Code 生態與 Skill | `stage-5/`：1 個；其餘是章內練習 |
| [Stage 6](../stages/06-memory-rag.md) | Embedding、RAG 與 Memory | `stage-6/`：5 個 |
| [Stage 7](../stages/07-multi-agent-production.md) | **Agent Production Engineering** | `stage-7/`：5 個 |
| [Track A1–A3](../tracks/cli/A1-cli-intro.md) | CLI 工作流 | 章內練習；沒有 `examples/track-a/` |

## 🧠 本機模型怎麼選

模型不是「越新就一定越適合」。先用題目指定的 tag，再跑固定測試。下載大小以 Ollama 官方 tag 頁在 **2026-08-30 UTC** 的顯示為準。

| 範圍 | 預設 tag | 官方顯示下載大小 | 為什麼 |
|---|---|---:|---|
| Stage 1–2 | [`gemma4:e4b`](https://ollama.com/library/gemma4:e4b) | 9.6 GB | 純對話與 Prompt 練習 |
| Stage 3–6 | [`qwen2.5:3b`](https://ollama.com/library/qwen2.5:3b) | 1.9 GB | 目前範例的工具呼叫練習預設 |
| Stage 7 | [`qwen3.5:4b`](https://ollama.com/library/qwen3.5:4b) | 3.4 GB | 觀察評測、監控與部署流程 |

完整的現行模型、價格、Context 與替代方案只在 [Stage 1](../stages/01-llm-basics.md) 維護，避免兩頁講成不同版本。

## ✅ 資料夾不是都長一樣

先開該題的 `README`。檔名會跟著要學的事情改，不要因為沒看到 `starter.py` 就以為檔案壞了。

| 形狀 | 實際資料夾 | 你會看到什麼 |
|---|---|---|
| 標準雙路徑 | 多數 Python 練習 | `starter.py`、`starter_anthropic.py`、兩個離線測試、三語 README、`requirements.txt` |
| Provider 切換 | `stage-1/04-cross-provider/` | 只用 OpenAI-compatible client 比較 endpoint，所以只有 `starter.py` 與 `test.py` |
| Schema 好壞比較 | `stage-3/06-schema-design/` | `starter_bad*` 與 `starter_good*`，不是一般 starter 檔名 |
| Framework／部署加碼 | `stage-4/01-same-agent-two-frameworks/`<br>`stage-4/04-codeact-vs-json-tool/`<br>`stage-7/05-deploy/` | 在標準雙路徑外，再加 CrewAI、Docker smoke test 或 `Dockerfile` |
| Skill 套件 | `stage-5/tool-calling-tutor/` | `SKILL.md`、references、translations 與三語 README；它不是 Python starter 專案 |

設計底線：每個 Python 練習都要能用離線測試檢查固定邏輯；Skill 套件由 repository 結構測試檢查。starter 保持小；環境變數只放假 key 範例；真實模型行為用固定 eval 核對；不要關掉必要 hook 或 approval。

<details markdown="1">
<summary>展開 Windows 編碼、貢獻規則與排錯</summary>

- Windows 的 `starter.py`／`test.py` 需把 stdout 設為 UTF-8，避免 cp950 無法輸出中文或 emoji。
- 一個 starter 原則上不超過 80 LOC；更深的完整教學改連官方文件或 canonical tutorial。
- 跑不過時先記錄資料夾、Python 版本、完整錯誤、執行命令與使用的 Path，再開 issue。
- 不要把真實 API key、`.env`、私人資料、模型回覆 log 一起上傳。

</details>

## 🎯 精選 Projects 與學習資源

星星是本學習地圖的閱讀優先度，不是 GitHub stars，也不是工具總排名。

<table>
<thead><tr><th>分類</th><th>資源</th><th>先學什麼</th><th>評分</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="2">模型執行</th><td><a href="https://github.com/ollama/ollama">ollama/ollama</a></td><td>先在本機跑一個模型，再讓 starter 呼叫它</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/vllm-project/vllm">vllm-project/vllm</a></td><td>需要伺服器級吞吐量時再學</td><td>⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">Python SDK</th><td><a href="https://github.com/openai/openai-python">openai/openai-python</a></td><td>理解 OpenAI-compatible client 與 response shape</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/anthropics/anthropic-sdk-python">anthropics/anthropic-sdk-python</a></td><td>比較 Anthropic messages 與 tool schema</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="2">驗證與資料</th><td><a href="https://github.com/pytest-dev/pytest">pytest-dev/pytest</a></td><td>從小型 assert 走到可重複的測試</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/pydantic/pydantic">pydantic/pydantic</a></td><td>驗證工具輸入、結構化輸出與錯誤</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
</table>

## ✅ 完成檢查

- [ ] 我能從 Stage 索引找到一個真的存在的資料夾。
- [ ] 我先跑 Mock，再決定要不要做 Live call。
- [ ] 我知道 OpenRouter 是 Router、Ollama 是 Local Runtime、OpenCode／Pi 是 Coding Agent。
- [ ] 我沒有把 key 或私人資料寫進 repo。
- [ ] 我用測試與 diff 判斷結果，不只看「程式有輸出」。

<small>範例目錄、模型 tag 與官方入口查核：2026-08-30 UTC。</small>
