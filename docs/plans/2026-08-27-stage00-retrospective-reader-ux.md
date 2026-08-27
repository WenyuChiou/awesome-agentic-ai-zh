# Stage 00 Retrospective Reader-UX Plan

> **Release rule:** This is a stacked, reviewable layer above PR #142. Open the PR and keep its branch and worktree. Do not merge, delete branches, remove worktrees, or prune until the user explicitly says `可以合併`.

## Goal

Restore the learning-resource ratings that were lost during the Stage 00 rewrite, replace three weaker or stale entry points with current primary sources, and keep the beginner page simple enough to scan without opening any menu.

This pass does not shorten away concepts, change the main exercise, or rewrite another stage.

## Stack boundary

- Base branch: `codex/stage02-shot-terms` (PR #142)
- Head branch: `codex/stage00-retro-ux`
- Canonical page first: `stages/00-foundations.md`
- Mirrors after the canonical page is stable:
  - `stages/00-foundations.en.md`
  - `stages/00-foundations.zh-Hans.md`
- Expected support files:
  - `scripts/reader-ux-pages.yml`
  - `scripts/check-reader-ux.py`
  - `scripts/test_reader_ux.py`
  - `scripts/repository-freshness-snapshot.json`
  - `CHANGELOG.md`
  - this plan

If the final file list changes, freeze the new list before staging and explain why in the CHANGELOG and PR.

## Reader contract to preserve

- Keep the visible `何時可以跳過這個階段` decision and its existing anchor.
- Keep the `📌`, `🛠`, `🎯`, and `✅` navigation icons. Stage 00 may use `📚` in the closed resource summary instead of adding a separate required-reading section.
- Keep the main GitHub API exercise fully copy/paste/run ready.
- Keep secondary setup, terminology, authentication, and all 18 resources inside closed `<details>` blocks.
- Do not remove Python, API, JSON, YAML, CLI, or Git. Explain each term in plain language and keep the exact technical word.
- Keep five accessible resource row groups with true HTML `rowspan`: `5 / 4 / 3 / 3 / 3`.
- Keep exactly 18 resources and the same group and row order in all three languages.

## Rating contract

Use the existing `resources/style-guide.md` recommendation scale without redefining it. These stars measure **learning priority**, not GitHub popularity:

- `⭐⭐⭐⭐⭐`: required; skipping it blocks completion of the stage.
- `⭐⭐⭐⭐`: strongly recommended for learning the topic more deeply.
- `⭐⭐⭐`: a solid example worth trying or comparing.
- `⭐⭐`: a useful optional reference.
- `⭐`: niche, advanced, or retained for completeness.

Stage 00 already says learners do not need to read all 18 resources. Therefore none of these optional rows receives five stars; use four or three stars honestly. Add a `推薦度` / `Recommendation` / `推荐度` column to the table and one short explanation before it. Do not restore volatile GitHub star counts.

### Frozen rating matrix

| Group | Resource | Rating | Reason for this stage |
|---|---|---:|---|
| Python | Python Crash Course | ⭐⭐⭐⭐ | Beginner-friendly practice, but the full book is paid. |
| Python | Real Python | ⭐⭐⭐⭐ | Strong topic lookup after the first basics. |
| Python | Corey Schafer YouTube | ⭐⭐⭐ | Helpful English video path, not the shortest universal start. |
| Python | Boot.dev | ⭐⭐⭐ | Interactive, but the complete path is paid. |
| Python | Official Python zh-TW tutorial | ⭐⭐⭐⭐ | Current primary reference; its own introduction expects some programming knowledge. |
| Git | Pro Git | ⭐⭐⭐⭐ | Free, canonical, and broad enough to keep using later. |
| Git | Atlassian Git Tutorials | ⭐⭐⭐⭐ | Clear visual workflow explanations. |
| Git | Pro Git — Undoing Things | ⭐⭐⭐⭐ | Primary-source recovery guidance with explicit data-loss warnings. |
| Git | git-flight-rules | ⭐⭐⭐ | Useful larger rescue manual after the basic official chapter. |
| CLI | The Art of Command Line | ⭐⭐⭐⭐ | Stable systematic reference; broader than the first task. |
| CLI | Microsoft Learn — PowerShell | ⭐⭐⭐⭐ | Official, guided starting point for the roadmap's Windows learners. |
| CLI | tldr pages | ⭐⭐⭐⭐ | Short, copyable command examples for Linux, macOS, and Windows. |
| REST API | MDN — HTTP | ⭐⭐⭐⭐ | Authoritative explanation of the protocol behind the exercise. |
| REST API | Postman Learning Center | ⭐⭐⭐⭐ | Visual API practice without writing code first. |
| REST API | HTTPie | ⭐⭐⭐ | Friendly command-line client, but optional for the main exercise. |
| YAML / JSON | YAML official site | ⭐⭐⭐ | Primary specification and syntax entry point. |
| YAML / JSON | JSON introduction | ⭐⭐⭐⭐ | Short primary introduction to the data format used in the exercise. |
| YAML / JSON | jq | ⭐⭐⭐⭐ | Practical follow-up for filtering API responses in a terminal. |

## Source decisions verified on 2026-08-27 UTC

Replace only these three entries:

1. `runoob.com Python 教學` → [Python 3.14.7 Traditional Chinese tutorial](https://docs.python.org/zh-tw/3/tutorial/). The official page is current and explicitly says it expects basic programming knowledge; describe it as an official reference after first practice, not a zero-experience course.
2. `Oh Shit, Git!?!` → [Pro Git — Undoing Things](https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things). The official Git book covers `git restore`, unstaging, amending, and clear warnings about irreversible loss.
3. `explainshell.com` → [tldr pages](https://github.com/tldr-pages/tldr). The maintained project gives short community-reviewed examples for common console commands across major operating systems.

Keep stable resources such as The Art of Command Line and HTTPie even when they update slowly. Age alone is not a defect; archived status, broken redirects, unsafe advice, or a clearly better current learning entry are stronger replacement signals.

## Implementation sequence

1. Confirm GitHub API UTC date, branch, clean worktree, base commit, and open upstream PR.
2. Recheck all three replacement URLs and repository metadata immediately before editing.
3. Edit zh-TW only. Run Stage 00 reader-UX, anchor, row-group, link, and visible-path checks.
4. Translate the frozen table to English and zh-Hans without changing URLs, order, ratings, counts, or meaning.
5. Add trilingual URL-to-rating row parity so a translation cannot swap two ratings while keeping the same totals.
6. Refresh the repository freshness snapshot through the repository script so the newly added tldr repository is covered; do not hand-edit API evidence.
7. Update CHANGELOG from the final diff and the GitHub API UTC date.
8. Run all relevant documentation and freshness gates.
9. Stage explicit paths, assert the exact file count, record the staged fingerprint, and run one independent `code-reviewer`.
10. Commit and open a stacked PR against `codex/stage02-shot-terms`. Wait for non-empty green checks. Leave the PR, branch, and worktree intact for user review.

Any edit after reviewer acknowledgment invalidates that acknowledgment and requires the relevant gates and review to run again.

## Acceptance criteria

- The unopened page still explains whether Stage 00 is needed and lets a learner run the main exercise.
- All important terms and the four navigation icons remain.
- The first command and Python program remain copy/paste/run ready.
- Three locales each contain 18 resources, 18 links, five row groups, and `rowspan` totals of 18.
- The same resource has the same rating in all three languages.
- Ratings are editorial learning priority; volatile repository popularity counts do not return.
- The three replacements use verified primary or official project sources and have beginner-accurate descriptions.
- No `<details>` is opened by default.
- All required repository gates pass.
- The PR is open and reviewable but remains unmerged until explicit user approval.
