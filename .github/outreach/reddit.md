# Outreach draft — Reddit

> **Status**: draft, not submitted. Maintainer posts manually, ONE
> subreddit per day max, tailored each time (cross-posting identical
> text reads as spam and gets auto-removed). Always disclose you're the
> author. Read each sub's rules + "self-promotion" policy first.

## Targets (priority order)

| Sub | Why | Rule note |
|---|---|---|
| r/AI_Agents | Exact audience (agent builders) | Self-promo tolerated if it's substantive + you engage |
| r/LocalLLaMA | Huge, builder-heavy, likes curation | No pure self-promo on weekends; lead with value |
| r/ClaudeAI | Later stages are Claude-ecosystem (MCP/Skills) | Fits; flair appropriately |
| r/learnmachinelearning | "How do I learn agents" asked daily | Post as a resource, not a launch |
| r/MachineLearning | Strict; only if framed as a resource, low priority | Needs heavy substance, mod-gated — optional |

## r/AI_Agents (primary)

**Title**: `A staged roadmap to learn agentic AI (not a flat awesome-list) — feedback wanted`

**Body**:
```
I kept seeing "awesome-X" lists for agents — useful as references, but
none gave an ORDER to actually learn in. So I built a sequenced roadmap
and I'd like this sub to poke holes in the sequencing.

- 10 learning stops: 8 topic stages + Stage 0 readiness + Stage 7.5 reading →
  Claude Code ecosystem (MCP/Skills) → memory/RAG → multi-agent →
  Computer/Browser Use. Each stage has entry conditions + an end self-check.
- 2 tracks: "use existing CLI agents" vs "build your own".
- 5 audience branches (researcher / dev / teacher / knowledge worker /
  everyday user).
- Curated projects (star / audience / what it teaches / how to run)
  + small runnable exercises (1–5 per stage). MIT.

Trilingual (the project is Chinese-origin but the English edition is
fully maintained, not MT slop). Rendered site:
https://wenyuchiou.github.io/awesome-agentic-ai-zh/

Honest bias: Claude-ecosystem-heavy in the later stages. What I want:
where is the stage order wrong, and what's a glaring omission?
```

## r/LocalLLaMA (variant — lead with the local-LLM angle)

**Title**: `Trilingual agentic-AI roadmap — every stage's exercises run on Ollama/local first, Claude as the prod reference`

**Body**: (same skeleton, swap first paragraph)
```
Built a staged learn-path for agentic AI. Relevant to this sub
specifically: the hands-on exercises are dual-path — Ollama / local
runner first (llama.cpp, LocalAI, MLX listed), with Claude/Anthropic as
the production reference, so you can do the whole roadmap locally before
spending an API cent.
```
(then the same 10-stops / 2-tracks / link / "honest bias" / "feedback
wanted" tail as r/AI_Agents)

## r/ClaudeAI (variant — lead with the ecosystem depth)

**Title**: `A learning path that actually covers the Claude Code ecosystem (MCP / Skills / Plugins / SDK), staged`

**Body**: lead paragraph emphasising Stage 5/8 (Claude Code ecosystem +
Agent Interfaces) as the differentiator vs framework-only tutorials;
same tail.

## r/learnmachinelearning (variant — resource framing, not launch)

**Title**: `Resource: a free, staged roadmap from LLM basics to multi-agent (with exit self-checks)`

**Body**: frame as "for the recurring 'how do I start with agents'
question" — emphasise Stage 0–2 foundation + the self-check gating;
same link; lighter on the build-track detail.

## Don'ts
- ❌ Identical body across subs (auto-spam-flag).
- ❌ "Please star/upvote".
- ❌ Drive-by post then disappear — must reply to comments for ~24h.
- ❌ Posting to r/MachineLearning without resource framing (removal).
