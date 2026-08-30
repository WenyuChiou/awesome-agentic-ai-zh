# Outreach: Zhipu BigModel community (智譜)

> **Status**: not contacted · **Channel**: 開發者社群（Discord / 知乎 / GitHub Discussions）
> **Primary lang**: zh-Hans
> **Last updated**: 2026-05-09
> **Their main surface**: https://bigmodel.cn / https://github.com/MetaGLM

**Why this target**: 智譜 (Zhipu) 是大陸頭部 AI lab 之一（GLM 系列模型）。我們的 §11 中文圈專用目前**沒有 Zhipu 的條目**——主要是因為他們官方的 agent SDK 沒有一個 active + Apache-licensed 的 canonical repo。

**Pitch angle (邀請式，不是推銷式)**: 我們是中文 agentic AI 的 10 站學習地圖（8 個主題 Stage + Stage 0 準備關 + Stage 7.5 閱讀站）；§11 已經收了 Qwen-Agent + Coze，缺 Zhipu。**邀請他們 PR 一個官方推薦的 Zhipu agent 教材 / SDK / cookbook**——他們在我們 catalog 站 §11 的位置，他們的開發者透過我們學 Zhipu 之外的整個 agentic 生態。

**Their counter-value**: 中文圈的 entrant developers 有結構化路線可學；GLM/AutoGLM 的曝光。

---

## Variant 1 — Social post (Weibo / 知乎 / X，~280 字)

```
中文 agentic AI 學習地圖 awesome-agentic-ai-zh，§11 中文圈專用 已經收 @QwenLM 跟
@coze-dev——缺 @zhipuai 的 entry。

如果智譜的同學 / 熱心開發者覺得有官方推薦的 GLM agent cookbook / SDK 該收進來，
歡迎 PR：github.com/WenyuChiou/awesome-agentic-ai-zh

分組整理的 projects · 三語齊全 · MIT
```

## Variant 2 — Discussion / 知乎文章 (200-300 字)

**Title**: 邀請：智譜 GLM agent 生態的官方 / 社群推薦項目，可以收進 awesome-agentic-ai-zh §11 嗎？

**Body**:

```markdown
你好智譜社群，

我维护 [awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh)
——一份中文 agentic AI 的 10 站三语学习地图（8 个主题 Stage + Stage 0 准备关 + Stage 7.5 阅读站；zh-TW canonical / zh-Hans / en，分组整理的
projects，MIT）。

**§11 中文圈专用** 已经收了：
- QwenLM/Qwen-Agent（阿里巴巴）
- coze-dev/coze-studio + coze-loop（字节跳动）
- chatchat-space/Langchain-Chatchat
- liaokongVFX/LangChain-Chinese-Getting-Started-Guide

**目前缺智谱 GLM 生态的 entry**——之前评估过 MetaGLM/glm-cookbook 但 246 天没更新，
不太符合 catalog 的「活跃维护」收录原则。

想问问智谱社群：
1. 有没有官方维护的 GLM agent SDK / cookbook / Skills 仓库可以推荐？
2. 如果有合适的项目，欢迎大家直接 PR 到 §11。我们的收录原则在
   [resources/style-guide.md](https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/resources/style-guide.md)
3. 评估标准：MCP / Skills / agent-shaped、license 清楚（避免无 license）、最近 90
   天有 commit、品质优于流行度（star 数不是门槛）

如果一时没合适项目也 OK——agent 生态发展很快，先开个 thread 留言追踪。

— Wenyu (Lehigh CEE PhD candidate，个人 maintainer)
```

## Variant 3 — DM / 邮件 (150 字)

```
你好智谱社群，

我是 awesome-agentic-ai-zh 的维护者 Wenyu。这份是中文 agentic AI 的 10 站三语
学习地图（分组整理的 projects，三语齐全，MIT）。

§11 中文圈专用 已经收阿里 Qwen-Agent + 字节 Coze，缺智谱的 entry。如果有官方推荐
的 GLM agent SDK / cookbook 我应该收进来，请告诉我；或者直接 PR 到 §11。收录原则
在 resources/style-guide.md（agent-shaped + license 清楚 + 最近活跃）。

谢谢！
— Wenyu
```

---

## Notes

- **Tone**: 邀請式（"Want to be listed? Send PR"），不是 sales（"買我們服務"）
- 不放 stars、forks 或流量快照；它們會漂移，也不能證明教學品質
- 如果 Zhipu 沒有合適 repo，**不要硬 fit**——保留 §11 的品質
- 如果有合適 PR 進來，注意 license 跟維護節奏（避免 archived / 246d-stale 的 MetaGLM/glm-cookbook 重蹈覆轍）
- Zhipu 中國大陸主要使用 知乎 + 微信 + 釘釘，GitHub Issues 是次要 channel
