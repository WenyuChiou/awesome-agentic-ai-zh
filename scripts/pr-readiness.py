#!/usr/bin/env python3
"""Create a factual PR preflight summary; a maintainer still makes the decision."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LOCALE_SUFFIXES = (".en.md", ".zh-Hans.md")
PUBLIC_LOCALE_ROOTS = {
    "branches",
    "examples",
    "resources",
    "stages",
    "tracks",
    "walkthroughs",
}
PUBLIC_SINGLE_LOCALE_ALLOWLIST = {
    "branches/DESIGN.md",
    "examples/stage-5/tool-calling-tutor/SKILL.md",
    "resources/diagrams/concept-prompts.md",
    "resources/diagrams/locale-variant-prompts.md",
    "stages/DESIGN.md",
}
STATUS_ZH = {
    "passed": "通過",
    "failed": "失敗",
    "unverified": "未驗證",
    "skipped": "未驗證",
    "success": "通過",
    "failure": "失敗",
    "cancelled": "失敗",
}


def git_diff(base: str, head: str) -> str:
    result = subprocess.run(
        ["git", "diff", "--find-renames", "--find-copies", "--unified=0", f"{base}...{head}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=90,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git diff failed")
    return result.stdout


def changed_paths(diff_text: str) -> set[str]:
    paths: set[str] = set()
    for line in diff_text.splitlines():
        match = re.match(r"diff --git a/(.+) b/(.+)$", line)
        if match:
            paths.add(match.group(2))
    return paths


def _family(path: str) -> tuple[str, tuple[str, str, str]]:
    if path.endswith(".zh-Hans.md"):
        canonical = path.removesuffix(".zh-Hans.md") + ".md"
    elif path.endswith(".en.md"):
        canonical = path.removesuffix(".en.md") + ".md"
    else:
        canonical = path
    stem = canonical.removesuffix(".md")
    return canonical, (canonical, stem + ".en.md", stem + ".zh-Hans.md")


def locale_coverage(root: Path, changed: set[str]) -> dict:
    missing: set[str] = set()
    families: list[str] = []
    checked: set[str] = set()
    for path in sorted(p for p in changed if p.endswith(".md")):
        canonical, members = _family(path)
        if canonical in checked:
            continue
        checked.add(canonical)
        family_paths = set(members)
        present_or_changed = {
            member for member in members
            if (root / member).exists() or member in changed
        }
        is_public = canonical.split("/", 1)[0] in PUBLIC_LOCALE_ROOTS
        requires_full_family = (
            is_public
            and canonical not in PUBLIC_SINGLE_LOCALE_ALLOWLIST
        )
        if not requires_full_family and len(present_or_changed) < 2:
            continue
        families.append(canonical)
        required = family_paths if requires_full_family else present_or_changed
        missing.update(member for member in required if member not in changed)
    return {
        "state": "complete" if not missing else "incomplete",
        "missing": sorted(missing),
        "families": families,
    }


def risk_flags(paths: set[str], diff_text: str) -> list[str]:
    lower_paths = [p.lower() for p in paths]
    added = "\n".join(line[1:].lower() for line in diff_text.splitlines()
                       if line.startswith("+") and not line.startswith("+++"))
    flags = ["general-content"]
    if any(token in added for token in (
        "price", "pricing", "價格", "价格", "model id", "context window",
        "availability", "available", "license", "授權", "授权", "preview",
        "deprecated", "legacy", "release date",
    )) or any("freshness" in p for p in lower_paths):
        flags.append("volatile-information")
    if any(p.startswith("examples/") or p.endswith((".py", ".js", ".ts", ".sh", ".ps1"))
           for p in lower_paths):
        flags.append("executable-example")
    if any(p.startswith(".github/workflows/") or any(t in p for t in
           ("security", "permission", "auth", "dependabot")) for p in lower_paths):
        flags.append("security-or-actions")
    if any(p.startswith(".github/workflows/") or "release" in p for p in lower_paths):
        flags.append("actions-or-release")
    if any(p.endswith((".png", ".jpg", ".jpeg", ".webp", ".css")) for p in lower_paths):
        flags.append("visual-or-layout")
    return flags


def _status(value: str) -> str:
    return STATUS_ZH.get(value.lower(), "未驗證")


def render_markdown(payload: dict) -> str:
    coverage = payload["locale_coverage"]
    locale_text = "完整" if coverage["state"] == "complete" else (
        "缺少：" + "、".join(f"`{p}`" for p in coverage["missing"])
    )
    risk_labels = {
        "general-content": "一般內容",
        "volatile-information": "易變資訊",
        "executable-example": "可執行範例",
        "security-or-actions": "安全／Actions",
        "actions-or-release": "Actions／Release",
        "visual-or-layout": "圖片／版面",
    }
    lines = [
        "<!-- pr-readiness-summary -->",
        "## PR 初步檢查",
        "",
        f"- 機器關卡：**{_status(payload['machine_gate'])}**",
        f"- 依賴審查：**{_status(payload['dependency_review'])}**",
        f"- 三語覆蓋：**{locale_text}**",
        "- 風險：" + "、".join(risk_labels.get(r, r) for r in payload["risks"]),
        f"- 變更檔案：**{len(payload['changed_files'])}**",
        "",
        "### 人工仍要確認",
        "",
        "- 易變事實是否仍與官方來源一致。",
        "- 三語是否真的在說同一件事，不只標題與段落數相同。",
        "- 圖片是否清楚、無重疊，且手機上仍看得懂。",
        "- 初學者主線是否簡單；必讀、核心詞、精選資源與完成條件是否保持展開。",
        "",
        "> **最終評定：等待 Maintainer**",
        "",
        "<sub>這是機器整理的證據，不是 Approve，也不會自動合併。</sub>",
    ]
    return "\n".join(lines) + "\n"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--diff-file", type=Path)
    parser.add_argument("--machine-gate", default="unverified")
    parser.add_argument("--dependency-review", default="unverified")
    parser.add_argument("--markdown", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args()

    diff_text = args.diff_file.read_text(encoding="utf-8") if args.diff_file else git_diff(args.base, args.head)
    paths = changed_paths(diff_text)
    payload = {
        "machine_gate": args.machine_gate,
        "dependency_review": args.dependency_review,
        "locale_coverage": locale_coverage(ROOT, paths),
        "risks": risk_flags(paths, diff_text),
        "changed_files": sorted(paths),
    }
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text(render_markdown(payload), encoding="utf-8")
    write_json(args.json, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
