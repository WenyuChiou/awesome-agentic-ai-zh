<div align="right">
  <strong>繁體中文</strong> | <a href="./README.zh-Hans.md">简体中文</a> | <a href="./README.en.md">English</a>
</div>

<div align="center" markdown="1">

![AI Agent 學習路徑](resources/diagrams/banner.png)

# awesome-agentic-ai-zh

**🤖 一張從「AI Agent 是什麼」走到「能做出可靠系統」的學習地圖**

**先選一條路，再一步一步走。重要概念、動手練習與精選資源都幫你排好順序。**

[![License](https://img.shields.io/badge/license-MIT-blue?style=flat)](LICENSE)
[![繁中](https://img.shields.io/badge/語言-繁體中文-red?style=flat)](README.md)
[![简中](https://img.shields.io/badge/語言-简体中文-orange?style=flat)](README.zh-Hans.md)
[![EN](https://img.shields.io/badge/lang-English-blue?style=flat)](README.en.md)
![GitHub stars](https://img.shields.io/github/stars/WenyuChiou/awesome-agentic-ai-zh?style=flat&logo=github)
[![線上文件站](https://img.shields.io/badge/線上閱讀-立即開始-2ea44f?style=flat)](https://wenyuchiou.github.io/awesome-agentic-ai-zh/)

</div>

> 📱 手機閱讀請使用[線上文件站](https://wenyuchiou.github.io/awesome-agentic-ai-zh/)。

## 🎯 這份地圖幫你做什麼？

**AI Agent** 是「能讀懂目標、使用工具，並依結果繼續下一步的程式」。這個 repo 不要求你一開始就懂所有名詞，而是帶你依序完成三件事：

1. **先懂基礎**：LLM、Prompt、API 與 Token 是什麼。
2. **再做出東西**：讓模型呼叫工具、跑 Agent Loop、讀文件與記住事情。
3. **最後做得可靠**：加入權限、Eval、人工批准、觀測與失敗復原。

這裡的角色是**學習路線圖 + 精選資源 + 可直接執行的小練習**。需要完整章節時，我們會帶你去官方文件、[Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents) 或對應的 Cookbook，不重寫另一套百科全書。需要連模型時，每個練習會再說明雲端或本機路徑。

重要技術詞第一次出現時會先用白話說明，再保留正式英文。忘記某個詞時，直接查[名詞表](resources/glossary.md)。

## 🚀 現在就開始

1. **完全沒寫過程式**：從 [Stage 0：基礎準備](stages/00-foundations.md)開始；API 或 CLI Agent 不熟時，搭配[零基礎設定指南](resources/setup-guide.md)。
2. **已經會 Python、Git 與 API**：從 [Stage 1：LLM 基礎](stages/01-llm-basics.md)開始。
3. **還不確定要走哪條路**：先看下面的 Track A／Track B 選擇表。

走 Track A 或 Track B 前，先確認 Stage 0–2；只走日常使用者路線的人可以直接打開角色指南。

| 你現在想做什麼？ | 建議路線 | 路線入口 |
|---|---|---|
| 用 Claude Code、Codex、OpenCode 等 CLI Agent 完成工作 | **Track A — CLI Power User** | [A1：選一個 CLI Agent](tracks/cli/A1-cli-intro.md) |
| 自己寫 Agent、工具迴圈、Workflow 與服務 | **Track B — Agent Builder** | [Stage 3：第一個 Agent Loop](stages/03-tool-use-and-hello-agent.md) |
| 只想在日常生活安全使用 AI，暫時不寫程式 | **日常使用者路線** | [日常使用者指南](branches/for-everyday-users.md) |

<details markdown="1">
<summary>💻 展開：下載到本機</summary>

```powershell
git clone https://github.com/WenyuChiou/awesome-agentic-ai-zh.git
cd awesome-agentic-ai-zh
```

下載後先開啟 `stages/00-foundations.md`，或依上表直接前往適合你的第一站。

</details>

## 從 Stage 0 到 Stage 8，另有 Stage 7.5 閱讀站

![AI Agent 學習地圖](resources/diagrams/learning-map.png)

這張地圖共有 **8 個主題 Stage + Stage 0 準備關 + Stage 7.5 進階閱讀站**，也就是 **10 個學習站**。Track A／B 讀者先確認 **Stage 0–2 共用基礎**；已經會 Python、Git 與 API 的人可以跳過 Stage 0。日常使用者可以直接走角色指南。

### 共用基礎：Stage 0–2

| Stage | 這一步解決什麼？ | 完成後你能做什麼？ |
|---|---|---|
| **0** · [基礎準備](stages/00-foundations.md) | 電腦與基本工具準備好了嗎？ | 用 Python 呼叫公開 API、讀 JSON，並用 Git 保存成果 |
| **1** · [LLM 基礎](stages/01-llm-basics.md) | LLM、Token、Context 與模型差在哪裡？ | 呼叫一個 LLM，並依需求選雲端或本機模型 |
| **2** · [Prompt 設計](stages/02-prompt-engineering.md) | 怎麼把目標、資料、規則與輸出說清楚？ | 用固定案例比較 Zero-Shot、One-Shot、Few-Shot 與 CoT 的邊界 |

### Track A：使用 CLI Agent 把工作做完

正式順序是 `A1 → A2 → Stage 5 → A3 → Stage 8`。

| 順序 | 這一步解決什麼？ | 完成後你能做什麼？ |
|---|---|---|
| **A1** · [選一個 CLI Agent](tracks/cli/A1-cli-intro.md) | OpenRouter、OpenCode、Pi、Ollama 分別是什麼？ | 選對工具並完成第一個小任務 |
| **A2** · [建立可重複流程](tracks/cli/A2-cli-workflow.md) | 怎麼把規則與步驟留給下一次使用？ | 寫 Project Instructions、Skill 與可重用工作流程 |
| **5** · [Claude Code 生態](stages/05-claude-code-ecosystem.md) | MCP、Skills、Plugins、Hooks 與 Subagents 怎麼分？ | 先讀核心 5.1–5.4；5.5–5.8 依工作需要選讀 |
| **A3** · [接進真實工作](tracks/cli/A3-cli-production.md) | 怎麼安全連接外部工具、CI 與團隊流程？ | 用最小權限、人工檢查與紀錄完成整合 |
| **8** · [Agent 操作介面](stages/08-agent-interfaces.md) | Agent 怎麼操作瀏覽器、畫面與 Sandbox？ | 判斷任務該用 CLI、Browser、Computer Use 還是 API |

### Track B：從零打造 Agent

| 順序 | 這一步解決什麼？ | 完成後你能做什麼？ |
|---|---|---|
| **3** · [工具使用與第一個 Agent Loop](stages/03-tool-use-and-hello-agent.md) | 模型怎麼安全呼叫工具並重複下一步？ | 做出有最大輪數、會驗證參數的 Agent Loop |
| **4** · [Workflow Graph 與 Agent 框架](stages/04-agent-frameworks.md) | 怎麼把多個步驟畫成工作地圖？ | 選擇 Workflow、Agent、Graph 與 Framework |
| **5** · [Claude Code 生態](stages/05-claude-code-ecosystem.md) | MCP、Skills、Plugins、Hooks 與 Subagents 怎麼合作？ | 組合工具、規則與可重用能力 |
| **6** · [Memory · RAG](stages/06-memory-rag.md) | Agent 怎麼查文件、保存與取回重要資訊？ | 建立最小 RAG、long-term memory 與 contextual retrieval 流程 |
| **7** · [Agent Production Engineering：Harness、Loop 與 Graph](stages/07-multi-agent-production.md) | Agent 怎麼在真實環境穩定運作？ | 加入 Eval、觀測、預算、Human-in-the-loop（HITL，人工批准）與復原 |
| **7.5** · [進階 Agentic 概念地圖](stages/07.5-advanced-agentic-concepts.md) | 還有哪些進階 Pattern 值得認得？ | 從 12 個概念選讀 PAR loop、agent-as-judge 等需要的主題 |
| **8** · [Agent 操作介面](stages/08-agent-interfaces.md) | Agent 怎麼操作 API 以外的真實環境？ | 選擇 Computer Use、Browser Use 或 Code Sandbox |

Stage 4 先看懂 **Workflow Graph**，再用 framework 把它做出來；Stage 7 再加入 Eval、觀測、批准與復原，讓同一張工作圖可以穩定運作。

> 🔭 **學習順序**：Stage 2 Prompt → Stage 3 **Agent Loop** → Stage 4 **Workflow Graph**／Framework → Stage 5 工具與規則 → Stage 6 **Context Engineering** → Stage 7 production。`prompt → context → harness → loop → graph` 是五個控制問題，不是章節順序。

完成 A3 或 Stage 7 後，可以開始 [Capstone 專案](CAPSTONE.md)；想記錄進度可使用 [PROGRESS.md](PROGRESS.md)。

<details markdown="1">
<summary>⏱️ 查看時間估算（安排參考，不是截止日期）</summary>

- **Track A**：約 8–10 週。重點是使用現成 CLI Agent 完成工作。
- **Track B**：主幹約 16–22 週；每週投入 5–8 小時時，通常需要 5–7 個月。
- **Stage 5** 是工具與規則 Hub：Track A 看怎麼用，Track B 看怎麼組合。
- **Stage 8** 是操作介面 Hub：Track A 看怎麼委派，Track B 看怎麼接進自己的 Agent。

時程只是安排參考。先完成眼前的一步，不需要一次讀完整張地圖。

</details>

### 依你的身分繼續走

![依身分選擇延伸路線](resources/diagrams/branch-decision-tree.png)

| 路線 | 適合誰 | 你會處理什麼？ |
|---|---|---|
| 🔬 [研究人員](branches/for-researcher.md) | 研究生、博後、PI | 文獻證據、可重現流程、Multi-Agent Review |
| 💻 [開發者](branches/for-developer.md) | 軟體工程師 | CLI Delegation、Code Review、測試與回復 |
| 🎓 [教師](branches/for-teacher.md) | 老師、講師 | 備課、回饋、隱私與教學 Prompt |
| 📊 [知識工作者](branches/for-knowledge-worker.md) | 顧問、PM、分析師 | Email、會議與報告工作流程 |
| 👥 [日常使用者](branches/for-everyday-users.md) | 不一定寫程式的 AI 使用者 | 寫作、學習、隱私與安全使用 |

## 💡 怎麼學才不容易卡住？

1. **一次只走一個 Stage**：先回答這一章的核心問題。
2. **核心詞與必讀先看**：它們會直接用在後面的練習。
3. **直接複製第一個指令**：先跑不連網的測試，不必抄一份空白檔案。
4. **一次只改一件事**：改完立刻再跑測試，才知道是哪個改動造成結果。
5. **做到完成條件再往下走**：看懂不等於做得到。

每個 `starter.py` 都是可執行參考。先看題目與成功條件，再修改一個地方並重跑測試。完整方法見[如何使用這份教材](docs/HOW_TO_USE.md)。

## 📚 先收藏的學習入口

這裡只放最常用入口；完整清單在 [RESOURCES.md](RESOURCES.md)。星號表示**學習優先順序**，不是專案排行榜。

<table>
  <thead><tr><th>用途</th><th>入口</th><th>什麼時候用？</th><th>重要性</th></tr></thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">開始</th><td><a href="resources/setup-guide.md">零基礎設定指南</a></td><td>第一次安裝與執行</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="docs/HOW_TO_USE.md">如何使用這份教材</a></td><td>開始第一個動手練習前</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="PROGRESS.md">學習進度表</a></td><td>想知道下一步或記錄完成項目</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">學習</th><td><a href="resources/glossary.md">核心名詞表</a></td><td>遇到 Token、RAG、MCP 等陌生詞</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="examples/README.md">可執行範例入口</a></td><td>想直接跑離線測試與小型案例</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="resources/cookbook.md">實作 Cookbook</a></td><td>想做 Skill、MCP、Office、Zotero 或本機 LLM</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">查資料</th><td><a href="resources/README.md">資源工具櫃</a></td><td>不知道該查 Guide、Catalog 還是 Cookbook</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="RESOURCES.md">完整資源清單</a></td><td>想找官方文件、課程、社群與延伸閱讀</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="resources/cli-agents-guide.md">CLI Agent 選擇指南</a></td><td>準備走 Track A 或比較 CLI 工具</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="resources/courses.md">課程與認證地圖</a></td><td>分清完成證書、技能徽章與認證考試</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
</table>

## 🤝 一起改進這張地圖

- 內容錯誤、失效連結或過時資訊：請開 [Issue](https://github.com/WenyuChiou/awesome-agentic-ai-zh/issues)。
- 想補一個專案或學習資源：請附上「它教哪個 Stage 的什麼」。
- 準備送 PR：先看 [CONTRIBUTING.md](CONTRIBUTING.md) 與[寫作規範](resources/style-guide.md)。
- 最近更新內容：查看 [CHANGELOG.md](CHANGELOG.md)。

<details markdown="1">
<summary>🧰 展開：完整貢獻方式與自動檢查</summary>

你可以修正文字、補三語鏡像、回報缺少的主題，或長期維護一個 Stage／角色路線。新增 GitHub 專案連結時，自動檢查會協助查看封存狀態、License 與最近更新；是否收錄仍由 maintainer 依學習價值判斷。

完整角色與規則見 [CONTRIBUTORS.md](CONTRIBUTORS.md)。

</details>

## 🙏 重要啟發與相關專案

- [**Datawhale Hello-Agents**](https://github.com/datawhalechina/hello-agents) — 適合需要完整章節與深度實作的讀者。
- [**Datawhale 社群**](https://github.com/datawhalechina) — 中文機器學習共學社群，提供許多可靠的學習入口。
- [**liyupi/ai-guide**](https://github.com/liyupi/ai-guide) — 偏向廣度資源庫；本 repo 則負責安排學習順序。

<details markdown="1">
<summary>📖 展開：貢獻者與引用格式</summary>

[![Contributors](https://contrib.rocks/image?repo=WenyuChiou/awesome-agentic-ai-zh)](https://github.com/WenyuChiou/awesome-agentic-ai-zh/graphs/contributors)

```bibtex
@misc{awesome_agentic_ai_zh_2026,
  title = {awesome-agentic-ai-zh: A Structured Learning Roadmap for Agentic AI},
  author = {Chiou, Wenyu},
  year = {2026},
  url = {https://github.com/WenyuChiou/awesome-agentic-ai-zh}
}
```

</details>

## ☕ 支持與聯絡

這份學習地圖採 MIT 授權，會繼續免費公開。一般問題與建議請使用 Issue；需要私下聯絡時可寄信至 [wenyuchiou12@gmail.com](mailto:wenyuchiou12@gmail.com)。

如果這份地圖幫到你，歡迎給一個 ⭐ Star，或[請作者喝杯咖啡](https://www.buymeacoffee.com/wenyuchiou)。

## License

MIT。Maintained by [@WenyuChiou](https://github.com/WenyuChiou)。
