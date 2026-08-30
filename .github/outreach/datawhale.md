# Outreach: Datawhale (datawhalechina)

> ⚠️ **Send content is now canonical in [`_send-day-packages.md`](_send-day-packages.md)** (package E — 10 learning stops / curated resources). This file is kept for positioning rationale; do not paste its older issue/stats blocks directly.

> **Status**: not contacted · **Channel**: GitHub issue + (later) WeChat group
> **Primary lang**: zh-Hans
> **Last updated**: 2026-05-09
> **Decision-maker**: Datawhale 開源教學團隊 (open-source curriculum team)

**Why this target**: Datawhale 是中文 AI 教學社群；他們的 [`hello-agents`](https://github.com/datawhalechina/hello-agents) 是 Agent 入門專案。我們的 Stage 5 cookbook 已經 cite 他們的 Extra05 / Extra08——cross-link 對雙方都加分。

**Pitch angle (我們對他們)**: 我們的 Stage 0 → Stage 8 三語學習地圖把 Hello-Agents 接在 Stage 5 / 6 的延伸資源——先學 LLM、prompt、tools 與 framework 基礎，再進 Hello-Agents 會比較容易吸收。我們等於是他們的「pre-flight」入口。

**Their counter-value (他們對我們)**: 如果他們在 Hello-Agents README / docs 提一句「想看完整學習路線可以參考……」，讀者就能從專案教學回到循序路線。

---

## Variant 1 — Social post (Weibo / Threads / X，~280 字)

> 「想用 Hello-Agents 但不確定該從哪裡入手？」
>
> awesome-agentic-ai-zh 把 agentic AI 排成 10 個學習站（8 個主題 Stage + Stage 0 準備關 + Stage 7.5 閱讀站；最後到 Stage 8 Agent Interfaces）。Stage 5/6 直接接到 @datawhalechina 的 Hello-Agents Extra05/08。
>
> 三語（zh-TW / zh-Hans / en）· 分組整理的 curated projects · MIT
> 👉 https://github.com/WenyuChiou/awesome-agentic-ai-zh

## Variant 2 — GitHub issue (200-300 字)

**Title**: Cross-link suggestion: structured learning path that points readers to Hello-Agents

```
Hi Datawhale 團隊！

我在維護 [awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh)
——一份中文 agentic AI 的 Stage 0 → Stage 8 三語學習地圖（zh-TW canonical / zh-Hans / en，
分組整理 curated projects，採用 MIT）。

我們的 Stage 5 cookbook 已經把 Hello-Agents 的 Extra05（記憶 + RAG 概覽）跟 Extra08
（多代理）放進 reading list（[cookbook.md](https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/resources/cookbook.md)），
作為走完前 4 階段 LLM 基礎之後的延伸閱讀。

**想 propose 一個雙向 cross-link**：

1. 我們這邊已經 link 你們了（無條件，已經 ship）
2. 如果你們覺得合適——能不能在 Hello-Agents 的 README 或 docs 裡加一句「想看更
   完整的 agentic AI 學習路線，可以參考 awesome-agentic-ai-zh」？
3. 或是 reverse PR：我們在 §11 中文圈專用 加 Hello-Agents 的正式 entry（你們
   review）？

我們這邊的讀者主要從 Stage 4 之後想進 framework 跟 multi-agent，Hello-Agents
正好是下一階段最強的中文教材。如果不合適也完全 OK，謝謝你們把 Hello-Agents
做出來——它本身就是中文社群的公共財。

— Wenyu (PhD candidate · Lehigh CEE，個人 maintainer)
```

## Variant 3 — Email / WeChat DM (150 字)

```
Hi Datawhale 團隊好，

我是 awesome-agentic-ai-zh 的維護者 Wenyu。這份 repo 是中文 agentic AI 的 Stage 0 → Stage 8
三語學習地圖（分組整理的 projects，三語齊全）。

我們 Stage 5 cookbook 已經把 Hello-Agents 的 Extra05/08 放進延伸閱讀清單。想跟你們
聊聊有沒有可能 reciprocal cross-link 的可能——細節在我剛開的 [GitHub issue]
（連結）。

謝謝你們把 Hello-Agents 做出來，這幾年中文 agentic AI 學習的公共財都是你們扛的，
真的很感激。

— Wenyu
```

---

## Notes

- **不要 promise**「我們會幫你們宣傳」之類的——只 offer 已經 ship 的 cross-link
- 如果他們同意 reverse PR 加 Hello-Agents 到 §11，先重查連結、授權與目前章節位置
- WeChat 是 Datawhale 主要互動 channel，但 GitHub issue 比較 maintainable + 可追蹤
- 如果一週沒回——OK，他們團隊很忙、不要 ping
