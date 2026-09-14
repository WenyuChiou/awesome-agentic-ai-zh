# 貢獻者 / Contributors

謝謝每一個讓這份 repo 變更好的人。

---

## 🛠 Maintainer

- [@WenyuChiou](https://github.com/WenyuChiou) — 創立、整體 curation、phase 1-5 主要作者

## 🌱 Stage 維護者 / Stage maintainers

> 每個 stage 都歡迎社群志願者掛名**長期維護者**——有空時 review 一輪、處理該 stage 的 issue、把關 PR。沒有強制節奏。
>
> 想擔任 maintainer？開個 issue 自薦就好，不用承諾固定 review 期程——能做幾次就幾次。

### 共用基礎（Stage 0-2）

| Stage | Maintainer | 加入日期 |
|---|---|---|
| Stage 0 — 基礎準備 | （社群 PR 機會） | — |
| Stage 1 — LLM 入門 | （社群 PR 機會） | — |
| Stage 2 — Prompt 設計 | （社群 PR 機會） | — |

### Track A — CLI Power User

| Stage | Maintainer | 加入日期 |
|---|---|---|
| A1 — CLI Agent 入門 + 選擇 | （社群 PR 機會） | — |
| A2 — CLI Workflow Patterns | （社群 PR 機會） | — |
| A3 — Integration & Production | （社群 PR 機會） | — |

### Track B — Agent Builder

| Stage | Maintainer | 加入日期 |
|---|---|---|
| Stage 3 — 工具使用與第一個 Agent Loop ⭐ | （社群 PR 機會） | — |
| Stage 4 — Workflow Graph 與 Agent 框架 | （社群 PR 機會） | — |
| Stage 5 — Claude Code 生態 ⭐⭐（兩條軌共用） | （社群 PR 機會） | — |
| Stage 6 — Memory · RAG · 進階 | （社群 PR 機會） | — |
| Stage 7 — Agent 上線工程：可測、可看、可停、可恢復 | （社群 PR 機會） | — |

## 🌳 Branch 維護者 / Branch maintainers

| Branch | Maintainer | 加入日期 |
|---|---|---|
| 🔬 for-researcher | （社群 PR 機會） | — |
| 💻 for-developer | （社群 PR 機會） | — |
| 🎓 for-teacher | **特別歡迎自薦**（學術引用待深化） | — |
| 📊 for-knowledge-worker | **特別歡迎自薦**（目前最薄） | — |
| 👥 for-everyday-users | （社群 PR 機會） | — |

## 💬 內容貢獻者 / Content contributors

> 每次 merged PR 或實質 issue 修正都會在這裡留名。第一次 contribution 不分大小都會列入。

| Contributor | 貢獻 / Contribution | First contribution |
|---|---|---|
| [@scott0127](https://github.com/scott0127) | **Stage 6 RAG 教材** — chunking strategies guide ([#2](https://github.com/WenyuChiou/awesome-agentic-ai-zh/pull/2))、unit guide overview ([#5](https://github.com/WenyuChiou/awesome-agentic-ai-zh/pull/5)) · **for-teacher 框架** — 3-tier 教師 AI 應用情境 + 學術引用 (Chen 2020 / Mittal 2024) ([#6](https://github.com/WenyuChiou/awesome-agentic-ai-zh/pull/6)) | 2026-05-08 |
| [@xfq](https://github.com/xfq) | **i18n correctness audit** — flagged BCP 47 / W3C compliance issue (`zh-CN` → `zh-Hans`) and provided the script subtag rationale ([#9](https://github.com/WenyuChiou/awesome-agentic-ai-zh/issues/9)). [W3C i18n lead](https://www.w3.org/International/). | 2026-05-10 |
| [@demo112](https://github.com/demo112) | **中國生態 catalog** — 新增 whale (DeepSeek terminal assistant) + a-stock-data (A 股工具包) 到 Chinese ecosystem ([#14](https://github.com/WenyuChiou/awesome-agentic-ai-zh/pull/14)) | 2026-05-14 |
| [@Rain120](https://github.com/Rain120) | **zh-Hans 大陸在地化** — 系統盤點 zh-Hans 鏡像的台灣用詞,促成 `scripts/zh-hans-localize.py`(curated 台→陸詞表 + 大陸引號,已套全 54 檔並進 lint CI gate;貢獻者掛 commit `7f73b8a` Co-Author)([#18](https://github.com/WenyuChiou/awesome-agentic-ai-zh/pull/18)) | 2026-05-16 |
| [@JunLin-Bobby](https://github.com/JunLin-Bobby) | **Stage 3 ReAct 練習 bug fix** — `trace.append` 移進 `for tc in tool_calls:` 迴圈內(原本在外層、一步多 tool 只記錄 `tool_calls[0]`)+ 為 question 內的 lookup key 加引號避免 LLM 跨語轉譯失敗(qwen2.5:3b + gemini-3-flash-preview 雙模型交叉驗證)([#26](https://github.com/WenyuChiou/awesome-agentic-ai-zh/pull/26)) | 2026-05-24 |
| [@thebrierfox](https://github.com/thebrierfox) | **§12 Finance hosted-MCP example** — 新增 YIELD INTELLIGENCE MCP (hosted remote server) 到 §12 其他常用、tri-locale。catalog 第一個用 style-guide §1 非 repo entry exemption 的 hosted-service entry (`形式 = hosted MCP server` 取代 Stars/License)、為 Stage 5 學習者示範 hosted vs self-hosted MCP 架構差異 ([#28](https://github.com/WenyuChiou/awesome-agentic-ai-zh/pull/28)) | 2026-05-26 |

---

## 🤖 AI 工具貢獻

這個 repo 有相當部分的繁體中文翻譯、結構審查、license 驗證、跨檔一致性檢查由 AI 工具協助完成：

- **Claude (Anthropic)** — 主要 curation、結構設計、zh-TW 翻譯、跨 phase planning
- **Codex (OpenAI)** — 多輪審查（Phase 2-5 各一次 + cross-phase audit），抓出實質的 license 錯標、overclaim 用語、文件 drift 問題
- **gh API** — 所有 entry 的 stars / license / pushed-at 都用 `gh api` 驗證過，避免幻覺

人工 review 仍是 ground truth——AI 找出**疑似問題**，最終決定（接受、拒絕、改寫）由 maintainer 拍板。

---

## 怎麼上這份名單

1. **Bug report / 連結修正 / 內容更新**：開 issue 或直接 PR
2. **新增 project entry**：照 [`resources/style-guide.md`](resources/style-guide.md) 的 schema 加，[PR template](.github/PULL_REQUEST_TEMPLATE.md) 會引導 checklist
3. **擔任 stage / branch maintainer**：開 issue 自薦，講清楚你願意 commit 多久（建議至少一季）
4. **改善 walkthroughs / scripts / 文件**：直接 PR

每次合併 PR 後，maintainer 會在這份檔案加你的 GitHub handle + 貢獻摘要。

---

## License

本檔案內容遵循 repo 的 MIT license。貢獻即視為同意以 MIT 授權你的內容。
