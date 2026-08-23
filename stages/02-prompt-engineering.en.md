# Stage 2 — Prompt Engineering

> [繁體中文](./02-prompt-engineering.md) | [简体中文](./02-prompt-engineering.zh-Hans.md) | **English**


⏱ **Time estimate**: 1-2 weeks (~5-12 hours)

> 👋 **Coming from [Stage 1](01-llm-basics.en.md)?** Good — you can call an API. The next 5-12 hours: write reusable structured prompts, use few-shot and chain-of-thought for hard reasoning tasks, and quantify prompt improvement with evals. **Jumped straight here?** Make sure you can call an LLM API and estimate cost in tokens — if not, head back to [Stage 1](01-llm-basics.en.md).

> 💡 Term-unfamiliar? (prompt / few-shot / CoT / system prompt / …) → see [`resources/glossary.en.md`](../resources/glossary.en.md).

> 📋 **Chapter structure**: Learning goals → Entry conditions → Required reading → [optional · concept map] → Hands-on exercises → Curated Projects → Self-check
> 🔑 **Key terms**: see [`resources/glossary.en.md`](../resources/glossary.en.md) (every term used in each stage is collected there)

## 📌 Learning Goals

After this stage you will be able to:

- Write structured prompts (role + task + format + examples)
- Apply few-shot prompting and know when it helps
- Use chain-of-thought (CoT) for reasoning tasks
- Iteratively refine a prompt and measure improvement
- Recognize when prompting hits its limit (and you need tools / agents)

## 🚪 Entry Conditions

You should already:

- Be able to call an LLM API (Stage 1)
- Be able to parse / iterate over API responses

## 📚 Required Reading

1. [**anthropics/prompt-eng-interactive-tutorial**](https://github.com/anthropics/prompt-eng-interactive-tutorial) ⭐⭐⭐⭐⭐ ★ 37k+ — **Anthropic's official interactive tutorial**, 9 chapters of Jupyter notebooks (basic / intermediate / advanced + appendix), with playground and answer key. Runs on Claude 3 Haiku (cheapest). **The canonical hands-on resource for Stage 2.** Also packaged as module 2 of the [**anthropics/courses**](https://github.com/anthropics/courses) 5-course umbrella — for broader coverage (API Fundamentals / Real World Prompting / Eval / Tool Use) go straight to the umbrella
2. [**anthropics/courses — Real World Prompting**](https://github.com/anthropics/courses) ⭐⭐⭐⭐ ★ 22k+ — Module 3 of the same umbrella, **"how to actually use prompting in real situations"**: chatbot / legal / financial / coding case walkthroughs. Read #1 first, then this.
3. [**Anthropic Prompt Engineering Guide**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — official docs, pairs with #1
3. [**OpenAI Prompt Engineering**](https://platform.openai.com/docs/guides/prompt-engineering) — OpenAI's perspective
4. [**dair-ai Prompt Engineering Guide**](https://www.promptingguide.ai/) — academic-flavored, in-depth
5. [**Anthropic — Prompting Best Practices**](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct) — be clear and direct

**🎥 Video supplements (highly recommended)**:

- [**Hung-yi Lee — Introduction to Generative AI (NTU, Spring 2024)**](https://speech.ee.ntu.edu.tw/~hylee/genai/2024-spring.php) ⭐⭐⭐ — the later episodes cover prompt engineering (few-shot, CoT, in-context learning) plus the matching labs. The most complete university-level treatment of prompting in Mandarin. Latest consolidated edition: [**GenAI-ML, Fall 2025**](https://speech.ee.ntu.edu.tw/~hylee/GenAI-ML/2025-fall.php)
- [**Hung-yi Lee — Machine Learning, Spring 2025 (includes the prompt + LLM chapters)**](https://speech.ee.ntu.edu.tw/~hylee/ml/2025-spring.php) — for those who want the full ML background

## 🛠 Hands-on Exercises

> 🦙 **This stage defaults to Ollama gemma4:e4b** (cost-driven; $0/run). Prompt engineering is especially instructive on small models — they are sensitive to prompt quality, so you can clearly see how much each technique (system prompts, few-shot, CoT, refinement) improves output. Every exercise has Path A (Ollama, default) + Path B (Anthropic, optional).
>
> 💰 **Stage 2 budget estimate** (4 exercises, 3-5 runs each): **all local = $0**, **all haiku ≈ $0.20**, **all sonnet ≈ $0.60**. The few-shot classifier alone is 12 calls × 5 reps ≈ $0.30 haiku / $0.90 sonnet. Full budget: [`examples/README.en.md#recommended-llm-list`](../examples/README.en.md#recommended-llm-list).
>
> Full three-path trade-off in [`examples/README.en.md`](../examples/README.en.md#three-paths--default-is-ollama-cost-driven).

### Exercise 1: System Prompt
Same user message, three different system prompts. Watch the personality / output format change.

<details markdown="1" open>
<summary>📋 <b>Starter code — Path A (local Ollama gemma4:e4b, default)</b> (copy to <code>practice_1.py</code>)</summary>

```python
# Requires: pip install openai
# Pre-req: ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

SYSTEM_PROMPTS = {
    "Strict lawyer": "You are a precise contract lawyer. Cite statute numbers, avoid subjective adjectives.",
    "Kindergarten teacher": "You are a kind kindergarten teacher speaking to a 5-year-old. Use analogies, colloquial language, under 80 words.",
    "JSON machine": "Reply only in JSON. schema: {\"answer\": string, \"confidence\": float}",
}

USER_MSG = "Explain what a lease agreement is."

outputs = {}
for label, system in SYSTEM_PROMPTS.items():
    # Ollama (OpenAI-compatible) puts system in the messages array (Anthropic uses system=)
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": USER_MSG},
        ],
    )
    outputs[label] = r.choices[0].message.content
    print(f"\n--- [{label}] ---")
    print(outputs[label])

# === Self-check ===
import json
last_text = outputs["JSON machine"]
assert "{" in last_text and "}" in last_text, "JSON-machine output should contain JSON braces"
try:
    parsed = json.loads(last_text.strip().split("\n")[-1] if "\n" in last_text else last_text)
    assert "answer" in parsed, "schema expects an 'answer' field"
except json.JSONDecodeError:
    pass  # some models add prose around the JSON; tolerate that

print(f"\n✅ Exercise 1 passed — same question, three different personas / formats / tones")
```

**Expected output** (sample; gemma4:e4b follows the system prompt reasonably well, though less strictly than Claude):
```
--- [Strict lawyer] ---
Per Article 421 of the Civil Code...

--- [Kindergarten teacher] ---
A lease is like lending a toy to a friend — you agree when it comes back and how many sweets it costs...

--- [JSON machine] ---
{"answer": "A lease is an agreement in which one party lets another use a thing...", "confidence": 0.85}
```

</details>

<details markdown="1">
<summary>📋 <b>Starter code — Path B (Anthropic API, optional)</b> (copy to <code>practice_1_anthropic.py</code>)</summary>

```python
# Requires: pip install anthropic
import sys, json
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic
client = anthropic.Anthropic()

SYSTEM_PROMPTS = {
    "Strict lawyer": "You are a precise contract lawyer. Cite statute numbers, avoid subjective adjectives.",
    "Kindergarten teacher": "You are a kind kindergarten teacher speaking to a 5-year-old. Use analogies, colloquial language, under 80 words.",
    "JSON machine": "Reply only in JSON. schema: {\"answer\": string, \"confidence\": float}",
}
USER_MSG = "Explain what a lease agreement is."

outputs = {}
for label, system in SYSTEM_PROMPTS.items():
    # Anthropic uses `system=` parameter (not part of messages array)
    msg = client.messages.create(model="claude-haiku-4-5", max_tokens=200,
                                 system=system, messages=[{"role": "user", "content": USER_MSG}])
    outputs[label] = msg.content[0].text
    print(f"\n--- [{label}] ---")
    print(outputs[label])

# Self-check (same JSON-shape assert; schema is cross-backend)
json_output = outputs["JSON machine"]
assert "{" in json_output and "}" in json_output
print(f"\n✅ Exercise 1 passed (Anthropic)")
```

**Key difference**: Anthropic uses `system=` parameter; OpenAI/Ollama puts system in messages array. Claude follows system prompts more strictly than gemma4:e4b — the "Strict lawyer" persona will actually cite statute numbers. **Cost**: ~$0.003 / 3 personas.

</details>

### Exercise 2: Few-Shot

**Get these three terms first** — the only difference is how many examples you show the LLM:

- **Zero-shot (0-shot)**: no examples, just ask.
- **One-shot (1-shot)**: give **1** "input → answer" example first, then ask.
- **Few-shot (the 3-shot below is exactly this)**: give a few (usually 2–5) examples first — the LLM copies their format and judgment criteria, and accuracy usually jumps.

Pick a classification task. Run it 0-shot, then 3-shot. Measure accuracy difference.

<details markdown="1" open>
<summary>📋 <b>Starter code — Path A (local Ollama gemma4:e4b, default)</b> (copy to <code>practice_2.py</code>)</summary>

```python
# Requires: pip install openai
# Pre-req: ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# Sentiment classifier: positive / negative / neutral
TEST_SET = [
    ("This movie was amazing — I want to watch it again!", "positive"),
    ("Boring plot, awkward acting.", "negative"),
    ("This is a 2019 film.", "neutral"),
    ("Not sure how I feel about it, might think more.", "neutral"),
    ("Season 1 was great but season 2 fell apart.", "negative"),
    ("Left in a great mood — recommended!", "positive"),
]

FEW_SHOT_EXAMPLES = """Examples:
input: The steak at this place made me cry tears of joy.
output: positive

input: The waiter was rude. Never coming back.
output: negative

input: This shop is in New Taipei City.
output: neutral
"""

# Both conditions share the SAME task instruction; few-shot only adds examples. That keeps the comparison clean — what you measure is the effect of the examples themselves, not "finally telling the model what the task is."
TASK = "Classify the sentence below into exactly one of positive / negative / neutral. Output only one of those three words, nothing else.\n\n"


def classify(text: str, *, use_few_shot: bool) -> str:
    prefix = FEW_SHOT_EXAMPLES + "\n" if use_few_shot else ""
    prompt = f"{TASK}{prefix}input: {text}\noutput:"
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content.strip().splitlines()[0]


def evaluate(use_few_shot: bool) -> tuple[int, int]:
    correct = 0
    for text, label in TEST_SET:
        pred = classify(text, use_few_shot=use_few_shot)
        ok = label in pred
        print(f"  {'✓' if ok else '✗'} [{label}] {text[:30]}... → '{pred}'")
        if ok:
            correct += 1
    return correct, len(TEST_SET)


print("=== 0-shot ===")
c0, n = evaluate(use_few_shot=False)
print(f"correct {c0}/{n} = {c0/n:.0%}")

print("\n=== 3-shot ===")
c3, _ = evaluate(use_few_shot=True)
print(f"correct {c3}/{n} = {c3/n:.0%}")

# === Self-check ===
# Both conditions got the same task instruction, so this measures the effect of the EXAMPLES alone.
# few-shot isn't guaranteed to win (depends on the model / test set / sampling), so we don't assert c3 >= c0.
assert n == 6 and 0 <= c0 <= n and 0 <= c3 <= n, "both conditions must run all 6 items"
print(f"\n✅ Exercise 2 passed — 0-shot {c0}/{n}, 3-shot {c3}/{n}; few-shot net gain {c3 - c0} (may be 0 or even negative — that's normal) (local, $0)")
print("💡 With a clear instruction, 0-shot already has a baseline; few-shot's value is pinning the output FORMAT + showing judgment on ambiguous cases (like 'neutral')")
print("💡 Small models (gemma4:e4b) are more format-sensitive, so few-shot usually helps them more than Claude — still not guaranteed, so you measure")
```

</details>

<details markdown="1">
<summary>📋 <b>Starter code — Path B (Anthropic API, optional)</b> (copy to <code>practice_2_anthropic.py</code>)</summary>

```python
# Requires: pip install anthropic
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import anthropic
client = anthropic.Anthropic()

# Same TASK / TEST_SET / FEW_SHOT_EXAMPLES as Path A — only the classify() body changes:
def classify(text: str, *, use_few_shot: bool) -> str:
    prefix = FEW_SHOT_EXAMPLES + "\n" if use_few_shot else ""
    msg = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=10,
        messages=[{"role": "user", "content": f"{TASK}{prefix}input: {text}\noutput:"}],
    )
    return msg.content[0].text.strip().splitlines()[0]
# Rest of TASK / TEST_SET / FEW_SHOT_EXAMPLES / evaluate() stays identical to Path A
```

**Cost**: 12 calls ≈ $0.005. Claude is usually accurate at 0-shot already, so the few-shot lift is smaller than on gemma4:e4b — that contrast is the actual teaching point.

</details>

### Exercise 3: CoT
Pick a math word problem. Compare:

- Plain prompt
- Plain prompt + "Let's think step by step"
- Plain prompt + worked example showing CoT

<details markdown="1" open>
<summary>📋 <b>Starter code — Path A (local Ollama gemma4:e4b, default)</b> (copy to <code>practice_3.py</code>)</summary>

```python
# Requires: pip install openai
# Pre-req: ollama pull gemma4:e4b && ollama serve
import sys, re
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

QUESTION = "Tom has 3 apples. He gives Sarah 1, then mom gives him 5 more, then he eats 2. How many does he have now?"
ANSWER = 5  # 3 - 1 + 5 - 2 = 5

COT_EXAMPLE = """Example:
Q: A chicken has 2 legs. 3 chickens and 1 person — how many legs total?
A: Let me work through this step by step. 3 chickens × 2 legs = 6 legs. 1 person has 2 legs. Total 6 + 2 = 8 legs. The answer is 8.
"""


def ask(prompt: str) -> str:
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return r.choices[0].message.content


def extract_number(text: str) -> int | None:
    """Pull the last number from the response as the answer."""
    nums = re.findall(r"-?\d+", text)
    return int(nums[-1]) if nums else None


out_a = ask(QUESTION)
ans_a = extract_number(out_a)

out_b = ask(QUESTION + "\nLet's think step by step.")
ans_b = extract_number(out_b)

out_c = ask(COT_EXAMPLE + "\n\nQ: " + QUESTION + "\nA:")
ans_c = extract_number(out_c)

for label, out, ans in [("A plain", out_a, ans_a), ("B +step-by-step", out_b, ans_b), ("C +CoT example", out_c, ans_c)]:
    print(f"\n--- [{label}] answer={ans} {'✓' if ans == ANSWER else '✗'} ---")
    print(out[:200])

# === Self-check ===
correct = sum(1 for a in (ans_a, ans_b, ans_c) if a == ANSWER)
assert correct >= 1, f"at least 1 of 3 prompts should be correct, got {correct}/3"
assert ans_b == ANSWER or ans_c == ANSWER, "B (step-by-step) or C (CoT example) must be correct — CoT is non-negotiable for small models"
print(f"\n✅ Exercise 3 passed — {correct}/3 correct")
```

</details>

<details markdown="1">
<summary>📋 <b>Starter code — Path B (Anthropic API, optional)</b> (copy to <code>practice_3_anthropic.py</code>)</summary>

Same logic as Path A, just swap the client and `ask()`:

```python
import anthropic
client = anthropic.Anthropic()

def ask(prompt: str) -> str:
    msg = client.messages.create(model="claude-haiku-4-5", max_tokens=300,
                                 messages=[{"role": "user", "content": prompt}])
    return msg.content[0].text
# Rest (QUESTION, ANSWER, COT_EXAMPLE, extract_number, 3 calls, assert) stays identical
```

**Claude typically gets 3/3 right** including the plain-prompt baseline — that contrast with gemma4:e4b (where CoT is essential) is the actual teaching point. **Cost**: 3 calls ≈ $0.002.

</details>

> 🧠 **When NOT to hand-write CoT**: for **reasoning-native models** (Claude Opus 4.x / 5, the o-series, Gemini thinking, and other models with built-in thinking), using their extended thinking is usually better than hand-writing "Let's think step by step"; forcing your own steps can interfere with their native reasoning. Hand-written CoT still applies to plain chat models without built-in reasoning.

### Exercise 4: Iterative Refinement
Take a vague prompt, refine it 5 times. Track the iterations. Notice what changes improve quality.

<details markdown="1" open>
<summary>📋 <b>Starter code — Path A (local Ollama gemma4:e4b, default)</b> (copy to <code>practice_4.py</code>) — this exercise has no "right answer"; the point is observing the process</summary>

```python
# Requires: pip install openai
# Pre-req: ollama pull gemma4:e4b && ollama serve
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# 5 iterations, each adds one constraint
PROMPTS = {
    "v1 vague": "Write a paragraph about ReAct.",
    "v2 +audience": "Write a paragraph about ReAct for software engineers who know Python.",
    "v3 +format": "Write a paragraph about ReAct for software engineers who know Python. Under 100 words, single paragraph.",
    "v4 +example": "Write a paragraph about ReAct for software engineers who know Python. Under 100 words, single paragraph, ending with a concrete example (e.g. weather lookup).",
    "v5 +bans": "Write a paragraph about ReAct for software engineers who know Python. Under 100 words, single paragraph, ending with a concrete example (e.g. weather lookup). Avoid words like 'empower', 'leverage', 'intelligent'.",
}

outputs = {}
for label, prompt in PROMPTS.items():
    r = client.chat.completions.create(
        model="gemma4:e4b",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    text = r.choices[0].message.content
    outputs[label] = text
    print(f"\n--- [{label}] ({len(text)} chars) ---")
    print(text)

# === Self-check ===
v1_len, v5_len = len(outputs["v1 vague"]), len(outputs["v5 +bans"])
banned_words = ("empower", "leverage", "intelligent")
v5_text_lower = outputs["v5 +bans"].lower()
v5_has_banned = any(w in v5_text_lower for w in banned_words)
assert v5_len > 0, "v5 must have output"
assert not v5_has_banned, f"v5 should avoid banned words; got: {[w for w in banned_words if w in v5_text_lower]}"
print(f"\n✅ Exercise 4 passed — v5 length {v5_len}, no banned words")
print(f"💡 Observe: v1 ({v1_len} chars) is typically looser than v5 ({v5_len} chars); constraints tighten prompts")
print("💡 The 5 dimensions: (1) target audience (2) format (3) length (4) example demand (5) banned words")
```

</details>

<details markdown="1">
<summary>📋 <b>Starter code — Path B (Anthropic API, optional)</b> (copy to <code>practice_4_anthropic.py</code>)</summary>

Same loop and PROMPTS as Path A, with Anthropic SDK:

```python
import anthropic
client = anthropic.Anthropic()

outputs = {}
for label, prompt in PROMPTS.items():
    msg = client.messages.create(model="claude-haiku-4-5", max_tokens=200,
                                 messages=[{"role": "user", "content": prompt}])
    outputs[label] = msg.content[0].text
# Rest (length compare, banned-word assert) stays identical
```

**Cost**: 5 calls ≈ $0.002. **Claude's v1 is already coherent** so the v5 lift is smaller; gemma4:e4b makes the lift more dramatic.

</details>

**Going further**: dump all 5 rounds of output to a CSV. Stage 7 Exercise 2 shows how to turn that into an eval harness (the outer program / control layer used to run evals; see Advanced: what layers sit above prompting?) so you can quantify *how much* a prompt actually improved.

## 🎯 Curated Projects

4 categories, 9 projects in one table. **Pick by "Best for"; click through for depth on the repo / site.**

| Category | Project | ⭐ | Best for | Why / Notes |
|---|---|---|---|---|
| **Academic / teaching-style guide**<br>(start here) | [dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) | ⭐⭐⭐⭐⭐ | Reference book; look up a specific technique | Basics to advanced (CoT / ToT / ReAct / RAG) end to end, ★ 74k+, MIT |
| | [PromptingGuide.ai](https://www.promptingguide.ai/) | ⭐⭐⭐⭐ | Phone reading; want runnable examples | Same content as dair-ai GitHub in website form + runnable examples |
| | [NirDiamant/Prompt_Engineering](https://github.com/NirDiamant/Prompt_Engineering) | ⭐⭐⭐⭐ | Learn-by-running | 22 techniques, each in its own notebook, more hands-on than dair-ai, ★ 7.7k+ |
| **Official cookbook** | [Anthropic Cookbook — Prompt patterns](https://github.com/anthropics/claude-cookbooks) | ⭐⭐⭐⭐⭐ | Advanced Claude prompting (prompt caching / multimodal) | Introduced in Stage 1; for this stage focus on `misc/prompt_caching.ipynb` and `multimodal/` |
| | [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai) | ⭐⭐⭐ | Google stack (PaLM / Gemini) users | Google Cloud's prompting cookbook; cross-vendor perspective |
| **Inspiration collection**<br>(steal patterns, don't copy)| [f/awesome-chatgpt-prompts](https://github.com/f/awesome-chatgpt-prompts) | ⭐⭐⭐ | When you're stuck for ideas | Hundreds of "Act as a [role]..." prompts, ★ 166k+, CC0. **Take the pattern, rewrite — don't copy verbatim** |
| **Production management**<br>(scale up)| [microsoft/prompt-engine](https://github.com/microsoft/prompt-engine) | ⭐⭐ (⚠️ archived) | Managing many prompts in production | TypeScript library; ⚠️ **no updates since 2023, repo archived** — find a maintained alternative |
| | [microsoft/promptflow](https://github.com/microsoft/promptflow) | ⭐⭐⭐ | Team apps needing eval | Visual prompt design + eval tooling, ★ 11k+ |
| | [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy) ⭐ **Stage 2 → 3 bridge** | ⭐⭐⭐⭐⭐ | After dair-ai, want to scale prompts | Treat prompts as code, compiler auto-optimizes, ★ 36k+, MIT |

> **Note**: dspy is a framework, not a tutorial — higher entry barrier; pair it with the [dspy.ai](https://dspy.ai/) official tutorial. NirDiamant uses NOASSERTION custom terms (research / non-commercial leaning).

> 💡 **Suggested reading order**: dair-ai guide for theory → Anthropic Cookbook for Claude implementation → NirDiamant for hands-on → dspy when going to production.

## 🔭 Advanced: What layers sit above prompting?

Engineering practice for LLM-powered systems is layered. This is not about "one call vs. many calls." **Here we only look at the three layers directly adjacent to prompt writing**; the full model has **five layers**, with Loop and Graph further out. See [Stage 7 five-layer engineering split](07-multi-agent-production.en.md#the-five-layer-engineering-split-prompt--context--harness--loop--graph), the canonical source for the layering model. Each layer engineers a different object:

The three layers engineer, respectively: **the string sent into the model** (this stage), **what goes into the context window** (Stage 6), and **the execution and control layer outside the model** (Stage 7). Definitions and which stage covers each are in the table below.

→ The three layers are **orthogonal**: a one-call RAG app is still doing context engineering (the point is assembling context, not how many calls happen); a 50-call chatbot with no retrieval is still only doing prompt engineering.

**Where these three layers fit in this roadmap** (for the full five-layer model, see Stage 7):

| Discipline | What is being engineered | Where this roadmap teaches it fully |
|---|---|---|
| **1. Prompt Engineering** | The string sent into the LLM itself (system prompt / few-shot / format) | **This stage (Stage 2)** |
| **2. Context Engineering** | What information goes into the context window (RAG / memory / tool defs / history) | [Stage 6 — Context Engineering: RAG and Memory](06-memory-rag.en.md) |
| **3. Harness Engineering** | The execution and control layer around the model (agent loop / retry / sandbox / observability) | [Stage 7 — Multi-Agent · Productionization](07-multi-agent-production.en.md) |

> 💡 **Karpathy 2025-06**: context engineering is the delicate art of putting information that is **just useful for the next step** into the context window.
>
> 💡 **Simon Willison / Addy Osmani**: "coding agent = LLM + harness"; a harness is all the code that is not the model itself. [OpenAI also used the term "Harness Engineering" in February 2026](https://openai.com/index/harness-engineering).

**You do not need to finish the latter two layers in this stage**. This section only gives you the direction so that Stage 6 / 7 feel like a continuation of the same lineage.

Further reading (optional, for when you want to dig deeper):

- [`Meirtz/Awesome-Context-Engineering`](https://github.com/Meirtz/Awesome-Context-Engineering) (★ 3.3k+) — comprehensive survey from prompt engineering to production agents
- [`Windy3f3f3f3f/how-claude-code-works`](https://github.com/Windy3f3f3f3f/how-claude-code-works) (★ 3.3k+) — Claude Code internals, includes a context-engineering chapter

## ✅ Self-Check Before Stage 3

Can you:

- [ ] Write a prompt with system message + user message + 3 example messages (few-shot)
- [ ] Demonstrate CoT improving accuracy on a reasoning task
- [ ] Iteratively refine a prompt 5 times tracking each version
- [ ] Identify when prompting is the wrong tool (and tool use is needed)

If yes → proceed to [Stage 3 — Tool Use & Agent Intro](03-tool-use-and-hello-agent.en.md). This is the most important stage — don't rush past prompts but also don't get stuck here.
