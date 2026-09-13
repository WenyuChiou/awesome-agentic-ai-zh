# 結業專題 / Capstone

> **繁體中文** | [简体中文](./CAPSTONE.zh-Hans.md) | [English](./CAPSTONE.en.md)

走完一條軌道後,**自己做一個東西出來**——這份檔案不是教學、不是 walkthrough,沒有標準答案。它的用途是把「我讀完 roadmap」變成「我有一個能展示的作品 + 一份自己給自己的評分」。

**怎麼用這份檔案**:

1. 選你**真的有的一個問題**(工作上、研究上、生活上),別挑玩具題目——capstone 的價值來自真實。
2. 對照你那條軌道的「進入條件」,確認該完成的 stage 都過了它的「自我檢查」。
3. 做完後,用對應的 **rubric 自評**(四級:未達 / 基本 / 良好 / 優秀)。誠實打分比分數高更有用。
4. 想要回饋?把成品 + 自評貼到 [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions) 找人 peer review(可選,不強制)。

> 每一站「學什麼 / 進入前要會什麼 / 怎麼算學會」一律以該 stage 檔案內的「學習目標 / 進入條件 / 自我檢查」為準;這份檔案只定義**結業專題**本身。

---

## Track A Capstone — CLI Power User

**進入條件**：Stage 0–2 + A1 + A2 + Stage 5 的 Track A 核心 5.1–5.4 + A3 都通過自我檢查。Stage 5 的 5.5–5.8 不擋入場。建議接著完成 Stage 8，但它也不擋 Capstone 入場；Track A Capstone 聚焦 CLI 工作流。

**題目**:組一條**你會重複用**的 CLI-agent 工作流,把一件你現在手動做的事自動化。

**必要條件**(缺一不可):

- 用一個 CLI agent(Claude Code 或同類)當核心
- 至少接 **1 個** MCP server **或** 自寫的 skill / command
- 有明確輸入 → 產出可用的成品(不是「跟它聊天」)
- **能被別人重跑**:附 `怎麼跑`(安裝、設定、執行、預期輸出)
- 處理至少 **1 種失敗情況**(輸入缺、API 失敗、結果不對時會怎樣)

**交付物**:一個資料夾 / repo,含成品 + `README` + 至少一次真實執行的證據(log / 截圖 / 產出檔)+ 150 字內的反思(哪裡卡、下次怎麼改)。

**時間**:3–8 小時(不含學 stage 的時間)。

### Track A 評分 rubric(自評,四級)

| 面向 | 未達 | 基本 | 良好 | 優秀 |
|---|---|---|---|---|
| 問題真實度 | 玩具題 | 有點用 | 真實、會重複用 | 真實且有可量化指標(省時 / 減錯次數等) |
| 工具運用 | 只用基本對話 | 用了 CLI agent | + MCP 或自寫 skill/command | 多元件協作且選型有理由 |
| 可重現 | 只有自己跑得動 | 步驟不全 | 別人照 README 跑得起來 | 一鍵 / 全自動且有前置檢查 |
| 韌性 | 一出錯就崩 | 有提到風險 | 處理 1 種失敗 | 多種失敗有 fallback |
| 文件與反思 | 無 | 有 README | README 清楚 + 反思 | 反思具體可指出下一步改進 |

---

## Track B Capstone — Agent Builder

**進入條件**:Stage 0–8(含 Stage 3、4、5、6、7、7.5、8)都過了各自的自我檢查。

**題目**:設計、實作、並**評測**一個解決具體問題的小型系統,二選一:

- **A. Multi-agent**:≥ 2 個分工協作的 agent,有編排邏輯;或
- **B. RAG 系統**:檢索 + 生成的完整管線。

**必要條件**(缺一不可):

- 有 tool use
- 有一個對外 interface(CLI / API / chat 任一,對應 Stage 8)
- **有明確 evaluation**：準備一份有版本的 Eval suite，至少 5 個 development cases + 3 個 frozen holdout cases；寫清楚成功條件、grader、trial 次數與 baseline，再量通過率／質性結果（這條不可省——這套課最容易跳過的就是「驗證」）
- **失敗模式分析**:寫清楚它在什麼情況會壞、你怎麼知道
- 架構草圖(一張圖或一段文字說明元件與資料流)

**交付物**：程式 repo + 架構說明 + Eval 報告（dataset version、development／holdout、每題結果、trial 次數、baseline 與 regression）+ `README` + 200 字內反思（架構哪裡判斷錯、重來會怎麼改）。

**時間**:8–20 小時(不含學 stage 的時間)。

### Track B 評分 rubric(自評,四級)

| 面向 | 未達 | 基本 | 良好 | 優秀 |
|---|---|---|---|---|
| 問題定義 | 模糊 | 有目標 | 範圍清楚、可驗收 | 清楚且說明為何值得做 |
| 架構 | 無設計 | 能跑就好 | multi-agent / RAG 選型有理由 | 設計權衡寫得出來 |
| 實作正確性 | 跑不動 | 主流程能跑 | 邊界情況也處理 | 穩定且程式可讀 |
| **評測嚴謹度** | 沒測 | 手動試幾次 | 有版本化 development／holdout cases、成功條件與 grader | 多次 trials、baseline 對照、回歸可重跑且 holdout 沒被拿來調參 |
| 韌性與失敗分析 | 無 | 提到風險 | 具體失敗模式 | 失敗有偵測 + 緩解 |
| 介面與文件 | 無 | 能跑 | interface + README 清楚 | 別人能直接用 |
| 反思 | 無 | 一句話 | 具體(指得出架構或元件選擇的具體問題) | 指得出架構級的下一步 |

---

## 依身分選題(audience flavor)

同一個 capstone,換你的場景就好——不用另外做:

- 🔬 **researcher**:文獻問答 / 實驗 log 整理 / 資料前處理 agent
- 💻 **developer**:CI 內的 review/triage agent / repo 問答 / 自動化 release note
- 🎓 **teacher**:出題 + 評分輔助 / 教材改寫 / 課程問答(注意學術誠信邊界)
- 📊 **knowledge-worker**:會議記錄 → 行動項 / 跨文件彙整 / 週報初稿
- 👥 **everyday-user**:個人資料彙整 / 行程與提醒 / 重複雜務自動化

---

## 怎麼展示

- 貼到 [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions) 的對應分類,附成品連結 + 你的 rubric 自評。
- 放進你自己的 portfolio / GitHub;描述用具體事實(做了什麼、量到什麼),**避免**「最強 / 全世界最好」這類話術。
- 想替別人 review:照對方那條軌道的 rubric 給回饋,對事不對人。

> 這份檔案只定義結業專題與評分標準。各 stage 的學習內容與通過條件,仍以該 stage 檔案為準。
