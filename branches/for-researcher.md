# 研究者延伸路線（For Researchers）

> **繁體中文** | [简体中文](./for-researcher.zh-Hans.md) | [English](./for-researcher.en.md)

> 🚀 **計算型研究者**（會跑 Python script、有 API key、會用 git）可直接進階；**非程式背景研究者**（人文社科、臨床研究、文獻為主）可先從文獻 Q&A（NotebookLM）、Zotero AI 工具開始、需要時再看 [`resources/setup-guide.md` A-C](../resources/setup-guide.md)。

> [← 回主路線 README](../README.md) · 走完 **Track A 的 A3** 或 **Track B 的 Stage 7** 後從這裡接續。把 agentic AI 應用到研究流程上。

## 使用情境（研究階段 × AI 怎麼幫）

研究者一天分成幾個階段、AI 在每個階段的角色不同。下表幫你定位：

| 階段 | 你常遇到的痛點 | AI 能幫的部分 | 推薦工具（從輕到重） |
|---|---|---|---|
| **文獻探索** | 不知道某個領域有哪些經典 paper | 推薦 + 摘要 + 比較 | NotebookLM → paper-qa → gpt-researcher |
| **文獻精讀** | PDF 翻一半就忘 / 抓不到 claim | 抓 claim、figure、citation、做筆記 | Zotero + zotero-gpt → zotero-skills |
| **研究設計** | RQ 模糊、不知選哪個 method | 對話釐清、列出 trade-off | Claude.ai 對話 → ai-research-skills |
| **實驗 / 寫程式** | 重複 boilerplate、寫 plot 浪費時間 | 寫 / 改 code、batch refactor | Claude Code → codex-delegate |
| **論文撰寫** | 草稿卡關、句子不通 | 大綱 → 段落 → 潤色 | Claude.ai → Gemini CLI（長稿） |
| **改稿 / 投稿** | 期刊規範一堆、容易漏 | banned-word / figure-text / submission checklist | academic-writing-skills |
| **跨 paper synthesis** | 5 篇 paper 互相對話、context 爆 | 1M token 一次讀完 + 整理 | Gemini CLI |

> 💡 **計算型 vs 非程式背景**：表中「推薦工具」由輕到重——非程式背景研究者先停在每行**第一個**就夠了；計算型研究者要自動化才往後挑。

## 精選 Projects

> 💡 **想把 Claude Code 接到 NotebookLM、Obsidian、Notion、Excel、PDF、Excalidraw 等研究常用工具？** 81+ 個整合在 [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)（按使用情境分類）。下面這節保留「研究專屬」的工具與 marketplace。

### 研究流程 Marketplace

#### [flonat/claude-research](https://github.com/flonat/claude-research) ⭐⭐⭐

給博士研究者的 Claude Code 基礎建設——學術流程用的 skill、agent、hook、規則。LaTeX / 文獻管理為主。

---

### 文獻 RAG / Q&A

#### [Future-House/paper-qa](https://github.com/Future-House/paper-qa) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 8.9k+ |
| License | Apache-2.0 |

**教什麼**：對 PDF 文件以 **citation-grounded Q&A** 為設計目標——每個答案附句子層級的引用、減少幻覺風險。實際準確率依文件類型而異、評測結果以官方 benchmark / paper 為準。

**適合誰**：寫文獻回顧、需要「查文獻時答案要可追溯」的研究者。比一般 RAG 更嚴謹。

---

#### [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 28k+ |
| License | Apache-2.0 |

**教什麼**：自主 deep-research agent——planner + multi-source crawl + report 合成。給定一個研究主題，自動產出 markdown / PDF brief。

**適合誰**：要快速 scope 新題目、產 research brief 的研究者。

---

### 大綱與寫作

#### [stanford-oval/storm](https://github.com/stanford-oval/storm) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 30k+ |
| License | MIT |

**教什麼**：multi-perspective outline-then-write pipeline——**白話三步**：(1) 先模擬不同觀點提出問題、(2) 把問題整理成大綱、(3) 最後生成 Wikipedia-style 草稿。Stanford OVAL 出品。

**適合誰**：想學「**outline-driven 寫作**」的人。從零產主題 brief 時的好工具，類似 NotebookLM structured report 流程的開源版。

**備註**：最後一次推送已超過 6 個月，使用前確認最新 commit 日期。

---

#### [kaixindelele/ChatPaper](https://github.com/kaixindelele/ChatPaper) ⭐⭐⭐⭐⭐（中文讀者）

| 欄位 | 內容 |
|---|---|
| 語言 | 中文 + Python |
| Stars | ★ 19k+ |
| License | NOASSERTION（自訂條款，非商用） |

**教什麼**：中文研究者向的 arXiv 全流程工具——論文總結 + 翻譯 + 潤色 + 審稿回覆生成。中國研究團隊維護，預設值對中文場景友善。

**適合誰**：中文研究生想找對中文友善的 paper 全流程入門工具。

**備註**：License 是自訂的非商用條款，使用前請先讀原始條款；研究或個人用途常見，但條款還是要自己看過確認。

---

### 文獻管理整合

#### [MuiseDestiny/zotero-gpt](https://github.com/MuiseDestiny/zotero-gpt) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 7k+ |
| License | AGPL-3.0 |

**教什麼**：Zotero 的 LLM plugin——可以跟你的文獻庫對話、總結 selection、生成 inline notes。

**適合誰**：Zotero 重度使用者，想在閱讀流程裡直接接 AI 而不用切到別的工具。

**備註**：AGPL-3.0 license（傳染性開源）— 修改後要散布的衍生產品需遵守條款。

---

### Multi-LLM 研究組合（本 repo 維護者的研究 setup）

研究流程裡有些任務 Claude 一個就夠（對話、設計、review），有些 Claude 做會浪費 token（大批 code refactor、長稿 draft）。維護者實際用的搭配是 **Claude 當 planner / reviewer、Codex 跑程式、Gemini 跑長稿**——下表列何時用哪個：

| 任務類型 | 例子 | 用哪個 LLM | 為什麼 |
|---|---|---|---|
| 研究設計 / 假設討論 | 「這個 RQ 該用 logistic vs survival？」 | Claude.ai 對話 | 對話協作、context memory |
| 寫 / 改 code | 「50 個 simulation script 都加 logging」 | codex-delegate | 機械式編輯快、不燒 Claude token |
| 寫長稿（中英文） | 「draft 一個 8 頁 paper section」 | Gemini CLI | 1M context、長 prose 強項 |
| Second opinion | 「請 Gemini 看我的 discussion 段落」 | Gemini CLI | LLM-vs-LLM 對照、容易看出 Claude 自身偏誤 |
| 投稿前 audit | 「跑 banned-word + figure-text checklist」 | academic-writing-skills | structured audit、不靠 LLM 即興判斷 |

#### 維護者自用的 6 個研究 skill

> ⚠️ **揭露**：以下 6 個工具是維護者 [@WenyuChiou](https://github.com/WenyuChiou)（Lehigh CEE PhD candidate）日常在用的研究 skills、公開讓有相似需求的人用。**未經第三方獨立評測**——適合 PhD 學位寫作 / 跨 paper 文獻整理這類流程；不一定適合你的領域。詳細 entry 看 [`resources/mcp-skills-catalog.md` 13 + 14](../resources/mcp-skills-catalog.md#13-研究工作流-skills學術--paper--文獻)。

| 工具 | 適合階段 | 一句話 |
|---|---|---|
| **[ai-research-skills](https://github.com/WenyuChiou/ai-research-skills)** ⭐⭐⭐⭐⭐ | 全流程 | 14 個研究 skill 打包成 5-plugin marketplace、一個指令裝整套 |
| **[research-hub](https://github.com/WenyuChiou/research-hub)** ⭐⭐⭐⭐ | 文獻整理 | Zotero + Obsidian + NotebookLM 三工具整合 workspace、CLI / MCP / REST / dashboard 四介面 |
| **[zotero-skills](https://github.com/WenyuChiou/zotero-skills)** ⭐⭐⭐⭐ | 文獻管理 | Zotero CLI skill（搜 / 加 / 分類 / 標記）——跟 zotero-gpt 互補（後者在 Zotero 裡 chat、這份從外部操作） |
| **[academic-writing-skills](https://github.com/WenyuChiou/academic-writing-skills)** ⭐⭐⭐ | 投稿前 | banned-word audit、figure-text coupling、submission checklist；per-paper 可自訂 journal_format / style_overrides |
| **[codex-delegate](https://github.com/WenyuChiou/codex-delegate)** ⭐⭐⭐⭐⭐ | 寫程式 | Claude planner + Codex executor 的標準 skill——batch refactor / boilerplate / migration |
| **[gemini-delegate-skill](https://github.com/WenyuChiou/gemini-delegate-skill)** ⭐⭐⭐（⚠️ 已封存） | 長稿 / synthesis | Claude planner + Gemini 寫 1M context 長文 / CJK / second-opinion。**⚠️ repo 已封存 2026-07**——workflow 仍可直接用 [Gemini CLI](https://github.com/google-gemini/gemini-cli) 做 |

---

### Multi-Agent for Research

#### [langchain-ai/open_deep_research](https://github.com/langchain-ai/open_deep_research) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 12k+ |
| License | MIT |

**教什麼**：開源版的 Deep Research——支援單 agent 跟 supervisor + multi-researcher 兩種架構（multi-agent 那條目前在 `src/legacy/`）、平行搜尋、再合成成有引用的 report。是學「LLM agent 怎麼自動產出有引用 brief」的好參考。

**適合誰**：要打造「agent 自動產出有引用 brief」工作流程的研究者。是這個分類最 canonical 的開源選擇。

**備註**：依賴 LangGraph + 搜尋 tool（要 API key）。

---

#### [SakanaAI/AI-Scientist-v2](https://github.com/SakanaAI/AI-Scientist-v2) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 6.9k+ |
| License | The AI Scientist Source Code License（source-available，非商用 + 有 manuscript-disclosure 條款） |

**教什麼**：端到端的 multi-agent 科學研究 loop：構想 → 寫程式 → 跑實驗 → 寫 paper → 互審。Sakana AI 的「AI 寫整篇 ML paper」研究實作。

**適合誰**：想看「多個 agent 跑完整研究 lifecycle 會長什麼樣」的研究者。研究架構參考、不是 production 工具。

**備註**：產出是 demo 等級（不是直接投稿用），ML / CS 領域偏多。License 是自訂的 source-available 條款（含 manuscript-disclosure 規定），使用前請先讀 LICENSE 檔。

---

> 還缺：peer-review 自動化、conference review pipeline 的活躍開源案例。如果你做過或知道有，歡迎開 PR。

## 必修閱讀

1. [The Effortless Academic — Claude Code beginner guides](https://effortlessacademic.com/claude-code-and-cowork-for-academics-beginner-guide-part-1/)
2. [Pedro Sant'Anna — Researcher setup guide](https://paulgp.substack.com/p/getting-started-with-claude-code)

## 必練流程（按使用頻率）

研究者用 AI 的最大誤區是「只在卡關才打開 ChatGPT」。把 AI 變成日常工具的關鍵是**設好頻率**——下表 7 條都是維護者自己每週都在跑的、不是空想。

| 頻率 | 流程 | 怎麼做（≤ 3 步） | 推薦工具 | 適合誰 |
|---|---|---|---|---|
| **每天** | 文獻 inbox 分流 | (1) 把昨天看到的 paper 丟 paper-qa<br>(2) 抓 claim + 4-5 行 summary<br>(3) 進 Zotero / Obsidian | paper-qa + zotero-gpt | 全研究者 |
| **每天** | 寫作 sprint（25 min） | (1) 寫一段給 Claude.ai<br>(2) 跑 banned-word + figure-text audit<br>(3) 改完進 main draft | Claude.ai + academic-writing-skills | 寫 paper 階段 |
| **每週** | 跨 paper synthesis | (1) 把 5-10 篇 PDF 餵 Gemini<br>(2) 問「這幾篇 disagree 在哪」<br>(3) 寫成 1 頁 brief | Gemini CLI（1M context） | 計算型 |
| **每週** | Zotero 整理 | (1) 標未讀 / 已讀<br>(2) 重 tag<br>(3) 抓出該歸檔的 PDF | zotero-skills 或 zotero-gpt | 全研究者 |
| **每月** | 研究進度 brief | (1) 從 Obsidian + Zotero + NotebookLM 抓近期筆記<br>(2) 整理出 5 個進度點<br>(3) 送指導教授 | research-hub | 同時用 3 工具的人 |
| **Per paper** | 投稿前 final audit | (1) banned-word audit<br>(2) figure-text coupling check<br>(3) submission checklist | academic-writing-skills | 投稿前 1 週 |
| **Per paper** | Multi-agent peer review | (1) Claude 看 logic / argument<br>(2) Codex 看 code / table 數字<br>(3) Gemini 看 prose / clarity | codex-delegate + Gemini CLI | 投稿前 second-opinion |

> 💡 **新手起手式**：先做「每天 inbox 分流」+「寫作 sprint」兩條一個月、習慣後再加進階流程。一次裝太多會養不起來。

## 層級建議

研究者不需要一開始就裝 Claude Code。下表是建議的進階路徑：

| Tier | 工具 | 適合誰 | 學習成本 |
|---|---|---|---|
| **Tier 0** | Claude.ai 網頁版 + NotebookLM | 非程式背景、人文社科、臨床研究 | 0（會用瀏覽器就行） |
| **Tier 1** | Claude Desktop + Zotero MCP / Obsidian MCP | 已有 Zotero / Obsidian 習慣的研究者 | 半天裝好 |
| **Tier 2** | Claude Code + ai-research-skills | 計算型研究者、寫 / 改程式為主 | 1-2 天上手 |
| **Tier 3** | Claude Code + codex-delegate + Gemini CLI + research-hub | 想跑 multi-LLM 研究 pipeline、跨多工具整合 | 1 週 setup + 持續調 |

**多數研究者停在 Tier 1-2 就夠了**——Tier 3 是有大量重複流程（譬如每週跑同樣的 paper synthesis）才值得。
