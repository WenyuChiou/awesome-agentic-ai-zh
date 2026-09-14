#!/usr/bin/env bash
# build-mdbook.sh — 把 repo 的 markdown 檔案打包成 mdBook 網站
#
# 用法：
#   bash scripts/build-mdbook.sh                   # 建到 book/dist/
#   bash scripts/build-mdbook.sh --serve           # 建好後本機開 server
#
# 依賴：
#   - mdBook (cargo install mdbook)
#
# Windows 安裝：
#   - 裝 Rust: https://rustup.rs
#   - cargo install mdbook
#
# Note: mdbook-mermaid preprocessor 已移除（repo 內已無 ```mermaid``` 區塊）。

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SRC_DIR="book/src"
SERVE_FLAG=""
[[ "${1:-}" == "--serve" ]] && SERVE_FLAG="serve"

echo "Preparing $SRC_DIR ..."
rm -rf "$SRC_DIR"
mkdir -p "$SRC_DIR/stages" "$SRC_DIR/branches" "$SRC_DIR/walkthroughs" "$SRC_DIR/resources"

# 複製 zh 版本的 markdown 檔案到 book/src/
cp README.md "$SRC_DIR/README.md"
cp CONTRIBUTING.md "$SRC_DIR/CONTRIBUTING.md"
cp stages/*.md "$SRC_DIR/stages/" 2>/dev/null || true
cp branches/*.md "$SRC_DIR/branches/" 2>/dev/null || true
cp walkthroughs/*.md "$SRC_DIR/walkthroughs/" 2>/dev/null || true
cp resources/*.md "$SRC_DIR/resources/" 2>/dev/null || true

# 移除 .en.md（mdBook 只渲染主語版本）
find "$SRC_DIR" -name "*.en.md" -delete

# 產生 SUMMARY.md
cat > "$SRC_DIR/SUMMARY.md" <<'EOF'
# Summary

[awesome-agentic-ai-zh](README.md)

# 主路線

- [Stage 0 — 基礎準備](stages/00-foundations.md)
- [Stage 1 — LLM 入門](stages/01-llm-basics.md)
- [Stage 2 — Prompt 設計](stages/02-prompt-engineering.md)
- [Stage 3 — 工具使用與第一個 Agent Loop](stages/03-tool-use-and-hello-agent.md)
- [Stage 4 — Workflow Graph 與 Agent 框架](stages/04-agent-frameworks.md)
- [Stage 5 — Claude Code 生態](stages/05-claude-code-ecosystem.md)
- [Stage 6 — Memory · RAG · 進階](stages/06-memory-rag.md)
- [Stage 7 — Agent 上線工程：可測、可看、可停、可恢復](stages/07-multi-agent-production.md)

# 跨 Stage 範例

- [7 步打造你的第一個 AI Agent](walkthroughs/build-first-agent-in-7-steps.md)

# 進階分支

- [研究人員](branches/for-researcher.md)
- [開發者](branches/for-developer.md)
- [知識工作者](branches/for-knowledge-worker.md)
- [教師](branches/for-teacher.md)

# 規範

- [風格指南](resources/style-guide.md)
- [貢獻指南](CONTRIBUTING.md)
EOF

echo "Generated $SRC_DIR/SUMMARY.md"

# 確認 mdbook 有裝
if ! command -v mdbook &> /dev/null; then
  echo "❌ mdbook 沒裝。請先：cargo install mdbook" >&2
  exit 1
fi

echo ""
if [[ -n "$SERVE_FLAG" ]]; then
  mdbook serve --open
else
  mdbook build
  echo ""
  echo "✅ Built book/dist/  (open book/dist/index.html in browser)"
fi
