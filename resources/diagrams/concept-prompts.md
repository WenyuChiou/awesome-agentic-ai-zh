# Stage 7.5 概念圖 — Image 2.0 重產規格（2 圖 × 3 語言）

> 2026-08-28 使用 Codex 內建 Image 2.0 重畫。`NAME.png` 是繁中，
> `NAME.en.png` 是英文，`NAME.zh-Hans.png` 是簡中。正文只保留這兩組圖。

## 共用視覺規格

每次只生成一張圖，使用下列共同要求，再接上對應語言的文字表：

```text
Create a polished educational infographic for a beginner-friendly Agentic AI
learning roadmap. 16:9 landscape, 1672×941, warm white background, deep navy
typography, bright coral/blue/green/purple rounded cards, generous whitespace,
crisp flat vector icons, accessible high contrast, and a friendly modern
technical style. Keep every supplied label large and readable.

Use only the supplied locale text. Do not add vendors, models, dates, rankings,
prices, benchmark numbers, source labels, watermarks, or decorative prose.
Do not mix languages. Do not turn the diagram into a dense matrix or article.
```

生成後必須人工逐字檢查；模型回報成功不等於文字正確。

## 圖 A：12 個概念按問題分四組

檔案：

- `concept-cluster.png`
- `concept-cluster.en.png`
- `concept-cluster.zh-Hans.png`

固定版面：四個等大的問題群組，每組三張概念卡；中央只有一句「每次選 1–2 個」。
不要再使用舊版 `Service／Repo／Config／Types` 軸，因為那是特定 codebase 的架構切片，
不是通用 Agent stack。

### 繁中

```text
Title: 12 個進階 Agentic 概念：先按問題分四組
Group 1: 邊界與契約
  工作邊界 | 契約交接 | 規格驅動
Group 2: 規劃與合作
  平行探索 | 分層拆解 | 動態團隊
Group 3: 檢查與學習
  原則審查 | 計畫・行動・回看 | 故障注入
Group 4: 控制與復原
  自主權階梯 | 預算閘門 | 平穩降級
Callout: 每次只挑 1–2 個
Traditional Chinese only except Agentic.
```

### English

```text
Title: 12 Advanced Agentic Concepts: Start with the Problem
Group 1: Boundaries & Contracts
  Work Boundary | Contract Hand-off | Spec-driven
Group 2: Planning & Collaboration
  Parallel Exploration | Hierarchical Decomposition | Self-organizing Teams
Group 3: Checking & Learning
  Principle-based Review | Plan・Act・Reflect | Failure Injection
Group 4: Control & Recovery
  Autonomy Gradients | Budget Gates | Graceful Degradation
Callout: Pick only 1–2 at a time
English only.
```

### 簡中

```text
Title: 12 个进阶 Agentic 概念：先按问题分四组
Group 1: 边界与契约
  工作边界 | 契约交接 | 规格驱动
Group 2: 规划与合作
  并行探索 | 分层拆解 | 动态团队
Group 3: 检查与学习
  原则审查 | 计划・行动・回看 | 故障注入
Group 4: 控制与恢复
  自主权阶梯 | 预算闸门 | 平稳降级
Callout: 每次只选 1–2 个
Simplified Chinese only except Agentic.
```

## 圖 B：卡在哪裡，就先讀哪一組

檔案：

- `reading-decision-tree.png`
- `reading-decision-tree.en.png`
- `reading-decision-tree.zh-Hans.png`

固定版面：上方一個問題框，下方五條互不交叉的分支。每條分支只保留「症狀 →
先讀哪一組」，不放文章名稱、閱讀時間或供應商。

### 繁中

```text
Title: 卡在哪裡，就先讀哪一組
Question: 你現在卡在哪裡？
1. 改到不該碰的東西 → 邊界與契約
2. 交接後資料不見 → 邊界與契約
3. 一直失敗、一直重試 → 檢查與學習
4. 花太久、花太多 → 控制與復原
5. 工具壞掉就停擺 → 控制與復原
Callout: 先做一個小檢查，再決定要不要加更多 Agent
Traditional Chinese only except Agent.
```

### English

```text
Title: Start with the Group That Matches Your Problem
Question: Where are you stuck?
1. It changed things outside the task → Boundaries & Contracts
2. Data vanished during hand-off → Boundaries & Contracts
3. It keeps failing and retrying → Checking & Learning
4. It takes too long or costs too much → Control & Recovery
5. One broken tool stops everything → Control & Recovery
Callout: Run one small check before adding more agents
English only.
```

### 簡中

```text
Title: 卡在哪里，就先读哪一组
Question: 你现在卡在哪里？
1. 改到不该碰的东西 → 边界与契约
2. 交接后资料不见 → 边界与契约
3. 一直失败、一直重试 → 检查与学习
4. 花太久、花太多 → 控制与恢复
5. 工具坏掉就停摆 → 控制与恢复
Callout: 先做一个小检查，再决定要不要加更多 Agent
Simplified Chinese only except Agent.
```

## 驗收清單

- 三語版面、群組、箭頭與閱讀順序相同，但圖檔 bytes 必須不同。
- 繁中不混簡中；英文不混 CJK；簡中不殘留繁體字。
- 圖 A 恰好 `4 × 3 = 12` 張概念卡，沒有額外分類軸。
- 圖 B 恰好五條分支，沒有文章、時間、版本或 vendor 名稱。
- 正文各語言引用自己的 locale 圖檔。
- 執行 `python scripts/check-image-locale.py` 與
  `python -m pytest scripts/test_stage075_content.py -q`。
