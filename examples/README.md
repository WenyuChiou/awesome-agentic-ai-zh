<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

# `examples/` — 動手練習可跑範例

> [← 回主路線 README](../README.md)

學習地圖每個 stage 都有「動手練習」section、講「該做什麼」。這個資料夾補上**真的可以跑的範例 code**——複製 → 裝依賴 → `python starter.py` 看到預期輸出。

## 目錄結構

```
examples/
├── stage-2/                     # Prompt 設計
│   ├── 01-prompt-eval-loop/     # 練習：改一件事，再看分數
│   │   ├── starter.py           # 主程式（固定答案 + --live）
│   │   ├── starter_anthropic.py # Anthropic 對照版
│   │   ├── test.py              # Ollama 路徑自我驗證
│   │   ├── test_anthropic.py    # Anthropic 路徑自我驗證
│   │   ├── README.md            # 三語走查（+.zh-Hans.md +.en.md）
│   │   └── requirements.txt     # 有上下限的依賴版本
├── stage-3/                     # Tool Use & Agent 入門
│   ├── 01-function-calling/     # 練習 1：一個工具、一次呼叫
│   │   ├── starter.py           # Ollama 路徑
│   │   ├── starter_anthropic.py # Anthropic 路徑
│   │   ├── test.py              # Ollama 路徑自我驗證
│   │   ├── test_anthropic.py    # Anthropic 路徑自我驗證
│   │   ├── README.md            # 三語走查（+.zh-Hans.md +.en.md）
│   │   ├── README.en.md         # English walkthrough
│   │   ├── README.zh-Hans.md    # 简体中文走查
│   │   └── requirements.txt     # 有上下限的依賴版本
│   ├── 03-react-from-scratch/   # 練習 3：從零實作 ReAct
│   │   ├── starter.py           # 主程式
│   │   ├── test.py              # 自我驗證（pure assert、無 pytest）
│   │   ├── README.md            # 200-400 字走查（+.zh-Hans.md +.en.md）
│   │   └── requirements.txt     # 依賴釘版本
│   └── ...
├── stage-1/
└── ...
```

短的練習（≤30 LOC）直接以 `<details markdown="1">` 收摺塞在 stage 檔內、不開資料夾。長的（>30 LOC）才開資料夾——避免 stage 檔被 code block 撐爆。

## 怎麼跑任一個範例

```powershell
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py                     # Ollama 路徑
$env:ANTHROPIC_API_KEY = "your-key"
python starter_anthropic.py           # Anthropic 路徑
python test.py                        # 跑驗證（用 mock、不花錢）
```

## 設計原則

| 維度 | 規則 |
|---|---|
| 程式長度 | starter ≤80 LOC、超過拆檔 |
| 依賴 | stdlib + 最多 2 個 pip 套件、釘版本 |
| 測試 | 純 `assert`、不用 pytest、reader 跑 `python test.py` 看 ✅ |
| 註解 | 中文（zh-TW 為主）、變數 / 函式名英文 |
| 自我驗證 | 每個 starter.py 結尾必有 `# === 自我驗證 ===` 區塊 |
| 環境變數 | 頂端註解寫清楚需要哪些 key |
| Free-tier 友善 | 用最便宜 model（claude-haiku / Ollama）、註解寫怎麼換 Sonnet |
| **Windows 編碼** | **每個 .py 頂端必須有 UTF-8 reconfigure**（見下） |

### Windows cp950 編碼 fix（每個 starter.py / test.py 必加）

Windows 預設 console 是 cp950（Big5）、印不出 emoji 跟非 Big5 中文。每個 `.py` 檔頂端 import 區後立刻加：

```python
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
```

否則 Windows reader 在 PowerShell / cmd 跑會炸 `UnicodeEncodeError: 'cp950' codec can't encode character '✅'`。

## 三條路徑 — **預設用 Ollama（成本考量）**

> 💰 **為什麼默認 Ollama？** Ollama 的 API 成本是 $0，但不包含硬體與電費。Cloud LLM 以輸入／輸出 token 計費：Haiku 4.5 是每 1M input $1、每 1M output $5；預留 $0.05，再用 `（input_tokens × $1 + output_tokens × $5） / 1,000,000` 估算，並以 2026-08-27 的官方定價核對。**學習階段不該被 API 成本卡住**。

每個練習都同時提供 3 條路徑：

### Path A（**默認、推薦**）— Ollama 本機
- 預設 `starter.py` / 第一個 inline `<details markdown="1">` 用本機 LLM
- 需 [Ollama](https://ollama.com)、按 stage pull 對應 model：
  - **Stage 1 + 2**（純 chat / prompt eng）：`ollama pull gemma4:e4b`（~7.5 GB、多模態、CPU 跑得動）
  - **Stage 3+**（tool use / agent）：`ollama pull qwen2.5:3b`（1.9 GB；模型表現會變，請在自己的電腦上跑資料夾內的固定測試）
- Ollama API 成本是 $0（不包含硬體與電費）、offline、隱私敏感資料 OK
- SDK 用 `openai` package（OpenAI-compatible API）、`base_url="http://localhost:11434/v1"`
- 適合：所有讀者（默認推這條）

### Path B（選擇性）— Anthropic API（想看 cloud 高品質時）
- 對照 `starter_anthropic.py`（folder）或第二個 inline `<details markdown="1">` 區塊
- 需 `ANTHROPIC_API_KEY`；以 Haiku 4.5 每 1M input $1、每 1M output $5 的公式估算，預留 $0.05，並以 2026-08-27 的官方定價核對
- 行為會隨模型、提示與硬體而變；用固定 eval 實測
- 適合：production 要求高品質、需要 long-context、Stage 7 production tier

### Path C（驗邏輯、不打 API）
- 所有 `test.py` 都用 `unittest.mock`、`python test.py` 看程式邏輯有沒有寫對
- 跟 Path A / B 互補：先 mock 驗邏輯、再 real call 確認

### 三條路的 Trade-off

| 維度 | A Ollama（默認）| B Anthropic | C Mock |
|---|---|---|---|
| Cost / call | $0（不含硬體／電費） | $0.05 預留；依上方 token 公式 | $0 |
| 需要 | Ollama install | API key | 無 |
| 答案品質 | 會變；請跑資料夾內的固定測試 | 會變；請用同一組固定測試比較 | 預設答案，看不出模型的真實表現 |
| 速度 | 依硬體；用固定 eval 實測 | 依服務；用固定 eval 實測 | 依環境；用固定 eval 實測 |
| Offline | ✅ | ❌ | ✅ |
| 隱私敏感資料 | ✅ | ❌ | ✅ |
| Stage 3+ tool use | ✅（qwen2.5 / llama3.2） | ✅ | ✅ |
| 適合 | **默認、無預算壓力** | production 升級 | 程式邏輯驗證 |

→ **建議流程**：先 C 驗邏輯（不花錢）、再 A 本機跑看實際 model 行為、production 階段（Stage 7）再升 B 看 cloud 品質。

## 推薦 LLM 清單

> 本機 + cloud、user 視角。  
> 💡 不是要你全裝、是讓你看到「練習用哪個」「production 升級到哪個」。**Claude 是 canonical / production 主軸；Ollama 是練習默認**。

不知道怎麼選時：Stage 1–2 用 `gemma4:e4b`，Stage 3 起用 `qwen2.5:3b`；想做 cloud 對照再用 Haiku 4.5。

<details markdown="1">
<summary>📚 展開：模型詳表、價格與替代供應商</summary>

### 本機 LLM（練習默認、用 Ollama）

| Model | 下載大小 | 建議 RAM | 對應 Stage | Tool-use | 速度（CPU/GPU） | 主用途 |
|---|---|---|---|---|---|---|
| **`gemma4:e4b`** ⭐ | 7.5 GB | 8 GB | 1+2 | 基本 | 慢 / 中 | Stage 1-2 純 chat / prompt eng（默認）|
| **`qwen2.5:3b`** ⭐ | 1.9 GB | 4 GB | 3+ | 會變；請跑固定測試 | 依硬體實測 | Stage 3+ tool use / agent（默認）|
| `llama3.2:3b` | 2.0 GB | 4 GB | 3+ | 會變；請跑固定測試 | 依硬體實測 | qwen2.5:3b 的替代 |
| `mistral-nemo:12b` | 7.1 GB | 16 GB | 3+ | 會變；請跑固定測試 | 依硬體實測 | 用固定 eval 比較 |
| `qwen2.5:14b` | 9.0 GB | 16 GB | 進階 | 會變；請跑固定測試 | 依硬體實測 | 大 model 對照 |
| `gemma4:e2b` | 4.0 GB | 4 GB | 1+2 | 基本 | 依硬體實測 | 4GB RAM 機器替代 |

安裝：`ollama pull <model>` + `ollama serve`。詳細硬體配置看 [resources/cli-agents-guide.md](../resources/cli-agents-guide.md)。

### Cloud LLM（canonical / production 主軸、用 Anthropic）

| Model | 每 1M input | 每 1M output | Context | 主用途 |
|---|---|---|---|---|
| `claude-fable-5` | $10 | $50 | 1M | Mythos 級（位階在 Opus 之上）；2026-06-12 暫停、**2026-07-01 恢復**（出口管制解除）——目前最高階的 Claude 層級 |
| **`claude-haiku-4-5-20251001`** ⭐ | $1 | $5 | 200k | Stage 1-7 練習 cloud 對照 |
| **`claude-sonnet-5`** ⭐ | $2 | $10 | 1M | **production 默認**、Stage 5+ agent 開發 |
| `claude-opus-5` | $5 | $25 | 1M | Opus 級旗艦（2026-07-24 推出、接替 Opus 4.8、同價）、複雜推理 / 長 context refactor |

> 💰 API 價格已於 **2026-08-27** 對照 [Anthropic 官方定價頁](https://platform.claude.com/docs/en/about-claude/pricing)。價格會變；真正執行前請再看一次官方頁面。

若你使用訂閱方案而不是 API 計費，請看官方方案頁；訂閱額度與 API 費用不是同一件事。工具選擇詳見 [resources/cli-agents-guide.md](../resources/cli-agents-guide.md)。

### Cloud LLM 中國 / 開源 alternatives（地區限制 / 預算敏感 / 中文場景）

> 不能 / 不想用 Anthropic？這些 API **都 OpenAI-compatible**、改 `base_url` 跟 model name 就能跑本 repo 同一份練習。

| Provider | 主 model | 每 1M input | 每 1M output | OpenAI-compat? | 主賣點 |
|---|---|---|---|---|---|
| **DeepSeek** ⭐ | `deepseek-v4-flash` | $0.14 | $0.28 | ✅ | 最便宜 cloud（比 haiku $1/$5 便宜約 7 倍）、中英文俱佳、含免費 web `chat.deepseek.com` |
| DeepSeek V4-Pro | `deepseek-v4-pro` | $0.44 | $0.87 | ✅ | 更強推理、價格仍遠低於同級 |
| **Moonshot Kimi** | `kimi-k3` | 依階梯 | 依階梯 | ✅ | **1M token context**（賣點）、適合大檔案 / 長對話；價格依 context 階梯、見 platform。web 版 `kimi.com` 免費 |
| **通義千問 Qwen** | `qwen-max` / `qwen-turbo` | $0.50-1.50 | $1.50-6 | ✅（DashScope）| 中文 native、**同 model 也能 Ollama 本機跑**（cloud + local 兩條路徑都通） |
| **智譜 GLM** | `glm-4.5` / `glm-4-plus` | $0.30-2 | $1.50-9 | ✅ | 中國 native、有 free tier。web `chatglm.cn` 免費 |
| **NVIDIA NIM** | Llama / Mistral / DeepSeek / Qwen 等 hosted | free tier 1000 credits | (同) | ✅ | **托管 10+ open model**、新帳號送 credits、不必本機 GPU。`build.nvidia.com` |

**API endpoints（OpenAI SDK 接法）**：

```python
# DeepSeek
client = OpenAI(api_key=os.environ["DEEPSEEK_API_KEY"], base_url="https://api.deepseek.com/v1")
r = client.chat.completions.create(model="deepseek-v4-flash", messages=[...])

# Moonshot Kimi（中國 endpoint；海外用 .ai 結尾）
client = OpenAI(api_key=os.environ["MOONSHOT_API_KEY"], base_url="https://api.moonshot.cn/v1")
r = client.chat.completions.create(model="kimi-k3", messages=[...])

# 通義千問 Qwen（Alibaba DashScope）
client = OpenAI(api_key=os.environ["DASHSCOPE_API_KEY"],
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")
r = client.chat.completions.create(model="qwen-turbo", messages=[...])

# 智譜 GLM
client = OpenAI(api_key=os.environ["ZHIPUAI_API_KEY"], base_url="https://open.bigmodel.cn/api/paas/v4")
r = client.chat.completions.create(model="glm-4.5-flash", messages=[...])

# NVIDIA NIM（hosted open-source）
client = OpenAI(api_key=os.environ["NVIDIA_API_KEY"], base_url="https://integrate.api.nvidia.com/v1")
r = client.chat.completions.create(model="meta/llama-3.3-70b-instruct", messages=[...])
```

**怎麼挑**：

| 情境 | 選 | 理由 |
|---|---|---|
| 中國大陸、無 cloud 訪問 | Ollama 本機 / DeepSeek API | 本機免費；DeepSeek 在中國有 endpoint |
| 預算極敏感（< $1/月） | DeepSeek API | 列示 token 價格較低；用固定 eval 核對行為 |
| 大檔案 / 長文檔 RAG | Moonshot Kimi | 1M token context 賣點 |
| 中文 native task（古文、中文搜索）| Qwen / GLM | 訓練語料中文佔比高 |
| 想試 10+ open model 沒 GPU | NVIDIA NIM | 一個 key 玩 Llama / Mixtral / Qwen / DeepSeek |
| Production agent（agent / tool use）| Anthropic Claude（canonical）| 本 repo Path B 默認；用固定 eval 核對 tool calling 行為 |

</details>

### 預算與時間怎麼估（Stage 1–7 共 54 個練習）

<details markdown="1">
<summary>💰 展開：依自己的電腦與 token 用量計算</summary>

| 學習路徑 | 時間怎麼估 | 成本怎麼估 | 適合誰 |
|---|---|---|---|
| **全本機 Ollama** | 用一個練習實測，再乘預計練習數 | API $0；不含硬體與電費 | 預算敏感、隱私需求、中國大陸無 cloud 訪問 |
| **混合：本機練 + Haiku 終驗** ⭐ | 本機實測時間 + cloud 呼叫次數 | 本機 API $0；cloud 依 Haiku token 公式 | **推薦默認**：先本機練，最後用同一組固定測試核對 cloud 行為 |
| **全 Haiku** | 依服務速度與呼叫次數實測 | `（input × $1 + output × $5）/ 1,000,000` | 想看完整 cloud 體驗 |
| **全 Sonnet** | 依服務速度與呼叫次數實測 | `（input × $2 + output × $10）/ 1,000,000` | 深度練習與 production 對照 |
| **Sonnet 為主 + Opus 難題** | 依兩種模型的呼叫次數實測 | 分別用官方 token 單價計算後相加 | 已是 production agent 開發者 |

> 🎯 **新手默認**：先在本機跑。要用 cloud 前，先用公式估算，再在供應商帳戶設定你能接受的費用上限。**Stage 7 production tier 才考慮 Sonnet 升級**。

</details>

### 怎麼從 Ollama 換到 Anthropic？

每個練習都有 `<details markdown="1">` Path B 區塊或 `starter_anthropic.py`、改 3 行：

```python
# 從這個（Path A 默認）：
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
r = client.chat.completions.create(model="gemma4:e4b", ...)

# 換成這個（Path B、若有 ANTHROPIC_API_KEY）：
import anthropic
client = anthropic.Anthropic()
r = client.messages.create(model="claude-haiku-4-5-20251001", ...)
```

主要差異：messages create 方法名、response shape（`choices[0].message.content` vs `content[0].text`）、tool spec wrap（OpenAI 多一層 `{"type": "function", "function": {...}}`）。詳細對照表見 [`resources/cli-agents-guide.md`](../resources/cli-agents-guide.md)。

## 對應 stage 索引

| Stage | 練習 | 範例位置 |
|---|---|---|
| 1 LLM 基礎 | 6 個 | inline 4 + folder 2（`examples/stage-1/`） |
| 2 Prompt eng | 4 個 | inline 3 + folder 1（`examples/stage-2/`） |
| **3 Tool use** | **6 個** | folder 6（`examples/stage-3/`） |
| 4 Frameworks | 5 個 | 5 個雙路徑、離線可驗證的 folder（`examples/stage-4/`；Python 3.11） |
| 5 Claude Code 生態 | 11 個 | inline 6 + folder 5（`examples/stage-5/`） |
| 6 Memory/RAG | 5 個 | 全 folder（`examples/stage-6/`） |
| 7 Multi-agent | 5 個 | inline 1 + folder 4（`examples/stage-7/`） |
| Track A1-A3 | 12 個 | 12 個 inline 練習；沒有獨立的 `examples/track-a/` 資料夾 |

> Stage 4 的五個 folder 使用不同 framework。請在**每個 folder 各建一個 Python 3.11 `.venv`**，不要合併五份 `requirements.txt`。

→ T1 完成範圍：**只有 Stage 3 全部 6 個**（剩餘 stage 按 plan 分批推進）。

## 貢獻 / 報錯

跑不過、結果跟預期輸出對不上、或想補一個新練習：

- 開 issue 標 `examples` label
- 或直接 PR、follow 本資料夾「設計原則」表格的規則

## 為什麼這樣分（不直接全塞 stage 檔）

1. **Stage 檔保持 readable**：學習地圖讀者不一定要看 code、只想理解 concept；長 code block 干擾閱讀流
2. **範例可獨立演進**：API SDK 升版、model name 改、範例需要單獨 commit、不污染學習地圖 git log
3. **Reader 可以 clone 單一 example**：`svn export` 或 `git clone --filter=tree:0` 只抓一個資料夾
4. **未來 CI**：example 失敗不應 block mdbook deploy；分開可讓 CI 有條件性檢查
