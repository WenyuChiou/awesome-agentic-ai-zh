# AI Agent 課程地圖：先學會，再決定要不要拿證書

> **繁體中文** | [简体中文](./courses.zh-Hans.md) | [English](./courses.en.md)

<!-- freshness: canonical=resources/courses.md; verified_on=2026-08-29; scope=course-availability,cost,certificate,assessment,repository-status; max_age_days=90 -->

這一頁幫你做一件事：**從很多課裡，挑一門真的適合現在的你。** 不必先蒐集證書，也不必一次報名五門。先選一門、做出一個可以展示的作品，再走下一步。

想照本專案一步一步實作，回到 [主學習路線](../README.md)；看到陌生名詞，可查 [用語小辭典](glossary.md)。

## 🧩 先分清五個容易混在一起的詞

| 核心詞 | 五歲也能懂的說法 | 正確意思 |
|---|---|---|
| **Course（課程）** | 老師排好一條學習路。 | 一組依順序安排的影片、文章、練習或專案。 |
| **Certificate of Completion（完成證書）** | 證明你把這門課走完了。 | 證明完成指定內容；不等於學位，也不單獨證明已能做 production 系統。 |
| **Skill Badge（技能徽章）** | 一張小貼紙，表示你做過某項任務。 | 平台針對短模組或特定技能發出的數位徽章。 |
| **Professional Certificate（專業課程證書）** | 好幾門課裝成一個比較大的學習包。 | 由公司或學校設計的系列課程證書；通常仍不是學位或執照。 |
| **Certification Exam（認證考試）** | 不只上課，還要另外考試。 | 由供應商或考試機構驗證特定產品知識的考試；可能要付費、驗證身分或定期更新。 |

**最重要的規則：證書證明你完成一條路；作品才讓別人看到你會做什麼。**

## ⚡ 先選一條，不要全部一起讀

| 你現在想做什麼 | 先選這個 | 為什麼 |
|---|---|---|
| 完全不知道從哪開始 | [Hugging Face AI Agents Course](https://huggingface.co/learn/agents-course) | 免費，先教 Agent、工具與基本框架，再做挑戰。 |
| 想看大量可執行程式 | [Microsoft AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners) | 每課都有文字、影片與程式；但範例偏 Microsoft Agent Framework。 |
| 想讀完整中文教材 | [Datawhale Hello-Agents](https://github.com/datawhalechina/hello-agents) | 從原理一路走到 RAG、Multi-Agent、MCP 與部署。 |
| 想先學不綁框架的設計方法 | [DeepLearning.AI Agentic AI](https://www.deeplearning.ai/courses/agentic-ai/) | 從零實作 reflection、tool use、planning、eval 與 multi-agent。 |
| 已決定用 Claude／LangGraph | [Claude Academy](https://academy.claude.com/)／[LangChain Academy](https://academy.langchain.com/courses/intro-to-langgraph) | 直接學供應商的現行工具；記得把通用觀念和產品按鈕分開。 |
| 主要目標是系列證書 | [IBM](https://www.coursera.org/professional-certificates/ibm-rag-and-agentic-ai)／[Vanderbilt](https://www.coursera.org/specializations/ai-agents) | 是較長的付費系列課；先確認費用、語言與專案是否符合需要。 |

## 🎯 精選課程與學習路線

星等是本專案的**編輯推薦度**，不是證書排名：⭐⭐⭐⭐⭐ 適合當主線；⭐⭐⭐⭐ 很值得讀，但較偏特定工具或目的；⭐⭐⭐ 適合已確定使用該供應商的人。

<table>
  <thead>
    <tr><th scope="col">學習目的</th><th scope="col">課程／教材</th><th scope="col">語言與費用</th><th scope="col">你會做出什麼</th><th scope="col">證書／限制</th><th scope="col">推薦度</th></tr>
  </thead>
  <tbody>
    <tr><th scope="rowgroup" rowspan="3">免費打底</th><td><a href="https://huggingface.co/learn/agents-course">Hugging Face — AI Agents Course</a></td><td>英文為主；免費</td><td>認識 Agent Loop，實作 smolagents、LlamaIndex、LangGraph、Agentic RAG 與 Eval。</td><td>Unit 1 測驗達 80% 可取得基礎完成證書；完整路徑另含作業與最終挑戰。</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/microsoft/ai-agents-for-beginners">Microsoft — AI Agents for Beginners</a></td><td>多語；免費開源</td><td>用文字、影片與 Python／.NET 範例做工具、記憶、規劃、RAG、Multi-Agent 與部署。</td><td>沒有完成證書；現行範例偏 Microsoft Agent Framework 與 Foundry。</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://github.com/datawhalechina/hello-agents">Datawhale — Hello-Agents</a></td><td>簡體中文；免費開源</td><td>從 Agent 原理與經典 pattern，一路做到 RAG、記憶、Multi-Agent、MCP 與完整專案。</td><td>沒有完成證書；章節很多，請按自己的問題選讀，不必一次讀完。</td><td>⭐⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="4">建構與上線</th><td><a href="https://www.deeplearning.ai/courses/agentic-ai/">DeepLearning.AI — Agentic AI</a></td><td>英文；影片可免費旁聽</td><td>從零實作 reflection、tool use、planning、Multi-Agent、錯誤分析與 component Eval。</td><td>測驗、graded assignments 與證書需要 Pro；免費旁聽不含證書。</td><td>⭐⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://academy.claude.com/">Claude Academy</a></td><td>英文；免費</td><td>依需要學 Claude API、Claude Code、MCP、Agent Skills 與 Subagents。</td><td>通過課程 quiz 可取得免費完成徽章；它是 Claude 產品路線，不取代通用 Agent 基礎。</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://academy.langchain.com/courses/intro-to-langgraph">LangChain Academy — Introduction to LangGraph</a></td><td>英文；免費</td><td>做 graph、state、memory、HITL、subgraph、deployment 與 long-term memory。</td><td>偏 LangGraph／LangSmith；現行公開課程頁沒有清楚列出證書門檻。</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://www.kaggle.com/learn-guide/5-day-agents">Google × Kaggle — 5-Day AI Agents Intensive</a></td><td>英文；免費自學</td><td>按模型、工具、orchestration、memory 與 Eval 理解 Agent，再做 capstone。</td><td>原本是限時 intensive，現在以自學 guide 使用；不要把 cohort 活動資格當成永久證書。</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">較長的系列課</th><td><a href="https://www.coursera.org/professional-certificates/ibm-rag-and-agentic-ai">IBM — RAG and Agentic AI Professional Certificate</a></td><td>英文；付費訂閱，可查看助學選項</td><td>用多門課完成 RAG、Agentic AI、工具、向量資料庫與實作專案。</td><td>IBM／Coursera 系列證書；不是學位，費用與可用補助依地區及帳號為準。</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://www.coursera.org/specializations/ai-agents">Vanderbilt — AI Agent Developer Specialization</a></td><td>英文；付費訂閱，平台提供多語字幕</td><td>用 Python、工具、記憶與 Agent architecture 做一組應用專案。</td><td>Vanderbilt／Coursera Specialization 證書；部分內容偏 OpenAI 工具。</td><td>⭐⭐⭐⭐</td></tr>
  </tbody>
  <tbody>
    <tr><th scope="rowgroup" rowspan="2">中文供應商路線</th><td><a href="https://www.nvidia.cn/training/certification/generative-ai-llm-learning-path/">NVIDIA — 代理式 AI 中文學習路徑</a></td><td>簡體中文；自學與講師帶領課多為付費</td><td>依序學 RAG Agent、Agentic AI 應用、評估與 production deployment。</td><td>部分課程授予 DLI 培訓證書；價格與排課依官方頁，且內容偏 NVIDIA stack。</td><td>⭐⭐⭐⭐</td></tr>
    <tr><td><a href="https://edu.aliyun.com/certification/cldm02">阿里雲 — 基於百煉平台構建智能體應用</a></td><td>簡體中文；目前可免費啟用</td><td>做低程式碼智能體、工作流程與智能體編排，連到網站、釘釘等場景。</td><td>完成學習與考試後領 Clouder 證書；需符合官方列出的身分文件條件，且綁百煉平台。</td><td>⭐⭐⭐</td></tr>
  </tbody>
</table>

想用中文伴讀 DeepLearning.AI，可接著看 [Datawhale 的開源整理](https://github.com/datawhalechina/agentic-ai)。

## 🧪 每讀一門課，都留下同一份作品證據

不要只下載 PDF。直接複製這張小卡，替每門課留下可檢查的成果：

```text
我解決的問題：
Agent 可以使用的工具：
我怎麼知道它做對：
失敗時怎麼安全停止：
可執行程式或 Demo 連結：
```

最小作品可以只是一個會查資料、呼叫一個工具、留下 Eval 結果的小 Agent。完成後再回本專案對照 [Stage 3 工具使用](../stages/03-tool-use-and-hello-agent.md)、[Stage 4 Workflow Graph](../stages/04-agent-frameworks.md) 與 [Stage 7 上線工程](../stages/07-multi-agent-production.md)。

<details markdown="1">
<summary>📜 展開：證書到底能證明什麼？</summary>

1. **完成證書只證明完成指定步驟。** 它不是學位，也不保證已能獨立上線 Agent。
2. **考試認證和完成證書不同。** 前者可能需要監考、身分驗證與另外付費；不要把免費課程徽章寫成專業執照。
3. **免費不等於差，付費也不保證適合。** 先看有沒有練習、Eval、專案與現行文件。
4. **履歷同時放作品。** 誠實寫「完成什麼、做出什麼、怎麼測」，不要只貼一排 badge。
5. **課程會變。** 報名前重新確認費用、證書門檻、語言與需要的 API／雲端帳號。

</details>

<details markdown="1">
<summary>🔎 展開：這份清單怎麼維護？</summary>

- 先看課程或供應商的官方頁，再看官方 repository；第三方文章只能當線索。
- 星等評的是教學價值、實作完整度、更新狀態與可轉移性，不評「哪張證書比較好找工作」。
- 不列只有行銷頁、無法確認課綱或把一般完成證書包裝成執照的項目。
- repository 的 stars 只用來發現社群關注，不寫進正文；維護狀態要看是否封存、最近更新與現行文件。
- 費用、證書與 cohort 有變動時，三語內容與測試要一起更新。

- 2026-10-02：W&B AI Engineering: Agents 暫移出現行推薦。舊入口回傳 404，新入口目前無法開啟。這不代表永久停課；確認可用的官方課程入口後再評估。

</details>

<small>資料查核：2026-08-29 UTC。</small>
