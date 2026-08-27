# 路線圖 / Roadmap

> **繁體中文** | [简体中文](./ROADMAP.zh-Hans.md) | [English](./ROADMAP.en.md)

這份 repo 是**社群維護的學習路線圖**——沒有發行日期、沒有承諾的時程。這份文件公開「我們知道哪裡還不夠好、接下來想往哪走」,讓想貢獻的人能挑一塊上手,而不用先讀完整個 repo 才知道缺什麼。

> 想動其中一項?開個 [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions) 講一聲,或直接 PR。擔任 stage / branch 長期維護者請看 [`CONTRIBUTORS.md`](CONTRIBUTORS.md)。新手切入點看 [`CONTRIBUTING.md`](CONTRIBUTING.md) 的「好上手的 5 個切入點」。

**狀態圖例**:🟢 進行中 / 隨時可貢獻 · 🟡 已知缺口、想做 · 🔵 想法、待討論 · ✅ 近期完成

---

## 近期想補的缺口

### 🟡 動手練習覆蓋補齊
`examples/` 目前涵蓋 Stage 1、2、3、4、5、6、7。**缺**:Stage 0(基礎概念)、Stage 7.5(進階 Agentic 概念)、Stage 8(Agent Interfaces)。也就是只剩 Stage 0、7.5、8 尚未有對應的 hands-on 範例。每個範例要能在 30 分鐘內跑完、附 `怎麼跑` 指令。

### 🟡 audience branch 深化
5 條 audience branch 篇幅(zh-TW canonical,2026-05 snapshot):for-knowledge-worker(143 行,最短)< for-developer(166)< for-everyday-users(179)< for-researcher(208)< for-teacher(224)。**篇幅最短的 `for-knowledge-worker.md` / `for-developer.md` 最需要補情境**。`for-teacher.md` 篇幅其實最長,但 `CONTRIBUTORS.md` 仍把它標「特別歡迎自薦」——它真正薄的是**教師情境的學術引用深度**(目前只有 Chen 2020 / Mittal 2024 兩筆),歡迎補更多 3-tier 教師 AI 應用情境 + 對應引用。

### 🟡 Stage 2 / Stage 3 2026 freshness 小修
幾處 2026 用語 / 模型引用的小幅更新還沒同步到鏡像(約 5 行 diff × 2 locale)。

---

## 進行中 / 隨時可貢獻

- 🟢 **過時 entry 回報** — 跑 `python scripts/refresh-stars.py` 找星數差距大的 repo,開 issue 或 PR 標註 / 移除。
- 🟢 **失效連結修正** — link-rot 每月 CI 會掃,但即時發現的直接 PR 最快。
- 🟢 **`怎麼跑` section 補完** — 很多 entry 缺安裝 / 執行指令,你跑過就補。
- 🟢 **鏡像翻譯順稿** — 對照 `.en.md` / `.zh-Hans.md` 與 zh-TW,改一句翻得不順的。
- 🟢 **stage / branch 長期維護者** — 認領一個 stage 或 branch,有空時 review 一輪。名額表在 `CONTRIBUTORS.md`。

---

## 基礎建設(maintainer 進行中)

- ✅ **社群健康檔** — `CODE_OF_CONDUCT.md` / `SECURITY.md` / `CITATION.cff` / issue-template 導流(本路線圖同批)。
- 🟢 **學習者進度層** — `PROGRESS.md` 自我打勾範本 + 每個 stage 結尾「自我檢核 / Exit check」(規劃中)。
- 🔵 **可瀏覽文件站** — 把 stages/tracks/branches 渲染成有導覽 + 搜尋 + 語言切換的網站(GitHub Pages,評估中)。
- 🟢 **三語鏡像 parity** — `mirror-sync-reminder` + `check-mirror-sync.py` 已在 PR 時把關,持續清 legacy drift。
- 🟢 **品質 gate** — link-rot / star-drift / banned-word / anchor / zh-Hans 在地化 CI 已上線並維護中。

---

## 想法箱(待討論,還沒承諾)

- 🔵 **更多 audience branch**:目前 5 條(researcher / developer / teacher / knowledge-worker / everyday-users),是否要再分(例如 PM / 設計師 / 法務)看社群需求。
- 🔵 **第三條軌道?**:目前 Track A = CLI Power User(`tracks/cli/` 的 A1–A3)、Track B = stages 學習路線(`stages/` 目錄 Stage 0–8,**不是** `tracks/` 下的獨立目錄)。是否要有第三條軌道(例如「只用 no-code agent」)待討論。
- 🔵 **影音 / 互動補充**:純文字學習路線是否要配最小影音 walkthrough,成本與維護負擔待評估。

要提想法請開 [Discussion](https://github.com/WenyuChiou/awesome-agentic-ai-zh/discussions),不要開 issue(issue 留給 bug / 過時 entry / 新增 project)。

---

> 這份路線圖不是契約。它反映「現在」的方向,會隨社群投入而變。最可靠的「接下來要做什麼」永遠是 open issues + Discussions。
