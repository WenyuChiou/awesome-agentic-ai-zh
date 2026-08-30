# Outreach draft — Hacker News (Show HN)

> **Status**: draft, not submitted. Maintainer reviews + posts manually.
> One shot — don't repost if it doesn't catch. Pick a weekday, ~08:00–10:00
> US Eastern (HN morning), not Fri/weekend.

## Why HN

Largest single English dev-audience spike potential. Audience overlaps
exactly: people building with LLMs / agents who like structured depth.
Risk: HN is allergic to hype and to "another awesome-list". The draft
below leads with the concrete artifact and pre-empts the two predictable
top comments ("why another list" / "is the English LLM-translated").

## Title (pick one — no emoji, no hype, ≤ 80 chars)

1. `Show HN: A trilingual, staged roadmap from LLM basics to multi-agent systems`
2. `Show HN: Agentic-AI learning roadmap – 10 learning stops, curated projects`
3. `Show HN: An opinionated path to learn agentic AI (not an awesome-list dump)`

Recommended: **#1** (says what it is + the trilingual angle, no adjectives).

## Body (paste into the text field, keep it short)

```
I built a structured learning roadmap for agentic AI because every
"awesome-list" I found was a flat link dump with no order — great as a
reference, useless as a path if you don't already know what you don't
know.

This is sequenced as 10 learning stops: 8 topic stages plus Stage 0 readiness and a Stage 7.5 advanced reading stop, from basic terms to production agents
orchestration + Computer/Browser Use, with explicit entry conditions and
a self-check at the end of each stage, plus two tracks (use existing CLI
agents vs. build your own) and 5 audience branches (researcher /
developer / teacher / knowledge worker / everyday user).

It started as a Chinese-language project, but the English edition is
fully maintained, not a machine-translated afterthought (~0.4% of
English lines contain any CJK, almost all intentional term-mapping; CI
checks localization + anchor integrity). Rendered site (trilingual,
mkdocs): https://wenyuchiou.github.io/awesome-agentic-ai-zh/
Repo: https://github.com/WenyuChiou/awesome-agentic-ai-zh

It's MIT, with curated projects that explain audience, what each project
teaches, and how to run it, plus small runnable exercises (1–5 per stage). Honest limitation:
it's opinionated (Claude-ecosystem-heavy in the later stages — MCP /
Skills / SDK), and the deep exercises point out to first-party cookbooks
rather than re-teaching them. Feedback on the sequencing + what's
missing is what I'm after.
```

## First-comment (post yourself, immediately, as the author)

```
Author here. Two things I expect to come up:

1. "Why not just a list?" — the curation IS in there (entries with
   the usual metadata), but the value I was missing was ORDER + exit
   criteria, so the spine is the stage sequence, not the list.

2. "Is the English LLM-slop?" — fair worry for a zh-origin repo. It's
   not a thin mirror: measured ~0.4% CJK across 64 English files, the
   required-reading per stage is English-native primary sources
   (Anthropic/OpenAI/HF docs), and structure is CI-gated. Tell me where
   it reads translated and I'll fix it.

Happy to take "this stage is wrong / out of date" specifics.
```

## Don'ts
- ❌ Don't say "the best / definitive / production-grade" (HN will pile on).
- ❌ Don't lead with the star count.
- ❌ Don't repost a flopped submission within weeks.
- ❌ Don't ask for upvotes/stars anywhere.
