# Outreach: punkpeye/awesome-mcp-servers (PRIMARY)

> **Status**: not contacted · **Channel**: GitHub PR
> **Primary lang**: en
> **Last updated**: 2026-05-09
> **Primary repo**: https://github.com/punkpeye/awesome-mcp-servers (★86k+, MIT, has "Tutorials" section)
> **Secondary (skip for now)**: wong2/awesome-mcp-servers (★4k, MIT, **server-only policy** — no Tutorials section, off-policy for us)

**Why this target**: We already cite both in our README's "Related projects" section (mutual benefit baked in). punkpeye is the canonical large MCP catalog and **has an explicit `## Tutorials` section** that fits us. wong2 is a stricter server-only fork — we'll skip that one to respect their list shape.

**Pitch angle**: Their readers want to use MCP servers; we teach them how MCP works first (Stage 5.2 of our roadmap). Our §5.2 walkthrough → their flat catalog is a natural funnel.

**Their counter-value**: Reciprocal cross-link; better onboarding for their ★86k readers.

---

## Variant 1 — Social post (X, ~280 chars)

```
Browsing the awesome-mcp-servers catalog and unsure where to start? Stage 5.2
of awesome-agentic-ai-zh walks through MCP from concept to first install in
~2 hours, then hands you off to wong2/awesome-mcp-servers for the actual
catalog browsing.

★525 week 1 · MIT
🔗 github.com/WenyuChiou/awesome-agentic-ai-zh
```

## Variant 2 — GitHub PR (200-300 words)

**Target file**: `README.md` — `## Tutorials` section
**PR title**: Add awesome-agentic-ai-zh to Tutorials — trilingual 8-stage learning roadmap

**Diff** (insert in alphabetical or chronological position within `## Tutorials`):

```diff
+ - [awesome-agentic-ai-zh](https://github.com/WenyuChiou/awesome-agentic-ai-zh)
+   — Trilingual (zh-TW · zh-Hans · en) 8-stage learning roadmap. Stage 5.2 is
+   a dedicated walkthrough of MCP (concept → first install → writing your
+   own server), with prerequisites and time estimates. Catalog includes 81+
+   integrations grouped by use case.
```

**PR description**:

```markdown
Hi @punkpeye,

awesome-mcp-servers is already in our `Related projects` section
([README.md](https://github.com/WenyuChiou/awesome-agentic-ai-zh/blob/main/README.md))
— we cite you as the primary catalog for MCP server discovery.

Our repo is the **structured learning complement**:

- Stage 5.2 of our roadmap is a **dedicated MCP walkthrough**: concept →
  first install → writing your own server, with hands-on exercises and time
  estimates
- After Stage 5.2, readers are sent to your catalog to find specific servers
  for their stack
- Trilingual (zh-TW / zh-Hans / en), MIT, ★525 week 1

Targeting your `## Tutorials` section (line ~XX in README) since this is a
"how to learn MCP" resource, not a server. If a different section fits
better, just redirect — happy to update.

Stats (week 1): 6,869 views / 3,185 unique / 1,099 clones / 408 unique cloners
/ 50 forks. CI runs banned-word audit + link-rot check on every PR.

— Wenyu (PhD candidate, individual maintainer)
```

## Variant 3 — DM / Twitter (150 words)

```
@punkpeye — your awesome-mcp-servers list is already in our README's
"Related projects". I run awesome-agentic-ai-zh: a trilingual 8-stage
learning roadmap with Stage 5.2 dedicated to MCP (walkthrough → install →
writing your own server, with cost/time estimates).

After Stage 5.2 our readers are sent to your catalog. Reciprocal link in
your Tutorials section would be natural — opened a PR (<link>). Close it
if it doesn't fit.

— Wenyu
```

---

## Notes

- **Targeting punkpeye, not wong2** — punkpeye has a `## Tutorials` section
  (★86k repo, very large reach); wong2 is server-only-policy by design (★4k,
  no tutorials section, off-policy for our pitch)

- Confirm the line number / position of `## Tutorials` in punkpeye's README
  before opening PR — alphabetical sort within the section is the convention

- punkpeye is responsive — PRs typically reviewed within ~7 days
- If they accept, mirror cross-cite by ensuring our README still references
  them (already done as of 2026-05-09)

- If they redirect to a different section, follow their guidance — don't
  push back
