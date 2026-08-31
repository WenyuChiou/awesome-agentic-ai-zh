# Launch checklist

> 這份是 maintainer 內部用的——repo 從 Phase 5 ship 到開始**主動推廣**前要走完的一次性步驟。

---

## ✅ Pre-launch（已完成）

- [x] Phase 1-5 內容 ship（134 entries、style guide、walkthrough、Mermaid 圖）
- [x] `.github/` issue + PR template
- [x] `resources/style-guide.md` zh + en
- [x] `scripts/check-links.py` + `refresh-stars.py` 可跑
- [x] CI lint workflow（zh-Hans slip + overclaim 自動檢查；每月跑 link-rot + star-drift）

## 🟡 Pre-launch（一次性手動 setup）

- [x] **GitHub Pages**：Source 已使用 **GitHub Actions**；`.github/workflows/docs.yml` 推 main 會 build mkdocs（`/`）+ mdBook（`/book/`），由單一 workflow 部署到 `https://wenyuchiou.github.io/awesome-agentic-ai-zh/`
- [ ] **GitHub Discussions**：repo Settings → Features → enable Discussions
  - Categories 建議：
    - 🙋 Q&A — 學習問題
    - 💡 Project nominations — 推薦新 project（先討論再 PR）
    - 📚 Stage discussion — 每個 stage 一個 thread
    - 🎯 Show & tell — 走完 stage 的人 share 自己的成果
- [x] **`release` Environment**：已建立並要求 `WenyuChiou` 人工批准；workflow 也會在缺少 required reviewer 時 fail closed
- [ ] **第一次三語 PDF Release**：從 Actions 手動啟動 `Trilingual Release`，下載 candidate artifact，確認繁中／簡中／英文三份 PDF 後才批准 `release` Environment
- [ ] **Calendar Release**：使用 `vYYYY.MM.DD`（同日第二版加 `-2`）；一個 Release 同時放三語 notes 與三份固定命名 PDF

## 🟢 Soft launch（小範圍宣傳）

- [ ] 跟 `WenyuChiou` 朋友圈分享（內測）
- [ ] 修 1-2 輪內測回饋（issue 處理）

## 🚀 Public launch（推廣）

### 提交到中文社群 awesome list

- [ ] [`AiHubCN/Awesome-Chinese-LLM`](https://github.com/AiHubCN/Awesome-Chinese-LLM) — 開 PR 加進 catalog（教學資源 / 學習路線 section）
- [ ] [`WangRongsheng/awesome-LLM-resources`](https://github.com/WangRongsheng/awesome-LLM-resources) — 開 PR
- [ ] [`hesreallyhim/awesome-claude-code`](https://github.com/hesreallyhim/awesome-claude-code) — 開 PR（learning resources）
- [ ] [`travisvn/awesome-claude-skills`](https://github.com/travisvn/awesome-claude-skills) — 開 PR（learning resources）

> 📡 **Channel partner outreach**：完整 outreach 計畫（8 個目標 × 3 種 pitch 變體 + 1-2 sends/day pacing）跟追蹤 matrix 在 [`.github/channel-partners.md`](channel-partners.md)。各 target 的 pitch 草稿在 [`.github/outreach/<slug>.md`](outreach/)。

### 寫 launch 文章

- [ ] **Threads 短版**（2-3 則）— 重點：134 個 project、跨 stage walkthrough、誠實時程
- [ ] **dev.to 長版**（一篇 1000-1500 字）— 寫「為什麼平鋪 awesome 不夠用、結構化路線怎麼做」
- [ ] （選）**個人部落格** — 同樣內容深度版

### 中文 LLM 社群

- [ ] Datawhale 微信社群（如果有 zh-TW 受眾）
- [ ] Hacker News（zh-TW 故事性夠強的話）
- [ ] r/LocalLLaMA、r/MachineLearning（看 reddit 接受度）

## 🔁 Post-launch（持續）

這份是**參考節奏，不是 SLA**——能做就做、忙起來放著也沒關係。社群開放型 repo 不需要強制定期維護。

- 有空時：review issue / 合併 PR
- 偶爾跑：CI 已設定每月自動跑 link rot + star drift（被動的、不用人工）
- 想做的時候：加幾個新 entry、清掉幾個 archived repo
- 不必排定期程：phase milestone、新增 branch 等大改——有 traction 訊號再做

---

## 📊 成功指標（不是目標、是訊號）

排序大致按 fingerprint 強度——前面比後面更可靠。

1. **每月新 issue / PR 數量**（活躍社群訊號）
2. **stage maintainer 自薦數**（深度 engagement）
3. **被引用 / 被收錄到其他 awesome list 數**
4. **Star 數**（弱訊號，容易被刷；只看趨勢、不看絕對值）

---

## 不該做的（deliberate "no"s）

- ❌ 為了上熱門就刷 SEO 關鍵字
- ❌ 為了 star 數加 low-quality entry
- ❌ 把 PR 合進 main 而不 review（即使是 typo 也要 review）
- ❌ 自家 repo 重新加回 catalog（先前刻意移除）
- ❌ 接 sponsor / affiliate link（會影響推薦獨立性）
