# 日常使用者延伸路線（For Everyday Users）

> **繁體中文** | [简体中文](./for-everyday-users.zh-Hans.md) | [English](./for-everyday-users.en.md)

> 🚀 **日常使用者可直接從 Tier 0 開始**（網頁 / 手機 App）、**不需要任何 setup**。只有當你想跑本地 LLM（Tier 3）或用 CLI 自動化（Tier 2）時、才需要看 [`resources/setup-guide.md` A-C](../resources/setup-guide.md)（30 分鐘從零裝好）。

> [← 回主路線 README](../README.md) · 你**不一定要走完整條主幹**才能從這裡開始——這條分支是給「**只想 USE AI、不一定要 BUILD agent**」的人。

## 使用情境（生活場景 × AI 怎麼幫）

下表把日常使用者一天會遇到的 7 個情境拆開——多數場景在網頁版（Tier 0）就能搞定：

| 場景 | 你常遇到的痛點 | AI 能幫的部分 | 推薦工具 |
|---|---|---|---|
| **寫 email / cover letter** | 卡在「該怎麼開頭」 | 起草 + 改語氣 + 多版本對比 | Claude.ai / ChatGPT |
| **學新技能** | 教材太正式、沒人問問題 | 個人化 tutor、可隨時打斷問 | Claude.ai / ChatGPT |
| **練語言** | 沒對話對象、不知文法錯哪 | 語音對話、即時糾錯 | ChatGPT Voice / Gemini |
| **查資料 / 比較** | 不知該信哪個來源 | 多源搜尋 + 附引用 | Perplexity |
| **整理生活流程** | 食譜 / 行程 / 待辦清單散落 | 整合 + 結構化 | Claude.ai / ChatGPT |
| **批次整理檔案** | 100 個 PDF / 圖片不知怎麼分 | 重命名 + 分類 + 摘要 | Claude Desktop / Claude Code |
| **隱私敏感 chat** | 醫療 / 法律 / 財務筆記不想送雲 | 本地跑 LLM | Ollama + qwen2.5 |

> 💡 **不要被催著升級**：前 5 個場景都可以停在 Tier 0（網頁版）。只有要「重複跑同一個流程」或「資料絕對不能送雲」才需要 Tier 1-3。

## 起步：你應該從哪一層進來？

按「**動手願意度**」分 4 層，從低到高：

```
Tier 0：網頁 / 手機 App（推薦從這裡開始）
   ↓
Tier 1：Desktop App（要處理本機檔案再升級）
   ↓
Tier 2：CLI Agent（願意學一點命令列，能自動化日常流程）
   ↓
Tier 3：本地 LLM（隱私敏感、API 費用敏感、想 offline）
```

**多數人停在 Tier 0 / Tier 1 就夠用了**——Tier 2-3 是給有特殊需求或想學的人。

---

## 🎯 精選 Projects

### Tier 0 — 網頁 / 手機 App ⭐ 入門

#### [Claude.ai](https://claude.ai) ⭐⭐⭐⭐⭐
Anthropic 官方介面。長文章、深度討論、複雜問題很適合用——回答風格較收斂、不太瞎掰。

#### [ChatGPT](https://chatgpt.com) ⭐⭐⭐⭐⭐
OpenAI 官方介面。生態最廣（GPTs、Custom Instructions、Voice mode）。一般用途的標準選擇。

#### [Gemini](https://gemini.google.com) ⭐⭐⭐⭐
Google 出品。長 context（一次能讀很長文件、約一本厚書的量）特別適合丟整本 PDF 進去問問題；仍要自己檢查引用與摘要是否正確。整合 Google 服務（Gmail、Docs）。

#### [Perplexity](https://perplexity.ai) ⭐⭐⭐⭐
搜尋引擎 × LLM——每個答案都附引用來源。比 ChatGPT 適合「需要查最新資訊」的場景。

---

### Tier 1 — Desktop App

#### [Claude Desktop](https://claude.ai/download) ⭐⭐⭐⭐⭐
比網頁版多了：拖檔案進去、本機檔案讀取、保留長期對話脈絡。**也是進入 AI 工具整合生態（MCP）的入口**——可以接 Slack / Gmail / 行事曆，讓你在 Claude 裡直接操作這些服務。

#### [ChatGPT Desktop](https://chatgpt.com/download/) ⭐⭐⭐⭐
ChatGPT 桌面版。可以對螢幕截圖問問題、語音對話、跟其他 App 整合。

---

### Tier 2 — CLI Agent（願意學命令列的進階使用者）

> 這些工具雖然定位給開發者，但**日常使用者也能用**——例如批次重新命名檔案、整理下載資料夾、自動寫每週回顧、把 PDF 摘要存成 Markdown。
>
> 想知道哪種 CLI agent 適合你？見 [`resources/cli-agents-guide.md`](../resources/cli-agents-guide.md)（依工作方式選工具、常見坑、實用搭配）。
>
> 想要 step-by-step 上手？見 [`tracks/cli/A1-cli-intro.md`](../tracks/cli/A1-cli-intro.md)（Track A 第一站，從安裝到第一個任務）。
>
> 想把 CLI agent 接到你的 Notion / Obsidian / Excel / Google 文件等日常工具？見 [`resources/mcp-skills-catalog.md`](../resources/mcp-skills-catalog.md)（按分類整理 81+ 個 MCP server / Skill）。

#### [anthropics/claude-code](https://github.com/anthropics/claude-code) ⭐⭐⭐⭐⭐
★ 138k+ — Anthropic 官方的 CLI agent。能讀寫檔案、執行指令、做多步驟任務。**日常使用者最容易上手的 CLI 工具**。

#### [openai/codex](https://github.com/openai/codex) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 115k+ |
| License | Apache-2.0 |

**教什麼**：OpenAI 出品的終端機 agent——可以在命令列幫你整理檔案、批次處理文字、執行多步驟任務；寫程式只是其中一種用途。跟 Claude Code 同類、但用的是 OpenAI 的模型。

**適合誰**：已經訂 ChatGPT Plus / Pro，想在終端機用同一個帳號做事的人。

#### [anomalyco/opencode](https://github.com/anomalyco/opencode) ⭐⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 196k+ |
| License | MIT |

**教什麼**：開源版的 coding agent，**不綁特定 LLM provider**——可以用 Claude、GPT、Gemini、本地 Ollama 任何一個。社群維護、迭代速度快。

**適合誰**：想 self-host、不想被 API provider 綁住，或要在多個 LLM 之間切換的人。

#### [google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) ⭐⭐⭐⭐

| 欄位 | 內容 |
|---|---|
| Stars | ★ 103k+ |
| License | Apache-2.0 |

**教什麼**：Google 官方的 Gemini CLI agent。把 Gemini 的長 context 跟 Google 生態整合到終端機。

**適合誰**：Google 生態的重度使用者（Gmail、Drive、Docs）。

---

### Tier 3 — 本地 LLM（隱私 / 離線 / 省錢）

#### [Ollama](https://github.com/ollama/ollama) ⭐⭐⭐⭐⭐
★ 170k+ — 一行指令跑本地 LLM。隱私敏感資料（病歷、合約、家人對話）不適合送去雲端時用這個。詳見 [Stage 1 — Local LLM 執行](../stages/01-llm-basics.md)。

#### [LM Studio](https://lmstudio.ai/)
非開源但對非開發者最友善——拖拉介面、不用 command line。Mac / Windows / Linux 都有。

---

### Prompt 素材庫

#### [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) ⭐⭐⭐⭐
★ 161k+ — 社群維護的 prompt 大全。「act as 翻譯家 / 履歷顧問 / 廚師...」幾百種角色。**不知道怎麼開頭時從這裡找靈感**。

---

## 必修閱讀

1. [**Anthropic — How to write effective prompts**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — 不用程式碼也能讀的 prompt 寫法
2. [**OpenAI — Prompting Guide**](https://platform.openai.com/docs/guides/prompt-engineering) — 對位的官方文件
3. [**ChatGPT 怎麼用得最好（中文）**](https://www.runoob.com/) — 各家中文部落格的整理（runoob 等等）

如果有興趣再深入，看 [Stage 2 — Prompt 設計](../stages/02-prompt-engineering.md)，那邊有正式系統性教學。

## 可以建的流程（按使用頻率）

下表 5 條是模板、配合你自己的場景調整：

| 頻率 | 流程 | 怎麼做（≤ 3 步） | 推薦工具 |
|---|---|---|---|
| **每天** | Email 分流 | (1) 早上把待回信件貼進 Claude<br>(2) 請它分類「立即回 / 今天回 / 這週回 / 不用回」<br>(3) 草擬回信讓你 review | Claude.ai / ChatGPT |
| **每天** | 練語言（口說） | (1) 打開 ChatGPT Voice 模式<br>(2) 對話練英 / 日<br>(3) 請它指出文法錯誤 | ChatGPT Voice / Gemini |
| **每週** | 週記整理 | (1) 跟 Claude 講這週做什麼<br>(2) 請它整理成週記 + 下週重點<br>(3) 存到 Obsidian / Notion | Claude.ai |
| **不定期** | 批次整理檔案 | (1) Claude Code 進 Downloads 資料夾<br>(2) 按日期 + 主題重命名<br>(3) 自動分到子資料夾 | Claude Code |
| **隱私場景** | 本地醫療 / 法律 / 財務筆記 | (1) Ollama 跑 qwen2.5:7b<br>(2) 整理個人筆記、資料不送雲<br>(3) ⚠️ 保護的是**隱私**、不是**正確性**——具體診斷 / 法律判斷 / 投資決策仍需專業人士 | Ollama + qwen2.5 |

> 💡 **新手起手式**：先把「每天 Email 分流」+「練語言」做一個月、習慣 AI 在日常的位置、再加其他流程。

## 給日常使用者的層級建議

下表是建議的進階路徑：

| Tier | 工具 | 適合誰 | 學習成本 |
|---|---|---|---|
| **Tier 0** | Claude.ai / ChatGPT / Gemini / Perplexity（網頁版） | 90% 的場景都在這裡——免安裝、免付費 | 0（會用瀏覽器就行） |
| **Tier 1** | Claude Desktop / ChatGPT Desktop + MCP | 要處理本機檔案、保留對話歷史、接 Gmail / Notion | 半小時裝好 |
| **Tier 2** | Claude Code / opencode（CLI） | 有重複自動化需求（每天做同樣的事 100 次） | 1-2 天上手 |
| **Tier 3** | Ollama 本地 LLM | 隱私敏感資料不能送雲、API 費用敏感、想 offline | 半天設定 |

> **不要被人催著升級**——多數人 Tier 0 就夠用了。Tier 2-3 是工具、不是身份地位。

## 社群備註

這條分支也歡迎社群貢獻：

- 推薦特定領域的 prompt template（料理、運動、學語言）
- 中文友善的 chat tools（國產 LLM、本地化 wrapper）
- 隱私 / 安全相關的最佳實踐（什麼資料能送 / 不能送）

詳見 [CONTRIBUTING.md](../CONTRIBUTING.md)。
