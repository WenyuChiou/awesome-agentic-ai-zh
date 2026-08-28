<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# 練習 4：CodeAct vs JSON tool（Smolagents）

對應 [Stage 4 — Agent Frameworks](../../../stages/04-agent-frameworks.md) 練習 4。
> 🎓 **學習模式**：這份 `starter.py` 是**完整解答**、不是 TODO skeleton。建議用**主動模式**——`mv starter.py starter_reference.py`、看 signature 不看 body、自己重寫一份 `starter.py`、跑 `python test.py` 驗證；卡 20 分鐘再回去對照 reference。完整方法論看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 兩條 SDK path，不是進階深度教材。深度教材推薦：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章節式 + 16 種 production 能力。**本練習對應 hello-agents 的 CodeAct vs JSON tool 章節**
> - [Smolagents 官方 cookbook](https://github.com/huggingface/smolagents/tree/main/examples) + [QuantaLogic/quantalogic](https://github.com/quantalogic/quantalogic)（另一個 CodeAct framework）
> - 完整 references 見 [Stage 4 精選 Projects](../../../stages/04-agent-frameworks.md#-精選-projects)


## 兩種 agent action 路線對照

| 路線 | 怎麼 act | 範例 framework |
|---|---|---|
| **JSON tool** | LLM 回 `{"name": "tool_x", "arguments": {...}}` | OpenAI function calling、LangGraph、CrewAI |
| **CodeAct** | LLM 寫 Python code、直接執行 | HuggingFace Smolagents |

**這題用 CodeAct 解同題（人口比例）、跟練習 1 / 3 的 JSON tool 路線對照**。

## 怎麼跑 — 兩條路徑

> ⚠️ **每個練習都要有自己的 Python 3.11 `.venv`。** 這題還需要 Docker；不要把模型產生的程式碼直接放到主機執行。這個示範容器仍可能連網，所以裡面不要放密碼或私密資料。

### Path A（默認、本機免費）

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
docker version
.\.venv\Scripts\python.exe test_docker_smoke.py
.\.venv\Scripts\python.exe starter.py
```

預算：模型 API 是 **$0**；本機硬體、電力與 Docker 資源仍有成本。小模型可能需要更多修正步驟，所以程式把 `max_steps` 限制為 4。

### Path B（Anthropic、比較雲端結果）

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py
```

預設固定型號：`anthropic/claude-haiku-4-5-20251001`。單次 2,000 input + 1,000 output tokens 的例子為 `$0.007`；CodeAct 可能多輪呼叫，因此先設供應商支出上限 **$0.10**。實際費用看 tokens 與步數。

<details markdown="1">
<summary>macOS／Linux 指令與查核資訊</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
docker version
./.venv/bin/python test.py
./.venv/bin/python test_docker_smoke.py
```

價格公式：`input_tokens / 1,000,000 × $1 + output_tokens / 1,000,000 × $5`。

官方來源：[Secure code execution](https://huggingface.co/docs/smolagents/tutorials/secure_code_execution)｜[Python executors](https://huggingface.co/docs/smolagents/reference/python_executors)｜[Docker port publishing](https://docs.docker.com/engine/network/port-publishing/)｜[Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>套件、model ID、價格與官方連結查核：2026-08-28 UTC。</small>
</details>

## 不花錢驗證程式邏輯

```powershell
.\.venv\Scripts\python.exe test.py # AST、JSON allowlist、loopback 控制埠與資源限制
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic 設定 + 相同安全邊界
```

這兩個離線測試**不會**執行模型產生的程式碼，也不需要 Docker daemon。`test_docker_smoke.py` 是另外一個手動 smoke test：它真的啟動 Jupyter executor，確認主機控制通道可用，而且控制埠只綁在 `127.0.0.1`；先讓 `docker version` 成功再跑。它不會假裝容器不能連網。

## CodeAct 是怎麼運作的

LLM 不回 JSON、而是**回 Python code block**：

````
（user）Find Taipei population, divide by NYC, give ratio.

（LLM 回應）
```python
pop_taipei = lookup_fact(query="Taipei population") # 2602000
pop_nyc = lookup_fact(query="New York population") # 8336000
ratio = calculator(expression=f"{pop_taipei}/{pop_nyc}") # 0.3122
print(ratio)
```

（Smolagents 執行這段 code、把 print 結果接回去給 LLM 繼續）
````

這份範例明確使用 Docker executor。Jupyter 控制埠只綁到主機的 `127.0.0.1`，並移除 Linux capabilities、禁止提權與 pickle，再限制記憶體、process 數與 agent 步數。一般 Docker bridge **仍可能讓容器連到外部網路或主機服務**，所以這只是受控教學示範，不是 production sandbox。需要執行不可信程式碼時，還要加真正的 egress／host 防火牆，或改用有正式隔離邊界的遠端 sandbox。

## CodeAct vs JSON tool 對照

| 維度 | JSON tool | CodeAct |
|---|---|---|
| LLM 輸出形式 | 結構化 JSON | Python 程式碼 |
| 變數綁定 | LLM 要自己記得 / 重複呼叫 | 自然有 variable（`pop_taipei = ...`） |
| 多步運算 | 每步一次 LLM call | 一次寫好幾行 code |
| 一輪 token 數 | 較少 | 較多（code 較長） |
| 對小 model | 較友善（穩定的 JSON） | 較吃力（要產正確 Python） |
| Debug 友善 | tool call 看得清楚 | 看 code execution log |
| 安全考量 | allowlist + 參數驗證 | 不可信程式碼，必須隔離、限權、限資源 |
| 哪些題目擅長 | 單步、邊界明確 | 多步運算、需要中間 variable |

**HuggingFace 的觀點**：CodeAct 更貼近「人類怎麼解問題」——你也是用變數記中間結果、不是每步都重新查。

## 兩個 path 觀察重點

| 觀察項 | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| 產出可執行 Python | 用相同測試題量測 | 用相同測試題量測 |
| 變數命名 / 重用 | 看 execution log | 看 execution log |
| 比例是否算對 | 驗證最終值 | 驗證最終值 |
| 步數 | 由 `max_steps=4` 限制 | 由 `max_steps=4` 限制 |
| 模型 API 成本 | 依 tokens 與步數 | $0 |

**punchline**：CodeAct 比 JSON tool 多了一個「執行程式碼」的風險面。不要先假設哪個模型或路線較好；用相同任務比較成功率、步數、成本與安全邊界。

## 常見坑

- **`@tool` 函式 docstring 是 prompt 的一部分**：Smolagents 把 docstring 當 tool description 給 LLM 看。**docstring 沒寫好、LLM 不知道何時用這 tool**
- **把 Docker 當完整 sandbox**：錯。這份範例只縮小權限並把控制埠綁在 loopback；上線前還要做映像、權限、egress、host access、資源與記錄審查
- **`max_steps` 不夠**：先看錯在哪一步，不要只把數字調大；較大上限會增加費用與 loop 風險
- **模型程式碼有 syntax error**：Smolagents 可以把錯誤接回模型修正，但會增加步數；是否換模型要看評測結果

## 想看更聰明的答案？

```powershell
$env:MODEL="anthropic/claude-sonnet-5"; .\.venv\Scripts\python.exe starter_anthropic.py
$env:MODEL="qwen2.5:7b"; .\.venv\Scripts\python.exe starter.py
```

## 延伸

- **加更多 tools**：`@tool` 裝飾函式即自動 wrap、Smolagents 自動拿 docstring 當 description
- **改 ToolCallingAgent**：Smolagents 也有非 CodeAct 的 `ToolCallingAgent`、用 JSON tool 路線。對照看
- **接 Hugging Face Hub**：用現行 `InferenceClientModel` 呼叫 HF inference（不必本機 Ollama）
- **看 [Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)**：Anthropic 的觀點是兩條路線都合理、看任務
