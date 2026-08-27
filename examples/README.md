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
│   ├── 03-react-from-scratch/   # 練習 3：從零實作 ReAct
│   │   ├── starter.py           # 主程式（~70 行可跑）
│   │   ├── test.py              # 自我驗證（pure assert、無 pytest）
│   │   ├── README.md            # 200-400 字走查（+.zh-Hans.md +.en.md）
│   │   └── requirements.txt     # 依賴釘版本
│   └── ...
├── stage-1/
└── ...
```

短的練習（≤30 LOC）直接以 `<details markdown="1">` 收摺塞在 stage 檔內、不開資料夾。長的（>30 LOC）才開資料夾——避免 stage 檔被 code block 撐爆。

## 怎麼跑任一個範例

```bash
cd examples/stage-3/03-react-from-scratch
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...   # 各範例頂端會說它要哪個 key
python starter.py                     # 跑真的 API 看輸出（會花一點點錢、約 $0.001）
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

> 💰 **為什麼默認 Ollama？** 練習場景跑 1000 次跑滿 Sonnet ~$4、跑 haiku ~$0.25、跑本機 Ollama $0。**學習階段不該被 API 成本卡住**。Cloud LLM 留給「想看高品質答案 / production deployment」時用。

每個練習都同時提供 3 條路徑：

### Path A（**默認、推薦**）— Ollama 本機
- 預設 `starter.py` / 第一個 inline `<details markdown="1">` 用本機 LLM
- 需 [Ollama](https://ollama.com)、按 stage pull 對應 model：
  - **Stage 1 + 2**（純 chat / prompt eng）：`ollama pull gemma4:e4b`（~7.5 GB、多模態、CPU 跑得動）
  - **Stage 3+**（tool use / agent）：`ollama pull qwen2.5:3b`（1.9 GB、tool-use 支援穩定）
- 全程 $0、offline、隱私敏感資料 OK
- SDK 用 `openai` package（OpenAI-compatible API）、`base_url="http://localhost:11434/v1"`
- 適合：所有讀者（默認推這條）

### Path B（選擇性）— Anthropic API（想看 cloud 高品質時）
- 對照 `starter_anthropic.py`（folder）或第二個 inline `<details markdown="1">` 區塊
- 需 `ANTHROPIC_API_KEY`、跑一輪約 $0.001（haiku）/ $0.004（sonnet）
- 答案品質 / latency 都比本機 Ollama 強
- 適合：production 要求高品質、需要 long-context、Stage 7 production tier

### Path C（驗邏輯、不打 API）
- 所有 `test.py` 都用 `unittest.mock`、`python test.py` 看程式邏輯有沒有寫對
- 跟 Path A / B 互補：先 mock 驗邏輯、再 real call 確認

### 三條路的 Trade-off

| 維度 | A Ollama（默認）| B Anthropic | C Mock |
|---|---|---|---|
| Cost / call | $0 | ~$0.001-0.004 | $0 |
| 需要 | Ollama install | API key | 無 |
| 答案品質 | 中（3-4B model） | 高 | 預設、看不出真實品質 |
| 速度 | 5-30s/call（無 GPU） | ~1-3s/call | <0.1s |
| Offline | ✅ | ❌ | ✅ |
| 隱私敏感資料 | ✅ | ❌ | ✅ |
| Stage 3+ tool use | ✅（qwen2.5 / llama3.2） | ✅ | ✅ |
| 適合 | **默認、無預算壓力** | production 升級 | 程式邏輯驗證 |

→ **建議流程**：先 C 驗邏輯（不花錢）、再 A 本機跑看實際 model 行為、production 階段（Stage 7）再升 B 看 cloud 品質。

## 推薦 LLM 清單

> 本機 + cloud、user 視角。  
> 💡 不是要你全裝、是讓你看到「練習用哪個」「production 升級到哪個」。**Claude 是 canonical / production 主軸；Ollama 是練習默認**。

### 本機 LLM（練習默認、用 Ollama）

| Model | 下載大小 | 建議 RAM | 對應 Stage | Tool-use | 速度（CPU/GPU） | 主用途 |
|---|---|---|---|---|---|---|
| **`gemma4:e4b`** ⭐ | 7.5 GB | 8 GB | 1+2 | 基本 | 慢 / 中 | Stage 1-2 純 chat / prompt eng（默認）|
| **`qwen2.5:3b`** ⭐ | 1.9 GB | 4 GB | 3+ | **穩定** | 中 / 快 | Stage 3+ tool use / agent（默認）|
| `llama3.2:3b` | 2.0 GB | 4 GB | 3+ | 穩定 | 中 / 快 | qwen2.5:3b 的替代 |
| `mistral-nemo:12b` | 7.1 GB | 16 GB | 3+ | 強 | 慢 / 中 | 想看更接近 cloud 品質 |
| `qwen2.5:14b` | 9.0 GB | 16 GB | 進階 | 強 | 慢 / 中 | 大 model 對照（需 GPU 偏好）|
| `gemma4:e2b` | 4.0 GB | 4 GB | 1+2 | 基本 | 中 / 快 | 4GB RAM 機器替代 |

安裝：`ollama pull <model>` + `ollama serve`。詳細硬體配置看 [resources/cli-agents-guide.md](../resources/cli-agents-guide.md)。

### Cloud LLM（canonical / production 主軸、用 Anthropic）

| Model | 每 1M input | 每 1M output | Context | 主用途 |
|---|---|---|---|---|
| `claude-fable-5` | $10 | $50 | 1M | Mythos 級（位階在 Opus 之上）；2026-06-12 暫停、**2026-07-01 恢復**（出口管制解除）——目前最高階的 Claude 層級 |
| **`claude-haiku-4-5`** ⭐ | $1 | $5 | 200k | 最便宜、Stage 1-7 練習 cloud 對照都 OK |
| **`claude-sonnet-5`** ⭐ | $3 | $15 | 1M | **production 默認**、Stage 5+ agent 開發 |
| `claude-opus-5` | $5 | $25 | 1M | Opus 級旗艦（2026-07-24 推出、接替 Opus 4.8、同價）、複雜推理 / 長 context refactor |

> 💰 **Sonnet 5 目前是優惠價**：[官方定價頁](https://platform.claude.com/docs/en/about-claude/pricing) 標明 **2026-08-31 前為 $2 / $10**、2026-09-01 起才回到表中的 $3 / $15。下面的預算估算用的是回歸後的標準價，所以現在實際跑會比估算便宜約三分之一。

訂閱替代：Claude Pro $20/月含 Sonnet 用量、Claude Max $100/月含 Opus。詳細看 [resources/cli-agents-guide.md](../resources/cli-agents-guide.md)。

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
| 預算極敏感（< $1/月） | DeepSeek API | 比 haiku 便宜約 7 倍、品質接近 |
| 大檔案 / 長文檔 RAG | Moonshot Kimi | 1M token context 賣點 |
| 中文 native task（古文、中文搜索）| Qwen / GLM | 訓練語料中文佔比高 |
| 想試 10+ open model 沒 GPU | NVIDIA NIM | 一個 key 玩 Llama / Mixtral / Qwen / DeepSeek |
| Production agent（agent / tool use）| Anthropic Claude（canonical）| 本 repo Path B 默認、tool calling 最穩 |

### 預算估算（跑完 Stage 1-7 全 54 練習）

| 學習路徑 | 總時間 | 總成本 | 適合誰 |
|---|---|---|---|
| **全本機 Ollama** | ~30 hr (CPU) / ~10 hr (GPU) | **$0** | 預算敏感、隱私需求、中國大陸無 cloud 訪問 |
| **混合：本機練 + haiku 終驗** ⭐ | ~30 hr | **$2-5** | **推薦默認**：練習 local 跑、最後 1-2 次用 haiku 看 cloud 品質 |
| **全 haiku** | ~10 hr | $5-15 | 想快、預算允許、想看完整 cloud 體驗 |
| **全 sonnet** | ~8 hr | $20-50 | 深度練習、追求高品質答案 |
| **混合：sonnet 為主 + opus 難題** | ~8 hr | $30-80 | 已是 production agent 開發者 |

> 🎯 **新手默認**：先全本機跑、預算上限 $5。**Stage 7 production tier 才考慮 sonnet 升級**。

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
r = client.messages.create(model="claude-haiku-4-5", ...)
```

主要差異：messages create 方法名、response shape（`choices[0].message.content` vs `content[0].text`）、tool spec wrap（OpenAI 多一層 `{"type": "function", "function": {...}}`）。詳細對照表見 [`resources/cli-agents-guide.md`](../resources/cli-agents-guide.md)。

## 對應 stage 索引

| Stage | 練習 | 範例位置 |
|---|---|---|
| 1 LLM 基礎 | 6 個 | inline 4 + folder 2（`examples/stage-1/`） |
| 2 Prompt eng | 4 個 | inline 3 + folder 1（`examples/stage-2/`） |
| **3 Tool use** | **6 個** | inline 1 + folder 5（`examples/stage-3/`） |
| 4 Frameworks | 5 個 | 全 folder（`examples/stage-4/`） |
| 5 Claude Code 生態 | 11 個 | inline 6 + folder 5（`examples/stage-5/`） |
| 6 Memory/RAG | 5 個 | 全 folder（`examples/stage-6/`） |
| 7 Multi-agent | 5 個 | inline 1 + folder 4（`examples/stage-7/`） |
| Track A1-A3 | 12 個 | 12 個 inline 練習；沒有獨立的 `examples/track-a/` 資料夾 |

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
