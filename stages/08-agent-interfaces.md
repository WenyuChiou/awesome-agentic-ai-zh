# Stage 8 — Agent 操作介面（Agent Interfaces）：Computer Use · Browser Use · Code Sandbox

> **繁體中文** | [简体中文](./08-agent-interfaces.zh-Hans.md) | [English](./08-agent-interfaces.en.md)

⏱ **時間估算**：2-3 週（約 12-20 小時）

> 💡 **本章用語密度高**（Computer Use、DOM、microVM、Firecracker、Sandbox、Cold start 等）。別擔心——這些都會在本章內就地解釋；不熟可以先讀 Stage 1 跟 Stage 7 的術語小辭典。

> 📋 **本章組成**：〔Agent Interfaces 是什麼（先定位）+ 三層 interface〕→ 學習目標 → 進入條件 → 必修閱讀 → 🖱 Computer Use（螢幕級）→ 🌐 Browser Use（web 級）→ 📦 Code Sandbox（隔離環境含**術語小辭典**）→ Track A 怎麼用 → Track B 怎麼 build → ⚠ 2026 Safety / Security → 動手練習 → 常用工具推薦 → 精選 Projects → 自我檢查 → 下一個 frontier（Voice / VLA forward note）

> 🔑 **關鍵名詞**：見本章內部解釋 + [`resources/glossary.md`](../resources/glossary.md)

**兩 track 共用 hub**——跟 Stage 5（Claude Code 生態）一樣、Track A（CLI Power User）+ Track B（Agent Builder）兩條路徑都會用到。Stage 5 + Stage 8 是 curriculum 兩個 hub。

## 🎯 Agent Interfaces 是什麼（先定位）

**Agent Interfaces 指的是 agent 如何操作 API 以外的真實環境，例如電腦畫面、網頁，或隔離的程式執行空間**——agent 與「非 API 世界」的對外互動層（IO boundary）。Stage 0-7 教你「**怎麼建 agent 本身**」（LLM → prompt → tool → context → memory → multi-agent → harness）；本 stage 教「**agent 蓋好後、怎麼操作真實環境**」。

**3 層 interface**：

| Interface | 操作對象 | 工作原理 | 代表工具 |
|---|---|---|---|
| **🖱 Computer Use**（screen-level）| 任何桌面 app（Excel / SAP / Photoshop / 沒 API 的軟體）| screenshot → vision → 算座標 → 模擬鍵鼠 | Anthropic Claude Computer Use / OpenAI Codex desktop / Gemini in Chrome |
| **🌐 Browser Use**（web-level）| 任何網頁 | DOM-aware navigation + 必要時 vision fallback | Comet / browser-use（OSS 108k stars）/ ChatGPT Agent Mode |
| **📦 Code Sandbox**（isolated exec）| agent 生成的 code 在隔離環境跑 | microVM / Container / user-space kernel（userland） | E2B / Daytona / Modal / Vercel Sandbox / OpenAI Agents SDK（April 2026 內建）|

### 跟前面 stage 的差別（避免概念混淆）

**Reader 第一個直覺問題**：這跟 Stage 3 Tool Use / Stage 5 MCP / Stage 7 Harness 有何不同？

| 比較對象 | 那邊管什麼 | 本 stage 管什麼 |
|---|---|---|
| **Stage 3 Tool Use** | agent **呼 API**（function calling、JSON schema）| agent **操作環境**（沒 API 的軟體 / 真實網頁 / 跑 code）|
| **Stage 5 MCP** | tool / data source 怎麼**標準化暴露**給 agent | agent 怎麼**實際 interact** 環境（MCP 是協定、Interface 是行為）|
| **Stage 7 Harness** | agent **runtime 控制流**（loop / retry / safety）| agent **IO 邊界**（runtime 內看不到的外界互動）|

→ **核心區分**：Tool 是 **API 呼叫**、Interface 是 **操作環境**——前者抽象 API、後者直接面對真實 GUI / web / OS。

### 為什麼 2024-2026 是 Agent Interface 的 breakthrough 年

**Why 現在才補這課**：

- **2024-10 之前**：agent 只能跟有 API 的世界互動（呼叫 OpenAI / GitHub / Slack API、回文字）
- **2024-10**：Anthropic Computer Use beta → **agent 第一次能操作真實螢幕**
- **2025-2026**：OpenAI（Atlas + Codex desktop）/ Google（Gemini in Chrome）全進場 → 主流化
- **2026-05**：OSWorld **v1** benchmark 達 **76.26%**（superhuman vs 72.36% human baseline）→ 從研究 curiosity 變 production reality（注意：v1 隨後接近飽和，2026-06 的 **OSWorld 2.0** long-horizon 版把 SOTA 重設到約 20%，見下方 benchmark 紀律段）

**沒這個 stage 的 curriculum gap**：學完 Stage 7 你以為 done、實際上 agent 只能跟 API 對話、**不能操作沒 API 的軟體 / 真實網頁 / 跑 code**——遇 safety issue（Comet 注入 / Amazon injunction、見[Safety](#-2026-safety--security-重點)）也沒警告過。

### 為什麼兩 track 共用

跟 Stage 5（Claude Code 生態）一樣、本 stage 是 **hub** 而非 track-specific：

- **Track A（CLI Power User）**：用 Claude Computer Use 委派桌面任務、用 Codex background mode、在 Claude Code 接 browser MCP
- **Track B（Agent Builder）**：embed browser-use 進自己 agent、用 E2B / Daytona 跑 agent-generated code、用 OpenAI Agents SDK 內建 sandbox

**兩個 track 都繞不開這 3 層 interface**——所以放 hub 位置。

## 📌 學習目標

學完本 stage 你能：

- 區分 3 層 agent interface（Computer Use / Browser Use / Sandbox）+ 跟 Tool / MCP / Harness 的關係
- 講出 Computer Use / Browser Use **mental model**（screenshot → vision → coords vs DOM-aware）
- 講出 microVM / Container / Firecracker / gVisor / Cold start 等隔離技術術語
- 知道怎麼讀 OSWorld / WebArena SOTA 數字（含 v1→2.0 飽和落差）+ 解讀 reward-hacking（agent 鑽 reward function 漏洞、拿高分但不是真的完成任務）警告
- **Track A**：在 daily CLI 工作流接 Computer Use + browser MCP + Codex background mode
- **Track B**：用 browser-use / E2B 在自己 agent 內 embed 環境互動 + sandbox 隔離
- 設計 4 個 safety pattern（approval gate / sandbox / human-in-loop / output filter）防注入攻擊

## 🚪 進入條件

你應該已經：

- 完成 [Stage 5](05-claude-code-ecosystem.md)（懂 MCP / Skills / Plugins、Claude Code 用過 daily）
- 完成 [Stage 7](07-multi-agent-production.md)（懂 harness engineering、knows what reward-hacking warning is about）
- 對 Docker / VM 概念基礎熟悉（本章會解釋 microVM / Container 差異、但完全沒接觸過 Docker 會卡）
- **若只 Track A**：Stage 5 完成就夠，Stage 7 可選；本章 Track A 部分不依賴 build 經驗
- **若 Track B**：Stage 7 必修，否則 9 build 範例會卡

沒到 → 回前面補。

## 📚 必修閱讀

1. [**Anthropic — Introducing Computer Use**](https://www.anthropic.com/news/3-5-models-and-computer-use) — Computer Use 原始 launch、reading 工作原理必看
2. [**Anthropic — Claude Release Notes（模型總覽）**](https://docs.anthropic.com/en/release-notes/overview) — Claude Opus 5（`claude-opus-5`，2026-07-24）是目前建議的預設模型，官方文件說複雜 agentic coding 與企業工作「從 Claude Opus 5 開始」。其上還有 Mythos-class 的 Claude Fable 5（`claude-fable-5`）——Anthropic 目前公開發布中能力最強的模型，留給需要最高能力的工作；Mythos 5（`claude-mythos-5`）規格相同但僅限邀請。Opus 4.8（2026-05，Dynamic Workflows + parallel subagent harness 隨它推出）仍可用，但官方文件已把它移到 Legacy models 區。
3. [**OpenAI — The next evolution of the Agents SDK**](https://openai.com/index/the-next-evolution-of-the-agents-sdk/) ⭐ **2026-04** — 把 workspace、session、approval 與 sandbox client 接進同一套 Agent API；Sandbox Agents 目前仍是 beta
4. [**OpenAI — Computer-Using Agent (CUA)**](https://openai.com/index/computer-using-agent/) — OpenAI 版 Computer Use + WebArena / OSWorld 數字
5. [**browser-use docs**](https://docs.browser-use.com/) — OSS web agent 第一名（108k+ stars）、5 行 Python 起步
6. [**Microsoft OmniParser**](https://microsoft.github.io/OmniParser/) — 開源 GUI parsing、Computer Use 重要 building block

> 💡 **挑著讀**：純 Track A 讀 1 + 2、純 Track B 必讀 3 + 5 + 6、想理解全局都讀。

## 🖱 Computer Use — 螢幕級 agent

### Mental model — 工作流跟 Why

**工作流**：
```
agent 收到任務
    ↓
1. 截圖（screenshot）→ 看到當前螢幕
    ↓
2. vision model 解析 → 識別按鈕 / 文字框 / icon
    ↓
3. 算出座標 → 「按鈕在 (453, 218)」
    ↓
4. 模擬鍵鼠 → click(453, 218) / type("hello")
    ↓
5. 再截圖 → 看結果、決定下一步
```

**Why 這個 paradigm（vs Tool Use）**：

- 大多軟體**沒 API、只有 GUI**——SAP / Excel / Photoshop / 任何傳統桌面 app、你要 agent 用就只能 screen-level
- API integration（Stage 3 Tool Use）要等廠商開介面、有時等不到
- Screen-level 是**最後一哩**——「agent 能做 human 在電腦上做的任何事」

**Why 2026 才行得通**：

- **Vision model 進步**：Claude 4.x / GPT-5.x 全 multimodal、看螢幕識別 element 準度大幅升
- **OS-level 訓練資料**：[OSWorld dataset (NeurIPS 2024)](https://github.com/xlang-ai/OSWorld) 釋出 369 個跨 OS 真實任務、讓 frontier lab 有資料訓
- **Anthropic Computer Use beta（2024-10）開啟商業競賽**——OpenAI / Google 跟上、benchmark 一路飆

### 2026 frontier 4 強對比

| Vendor | 產品 | 2026 狀態 | OSWorld | 強項 |
|---|---|---|---|---|
| **Anthropic** | [Opus 5 / Sonnet 5 Computer Use](https://www.anthropic.com/news/3-5-models-and-computer-use) | GA、跨 macOS / Linux / Windows（Docker）| **72.7%**（Opus 4.6 baseline、近 human 72.36%；Opus 4.7 / 4.8 / 5 後續的 Computer Use 專項數字均未公布）| reasoning + code agent、Stage 5/7 主場。Opus 5（2026-07-24）為 Opus 級旗艦；Mythos-class 的 Fable 5（2026-06-09）2026-06-12 暫停、2026-07-01 已恢復 |
| **OpenAI** | [Codex desktop](https://openai.com/index/codex-for-almost-everything/)（April 2026）| GA、**background mode** 不搶 cursor、in-app browser、90+ plugins | CUA 38.1% | 獨立桌面 coding agent、跨 app workflow；agentic 瀏覽已併入 ChatGPT 桌面 app（Atlas 2026-08 停運後併入）|
| **OpenAI** | [Computer-Using Agent (CUA)](https://openai.com/index/computer-using-agent/) | API | 38.1% / WebArena 58.1% | API-first、可整合自己 stack |
| **Google** | [Gemini in Chrome](https://gemini.google/overview/gemini-in-chrome/)（Gemini 3）| GA + Android | — | **Auto Browse** + **Chrome Skills**、Chrome Enterprise Premium $6/user/月 |
| **OpenAI Operator** | （**停運 2025-08**）| ❌ 不可用 | — | CAPTCHA / JS / session 處理不穩、被 Atlas 取代（Atlas 亦於 2026-08 停運）|

→ 詳細現況見 [Agentic Browser Landscape 2026](https://nohacks.co/blog/agentic-browser-landscape-2026)、[OSWorld leaderboard](https://os-world.github.io/)

### 為什麼 OSWorld 數字差這麼大（理解 benchmark 紀律）

**現況**：

| Model | OSWorld | 跟 human baseline 距離 |
|---|---|---|
| Human baseline | **72.36%** | — |
| Claude Opus 4.6（Anthropic）| **72.7%** | 持平 |
| OSWorld v1 2026-05 SOTA | **76.26%** | **superhuman**（v1，見下方）|
| OpenAI CUA | 38.1% | -34% |
| 多數一般 model | 30-50% | -22% ~ -42% |

> **⚠️ 2026-06 更新（OSWorld 2.0）**：上表是 OSWorld **v1** 的數字。v1 隨後被前沿模型逼近飽和，「superhuman」只在 v1 的短任務（多半 1-2 個 app）成立。[OSWorld 2.0](https://osworld-v2.xlang.ai/)（2026-06、arXiv 2606.29537）改用 108 個 long-horizon workflow（每個約 318 次 tool call，v1 只約 30），當時最強的 Claude Opus 4.8（max thinking）也只到 **20.6%**（500 步預算）、GPT-5.5 約 14%、137 分鐘以上的任務沒有任何模型破 10%。SOTA 從「76% superhuman」掉到「20% 真實長任務」，正是本段 benchmark 紀律要你警惕的落差。

**Why 比 SWE-bench 難**：

- **更開放任務**：SWE-bench 有清楚 test 判 pass / fail；OSWorld 任務 spec 模糊（"幫我把 csv 變成圖"）
- **跨多個 OS**：Ubuntu / Windows / macOS 都有
- **跨應用 chain**：常要打開 3-4 個 app（Excel → Chrome → Slack）

**Why 真實能力 ≠ 數字**（呼應 [Stage 7 reward-hacking 警告](07-multi-agent-production.md#-agent-benchmark-landscape怎麼看不要只看排行榜---reward-hacking-警告)）：

- OSWorld 也在 [UC Berkeley 2026-04 reward-hacking 報告](https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/) 名單上、被證可 hack 到 100%
- **看數字紀律**：別只看 leaderboard top、看你自己 use case 的 hold-out test 才是 ground truth

### 平台支援現況（2026-05）

| OS | Anthropic | OpenAI | Google |
|---|---|---|---|
| **macOS** | ✅ GA | ✅ Codex desktop GA（Atlas 已停運）| Chrome 內 |
| **Linux** | ✅ Docker | ⚠ 較緊 | Chrome 內 |
| **Windows** | ✅ Docker | 🔜 native preview（Atlas 未出 Windows 版）| Chrome 內 |
| **Mobile** | — | — | ✅ Gemini in Chrome on Android |

## 🌐 Browser Use — web 級 agent

### Mental model — DOM-aware vs screen-pixel + Why

**核心區分**：

| 路線 | 怎麼工作 | 何時用 |
|---|---|---|
| **DOM-aware**（瀏覽器內、有 DOM）| 直接 query `<button id="submit">`、`document.querySelector('.cart-item')` | 一般 web app、structured page |
| **Screen-pixel + vision**（沒 DOM、看截圖）| 跟 Computer Use 一樣、screenshot → vision → coords | iframe / Canvas / Shadow DOM / 防自動化 |

**Why DOM-aware 比 screenshot 精準**：

- 直接抓 `<input name="username">` element、**不用 vision 解析像素**
- 速度快 10-100×（不跑 vision model）
- 不會 misclick（element 有確切 bounding box）
- **缺點**：JS 動態渲染 / Shadow DOM / Canvas / iframe 之內 DOM 不暴露時失效

**結論 — production browser agent pattern**：**DOM-first + screenshot fallback**——先嘗試 DOM、抓不到再用 vision。browser-use / Atlas / Comet 都用這 pattern。

> 🌐 **瀏覽器 agent 的第三種模態：accessibility tree**：除了 DOM-aware 跟 screen-pixel（看截圖點座標），2026 production 主流是讀 **accessibility tree**——比 pixel 穩、比原始 DOM 省 token。要實際接，[microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)（★ 35k+、Apache-2.0、走 accessibility tree）是 Track A 直接掛 Claude Code 就能用的瀏覽器 MCP。

### Mini-glossary（就地解釋）

| 術語 | 解釋 |
|---|---|
| **DOM**（Document Object Model）| 瀏覽器內部把 HTML 解析成的樹狀結構、可程式化 query |
| **CSS selector** | 選 element 的語法（`#submit-btn`、`.cart > li:nth-child(2)`）|
| **Shadow DOM** | Web Component 的內部 DOM、外部 DOM query 不到（如 Salesforce / Reddit 新版）|
| **iframe** | 嵌入另一個網頁、跨 origin 的 DOM 通常隔離 |
| **Canvas** | `<canvas>` 元素內的圖形、純像素、DOM 看不到內容（如 Figma / Google Sheets）|

### 閉源 AI Browser 5 強對比（2026-05）

| Browser | 來源 | 平台 | Agent Mode | 風險 / 注意 |
|---|---|---|---|---|
| **Atlas** ⚠️ | OpenAI（2025-10，**停運 2026-08**）| 僅 macOS（未出 Windows）| 功能併入 ChatGPT app | — |
| **Comet** | Perplexity | iOS / Android / Win / Mac | ✅ research 最強 | ⚠ 2026 Brave 發現可被惡意網頁注入；2026-03 federal injunction 禁存取 Amazon |
| **Dia** | [Browser Company（被 Atlassian $610M 收購）](https://efficient.app/compare/dia-vs-comet) | macOS | ❌（**不走 agent mode**、聚焦效能）| — |
| **Gemini in Chrome** | Google（Gemini 3）| Chrome 全平台 + Android | ✅ **Auto Browse** + **Chrome Skills** | Enterprise Premium $6/user/月 |
| **Operator** | OpenAI | — | ❌ **停運 2025-08** | CAPTCHA / JS / session 處理不穩 |

→ 完整比較：[AI Browser Comparison（2027 更新版）](https://www.webfx.com/blog/ai/best-ai-browsers/)

### 開源 Browser Use 框架

| 框架 | 狀態 | 強項 |
|---|---|---|
| [**browser-use**](https://github.com/browser-use/browser-use) ⭐ | **108k+ stars、MIT** | 2026 最火 OSS、Python、5 行起步、支援 OpenAI / Claude / Gemini / Ollama |
| [**Microsoft OmniParser v2**](https://github.com/microsoft/OmniParser) | 2026 更新、Apache 2.0 | vision-based GUI parsing、60% latency 改善、ScreenSpot Pro 39.6% accuracy。同 repo 內含 **OmniTool**（Windows 11 VM 控制、可搭 GPT-5.5 / Claude Opus 5 / DeepSeek-V4-Pro / Qwen 2.5VL / Claude Computer Use）|
| **Playwright + LLM**（DIY）| — | 不是專門 framework、但 Playwright 是 web automation 標準、加 LLM wrapper 就能用 |

**Why browser-use 108k stars 這麼火**：

- DOM-first paradigm **比 screenshot+vision 對 web 精準** + 速度快
- LLM-vendor agnostic（不綁 Claude / GPT）
- 5 行 Python 起步、entry barrier 低

### 跟 web scraping / RPA 的差別

| 工具類 | 怎麼工作 | 適合 |
|---|---|---|
| **Web scraping**（BeautifulSoup / Scrapy）| 固定 selector、純 pull data | 結構穩定的網站、只要資料 |
| **RPA**（UiPath / Power Automate）| 固定 click / type script、不 reasoning | 流程已知 + 不變的企業內部任務 |
| **Browser Agent**（本 stage）| **可 reason + 動態決定怎麼操作** | 任務描述模糊、流程可能變、需要 agent 自己探索 |

## 📦 Code Execution Sandbox — 隔離環境（含術語小辭典）

### 為什麼 agent 一定要 sandbox

**Threat model**：agent 寫 code → 在哪跑？

- ❌ **Host 機器（最壞）**：agent 可能 `rm -rf /` / 連 internet 泄資料 / 讀 `.ssh/id_rsa` / 安裝 malware
- ⚠ **同 user 隔離 process（中等）**：能擋部分但 file system / network 仍開
- ✅ **隔離 sandbox（必要）**：獨立 filesystem / process / network、出事可丟掉

**為什麼 2026 才正式變 production 要求**：

- **2026-04 OpenAI Agents SDK 更新**：[內建支援 7 個 sandbox provider](https://openai.com/index/the-next-evolution-of-the-agents-sdk/)（Blaxel / Cloudflare / Daytona / E2B / Modal / Runloop / Vercel）
- 之前都靠 [Claude Code](05-claude-code-ecosystem.md) / [Cursor](https://www.cursor.com) 的 approval gate 擋——但 production agent **無人盯、必須 sandbox**

### 🔑 隔離技術術語小辭典

新 reader 卡關常見、就地解釋：

| 術語 | 一句解釋 | 隔離強度 | 啟動速度 | 典型用途 |
|---|---|---|---|---|
| **Container**（Docker / OCI）| Linux kernel namespace + cgroups、**多 container 共用 host kernel** | 弱（kernel exploit 跨界）| 快（< 1s）| 一般 web app、低風險 task |
| **VM**（Virtual Machine）| Hypervisor 配虛擬硬體、**獨立 kernel** | 最強 | 慢（秒級）| 高風險 / enterprise |
| **microVM** | VM 的精簡版、極小 footprint、仍獨立 kernel | **強** | **快（< 100ms）** | agent sandbox 甜蜜點 |
| **Firecracker** | AWS 開源 microVM、Rust 寫、**AWS Lambda 底層**、E2B 用它做 isolation | 強 | 快 | serverless / agent |
| **gVisor** | Google 寫的「user-space kernel（userland）」、攔截 syscall 自己模擬、不用 hypervisor | 中強 | 中快 | 介於 container / VM |
| **Cold start** | sandbox 從零啟動到可用的時間（Daytona 最快 27ms、E2B microVM 較慢）| — | — | latency-critical 場景關鍵 |
| **Persistence** | state 跨呼叫保留嗎（檔案 / process / network） | — | — | long-running agent 必要 |
| **GPU passthrough** | VM / microVM 訪問 host GPU 的技術（**Modal 唯一支援**）| — | — | sandbox 內跑 inference / fine-tune |

**核心要記**：

- **Container** = 快 + 隔離弱（共用 kernel）
- **VM** = 慢 + 隔離強（獨立 kernel）
- **microVM** = 兼顧（快 < 100ms + 獨立 kernel）→ **agent sandbox 多半選 microVM**

### 7 個 sandbox 對比（2026-05）

| Sandbox | 隔離技術 | 冷啟 | 強項 | 何時用 |
|---|---|---|---|---|
| [**Daytona**](https://www.daytona.io/) | Container | **< 90ms（最快 27ms）** | 啟動快、Docker 生態整合 | latency-critical |
| [**E2B**](https://github.com/e2b-dev/E2B) | **Firecracker microVM** | ~ 200ms | Python REPL iterative、最多 community template | agent 跑 Python loop |
| [**Modal**](https://modal.com/) | microVM + GPU | ~ 1s | **唯一 GPU sandbox** | sandbox 內 inference / fine-tune |
| [**Vercel Sandbox**](https://vercel.com/docs/sandbox) | Container | < 500ms | Vercel ecosystem 整合 | web stack |
| [**Cloudflare**](https://developers.cloudflare.com/workers-ai/) | Workers / Containers | < 100ms | edge global 部署 | low-latency 全球 |
| **Runloop** | — | — | 2026 OpenAI SDK 新支援 | （新進場）|
| **Blaxel** | — | — | 同上 | （新進場）|

→ 詳細 benchmark：[AI Code Sandbox Benchmark 2026 — Modal vs E2B vs Daytona](https://www.superagent.sh/blog/ai-code-sandbox-benchmark-2026)

### OpenAI Agents SDK April 2026 更新 — Why 是 milestone

**這次更新為什麼重要**：

- **之前**：團隊通常要自己把 workspace、session、approval、sandbox provider 與 agent loop 接在一起。
- **2026-04 之後**：Agents SDK 提供共用 harness／sandbox 介面與 Codex filesystem tools；Sandbox Agents 仍是 beta，不代表 production 隔離、審批與測試已自動完成。

**3 個關鍵新功能**：

1. **Native harness** — agent loop / model calls / tool routing / handoffs / approvals / tracing / recovery 全在 SDK 層
2. **Native sandbox execution** — bring your own sandbox 或用內建 7 個 provider（Blaxel / Cloudflare / Daytona / E2B / Modal / Runloop / Vercel）
3. **Codex filesystem tools** — agent 寫檔 / 讀檔 / 跑 command 都有 SDK-level API

→ Python first、TypeScript 之後。**Anthropic Claude Agent SDK 早就有類似抽象**——OpenAI 終於追上。

## 🧭 Track A 怎麼用（CLI Power User 視角）

**Reader pain**：Track A 想「**我怎麼用** Claude Computer Use 把桌面任務委派出去」、不是「怎麼 build」。

### 1. 在 Claude Code 內接 Computer Use / Browser MCP

**Why MCP 路線**：你已熟 Claude Code（[Stage 5](05-claude-code-ecosystem.md)），新功能能透過 MCP 接、不用換工具。

- **Computer-use MCP**（社群實作多版本）：在 `.mcp.json` 加 server 後、Claude Code 內就能叫「截圖 → 看 → 操作」
- **Browser MCP**：[microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) 等、Claude Code 可開瀏覽器跑 web 任務

### 2. 用 Codex desktop 在 background 跑

**Why background mode**：[OpenAI Codex desktop (April 2026)](https://openai.com/index/codex-for-almost-everything/) 預設不搶 cursor、agent 在後台跑、你繼續做別的事——**多個 agent workflow 可平行**。

- 適合：「分析 Q3 財報、整理成 slide、發 Slack」這種**長時間 + 不需要盯著看**的任務
- 跟 Claude Code 互補：Claude Code 做 code 任務、Codex desktop 做跨 app workflow

### 3. 用 Comet / Gemini in Chrome / ChatGPT Agent Mode 跑 web 任務

| 場景 | 推薦 | 理由 |
|---|---|---|
| 研究 / 跨頁面 synthesis | **Comet** | research-tuned、citation-backed |
| ChatGPT user / Agent Mode | **ChatGPT 桌面 app**（Agent Mode）| Plus/Pro/Business 內建（Atlas 2026-08 停運後併入）|
| Chrome / Google ecosystem | **Gemini in Chrome** | Auto Browse + Skills、enterprise DLP |
| **避開**：Comet 跑 e-commerce / banking | — | ⚠ 2026-03 federal injunction（詳見[Safety](#-2026-safety--security-重點)）|

### 跨 app workflow 範例

「**幫我把 Q3 csv 變成圖、存到 Slack #finance**」：

1. Claude Code（接 Computer-use MCP）打開 Excel
2. 載入 csv、用 chart wizard 生成圖表
3. 截圖
4. 切到 Slack、貼到 `#finance` channel
5. agent 回報完成

**為什麼這個範例值得做**：跨 3 個 app（Excel / 截圖工具 / Slack）、沒有 API 解法（Slack 有 API 但 Excel chart 沒有可程式化路徑）。

## 🧭 Track B 怎麼 build（Agent Builder 視角）

**Reader pain**：Track B 想看具體 build code、不是「怎麼用」。

### 1. 用 browser-use 寫 web agent

**Why browser-use**：108k stars、5 行起步、LLM-vendor agnostic、production-ready。

```python
from browser_use import Agent
from langchain_openai import ChatOpenAI

agent = Agent(
    task="Search Hacker News for top AI agent posts this week and summarize",
    llm=ChatOpenAI(model="gpt-5.5"), # 也可換 Claude Opus 5 / Gemini 3.5 Flash / DeepSeek-V4-Pro
)
result = await agent.run()
```

→ 內部：browser-use 開 Playwright browser、agent DOM-first navigation、有 fallback vision。

### 2. 用 E2B 跑 agent-generated code

**Why E2B**：[Firecracker microVM](#-隔離技術術語小辭典) isolation + Python REPL iterative + 最多 template。

```python
from e2b_code_interpreter import Sandbox

with Sandbox() as sandbox:
    # agent 寫的 code 在這跑、出事 sandbox 丟掉即可
    execution = sandbox.run_code(agent_generated_python)
    print(execution.text)
```

### 3. 用 OpenAI Agents SDK 內建 sandbox（2026-04 新）

**Why 這 SDK**：它把 workspace、session、approval 與 sandbox client 接進同一套 Agent API；這條 Sandbox Agents 路線仍是 beta，production 仍要自己驗證隔離、權限、審批與失敗復原。

```python
from openai.agents import Agent, Sandbox

agent = Agent(
    model="gpt-5.5",
    sandbox=Sandbox(provider="e2b"), # 或 daytona / modal / vercel / ...
    tools=[...]
)
```

→ 7 個內建 provider 可選、bring your own sandbox 也行。

### 4. GUI agent 訓練資料

如果你想**訓自己的 Computer Use model**（少數人會做）：

- [**OSWorld dataset**](https://github.com/xlang-ai/OSWorld) — 369 個跨 OS 任務、screenshot + ground truth action
- [**WebArena**](https://github.com/web-arena-x/webarena) — web navigation benchmark
- [**Mind2Web**](https://github.com/OSU-NLP-Group/Mind2Web) — real-world web tasks

→ 多數人用 frontier model（Claude / GPT）就好、不必訓。**這條線是 research**。

## ⚠ 2026 Safety / Security 重點

**Reader pain**：2026 已出真實事故、curriculum 沒警告 = 學完去 build 出事。

### 案例 1 — Comet 被 Brave 發現可被網頁注入

**攻擊原理**（[Brave Research 2026](https://brave.com/blog/comet-prompt-injection)）：

- Comet agent 看網頁 → 網頁裡藏惡意 prompt（如 HTML 註解內）
- LLM 解析網頁時把惡意 prompt 當指令執行
- 結果：agent 被 hijack 操作 user Gmail / 銀行 / 帳號

**Why 這是新攻擊面**：

- 傳統 SQL injection 攻擊路徑：**user input → server**（在 server-side 過濾就擋）
- Prompt injection through web content：**web content → LLM context**（在 LLM context 內難分指令 vs 內容）
- **Defense 完全不同**——無法套 SQL injection 那套

### 案例 2 — Federal injunction（2026-03 Comet 禁存取 Amazon）

2026-03 美國聯邦法官對 Comet 下 preliminary injunction、**禁止 agent 存取 Amazon 帳號**——理由是 Comet 在 Amazon 帳號操作不穩、且涉及未授權商業活動。

**Why 這是 legal risk signal**：

- Agent 操作他人帳號可能違反該平台 ToS
- 大型 e-commerce / banking 平台可能用 legal action 擋 agent
- production agent 部署前**必查目標平台 ToS**

### 4 個防護 pattern（必加）

![Agent 4 個防護 pattern](../resources/diagrams/agent-guardrail-patterns.png)

| Pattern | 怎麼做 | 何時必加 |
|---|---|---|
| **① Approval gate** | 高風險操作（刪檔 / 付錢 / 發 email / DB delete）前彈窗 user 確認 | **所有 production agent** |
| **② Sandbox** | agent 跑 code 必裝（見 7 七選一）| 任何會跑 code 的 agent |
| **③ Human-in-loop** | long-horizon task 中段 checkpoint | task > 10 steps 或 > 5 分鐘 |
| **④ Output filter** | destination 限定白名單（only post to internal Slack、only write to /tmp）| 跨 system 操作的 agent |

→ **呼應 [Stage 7 reward-hacking 警告](07-multi-agent-production.md#-agent-benchmark-landscape怎麼看不要只看排行榜---reward-hacking-警告)**：curriculum 一致教「**別 blindly 信 agent**」紀律——Stage 7 講 eval 紀律、Stage 8 講 runtime 紀律。

## 🛠 動手練習（兩 track 各有）

### 練習 1（Track A）：跨 app workflow 用 Computer Use
用 Claude Computer Use 完成：「打開 Excel 載入 `data.csv`、生成 bar chart、截圖、貼到 Slack `#test` channel」。**目標**：體會 agent **沒有 API 也能做事**。

### 練習 2（Track B）：browser-use 寫 web agent
用 browser-use（10 行內 Python）寫一個 agent、自動到 Hacker News 抓本週 top 5 AI 文章 + 摘要。**目標**：體會 DOM-first paradigm。

### 練習 3（兩 track）：E2B 跑 agent code
用 E2B sandbox、讓 agent 生成 Python 算數據圖、在 sandbox 內跑、回傳結果。**目標**：體會 microVM isolation 跟直接在 host 跑的差別。

### 練習 4（進階）：OpenAI Agents SDK + sandbox + Computer Use
用 OpenAI Agents SDK（2026-04 版）整合：sandbox 跑 code + Computer Use 操作 GUI、做一個小型 RPA-replacement workflow。**目標**：體會上線運行的 harness + sandbox 整合。

## 🎯 常用工具推薦（按用途分類）

| 場景 | 推薦工具 | 為什麼 |
|---|---|---|
| **第一次接觸 Computer Use** | Anthropic [Claude Computer Use Docker quickstart](https://github.com/anthropics/anthropic-quickstarts) | 官方 Docker、5 分鐘起步 |
| **桌面 background workflow** | [OpenAI Codex desktop](https://openai.com/index/codex-for-almost-everything/)（April 2026）| 不搶 cursor、可平行 |
| **第一個 web agent**（OSS） | [browser-use](https://github.com/browser-use/browser-use) ⭐ | 108k+ stars、5 行 Python、LLM-vendor agnostic |
| **GUI parsing 研究**（OSS）| [Microsoft OmniParser v2](https://github.com/microsoft/OmniParser) | vision-based、60% latency 改善 |
| **AI Browser 主力**（消費 / research）| [Comet](https://comet.perplexity.ai/)（research）/ ChatGPT Agent Mode（ChatGPT user；Atlas 2026-08 停運）| 各家 agent mode 強項不同 |
| **企業 / Chrome ecosystem** | [Gemini in Chrome](https://gemini.google/overview/gemini-in-chrome/) | Auto Browse + Skills + DLP |
| **第一個 sandbox**（agent Python）| [E2B](https://github.com/e2b-dev/E2B) | Firecracker microVM、Python REPL 友善 |
| **Latency-critical sandbox** | [Daytona](https://www.daytona.io/) | < 90ms cold start |
| **Sandbox + GPU**（inference / fine-tune）| [Modal](https://modal.com/) | 唯一 GPU sandbox |
| **Production agent SDK 起點**（2026-04 後）| [OpenAI Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/) | 內建 harness + 7 個 sandbox provider |
| **Claude agent 原生路線** | [claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | Stage 7 已介紹、Anthropic 早於 OpenAI 抽象出 harness |

**建議入手順序**：

1. **Track A 入門**：用 Claude Computer Use Docker quickstart 跑通第一個跨 app 任務（30 分鐘）
2. **Track B 入門**：用 browser-use 寫 web agent（10 分鐘）
3. 加 sandbox 隔離：接 E2B 或 Daytona
4. Production：用 OpenAI Agents SDK 或 Claude Agent SDK 整合 sandbox + Computer Use
5. 進階 / research：訓 GUI agent → OSWorld / WebArena dataset

## 🎯 精選 Projects（範本 / SDK / 工具 collection）

按用途分類、17 個項目一張表搞定。

| 分類 | Project | ⭐ | 適合誰 | 為什麼推薦 / 備註 |
|---|---|---|---|---|
| **Computer Use SDK** | [anthropics/anthropic-quickstarts](https://github.com/anthropics/anthropic-quickstarts) | ⭐⭐⭐⭐⭐ | 第一次接觸 Computer Use | 含 Docker quickstart、5 分鐘起步 |
| | [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | ⭐⭐⭐⭐⭐ | 用 OpenAI 寫 production agent | 2026-04 內建 harness + 7 sandbox provider |
| | [anthropics/claude-agent-sdk-python](https://github.com/anthropics/claude-agent-sdk-python) | ⭐⭐⭐⭐⭐ | 用 Claude 寫 production agent | Anthropic 早於 OpenAI 的 agent SDK、跟 Claude Code 同 runtime |
| **Browser Use OSS** | [browser-use/browser-use](https://github.com/browser-use/browser-use) ⭐ | ⭐⭐⭐⭐⭐ | OSS web agent 第一名 | 108k+ stars、MIT、LLM-vendor agnostic |
| | [microsoft/OmniParser](https://github.com/microsoft/OmniParser) | ⭐⭐⭐⭐ | vision-based GUI parsing | v2 60% latency 改善、Apache 2.0、含 OmniTool（Windows VM control）|
| **Computer Use Agent Stack** | [bytedance/UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) | ⭐⭐⭐⭐ | 在桌面跑開源 computer-use agent | ByteDance 開源的「computer use」agent、會看螢幕、操作你的桌面，38k+ stars、Apache-2.0 |
| | [trycua/cua](https://github.com/trycua/cua) | ⭐⭐⭐⭐ | 打造 / sandbox computer-use agent | 打造「computer use」agent 的開源工具箱：安全 sandbox、SDK、測試，跨 macOS / Linux / Windows，21k+ stars、MIT |
| **AI Browser**（閉源 / 消費）| [Atlas](https://openai.com/index/introducing-chatgpt-atlas/)（⚠️ 停運 2026-08）| ⭐⭐⭐ | ChatGPT user + Agent Mode | OpenAI 出品、功能已併入 ChatGPT 桌面 app |
| | [Comet](https://comet.perplexity.ai/) | ⭐⭐⭐⭐ | research 用 agent browser | Perplexity 出品、全平台、citation-backed。⚠ Brave 注入 + Amazon injunction |
| | [Dia](https://www.diabrowser.com/) | ⭐⭐⭐ | 想要 AI browser 但**不要** agent mode | Browser Company 出品（被 Atlassian $610M 收購）、聚焦效能 |
| **Sandbox**（microVM）| [e2b-dev/E2B](https://github.com/e2b-dev/E2B) | ⭐⭐⭐⭐⭐ | agent 跑 Python loop | Firecracker microVM、最多 template、Apache 2.0 |
| **Sandbox**（container 快）| [Daytona](https://www.daytona.io/) | ⭐⭐⭐⭐ | latency-critical | < 90ms cold start、Docker 生態 |
| **Sandbox**（GPU）| [Modal](https://modal.com/) | ⭐⭐⭐⭐ | sandbox 內跑 inference / fine-tune | 唯一 GPU sandbox、serverless |
| **Benchmark dataset** | [xlang-ai/OSWorld](https://github.com/xlang-ai/OSWorld) | ⭐⭐⭐⭐⭐ | 想訓 / 評估 Computer Use agent | NeurIPS 2024、369 個跨 OS 任務；後繼 [OSWorld 2.0](https://osworld-v2.xlang.ai/)（2026-06、108 個 long-horizon workflow）SOTA 僅約 20% |
| | [web-arena-x/webarena](https://github.com/web-arena-x/webarena) | ⭐⭐⭐⭐ | 評估 web agent | self-hosted 真實網站、OpenAI CUA 58.1% |
| | [OSU-NLP-Group/Mind2Web](https://github.com/OSU-NLP-Group/Mind2Web) | ⭐⭐⭐⭐ | real-world web tasks dataset | 137 個網站 / 2350 個任務 |
| **Visual web agent** | [illuin-tech/colpali](https://github.com/illuin-tech/colpali) | ⭐⭐⭐⭐ | vision RAG for PDF / 文件 | 直接 embed page image、繞 OCR、2024 NeurIPS |

> 💡 **建議入手路徑**：Track A → Anthropic quickstart + Comet；Track B → browser-use + E2B → OpenAI Agents SDK / Claude Agent SDK 整合。

## ✅ Stage 8 之後的自我檢查

你能不能：

- [ ] 解釋 Computer Use / Browser Use / Sandbox 三層 interface 各解決什麼問題
- [ ] 解釋 microVM / Container / Firecracker / gVisor 4 個術語、知道為什麼 agent sandbox 多半選 microVM
- [ ] 用 Claude Computer Use 或 OpenAI Codex desktop 跑完一個跨 app 任務（練習 1）
- [ ] 用 browser-use 5 行 Python 寫個 web agent（練習 2）
- [ ] 用 E2B 跑 agent-generated code、體會跟 host 直接跑的差別（練習 3）
- [ ] 講出 prompt injection through web content 為什麼是新攻擊面、4 個防護 pattern 各擋什麼
- [ ] 講出 OSWorld v1 76.26% → 2.0 約 20% 的落差背後的 reward-hacking / 飽和紀律（為什麼不能 blindly 信 SOTA 數字）

如果都可以 → 你已經跑完 curriculum 主幹。挑一個[特化分支](../README.md#-學習地圖兩條學習路徑)、或往下看 下一個 frontier。

## 💡 下一個 frontier — Voice agents · VLA 機器人

本 stage 涵蓋 **desktop / browser / sandbox** 三層 interface——這是 2024-2026 主場。但 agent 跟世界互動還有兩條軸線、curriculum 之後會處理：

### Voice agents（語音介面）

- [**Vapi**](https://vapi.ai/) / [**Retell**](https://www.retellai.com/) — 商業 voice agent platform
- [**LiveKit Agents**](https://github.com/livekit/agents) — OSS、★ 12k+
- [**OpenAI Realtime API**](https://platform.openai.com/docs/guides/realtime) — speech-to-speech 直接做 agent

### VLA（Vision-Language-Action）機器人

- [**RT-2**](https://robotics-transformer2.github.io/)（Google DeepMind）— 大型 robotic transformer
- [**OpenVLA**](https://openvla.github.io/) — OSS、Stanford
- [**π0**](https://www.physicalintelligence.company/blog/pi0)（Physical Intelligence）— foundation model for robotics
- **Helix**（Figure AI 2025）— humanoid VLA

**Why 不在本 stage 展開**：voice / VLA 是**另一條 modality 軸線**（聽 / 物理動作）、跟 desktop / browser / sandbox 屬性不同；展開會稀釋本 stage 主軸、放 Stage 9 處理。

---

## 接下來

你已經跑完主幹。下一步：

1. **挑一個 specialist branch**（[for-researcher](../branches/for-researcher.md) / [for-developer](../branches/for-developer.md) / [for-teacher](../branches/for-teacher.md) / [for-knowledge-workers](../branches/for-knowledge-worker.md) / [for-everyday-users](../branches/for-everyday-users.md)）
2. **回饋上游**——browser-use / OmniParser / OSWorld 都歡迎 PR
3. **追 2026 後續發展**——Voice / VLA 是下一波、follow Stage 9（待規劃）
