# Stage 1 — LLM 基礎（LLM Basics）

> **繁體中文** | [简体中文](./01-llm-basics.zh-Hans.md) | [English](./01-llm-basics.en.md)

⏱ **時間估算**：1 週（約 5-8 小時）

> 👋 **從 [Stage 0](00-foundations.md) 來的**：好，環境已經夠用——這 5-8 小時：第一次成功呼叫 Claude / GPT / Gemini API、搞懂 token / context window / temperature 怎麼影響輸出、用 per-token 計算實際成本。**直接從這裡開始的**：先確認你能跑 Python script、有任一家供應商的 API key——做不到請先回 [Stage 0](00-foundations.md)。

> 💡 **看不懂某個詞**（LLM / token / context window / temperature / RAG / agent⋯）→ 先翻 [`resources/glossary.md`](../resources/glossary.md) 查 30 秒再回來。

> 📋 **本章組成**：學習目標 → 進入條件 → 必修閱讀 →〔可選 · 概念地圖〕→ 動手練習 → 精選 Projects → 自我檢查  
> 🔑 **關鍵名詞**：見 [`resources/glossary.md`](../resources/glossary.md)（每 stage 用到的術語都收在那裡）

### 三個核心詞（先記住、後面 stage 都會用到）

| 詞 | 中文 | 一句話 |
|---|---|---|
| **token** | 詞元 | 模型計算文字長度與費用的基本單位（中文 1 字 ≈ 1.5-2 token） |
| **context window** | 上下文視窗 | 模型一次能看到多少 token（Claude 1M / GPT 1.05M / Gemini 2M）|
| **temperature** | 隨機程度參數 | 控制回答穩定或發散（0 = 最穩定、1 = 創意；分類任務用 0.0-0.3、創作用 0.7-1.0）|

→ 這 3 個詞貫穿後續所有 stage。Stage 1 的目標就是讓你用 API 跑出來、親手摸到它們如何影響輸出。

> 🧠 **temperature 為什麼能調？先懂 next-token**：LLM 的核心動作是**預測下一個 token**：它對「下一個字」算出一個機率分布，再從裡面**抽樣**一個。`temperature` 跟 `top_p` 就是在「重塑這個分布」——temperature 低 → 分布變尖、幾乎只挑最可能的（穩定、可重現）；temperature 高 → 分布變平、更敢挑冷門字（有創意但易跑題）。`max_tokens` 則是「最多抽幾次就停」。所以這些不是魔法旋鈕，而是在控制「怎麼從機率分布裡選字」。

## 📌 學習目標

走完這個階段後你會：

- 解釋 LLM 是什麼、token 是什麼、context window 是什麼意思
- 第一次成功呼叫 Claude / GPT / Gemini API 並解析回應
- 在強項上比較四大 LLM 家族（Claude / GPT / Gemini / Llama）
- 用 per-token 計價來估算單次任務的成本

## 🌐 主流 LLM 家族對比（2026-05 snapshot）

「Claude 跟 GPT 有什麼不同？」「中國模型能用嗎？」「我該裝 Ollama 跑哪個 OSS model？」——這節給你**客觀對照**。不下「最好」結論——用 **強項 / 適合任務 / 弱項** 3 維比較、附**官方 docs URL**讓你自己 verify。

> 💡 **先解釋幾個名詞**：
> - **Context window** = LLM 一次能記住的對話量、有上限（譬如 200k token ≈ 15 萬中文字）
> - **Apache 2.0 / MIT** = 可商用 / 可改 / 可閉源的開源條款；**Llama Community License** = 開源但有條款限制（譬如 ≥ 7 億 MAU 要授權）
> - **Frontier model** = 各家最強旗艦；**OSS** = open-source、weights 可下載 self-host

### 🇺🇸 美系商業 frontier（3 家）

這 3 家是 SaaS API、付 token 用、不能 self-host：

<!-- 維護慣例（下面 3 張表共用）：「旗艦」這格只寫現在的旗艦，最多再留前一代；出了新的就把舊名字換掉、別一直往上加；太舊、官網已經查不到的就刪掉。會變的資訊（暫停、preview、還沒出）別塞在格子裡，寫到表格下面那行「註」；等狀態結束了（正式上線、恢復、或永久退役）就把那行刪掉。「Context」這格只填數字。改完記得更新標題的月份（2026-MM）。 -->

| Model 家族 | 旗艦（2026-07）| Context | 強項 | 適合任務 | 官方 docs |
|---|---|---|---|---|---|
| **Claude**（Anthropic）| Opus 5 / Sonnet 5 / Haiku 4.5 | 1M | long-form / coding / agent / safety alignment | 寫 paper / code review / agent runtime | [platform.claude.com/docs](https://platform.claude.com/docs/en/about-claude/models/overview) |
| **GPT**（OpenAI）| GPT-5.6 Sol / Terra / Luna | 1.05M | 通用 / function calling / ecosystem 最廣 | 廣度查詢 / function-call 框架 / GPTs 生態 | [platform.openai.com/docs/models](https://platform.openai.com/docs/models) |
| **Gemini**（Google）| 3.5 Flash / 3.5 Pro（開發中）| 2M | 長 context / 原生 multimodal / Google 整合 | PDF / 影音 / 大量文件 / Google Workspace | [ai.google.dev](https://ai.google.dev/gemini-api/docs/models/gemini) |

> **註**：`（開發中）`= 還沒推出。Claude **Fable 5**（Mythos-class、位階在 Opus 之上、$10/$50）是目前最強的 Claude 層級；**Opus 5**（2026-07-24 推出、`claude-opus-5`、1M、$5/$25，跟前一代 Opus 4.8 同價）是官方 docs 建議的預設起點，Anthropic 宣稱它「接近 Fable 5 的能力、一半的價格」。**Opus 4.8 仍可用**（官方 docs 已移入 Legacy 區、未 deprecated）。Context 欄填的是旗艦的上限：Gemini Pro 系列 2M、Flash 1M；Claude 1M（Haiku 4.5 是 200k）；GPT-5.6 三款都是 1.05M。另外 **Sonnet 5**（2026-06-30 上線）是目前的 Sonnet 版本：1M context、速度快、比 Opus 便宜（$3/$15，Opus 是 $5/$25）。**GPT-5.6**（2026-07 上線）分三級：**Sol** 旗艦（$5/$30）、**Terra** 均衡（$2.50/$15）、**Luna** 最快最省（$1/$6），ChatGPT / Codex / API 皆可用。

### 🇨🇳 中國商業 + 開源 frontier（7 家）

中文場景的主力，分兩類：**純 API**（雲端付費、不能 self-host）和**有開源 weights**（可在自己機器跑）。

**① 純 API（雲端、付費為主）**

| Model 家族 | 旗艦（2026-05）| Context | 強項 | 適合任務 | 官方 |
|---|---|---|---|---|---|
| **DeepSeek**（深度求索）| V4-Flash（`deepseek-v4-flash`）/ V4-Pro（`deepseek-v4-pro`）| 1M | 推理 / coding / **cost 最低** | 大量 token / code 生成 / math | [api-docs.deepseek.com](https://api-docs.deepseek.com/zh-cn/) |
| **Kimi**（Moonshot）| K3（2.8T 參數、原生多模態）| **1M** | 長 context / 中文長文 | 整本書讀 / 文獻分流 | [platform.moonshot.cn](https://platform.moonshot.cn/) |
| **Hunyuan**（騰訊）| T1（深度思考）+ TurboS | 128k | **深度思考推理**（對標 DeepSeek R1 這條 2025 推理基線）、中文 | 中文推理 / 騰訊生態 | [hunyuan.tencent.com](https://hunyuan.tencent.com/) |
| **MiniMax** | M3 | 1M | 多模態 / 中文長 prose / coding | 中文寫作 / 影音 multimodal | [platform.minimax.io](https://platform.minimax.io/) |

> **註**：這組以雲端 API 為主、多為 proprietary。DeepSeek 另有部分開源權重（在 HF），主要用法仍是雲端 API（舊名 `deepseek-chat`/`deepseek-reasoner` 於 2026-07-24 停用、已改指向 v4-flash）。

**② 有開源 weights（可 self-host）**

| Model 家族 | 旗艦（2026-05）| Context | 強項 | 適合任務 | 官方 |
|---|---|---|---|---|---|
| **Qwen**（阿里）| Qwen 3.7 / 3.6（開源）| 128k+ | **中文最強 OSS** / 多模態 / agent | 中文長文 / agent / self-host | [qwen.ai](https://qwen.ai/) · [DashScope](https://help.aliyun.com/zh/dashscope/) |
| **GLM**（智譜 Zhipu）| GLM-5.2 | 1M | 中文 / tool use / agent | 中文 agent / 多輪對話 | [open.bigmodel.cn](https://open.bigmodel.cn/) · [chatglm.cn](https://chatglm.cn/) |
| **Yi**（01.AI / 李開復）| Yi-Lightning / Yi-34B-Chat | 200k | **中文 OSS**（⚠️ 01.AI 2025 起停 foundation 訓練、Yi 已凍結）| 中文 self-host / 中文 API | [01.ai](https://01.ai/) · [GitHub](https://github.com/01-ai/Yi) |

> **註**：這三家都走 **開源版（Apache 2.0 或 MIT）+ 付費雲端 API** 兩條路（GLM 開源版現為 5.2、MIT）。開源版可用 [Ollama](https://ollama.com/) 在自己機器跑。

> ⚠️ **小米 MiMo** 雖在 [`resources/cli-agents-guide.md`](../resources/cli-agents-guide.md) 列入 Hermes Agent routing、但 2026-05 無權威官方 source 可驗證、暫不收進此表。要試 → 透過 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 200+ provider routing 接入。

### 🌍 西方開源（5 家、self-host 主力）

跑在自己機器、不付 API、隱私敏感場景的主力——可透過 [Ollama](https://ollama.com/) 一行指令裝起來：

| Model 家族 | 大小（活躍）| License | 強項 | 適合任務 | 官方 |
|---|---|---|---|---|---|
| **Llama**（Meta）| 3.3 70B | Llama Community License | 通用 / 生態最廣 / Ollama 預設 | self-host 入門 / fine-tune base | [llama.com](https://www.llama.com/) · [HF Meta](https://huggingface.co/meta-llama) |
| **Muse**（Meta）| Glimmer 30B dense | Apache 2.0 | **agent 專用**（tool use / 長任務 / 失敗回復）/ 多模態輸入 / 131k context | 本機 agent / coding agent / 單張消費級 GPU | [developer.meta.com](https://developer.meta.com/ai/models/muse-glimmer/) · [HF meta-models](https://huggingface.co/meta-models/Muse-Glimmer-30B) |
| **Gemma**（Google）| Gemma 4 26B MoE + 31B dense | Apache 2.0 | **小巧高效** / Apple MLX 整合好 / multimodal | Edge / mobile / 4-8GB RAM 機器 | [ai.google.dev/gemma](https://ai.google.dev/gemma) |
| **Mistral**（Mistral AI）| Small 4 / Ministral 3 / Large 3 | 開源權重（license 依版本、Large 3 為 Apache 2.0）| Small 4 統一 reasoning / vision / coding、EU 主權 | 商用 self-host / EU 主權 | [mistral.ai](https://mistral.ai/) · [HF Mistral](https://huggingface.co/mistralai) |
| **Phi**（Microsoft）| Phi-4 14B + multimodal | MIT | **小但強** / reasoning / 適 edge | 4GB+ RAM / mobile / reasoning 入門 | [HF microsoft](https://huggingface.co/microsoft) |

> **註**：Llama 4（Scout / Maverick）於 2025-04 釋出，但屬大型 MoE，單機自架的實用基準仍是 3.3 70B（表中為 3.3）、Behemoth 未釋出；Gemma 4 為 2026-04 釋出、LMArena 開源組第 3；Phi-4 另有 multimodal 版。**Muse Glimmer** 為 2026-08-10 釋出、Meta 第一個專為 agent 設計的開放權重模型，由閉源的 **Muse Spark** 蒸餾而來(Meta 自己說它「整體不如 Spark」);**Spark 的 weights 目前還沒釋出**——Meta 說會放，但 HF 上還查不到，所以這裡只收 Glimmer。注意 Meta 現在兩條線並行:Llama 走 Llama Community License,Muse 走 Apache 2.0。

### 🎯 我該選哪家？（按場景反查）

| 你的場景 | 推薦 + 為什麼 |
|---|---|
| 第一次學 LLM API、教材完整度優先 | **Claude** — Anthropic Cookbook + Courses 是社群公認最完整 |
| 寫長文 / paper / code review | **Claude Sonnet** — long-form prose 強項 |
| 多模態（PDF / 影音 / 圖）| **Gemini** 或 **Kimi** — 原生 multimodal |
| 廣度查詢 + function calling 框架 | **GPT** — ecosystem 最廣、SDK 整合最深 |
| **中文場景 + 商業 API** | **Kimi**（長 context 強、能塞整本書）或 **DeepSeek**（cost 最低）或 **GLM**（agent 友善）|
| **中文場景 + 開源 self-host** | **Qwen 3.7 / GLM-5.2**（Apache 2.0 / MIT、中文最強 OSS 之一）|
| 推理 / math（reasoning model）| **DeepSeek V4-Pro** / **Hunyuan T1** / **OpenAI o-series** |
| 隱私 / offline / 不付 API | **Llama 3.3** / **Gemma 4** / **Qwen 3 OSS** via [Ollama](https://ollama.com/) |
| Edge / 4GB RAM 機器 | **Gemma 4** / **Phi-4** / **Qwen 3（3B 以下版本）** |
| 100k+ token 大文件 | **Gemini 3.1**（2M context）或 **Kimi K3**（1M）|
| **想 cost 最低**（API 帳單敏感）| **DeepSeek V4-Flash** — 同級英文 model 中 token 單價最低 |

### 📊 中立 benchmark 資源（自己 verify、不靠單一 source）

| 資源 | 用途 | URL | 2026-05 狀態 |
|---|---|---|---|
| **Artificial Analysis** | 第三方 benchmark + price/latency 整合（含中國 model）| https://artificialanalysis.ai/ | ✓ Active |
| **Arena AI**（前 LMSYS Chatbot Arena）| 人類盲測 ELO 排名 | https://arena.ai/leaderboard/text | ✓ Active |
| **Vellum LLM leaderboard** | 多 benchmark 整合 | https://www.vellum.ai/llm-leaderboard | ✓ Active |
| **HuggingFace OpenLLM Leaderboard** | 開源 model 排名 | https://huggingface.co/spaces/open-llm-leaderboard | ⚠️ 2026-05 偶爾 runtime error、改看 [Arena AI](https://arena.ai/) 開源 tab |
| **SuperCLUE**（中文 benchmark）| 中文場景權威評測 | https://www.superclueai.com/ | ✓ Active |

### ⚠️ 重要警語

- ⚠️ **Benchmark ≠ production performance**——LLM 在你 specific 任務的表現要自己跑 small eval（譬如貼 10 個你真實 prompt 看哪家答得最像你要的）、**不能只看排名選**
- ⚠️ **Frontier 6 個月洗牌一次**——上面所有數字是 **2026-05 snapshot**、之後請以**官方 docs** / [Artificial Analysis](https://artificialanalysis.ai/) 為準
- ⚠️ **「強項」是相對的、不是絕對的**——所有 frontier model 都能完成基本任務、差別在特殊或困難的情境（超長文件、複雜推理、多語言）
- ⚠️ **中文場景看 [SuperCLUE](https://www.superclueai.com/)**——一般國際 benchmark（如 MMLU）以英文為主、中文表現可能跟英文不一致

## 🚪 進入條件

你應該已經：

- 能跑 Python script
- 概念上知道 HTTP / REST 是什麼
- 至少有一家供應商的 API key（Anthropic / OpenAI / Google）

如果還沒——先回 Stage 0。

## 📚 必修閱讀

1. [**Anthropic — Claude 模型總覽**](https://docs.claude.com/en/about-claude/models/overview) — 官方模型 family、含 2026 的 Claude Fable 5（`claude-fable-5`、Mythos-class、2026-06-09 GA）以及 Opus 5 / Sonnet 5 / Haiku 4.5。**Fable 5 是目前最高階的 Claude 層級；Opus 5（2026-07-24 推出、`claude-opus-5`）是現行的 Opus 級旗艦，Opus 4.8 仍可用（官方 docs 已移入 Legacy 區、未 deprecated）。**
2. [**anthropics/courses — Anthropic API Fundamentals**](https://github.com/anthropics/courses) ⭐⭐⭐⭐⭐ ★ 22k+ — Anthropic 官方 5 course umbrella、**module 1「Anthropic API Fundamentals」對應本 stage**。Jupyter notebook、用 Claude 3 Haiku（最便宜）跑、跟著做就能拿到 API 基本功
3. [**OpenAI Quickstart**](https://platform.openai.com/docs/quickstart) — 第一次 API call 的步驟
4. [**A Visual Guide to LLM Tokenizers**](https://huggingface.co/learn/llm-course/chapter6/1) — Hugging Face 的入門
5. [**Anthropic API Pricing**](https://www.anthropic.com/pricing#anthropic-api) — 把計價表看完，算一下 1k input + 1k output 的成本

**🎥 中文影片補充（強烈推薦）**：

- [**李宏毅 — 生成式 AI 導論（2024 春台大課程）**](https://speech.ee.ntu.edu.tw/~hylee/genai/2024-spring.php) ⭐⭐⭐ — 第 1-5 集講 LLM 是什麼、怎麼運作、token / context window / temperature 怎麼影響輸出。中文圈最高品質的 LLM 學術級導論、台大授課、官方頁含投影片 + YouTube。最新整合版見 [**GenAI-ML 2025 秋**](https://speech.ee.ntu.edu.tw/~hylee/GenAI-ML/2025-fall.php)
- [**3Blue1Brown — Transformer 視覺化**](https://www.youtube.com/watch?v=wjZofJX0v4M)（中文配音版：[3Blue1Brown 中文](https://space.bilibili.com/88461692)）— LLM 內部運作 visual intro
- [**Andrej Karpathy — Intro to LLMs**](https://www.youtube.com/watch?v=zjkBMFhNj_g) — 英文影片、1hr、英文圈最被推薦的 LLM 入門影片

## 🛠 動手練習（基礎 illustrative 練習）

> 🦙 **本 stage 預設用 Ollama**（成本考量、本機 `gemma4:e4b` 跑得動、$0/run）。每個練習都有 Path A（Ollama、預設）+ Path B（Anthropic、選擇性、想看 cloud 高品質時用）。完整 3 路 trade-off 見 [`examples/README.md`](../examples/README.md#三條路徑--預設用-ollama成本考量)。
>
> 💰 **Stage 1 預算估算**（全 6 練習各跑 3-5 次）：**全本機 = $0**、**全 haiku ≈ $0.30**、**全 sonnet ≈ $0.90**。完整 model 清單 + Stage 1-7 全程預算估算見 [`examples/README.md#推薦-llm-清單`](../examples/README.md#推薦-llm-清單)。
>
> 💡 **只想讀、不想裝 Ollama** — 直接看每個練習的 Path B（Anthropic）區塊就好。想實際跑 Path A 才需要 [`pip install openai && ollama pull gemma4:e4b`](https://ollama.com) 就裝好 Path A 環境。

### 練習 1：LLM API（hello world）
五行 Python 呼叫 LLM 並印出回應。**預設用 Ollama 本機跑（免費、offline）**；想看 cloud 答案品質改 Path B Anthropic。詳見 [`examples/README.md`](../examples/README.md#三條路徑--預設用-ollama成本考量)。

<details markdown="1" open>
<summary>📋 <b>起手碼 — Path A（本機 Ollama gemma4:e4b、預設）</b>（複製到 <code>practice_1.py</code>、<code>python practice_1.py</code> 就跑）</summary>

```python
# 需要：pip install openai      (用 OpenAI-compatible SDK 跟 Ollama 溝通)
# 前置：ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama 不檢查、隨便填
)

r = client.chat.completions.create(
    model="gemma4:e4b",   # 換成 qwen2.5:3b / llama3.2:3b 也可
    max_tokens=100,
    messages=[{"role": "user", "content": "用一句話自我介紹。"}],
)

# === 自我驗證 ===
text = r.choices[0].message.content
print("回應：", text)
print("usage:", r.usage)

assert r.choices[0].finish_reason in ("stop", "length"), f"非預期 finish_reason: {r.choices[0].finish_reason}"
assert len(text) > 0, "回應不應為空"
assert r.usage.completion_tokens > 0, "output token 應 > 0"
print("✅ 練習 1 通過 — Ollama gemma4:e4b 已能本機回應、$0/次")
```

**預期輸出**（樣本）：
```
回應：嗨！我是 Gemma、一個由 Google 訓練的開源語言模型...
usage: CompletionUsage(completion_tokens=35, prompt_tokens=12, total_tokens=47)
✅ 練習 1 通過 — Ollama gemma4:e4b 已能本機回應、$0/次
```

**慢嗎？** Gemma 4B 在 CPU 上約 5-30s/答案、有 GPU（RTX 3060+）<2s。要更快用 `gemma3:1b`、要更聰明改 `qwen2.5:14b` / `llama3.3:8b`（需 8GB+ VRAM）。

</details>

<details markdown="1">
<summary>📋 <b>起手碼 — Path B（Anthropic API、選擇性、想看 cloud 高品質時）</b>（複製到 <code>practice_1_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
# 環境變數：export ANTHROPIC_API_KEY=sk-ant-...
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()
msg = client.messages.create(
    model="claude-haiku-4-5",  # haiku 最便宜；換 sonnet 改這行
    max_tokens=100,
    messages=[{"role": "user", "content": "用一句話自我介紹。"}],
)

# === 自我驗證 ===
text = msg.content[0].text
print("回應：", text)
print("usage:", msg.usage)

assert msg.stop_reason in ("end_turn", "max_tokens"), f"非預期 stop_reason: {msg.stop_reason}"
assert len(text) > 0, "回應不應為空"
assert msg.usage.input_tokens > 0 and msg.usage.output_tokens > 0, "token 數應 > 0"
print("✅ 練習 1 通過 — 你已成功打通 Anthropic API")
```

**預期輸出**（樣本）：
```
回應：我是 Claude，一個由 Anthropic 訓練的 AI 助理...
usage: Usage(input_tokens=18, output_tokens=42, ...)
✅ 練習 1 通過 — 你已成功打通 Anthropic API
```

**成本**：每次 ~$0.001 (haiku) / $0.004 (sonnet)、跑這個 hello world 比 Ollama 快 5-15 倍。

</details>

### 練習 2：Tokens
同一個 prompt 跑 100 次，觀察 token 數的變化。

- 注意：`temperature ≠ 0` 會產生變動
- 注意：同一句話的英文 vs 中文 token 數差異

<details markdown="1" open>
<summary>📋 <b>起手碼 — Path A（本機 Ollama gemma4:e4b、預設）</b>（複製到 <code>practice_2.py</code>）</summary>

```python
# 需要：pip install openai     (OpenAI-compatible SDK 跟 Ollama 溝通)
# 前置：ollama pull gemma4:e4b && ollama serve
import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

PROMPTS = {
    "中文": "用一句話描述一隻貓在做什麼。",
    "English": "Describe in one sentence what a cat is doing.",
}

N = 10  # 本機慢、N 小一點；確認 OK 後加大
for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(N):
        r = client.chat.completions.create(
            model="gemma4:e4b",
            max_tokens=80,
            temperature=1.0,  # 拉高 temperature 看 variance
            messages=[{"role": "user", "content": prompt}],
        )
        output_tokens.append(r.usage.completion_tokens)
    print(f"\n[{label}] prompt: {prompt}")
    print(f"  input tokens: {r.usage.prompt_tokens}")
    print(f"  output tokens — min={min(output_tokens)} max={max(output_tokens)} mean={statistics.mean(output_tokens):.1f} stdev={statistics.stdev(output_tokens):.1f}")

# === 自我驗證 ===
assert max(output_tokens) > min(output_tokens), "temperature=1.0 下、output 長度應該有 variance"
print("\n✅ 練習 2 通過 — 觀察到 temperature 對 output token 的 variance、本機跑 $0")
print("💡 中文 prompt 通常 input tokens 比 English 多（中文 token 化通常一字 ≈ 2 tokens）")
```

**預期輸出**（樣本）：
```
[中文] prompt: 用一句話描述一隻貓在做什麼。
  input tokens: 32
  output tokens — min=18 max=58 mean=35.2 stdev=11.4

✅ 練習 2 通過 — 觀察到 temperature 對 output token 的 variance、本機跑 $0
```

</details>

<details markdown="1">
<summary>📋 <b>起手碼 — Path B（Anthropic API、選擇性）</b>（複製到 <code>practice_2_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
import sys, statistics
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

client = anthropic.Anthropic()
PROMPTS = {"中文": "用一句話描述一隻貓在做什麼。", "English": "Describe in one sentence what a cat is doing."}

for label, prompt in PROMPTS.items():
    output_tokens = []
    for _ in range(20):
        msg = client.messages.create(model="claude-haiku-4-5", max_tokens=80, temperature=1.0,
                                     messages=[{"role": "user", "content": prompt}])
        output_tokens.append(msg.usage.output_tokens)
    print(f"[{label}] input={msg.usage.input_tokens} output min/max/mean={min(output_tokens)}/{max(output_tokens)}/{sum(output_tokens)/len(output_tokens):.1f}")
```

**主要差異**：`client.messages.create()` → `client.chat.completions.create()`；`usage.output_tokens` → `usage.completion_tokens`；`usage.input_tokens` → `usage.prompt_tokens`。**成本**：40 次 ≈ $0.01。

</details>

### 練習 3：Pricing / Latency
**成本敏感的工作必修**：算出你的 hello-world prompt 在不同 model 上跑 1000 次的成本。Ollama 本機是 $0 但有 latency 成本；Cloud LLM 有 $ 成本但快。**會算這兩個 trade-off 才能挑對 model**。

<details markdown="1" open>
<summary>📋 <b>起手碼 — Path A（本機 Ollama gemma4:e4b、量 latency）</b>（複製到 <code>practice_3.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：ollama pull gemma4:e4b && ollama serve
import sys, time
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 量 5 次 latency
latencies = []
for _ in range(5):
    t0 = time.time()
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[{"role": "user", "content": "你好！自我介紹一下。"}],
    )
    latencies.append(time.time() - t0)

# 統計
avg_latency = sum(latencies) / len(latencies)
out_tok_avg = r.usage.completion_tokens  # 末次當代表
tps = out_tok_avg / avg_latency if avg_latency > 0 else 0

print(f"model: gemma4:e4b (本機)")
print(f"5 次 latency (sec): min={min(latencies):.2f} max={max(latencies):.2f} mean={avg_latency:.2f}")
print(f"avg output: {out_tok_avg} tokens、約 {tps:.1f} tokens/sec")
print(f"\n1000 次成本: $0 (本機)、預計時長: {avg_latency * 1000 / 60:.1f} 分鐘")

# === 自我驗證 ===
assert avg_latency > 0, "latency 應 > 0"
assert out_tok_avg > 0, "output token 應 > 0"
print(f"\n✅ 練習 3 通過 — 本機 model $0 但要花 {avg_latency * 1000 / 60:.0f} 分鐘跑 1000 次")
print("💡 對照 Path B Anthropic：1000 次只要 ~10-20 分鐘但要 $0.25（haiku）")
```

**預期輸出**（樣本）：
```
model: gemma4:e4b (本機)
5 次 latency (sec): min=4.21 max=8.93 mean=6.54
avg output: 48 tokens、約 7.3 tokens/sec

1000 次成本: $0 (本機)、預計時長: 109.0 分鐘

✅ 練習 3 通過 — 本機 model $0 但要花 109 分鐘跑 1000 次
💡 對照 Path B Anthropic：1000 次只要 ~10-20 分鐘但要 $0.25（haiku）
```

</details>

<details markdown="1">
<summary>📋 <b>起手碼 — Path B（Anthropic API、算 $ 成本）</b>（複製到 <code>practice_3_anthropic.py</code>）</summary>

```python
# 需要：pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic

# Anthropic 2026 Q2 公開計價（每 1M token、USD）— 跑前對照 https://www.anthropic.com/pricing
PRICING = {
    "claude-haiku-4-5":   {"input": 1.00, "output":  5.00},
    "claude-sonnet-5":    {"input": 3.00, "output": 15.00},  # 標準價；2026-08-31 前為優惠價 2.00 / 10.00
    "claude-opus-5":      {"input": 5.00, "output": 25.00},  # Opus 5 (2026-07-24、接替 Opus 4.8) — 維持 5/25 同價
    "claude-fable-5":     {"input": 10.00, "output": 50.00},  # Fable 5 (Mythos-class、最高層級) 約 Opus 的 2 倍
}

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"

msg = client.messages.create(model=MODEL, max_tokens=200,
                             messages=[{"role": "user", "content": "你好！自我介紹一下。"}])
in_tok, out_tok = msg.usage.input_tokens, msg.usage.output_tokens
rates = PRICING[MODEL]
cost_one = (in_tok * rates["input"] + out_tok * rates["output"]) / 1_000_000

print(f"model: {MODEL}")
print(f"single: input={in_tok} output={out_tok} → ${cost_one:.6f}")
print(f"1000 calls cost across model tiers:")
for name, r in PRICING.items():
    c = (in_tok * r["input"] + out_tok * r["output"]) / 1_000_000 * 1000
    print(f"  {name:<22} ${c:.4f}")

# === 自我驗證 ===
assert cost_one > 0, "Cloud LLM 一定有成本"
print(f"\n✅ 練習 3 通過（Anthropic）— 1000 次 haiku ≈ $0.25、sonnet 5 ≈ $0.76、opus 5 ≈ $1.27")
```

**預期輸出**：
```
model: claude-haiku-4-5
single: input=14 output=48 → $0.000254
1000 calls cost across model tiers:
  claude-haiku-4-5       $0.2540
  claude-sonnet-5        $0.7620
  claude-opus-5          $1.2700
  claude-fable-5         $2.5400
```

**Trade-off 對照**：本機 Ollama 跑 1000 次免費但要 ~2 hr；Anthropic haiku ~10 min $0.25；sonnet ~10 min $0.76。**production 場景才考慮 cloud；學習 / 實驗 / debug 全用本機**。

</details>

### 練習 4：Cross-Provider 比較
同一個 prompt 同時送給 Claude、GPT、Gemini，比較三家的回應差異。觀察「同一句話為什麼產生不同答案」——回答風格、長度、判斷取捨都不一樣。建議用 OpenAI、Anthropic、Google 三家 SDK 各一段程式呼叫。

→ **基礎 starter 範本** → [`examples/stage-1/04-cross-provider/`](../examples/stage-1/04-cross-provider/)（含三家 SDK 並行呼叫 + table 對照、缺哪家 key 就 skip 哪家；illustrative，**不是 chapter-length 完整教學**）

### 練習 5：Error Handling
故意觸發錯誤情境並寫 retry：

- API key 錯誤 → 看怎麼 raise
- prompt 超長 → context window 滿了會發生什麼
- 網路斷掉 → 寫一個有 exponential backoff 的 retry wrapper

這是後面 Stage 3-8 寫 production agent 一定會用到的基礎。

→ **基礎 starter 範本** → [`examples/stage-1/05-error-handling/`](../examples/stage-1/05-error-handling/)（含 mock-based test、不用真的斷網就能驗證 retry 邏輯；illustrative，**不是 chapter-length 完整教學**）

### 練習 6：Local LLM
**不付 API 費用、跑在自己電腦上**：用 Ollama 下載一個小模型（建議 `llama3.2:3b` 或 `qwen2.5:3b`），用 OpenAI-相容 API 呼叫它。

```bash
# 1. 裝 Ollama: https://ollama.com
ollama pull qwen2.5:3b
ollama serve  # 預設 port 11434
```

<details markdown="1">
<summary>📋 <b>起手碼</b>（複製到 <code>practice_6.py</code>）</summary>

```python
# 需要：pip install openai
# 前置：Ollama 已 serve、qwen2.5:3b 已 pull
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama 不檢查、隨便填
)

r = client.chat.completions.create(
    model="qwen2.5:3b",
    messages=[{"role": "user", "content": "用 3 句話介紹什麼是 ReAct。"}],
)

text = r.choices[0].message.content
print("回應：", text)

# === 自我驗證 ===
assert len(text) > 10, "回應太短、Ollama 可能沒跑起來"
print(f"✅ 練習 6 通過 — 你的本機 Ollama 已能透過 OpenAI-compatible API 呼叫")
print(f"💡 跑這次完全沒花錢（除了你的電力）")
```

**預期輸出**（樣本、實際內容因 model 而異）：
```
回應：ReAct 是一種讓 AI 結合「推理」和「行動」的方法...
✅ 練習 6 通過 — 你的本機 Ollama 已能透過 OpenAI-compatible API 呼叫
💡 跑這次完全沒花錢（除了你的電力）
```

**為什麼要做**：學會跑本地 LLM 後，後面 Stage 3-6 的實驗都不會被 API 費用卡住；隱私敏感場景也能 offline。

**沒裝 Ollama 也想跑**：把 `base_url` 換成 [LM Studio](https://lmstudio.ai) (`http://localhost:1234/v1`) 或 [vLLM](https://github.com/vllm-project/vllm) endpoint、API 介面一樣。

</details>

## 🎯 精選 Projects

按用途分 5 類、17 個項目一張表搞定。**挑入口看「適合誰」、想深入點連結看 repo / 課程網站**。

| 分類 | Project | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|---|
| **官方 cookbook / 入門** | [Anthropic Cookbook](https://github.com/anthropics/claude-cookbooks) | ⭐⭐⭐⭐⭐ | 開始用 Claude API、當參考書查 | Claude API 全功能 notebook（tool use / batch / prompt cache），★ 50k+、MIT |
| | [Anthropic Courses](https://github.com/anthropics/courses) | ⭐⭐⭐⭐⭐ | 系統性從零學一遍 Claude | Anthropic 自家完整 5 門課（API 基礎 / prompt eval / real-world prompting / tool use），★ 22k+。先跑 `anthropic_api_fundamentals` |
| | [OpenAI Cookbook](https://github.com/openai/openai-cookbook) | ⭐⭐⭐⭐⭐ | 用 OpenAI API + structured output / function calling | 跟 Anthropic Cookbook 對照、★ 73k+、MIT。比 Anthropic 大很多、用搜尋 |
| | [Anthropic Claude API Quickstart](https://docs.anthropic.com/en/docs/get-started) | ⭐⭐⭐⭐ | 5 分鐘上手 | 官方文件、加 bookmark 用 |
| **中文教材**<br>（章節式） | [datawhalechina/happy-llm](https://github.com/datawhalechina/happy-llm) | ⭐⭐⭐⭐⭐ | 中文讀者想徹底搞懂 LLM 原理 | 對應 Karpathy「Zero to Hero」中文版，★ 32k+。等同 HF LLM Course 中文版 |
| | [datawhalechina/llm-universe](https://github.com/datawhalechina/llm-universe) | ⭐⭐⭐⭐⭐ | 中文新手想用 LLM 做東西 | API 基礎 / 知識庫 / RAG / 進階技巧，★ 13k+ |
| | [datawhalechina/llm-cookbook](https://github.com/datawhalechina/llm-cookbook) | ⭐⭐⭐⭐ | 想要完整中文 LLM 學習路線 | Andrew Ng 課程中文翻譯改編（⚠️ 2025-06 後更新放緩、CC BY-NC-SA）|
| | [jingyaogong/minimind](https://github.com/jingyaogong/minimind) | ⭐⭐⭐⭐ | 看完 Karpathy 影片想實際跑訓練 | 2hr 從零訓 64M LLM、Pretrain + SFT + LoRA + DPO + RLHF 全包，★ 53k+、Apache-2.0 |
| **英文 course**<br>（系統式） | [HuggingFace — LLM Course](https://huggingface.co/learn/llm-course) | ⭐⭐⭐⭐⭐ | 想搞懂 transformer 內部 + HF 生態 | 含 transformer 原理 + 應用、Apache 2.0 |
| | [LangChain Academy](https://academy.langchain.com/) | ⭐⭐⭐⭐ | 喜歡影片教學的視覺型學習者 | LangChain 官方免費課、含 RAG / agent。**忽略 LangChain 行銷段落** |
| **本地端執行**<br>（不付 API 費）| [ollama/ollama](https://github.com/ollama/ollama) | ⭐⭐⭐⭐⭐ | 第一次跑本地 LLM | 本 repo Path A 預設、OpenAI-compat API、★ 170k+ |
| | [ggml-org/llama.cpp](https://github.com/ggml-org/llama.cpp) | ⭐⭐⭐⭐⭐ | 想搞懂 quantization / 為什麼 7B 能塞 8GB RAM | Ollama 底層 inference engine，★ 119k+、MIT |
| | [mudler/LocalAI](https://github.com/mudler/LocalAI) | ⭐⭐⭐⭐ | 團隊合規、要 self-host 全套 OpenAI 替代 | drop-in OpenAI API 替代品（chat / embedding / image / TTS / STT），★ 48k+ |
| | [ml-explore/mlx](https://github.com/ml-explore/mlx) | ⭐⭐⭐⭐ | Mac 開發、想榨乾 Apple Silicon | Apple 為 M1+ 量身打造的 ML framework，★ 27k+。搭 `mlx-lm` 用最方便 |
| **從零打造**<br>（理解原理）| [karpathy — Let's build GPT from scratch](https://www.youtube.com/watch?v=kCc8FmEb1nY) | ⭐⭐⭐⭐⭐ | 想搞懂 LLM 內部、不只會呼叫 | 2hr 高密度影片、用 PyTorch 從零打造 GPT。**暫停跟著寫 code 不要被動看** |
| | [rasbt/LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) | ⭐⭐⭐⭐⭐ | 想用整本書速度慢慢讀完 | Karpathy 影片的書本版：tokenizer → attention → pretraining → finetuning，★ 100k+、Apache-2.0 |
| | [karpathy/LLM101n](https://github.com/karpathy/LLM101n) | ⭐⭐ | 歷史紀錄 | ⚠️ 已封存（2024-08）、只有大綱、課程沒做完。**直接看上面的「Build GPT from scratch」影片即可** |

> 💡 **建議閱讀路徑**：API 入手就 Anthropic / OpenAI Cookbook → 中文系統路線就 happy-llm + llm-universe → 想深入內部就 Karpathy 影片 + rasbt 書搭 code → 想跑本地就 Ollama 起步、進階再讀 llama.cpp。

## ✅ 進 Stage 2 前的自我檢查

你能不能：

- [ ] 用 5 行 Python 呼叫 Claude API
- [ ] 解釋為什麼「你好」可能用 2 個 token，但「Hello」只用 1 個
- [ ] 大致說出 Claude Sonnet vs Opus 的 per-token 價格
- [ ] 各說出 Claude / GPT / Gemini / Llama 的一個強項

如果可以 → 進 [Stage 2 — Prompt Engineering](02-prompt-engineering.md)。

如果不行 → 重看 Anthropic Quickstart + 把上面 3 個 hello-X 都跑一次。

---

> ✅ **Stage 1 完成？** 接下來 [**Stage 2 — Prompt Engineering**](02-prompt-engineering.md) 會用 5-12 小時帶你寫出可重用的結構化 prompt、用 few-shot 跟 chain-of-thought 解推理題、並學會用 eval 量化 prompt 改善幅度。**繼續往下走 →**
