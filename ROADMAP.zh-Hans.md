# 路线图 / Roadmap

> [繁體中文](./ROADMAP.md) | **简体中文** | [English](./ROADMAP.en.md)

这份 repo 是**社区维护的学习路线图**——没有发布日期、没有承诺的时间表。这份文件公开“我们知道哪里还不够好、接下来想往哪里走”，让想贡献的人能挑一块上手，而不用先读完整个 repo 才知道缺什么。

> 想动其中一项？开个 [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions) 说一声，或直接 PR。担任 stage / branch 长期维护者请看 [`CONTRIBUTORS.md`](CONTRIBUTORS.md)。新手切入点看 [`CONTRIBUTING.zh-Hans.md`](CONTRIBUTING.zh-Hans.md) 的“好上手的 5 个切入点”。

**状态图例**：🟢 进行中 / 随时可贡献 · 🟡 已知缺口、想做 · 🔵 想法、待讨论 · ✅ 近期完成

---

## 近期想补的缺口

### 🟡 动手练习覆盖补齐
`examples/` 目前覆盖 Stage 1、2、3、4、5、6、7。**缺**：Stage 0（基础概念）、Stage 7.5（进阶 Agentic 概念）和 Stage 8（Agent Interfaces）。也就是说，只剩 Stage 0、7.5 和 8 尚未有对应的 hands-on 示例。每个示例要能在 30 分钟内跑完，并附 `怎么跑` 命令。

### 🟡 audience branch 深化
5 条 audience branch 篇幅（zh-TW canonical, 2026-05 snapshot）：for-knowledge-worker（143 行，最短）< for-developer（166）< for-everyday-users（179）< for-researcher（208）< for-teacher（224）。**篇幅最短的 `for-knowledge-worker.md` / `for-developer.md` 最需要补情境**。`for-teacher.md` 篇幅其实最长，但 `CONTRIBUTORS.md` 仍把它标为“特别欢迎自荐”——它真正薄的是**教师情境的学术引用深度**（目前只有 Chen 2020 / Mittal 2024 两笔），欢迎补更多 3-tier 教师 AI 应用情境 + 对应引用。

### 🟡 Stage 2 / Stage 3 2026 freshness 小修
几处 2026 用语 / 模型引用的小幅更新还没同步到镜像（约 5 行 diff × 2 locale）。

---

## 进行中 / 随时可贡献

- 🟢 **过时 entry 反馈** — 跑 `python scripts/refresh-stars.py` 找星数差距大的 repo，开 issue 或 PR 标注 / 移除。
- 🟢 **失效链接修正** — link-rot 每月 CI 会扫，但即时发现的直接 PR 最快。
- 🟢 **`怎么跑` section 补完** — 很多 entry 缺安装 / 执行命令，你跑过就补。
- 🟢 **镜像翻译顺稿** — 对照 `.en.md` / `.zh-Hans.md` 与 zh-TW，改一句翻得不顺的。
- 🟢 **stage / branch 长期维护者** — 认领一个 stage 或 branch，有空时 review 一轮。名额表在 `CONTRIBUTORS.md`。

---

## 基础建设（maintainer 进行中）

- ✅ **社区健康文件** — `CODE_OF_CONDUCT.md` / `SECURITY.md` / `CITATION.cff` / issue-template 导流（本路线图同批）。
- 🟢 **学习者进度层** — `PROGRESS.md` 自我打勾模板 + 每个 stage 结尾“自我检查 / Exit check”（规划中）。
- 🔵 **可浏览文件站** — 把 stages/tracks/branches 渲染成有导航 + 搜索 + 语言切换的网站（GitHub Pages，评估中）。
- 🟢 **三语镜像 parity** — `mirror-sync-reminder` + `check-mirror-sync.py` 已在 PR 时把关，持续清 legacy drift。
- 🟢 **质量 gate** — link-rot / star-drift / banned-word / anchor / zh-Hans 本地化 CI 已上线并维护中。

---

## 想法箱（待讨论，还没承诺）

- 🔵 **更多 audience branch**：目前 5 条（researcher / developer / teacher / knowledge-worker / everyday-users），是否要再分（例如 PM / 设计师 / 法务）看社区需求。
- 🔵 **第三条轨道？**：目前 Track A = CLI Power User（`tracks/cli/` 的 A1–A3）、Track B = stages 学习路线（`stages/` 目录 Stage 0–8，**不是** `tracks/` 下的独立目录）。是否要有第三条轨道（例如“只用 no-code agent”）待讨论。
- 🔵 **视频 / 互动补充**：纯文字学习路线是否要配最小视频 walkthrough，成本与维护负担待评估。

要提想法请开 [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions)，不要开 issue（issue 留给 bug / 过时 entry / 新增项目）。

---

> 这份路线图不是契约。它反映“现在”的方向，会随社区投入而变。最可靠的“接下来要做什么”永远是 open issues + Discussions。
