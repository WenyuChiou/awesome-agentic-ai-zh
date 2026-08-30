> [繁體中文](./build-first-agent-in-7-steps.md) | [简体中文](./build-first-agent-in-7-steps.zh-Hans.md) | **English**

# Build Your First AI Agent in 7 Steps

> [← Back to main path README](../README.en.md)

> 📌 **This is for Track B (Agent Builder)** — teaches you to **write an agent from scratch**.
> [Track A (CLI Power User)](../tracks/cli/A1-cli-intro.en.md) learners **do not need to run this**; but reading it gives deeper understanding of "**how an agent gets composed step-by-step from LLM API to production**" — optional advanced supplement.

This is a **concrete cross-stage walkthrough** — the same agent, traced from Stage 1 through Stage 7, with executable code skeletons at each stage.

> **How to read this**: each section extends the previous one. Later snippets assume earlier stage files are in the same directory. To run:
> 1. Set up the environment in Stage 0
> 2. Save each stage to a new file (`step1_*.py`, `step2_*.py`, …)
> 3. Later stages import from earlier ones via `from step1_xxx import ...`
>
> Install all deps at once: `pip install anthropic openai requests beautifulsoup4 langgraph langchain-anthropic langchain-core chromadb langfuse fastapi uvicorn pydantic`

The agent to build: **Paper Summary Bot** — given an arXiv paper URL, output a 3-paragraph summary + 5 keywords + comparison with related work.

Each Stage **adds one capability** to the same agent. By the end, it can use multiple LLMs, remember the data it needs, and run as a deployed service.

---

## 📋 Overview

| Stage | Capability you add | Size of this step |
|---|---|---|
| 0 | Environment (Python, API key, git) | Setup |
| 1 | First LLM API call | Small |
| 2 | Write a professional prompt | Small |
| 3 | Tool use: auto-fetch arXiv | Medium |
| 4 | Rewrite with a framework + a reflection check | Medium; the framework wraps some details |
| 5 | Package as a Claude Code Skill | One config file + a small helper |
| 6 | Add RAG and Memory: retrieve old papers, then compare | Medium |
| 7 | Add Evals, Observability (run records), and Deployment | Larger |

**Final result**: one concrete example that grows from a small Python program into a service you can evaluate, inspect, and deploy.

---

## Stage 0 — Environment

```bash
# Install Python 3.11+
python --version

# Virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install all packages used across stages (one-time; later stages won't pip install again)
pip install anthropic openai requests beautifulsoup4 \
            langgraph langchain-anthropic langchain-core \
            chromadb langfuse fastapi uvicorn pydantic

# Claude API key (apply at console.anthropic.com)
export ANTHROPIC_API_KEY="sk-ant-..."

# Init repo
mkdir paper-summary-bot && cd paper-summary-bot
git init
echo ".env\n.venv/\n__pycache__/" > .gitignore
```

**Checkpoint**: `python -c "from anthropic import Anthropic; print('OK')"` should work without error.

---

## Stage 1 — First LLM Call

```python
# step1_hello_llm.py
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=500,
    messages=[{
        "role": "user",
        "content": "Explain ReAct agents in 3 sentences."
    }]
)

print(response.content[0].text)
print(f"\n--- Tokens: input={response.usage.input_tokens}, "
      f"output={response.usage.output_tokens} ---")
```

Run: `python step1_hello_llm.py`

**What you learn**: API call shape, `messages` structure, how `usage` counts tokens.

---

## Stage 2 — Professional Prompt

```python
# step2_paper_summary.py
from anthropic import Anthropic

client = Anthropic()

SYSTEM_PROMPT = """You are an academic paper summarization assistant. Your task:

1. Write a 3-paragraph summary describing: (a) motivation, (b) method, (c) results.
2. List 5 keywords.
3. Bullet 2-3 differences from mainstream approaches.

Format requirements:
- Each summary paragraph ≤ 60 words
- Keywords in English (technical terms)
- Total ≤ 300 words
- Don't fabricate; if not stated, say "not stated in the paper"."""

PAPER_TEXT = """[Paste paper abstract here]"""

# Run it (guarded by __main__: later stages import this file just to get
#   SYSTEM_PROMPT, and without the guard the import alone fires a real,
#   billed API call against the placeholder text)
if __name__ == "__main__":
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": PAPER_TEXT}]
    )
    print(response.content[0].text)
```

**What you learn**: system prompt vs user message split, explicit format constraints, anti-hallucination via "say not stated."

---

## Stage 3 — Tool Use: Auto-Fetch Papers

```python
# step3_tool_use.py
import requests
from anthropic import Anthropic
from step2_paper_summary import SYSTEM_PROMPT  # written in the previous stage

client = Anthropic()

# Define tool
TOOLS = [{
    "name": "fetch_arxiv",
    "description": "Fetch arXiv paper abstract by URL",
    "input_schema": {
        "type": "object",
        "properties": {
            "arxiv_url": {"type": "string"}
        },
        "required": ["arxiv_url"]
    }
}]

def fetch_arxiv(arxiv_url: str) -> str:
    """Tool implementation."""
    arxiv_id = arxiv_url.split("/")[-1].replace(".pdf", "")
    api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    r = requests.get(api_url)
    # Simplified: real version should parse XML
    return r.text[:5000]

# ReAct loop
def run_agent(user_query: str):
    messages = [{"role": "user", "content": user_query}]
    
    while True:
        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=2000,
            tools=TOOLS,
            messages=messages,
            system=SYSTEM_PROMPT,  # from Stage 2
        )
        
        # No more tool calls → done
        if response.stop_reason == "end_turn":
            return response.content[-1].text
        
        # Handle tool call
        tool_use = next(b for b in response.content if b.type == "tool_use")
        if tool_use.name == "fetch_arxiv":
            result = fetch_arxiv(**tool_use.input)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [{
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result,
                }]
            })

# Run it (same guard: Stage 7's eval_provider and step7 both import
#   run_agent, and without it every import runs a full agent turn)
if __name__ == "__main__":
    print(run_agent("Summarize this paper: https://arxiv.org/abs/2210.03629"))
```

**What you learn**: tool schema syntax, ReAct loop mechanics, `stop_reason` for termination, `tool_result` round-trip.

**This is the biggest Stage 3 leap — your code goes from "calling LLM" to "LLM calling your code."**

---

## Stage 4 — Framework + Reflection

> **Install**: `pip install langgraph langchain-anthropic langchain-core`

Rewrite with LangGraph and add a self-review node:

```python
# step4_langgraph.py
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

@tool
def fetch_arxiv(arxiv_url: str) -> str:
    """Fetch arXiv paper abstract."""
    import requests
    arxiv_id = arxiv_url.split("/")[-1].replace(".pdf", "")
    r = requests.get(f"http://export.arxiv.org/api/query?id_list={arxiv_id}")
    return r.text[:5000]

class State(TypedDict):
    messages: Annotated[list, add_messages]
    revisions: int  # bound the loop

llm = ChatAnthropic(model="claude-sonnet-5")
react_agent = create_react_agent(llm, tools=[fetch_arxiv])

MAX_REVISIONS = 2

def reflect(state: State) -> State:
    """Have the LLM review the previous summary and decide whether to redo."""
    last_summary = state["messages"][-1].content
    
    # Use an explicit yes/no verdict instead of keyword-matching prose
    review_prompt = (
        f"Does the following summary satisfy: 3 paragraphs, each ≤60 words, "
        f"5 English keywords, no fabrication?\n\n"
        f"{last_summary}\n\n"
        "Reply with PASS or NEEDS_REVISION only — no explanation."
    )
    verdict = llm.invoke(review_prompt).content.strip().upper()
    
    return {
        "messages": [HumanMessage(content=f"[Reviewer verdict: {verdict}]")],
        "revisions": state.get("revisions", 0) + 1,
    }

def should_continue(state: State) -> str:
    """Decide whether to loop back to agent or terminate."""
    last_msg = state["messages"][-1].content
    if state["revisions"] >= MAX_REVISIONS:
        return END  # bound reached, exit unconditionally
    if "NEEDS_REVISION" in last_msg:
        return "agent"  # redo
    return END  # PASS → exit

# Build graph
graph = StateGraph(State)
graph.add_node("agent", react_agent)
graph.add_node("reflect", reflect)
graph.add_edge("agent", "reflect")
graph.add_conditional_edges("reflect", should_continue, {"agent": "agent", END: END})
graph.set_entry_point("agent")
app = graph.compile()

# Run it (same guard: Stage 6 imports State / react_agent / reflect from here)
if __name__ == "__main__":
    result = app.invoke({
        "messages": [HumanMessage(content="Summarize https://arxiv.org/abs/2210.03629")],
        "revisions": 0,
    })
    # Same trap: messages[-1] is the reviewer verdict; the summary is the last AI message
    print(next(m.content for m in reversed(result["messages"]) if m.type == "ai"))
```

**What you learn**: what the framework abstracts (while loop, message structure, tool registration), how to define conditional branches with proper termination, how the reflection pattern lets an agent self-correct within a bounded number of rounds (no infinite loop).

**Note**: After Stage 4 we don't show LangGraph state internals again — later stages treat the LangGraph agent as a black box.

---

## Stage 5 — Claude Code Project Skill

> This step is **not** Python — it's repackaging the logic from Stages 1-4 as a Claude Code **project skill** that Claude loads natively. With a clear `description`, Claude will auto-trigger it when the user mentions a relevant request.

In your repo, create:

```
your-repo/
└── .claude/
    └── skills/
        └── paper-summary/
            └── SKILL.md
```

`SKILL.md` content:

```markdown
---
name: paper-summary
description: Summarize arXiv papers. Trigger when the user pastes an arXiv URL, mentions a paper ID (e.g. 2210.03629), or asks "summarize this paper / 摘要論文". Output: 3-paragraph summary + 5 keywords + differences from mainstream.
---

# Paper Summary Skill

## What this does
Summarize an arXiv paper into 3 structured paragraphs + keywords + difference points.

## When Claude should use this
The user:
- Pastes an arXiv URL (`https://arxiv.org/abs/...` or `arxiv.org/pdf/...`)
- Mentions a specific paper (title or ID) and asks for a summary
- Asks "how does this paper differ from other approaches"

## How to do it
1. Fetch paper content from the URL (use Claude Code's built-in WebFetch tool; or Read tool if a PDF is attached)
2. Apply this prompt structure:
   - Motivation (≤60 words)
   - Method (≤60 words)
   - Results (≤60 words)
   - 5 English keywords
   - 2-3 differences from mainstream
3. If something isn't stated, say "not stated in the paper" — never fabricate

## References
- `references/example-summaries.md` — 3 example outputs in the target style
```

Once placed, **open Claude Code in this repo** — project-level skills auto-load (no install command needed). Claude triggers the skill when the user's input matches the `description`.

To verify it works: paste `https://arxiv.org/abs/2210.03629` in a Claude Code session, see whether Claude responds in your defined format.

**What you learn**: the difference between project skills and plugin marketplace skills (this one is project-level, active as soon as you're in the repo; plugins are a separate distribution layer); `description` is the discovery mechanism (not a magic `trigger_phrases` field); how `references/` extends a skill with longer examples.

**Going further**: if you want to package this skill as a shareable plugin (so others can install it in their own Claude Code), see [Stage 5.4 Plugins & Marketplaces](../stages/05-claude-code-ecosystem.en.md#54--plugins--marketplaces). This walkthrough doesn't cover plugin packaging.

---

## Stage 6 — RAG Memory

Make the agent **remember papers it has seen**, comparing new ones against the past.

```python
# step6_memory.py
import chromadb
from chromadb.utils import embedding_functions
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-5")

# Local vector DB
chroma = chromadb.PersistentClient(path="./paper_memory")
embed_fn = embedding_functions.DefaultEmbeddingFunction()
collection = chroma.get_or_create_collection(
    name="papers",
    embedding_function=embed_fn,
)

def store_paper(arxiv_id: str, summary: str):
    """Store the summary in the vector DB. upsert, not add: re-running the same
    paper should overwrite it rather than be silently ignored."""
    collection.upsert(
        documents=[summary],
        ids=[arxiv_id],
        metadatas=[{"arxiv_id": arxiv_id}],
    )

def find_similar(query_summary: str, top_k: int = 3) -> list[dict]:
    """Find top 3 most similar past papers."""
    results = collection.query(query_texts=[query_summary], n_results=top_k)
    return [
        {"id": id_, "summary": doc}
        for id_, doc in zip(results["ids"][0], results["documents"][0])
    ]

# Modify Stage 4's agent — add a compare_with_memory step:
def compare_with_memory(state):
    # This node runs after reflect, so messages[-1] is reflect's "[Reviewer verdict: …]"
    # message, not the summary. Walk back to the last AI message for the agent output.
    new_summary = next(m.content for m in reversed(state["messages"]) if m.type == "ai")
    similar = find_similar(new_summary, top_k=3)
    
    if not similar:
        # Store first, then return. On the first paper the DB is empty, so an
        # early return here means store_paper is never reached and the memory
        # stays empty forever.
        store_paper(arxiv_id=state["arxiv_id"], summary=new_summary)
        return {"comparison": "(no related papers in DB yet — this is the first one)"}
    
    compare_prompt = f"""New paper summary: {new_summary}
    
Top 3 similar papers in DB:
{chr(10).join(f"- {p['id']}: {p['summary'][:200]}" for p in similar)}

List 2-3 unique contributions of the new paper not covered above."""
    
    response = llm.invoke(compare_prompt)
    
    # Store new paper in memory
    store_paper(arxiv_id=state["arxiv_id"], summary=new_summary)
    
    return {"comparison": response.content}
```

Wire `compare_with_memory` into the Stage 4 graph:

```python
# step6_memory.py (continued)
from step4_langgraph import State, react_agent, reflect, should_continue, MAX_REVISIONS
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

# State only declares messages / revisions, and LangGraph drops any key it
# does not know about. compare_with_memory returns `comparison`, so that key
# needs a slot in the schema — otherwise the LLM call is billed and discarded.
class MemoryState(State):
    arxiv_id: str      # key used to store into the vector DB; don't hardcode it
    comparison: str    # output of compare_with_memory

graph = StateGraph(MemoryState)
graph.add_node("agent", react_agent)
graph.add_node("reflect", reflect)
graph.add_node("compare", compare_with_memory)  # the new node
graph.add_edge("agent", "reflect")
graph.add_conditional_edges("reflect", should_continue, {"agent": "agent", END: "compare"})
graph.add_edge("compare", END)
graph.set_entry_point("agent")
app_with_memory = graph.compile()

# Run it (arxiv_id is required: store_paper uses it as the vector-DB key)
if __name__ == "__main__":
    result = app_with_memory.invoke({
        "messages": [HumanMessage(content="Summarize https://arxiv.org/abs/2210.03629")],
        "revisions": 0,
        "arxiv_id": "2210.03629",
    })
    print(result["comparison"])   # read comparison, not messages[-1]
```

**What you learn**: how to use a vector DB, embeddings + similarity queries, taking an agent from "stateless" to "stateful," persistent storage design, and how to extend a graph with a new node without rewriting earlier logic.

---

## Stage 7 — Eval + Observability + Deploy

### 7.1 Eval (`promptfoo`)

> **Install**: `npm install -g promptfoo`

Promptfoo's Python provider expects a callable function, not a module variable. So wrap a thin provider:

```python
# eval_provider.py
"""Promptfoo Python provider — function called by promptfoo."""
from step2_paper_summary import SYSTEM_PROMPT
from step3_tool_use import run_agent  # ReAct loop from Stage 3


def call_api(prompt: str, options: dict, context: dict) -> dict:
    """Promptfoo passes vars (context['vars']) + prompt."""
    paper_url = context["vars"]["paper_url"]
    output = run_agent(f"Summarize this paper: {paper_url}")
    return {"output": output}
```

```yaml
# promptfooconfig.yaml
prompts:
  - "Summarize: {{paper_url}}"

providers:
  - id: file://eval_provider.py
    label: paper-summary-agent

tests:
  - description: "ReAct paper"
    vars:
      paper_url: "https://arxiv.org/abs/2210.03629"
    assert:
      - type: contains
        value: "Reasoning"
      - type: llm-rubric
        value: "Output contains 5 English keywords, each paragraph ≤ 60 words"
  - description: "RAG paper"
    vars:
      paper_url: "https://arxiv.org/abs/2104.08663"
    assert:
      - type: contains
        value: "retrieval"
```

Run: `promptfoo eval && promptfoo view`

### 7.2 Observability (`langfuse`)

> **Install**: `pip install langfuse`
> **Env vars** (apply at [cloud.langfuse.com](https://cloud.langfuse.com)):
> ```bash
> export LANGFUSE_PUBLIC_KEY="pk-lf-..."
> export LANGFUSE_SECRET_KEY="sk-lf-..."
> export LANGFUSE_HOST="https://cloud.langfuse.com"  # or your self-hosted URL
> ```

```python
# step7_observability.py
# observe moved to the top-level package in langfuse **3.0**; only 2.x used
# `from langfuse.decorators import observe`. Both 3.x and 4.x use the line below —
# switch back to the old path only if you are pinned to 2.x.
from langfuse import observe
from step3_tool_use import run_agent  # agent from earlier stages

@observe(name="paper-summary-agent")
def run_paper_agent(arxiv_url: str) -> str:
    return run_agent(f"Summarize {arxiv_url}")

if __name__ == "__main__":
    out = run_paper_agent("https://arxiv.org/abs/2210.03629")
    print(out)
```

After running, view per-call trace, cost, latency, and tool use in the Langfuse dashboard.

### 7.3 Deploy (Docker + FastAPI)

> **Install**: `pip install fastapi uvicorn pydantic`

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from step7_observability import run_paper_agent  # the Langfuse-wrapped version

app = FastAPI()

class PaperRequest(BaseModel):
    arxiv_url: str

@app.post("/summarize")
def summarize(req: PaperRequest):
    return {"summary": run_paper_agent(req.arxiv_url)}
```

```text
# requirements.txt
anthropic
requests
langgraph
langchain-anthropic
langchain-core
chromadb
langfuse
fastapi
uvicorn
pydantic
```

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t paper-summary-bot .
docker run -p 8000:8000 \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -e LANGFUSE_PUBLIC_KEY=$LANGFUSE_PUBLIC_KEY \
  -e LANGFUSE_SECRET_KEY=$LANGFUSE_SECRET_KEY \
  paper-summary-bot
# Or deploy to Cloud Run / Fly.io / Railway / your own K8s
```

**What you learn**: eval as regression test, observability for debugging deployed agents, taking an agent from script to service.

---

## ✅ After the full walkthrough you should be able to:

- [ ] Build a ReAct agent from scratch (Stage 3)
- [ ] Rewrite with a framework and add advanced patterns (Stage 4)
- [ ] Package an agent as a Claude Code skill (Stage 5)
- [ ] Add RAG memory to make the agent stateful (Stage 6)
- [ ] Write evals + connect observability + deploy (Stage 7)

This walkthrough is longer than a single framework exercise because it shows the same agent growing one layer at a time. Each step should still run and be checkable on its own.

---

## ➡️ Next: return this Agent to the main route

1. Read [Stage 7.5 — Advanced Agentic Concepts](../stages/07.5-advanced-agentic-concepts.en.md) and choose only the advanced ideas this system actually needs.
2. Then read [Stage 8 — Agent Interfaces](../stages/08-agent-interfaces.en.md) to choose Search, Browser Use, Computer Use, or a Sandbox and add safety boundaries.
3. To choose a different route, return to the [main-path README](../README.en.md).

---

## 🚧 Advanced extensions

If you want to go deeper, this paper-summary-bot can extend into:

- **Multi-agent paper review**: two agents play supportive vs adversarial reviewer, while a third plays area chair → [researcher path](../branches/for-researcher.en.md)
- **Conference report generator**: given a conference proceedings URL, produce per-track high-level summaries → [knowledge-worker path](../branches/for-knowledge-worker.en.md)
- **Topic trend tracker**: scan arXiv weekly, compare new papers with existing Memory, and produce a weekly digest → [everyday-user path](../branches/for-everyday-users.en.md)

Each maps to a specialized branch.

---

## 💡 Maintaining this walkthrough

This example will evolve over time — SDK interfaces change, frameworks evolve, best practices shift. If something breaks:

1. Open an issue with the exact error + your env (Python version, package versions)
2. PR fixes should explain "why this change"
3. Don't refactor this file to demo only your favorite framework — this is a **multi-framework learning** example
