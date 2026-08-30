# Tool landscape and runnable-examples freshness plan

## Goal

Make the runnable-examples index and Agent tool reference easy to enter without
turning volatile product facts into permanent definitions. Keep exact terms,
required reading, curated projects, and editorial ratings visible.

## Reader contract

- The visible path defines each important term before using it.
- Required reading, the stage index, curated projects, and full ratings stay
  outside `<details>`.
- Time, setup variants, budget arithmetic, troubleshooting, and contribution
  mechanics may be collapsed.
- Grouped resource tables use real `<tbody>` row groups and `rowspan`; no blank
  category cells or repeated category labels.
- OpenCode and Pi are Coding Agents/Harnesses, OpenRouter is a Router, and
  Ollama is a Local Runtime. A product can expose several Surfaces and run in
  more than one Deployment location, so these are axes rather than five
  mutually exclusive “Agent types.”

## Current-fact pack (verified 2026-08-30 UTC)

- OpenCode: <https://opencode.ai/docs/>,
  <https://opencode.ai/docs/providers/>, <https://opencode.ai/docs/rules>, and
  <https://opencode.ai/docs/skills/>.
- Pi: <https://pi.dev/docs/latest/security> and
  <https://github.com/earendil-works/pi>.
- OpenRouter: <https://openrouter.ai/docs/faq>.
- Ollama model tags: <https://ollama.com/library/gemma4:e4b>,
  <https://ollama.com/library/qwen2.5:3b>, and
  <https://ollama.com/library/qwen3.5:4b>.
- Hermes Agent: <https://github.com/NousResearch/hermes-agent>.
- goose: <https://github.com/aaif-goose/goose>.
- Aider: <https://aider.chat/docs/git.html>.

GitHub repository status and licenses were checked through the GitHub API on
the same UTC date. Do not freeze GitHub stars, provider counts, account-specific
prices, hardware ceilings, or blanket “zero exposure” claims.

## Delivery shape

1. Normalize current OpenCode naming, docs, rule fallback, and Skill paths.
2. Rewrite the examples index around “pick one example → mock test → local live
   call → optional cloud comparison,” using the actual folder inventory.
3. Rewrite Agent paradigms around Identity, Surface, and Deployment axes; retain
   Subagent as a separate concept.
4. Add freshness markers, official-source packs, trilingual reader-UX parity,
   visibility assertions, and stale-pattern regression tests.
5. Run the real repository commands. `check-2026-freshness.py` is strict by
   default and has no `--strict` flag; there is no
   `scripts/test_track_a_content.py` in the current tree.
6. Stage explicit paths, obtain independent review for the stable fingerprint,
   then publish one new Draft PR on top of PR #204. Do not merge or delete an
   active stack branch without the user's explicit approval.
