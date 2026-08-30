# Outreach: Moonshot Kimi 開發者頻道

> **Status**: not contacted · **Channel**: 開發者社群（Discord / 知乎 / GitHub）
> **Primary lang**: zh-Hans
> **Last updated**: 2026-05-09
> **Their main surface**: https://kimi.moonshot.cn · https://github.com/MoonshotAI

**Why this target**: 月之暗面 (Moonshot) 是大陸 frontier AI lab 之一（Kimi K2 / Kimi-Chat）。我們 §11 中文圈專用 沒有 Moonshot entry——他們的開源主要是 model paper / weights，沒有 agent SDK 形態的 canonical repo。

**Pitch angle (邀請式)**: 跟 Zhipu 同邏輯——§11 缺 Moonshot 的 agent / Skills 入口；邀請他們社群推薦合適的 PR。

**Their counter-value**: Kimi 開發者透過我們學整個 agentic 生態；他們在 zh community 的 visibility 提升。

---

## Variant 1 — Social post (Weibo / X，~280 字)

```
中文 agentic AI 學習地圖 awesome-agentic-ai-zh，§11 中文圈專用 收了 Qwen-Agent +
Coze——缺 Moonshot 的 entry。

如果月之暗面的同學 / 熱心開發者覺得有 Kimi 系列的 agent skill / SDK / cookbook
該收進來，歡迎 PR：github.com/WenyuChiou/awesome-agentic-ai-zh

分組整理的 projects · 三語齊全 · MIT
```

## Variant 2 — Discussion / 知乎文章 (200-300 字)

**Title**: 邀請：月之暗面 Kimi agent 生態，有合適的開源項目可以收進 awesome-agentic-ai-zh §11 嗎？

**Body**:

```markdown
你好 Moonshot 社群，

我维护 [awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh)
——一份中文 agentic AI 的 10 站三语学习地图（8 个主题 Stage + Stage 0 准备关 + Stage 7.5 阅读站；zh-TW canonical / zh-Hans / en，分组整理的
projects，MIT）。

**§11 中文圈专用** 已经收了 Qwen-Agent / Coze / Langchain-Chatchat 等，但缺
Moonshot Kimi 的 entry。我评估过的几个候选：

- `MoonshotAI/Kimi-K2`：模型 paper / weights repo，不是 agent SDK 形态
- 没看到官方的 `kimi-agent-sdk` / `kimi-skills` / `kimi-cookbook` canonical 仓库

想问问 Moonshot 社群：
1. 有没有官方或半官方的 Kimi agent / Skills / cookbook 仓库可以推荐？
2. 如果有，欢迎 PR 到 §11。收录原则：
   - agent / Skill / SDK / MCP-shaped（不只是模型 API）
   - license 清楚
   - 最近 90 天有 commit
   - 品质优于流行度（star 数不是门槛）

社群的 chat-bot / agent 二次开发也算——只要是 Kimi 周边的合适学习资源都可以。

如果一时没合适项目，也 OK，先留个 thread 追踪 agent 生态成熟度。

— Wenyu (Lehigh CEE PhD candidate，个人 maintainer)
```

## Variant 3 — DM / 邮件 (150 字)

```
你好 Moonshot 社群，

我是 awesome-agentic-ai-zh 的维护者 Wenyu。这份是中文 agentic AI 的 10 站三语
学习地图（分组整理的 projects，三语齐全，MIT）。

§11 中文圈专用 收了 Qwen-Agent + Coze，缺 Kimi 的 entry。如果有官方推荐的 Kimi
agent / Skills / cookbook 仓库我应该收进来，请告诉我；或者直接 PR 到 §11。收录
原则：agent-shaped + license 清楚 + 90 天内活跃。

谢谢！
— Wenyu
```

---

## Notes

- **同 Zhipu 邏輯**：邀請式而非推銷式
- Moonshot 的開源相對少（主要是 paper + weights），如果真的沒合適 repo，**不
  要硬 fit**——可以先放著，等他們釋出 agent SDK 再收

- Moonshot 開發者社群入口：Discord / 知乎 / 飛書群（Kimi 開發者群）
- 不要與 Zhipu outreach 同日發送——避免「同一個人到處撒網」感
- 監測：如果 Moonshot 後續釋出 `MoonshotAI/Kimi-Agent` 或類似——優先收進 §11
