#!/usr/bin/env python3
"""Combine link, repository, and freshness evidence into one tracking report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def summarize(link: dict, repo: dict, *, freshness_exit: int,
              freshness_ran: bool, mode: str) -> dict:
    repo_errors = sum(item.get("severity") == "error" for item in repo.get("findings", []))
    repo_warnings = sum(item.get("severity") == "warning" for item in repo.get("findings", []))
    repo_unverified = sum(row.get("state") == "unverified" for row in repo.get("records", {}).values())
    freshness_is_hard = bool(mode == "release" and freshness_ran and freshness_exit)
    hard = int(link.get("failed", 0)) + repo_errors + (1 if freshness_is_hard else 0)
    unverified = int(link.get("unverified", 0)) + repo_unverified
    review = (unverified or int(link.get("new_unverified", 0)) or repo_warnings
              or bool(freshness_ran and freshness_exit))
    return {
        "mode": mode,
        "state": "hard-failure" if hard else ("review" if review else "healthy"),
        "hard_failures": hard,
        "unverified": unverified,
        "new_unverified": int(link.get("new_unverified", 0)),
        "repository_warnings": repo_warnings,
        "freshness_ran": freshness_ran,
        "freshness_failed": bool(freshness_ran and freshness_exit),
    }


def render(payload: dict) -> str:
    state = {
        "healthy": "✅ 沒有需要處理的新問題",
        "review": "⚠️ 有資料無法由機器確認",
        "hard-failure": "❌ 發現明確問題",
    }[payload["state"]]
    freshness = "已執行" if payload["freshness_ran"] else "本週不執行（每月或 Release 前執行）"
    return "\n".join([
        "# Content health report", "",
        f"- 狀態：**{state}**",
        f"- 模式：`{payload['mode']}`",
        f"- 明確錯誤：**{payload['hard_failures']}**",
        f"- 無法驗證：**{payload['unverified']}**（其中新出現 {payload['new_unverified']}）",
        f"- Repository 警告：**{payload['repository_warnings']}**",
        f"- 模型／產品 freshness：**{freshness}**",
        "",
        "完整明細在同一次 run 的 JSON／Markdown artifacts。Timeout、403、429 只會列為無法驗證，不會冒充 404。",
        "",
        "> 自動化只整理證據，不會自動改寫教材、送出 Approve 或合併 PR。最終判斷仍由 Maintainer 完成。",
    ]) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--link-json", type=Path, required=True)
    parser.add_argument("--repo-json", type=Path, required=True)
    parser.add_argument("--freshness-exit", type=int, required=True)
    parser.add_argument("--freshness-ran", choices=("true", "false"), required=True)
    parser.add_argument("--mode", choices=("weekly", "monthly", "release"), required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args()
    link = json.loads(args.link_json.read_text(encoding="utf-8"))
    repo = json.loads(args.repo_json.read_text(encoding="utf-8"))
    payload = summarize(
        link, repo,
        freshness_exit=args.freshness_exit,
        freshness_ran=args.freshness_ran == "true",
        mode=args.mode,
    )
    args.markdown.write_text(render(payload), encoding="utf-8")
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"state={payload['state']}")
    return 1 if payload["state"] == "hard-failure" else 0


if __name__ == "__main__":
    raise SystemExit(main())
