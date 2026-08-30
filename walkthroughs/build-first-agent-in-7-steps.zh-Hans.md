> [繁體中文](./build-first-agent-in-7-steps.md) | **简体中文** | [English](./build-first-agent-in-7-steps.en.md)

# 7 步打造你的第一个 AI Agent

> [← 回主路线 README](../README.zh-Hans.md)

> 📌 **这份是给 Track B（Agent Builder）的**——教你**从零写**一个 agent。
> 走 [Track A（CLI Power User）](../tracks/cli/A1-cli-intro.zh-Hans.md) 的人**不需要跑**这份；但读过之后对“**agent 从 LLM API 到 production 怎么一步步组起来**”会有更深的理解，可作为 optional 进阶补充。

这是一份**跨 7 个 stage 的具体 walkthrough**——同一个 agent，从 Stage 1 写到 Stage 7，每个 stage 都附可执行的代码骨架。

> **怎么读这份**：每一节都是上一节的延伸。后面 stage 的 snippet 默认你已经有前面 stage 的文件在同一个文件夹。要实际跑：
> 1. 照 Stage 0 设好环境
> 2. 每个 stage 开新文件（`step1_*.py`、`step2_*.py`...）
> 3. 后面 stage 用 `from step1_xxx import ...` 引用前面写的东西
>
> 所有依赖一次装完：`pip install anthropic openai requests beautifulsoup4 langgraph langchain-anthropic langchain-core chromadb langfuse fastapi uvicorn pydantic`

要做的 agent：**Paper Summary Bot** — 给定一个 arXiv 论文 URL，输出 3 段摘要 + 5 个关键词 + 跟相关论文的比较。

每个 Stage 都会给同一个 agent **加一层能力**。最后它会使用多个 LLM、记住需要的数据，也能部署成服务。

---

## 📋 全程概览

| Stage | 你会加的能力 | 这一步有多大 |
|---|---|---|
| 0 | 环境准备（Python、API key、git） | 准备工作 |
| 1 | 第一次调用 LLM API | 小 |
| 2 | 写一个专业的 prompt | 小 |
| 3 | Tool use：自动抓取 arXiv 论文 | 中 |
| 4 | 用 framework 重写，加上反思检查（reflection） | 中；framework 会包住部分细节 |
| 5 | 包成 Claude Code Skill | 一份配置文件 + 一个小程序 |
| 6 | 加 RAG 和 Memory：找回旧论文，再做比较 | 中 |
| 7 | 加 Eval（评测）、Observability（运行记录）和 Deploy（部署） | 较大 |

**最后成果**：一个从最小 Python 程序一路长成可评测、可查看运行记录、可部署服务的具体例子。

---

## Stage 0 — 环境准备

```bash
# 安装 Python 3.11+
python --version

# 建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装所有 stage 会用到的套件（一次装完，后面 stage 不会再 pip install）
pip install anthropic openai requests beautifulsoup4 
            langgraph langchain-anthropic langchain-core 
            chromadb langfuse fastapi uvicorn pydantic

# Claude API key（去 console.anthropic.com 申请）
export ANTHROPIC_API_KEY="sk-ant-..."

# 建 repo
mkdir paper-summary-bot && cd paper-summary-bot
git init
echo ".env
.venv/
__pycache__/" > .gitignore
```

**检查点**：你应该能跑 `python -c "from anthropic import Anthropic; print('OK')"` 而不报错。

---

## Stage 1 — 第一次调用 LLM

```python
# step1_hello_llm.py
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=500,
    messages=[{
        "role": "user",
        "content": "请用 3 句话介绍什么是 ReAct agent。"
    }]
)

print(response.content[0].text)
print(f"\n--- Tokens: input={response.usage.input_tokens}, "
      f"output={response.usage.output_tokens} ---")
```

跑：`python step1_hello_llm.py`

**学到什么**：API call 的长相、`messages` 结构、`usage` 怎么算 token。

---

## Stage 2 — 写专业的 prompt

```python
# step2_paper_summary.py
from anthropic import Anthropic

client = Anthropic()

SYSTEM_PROMPT = """你是学术论文摘要助手。你的任务：

1. 用 3 段摘要描述论文：(a) 动机、(b) 方法、(c) 结果。
2. 列出 5 个关键词。
3. 用条列点出 2-3 个跟主流方法的差别。

格式要求：
- 每段摘要 ≤ 60 字
- 关键词用英文（technical term）
- 整体 300 字以内
- 不要瞎掰；不知道就说「论文没提到」"""

PAPER_TEXT = """[论文 abstract 贴这里]"""

# 跑（包在 __main__ guard 里：后面的 stage 会 import 这个文件拿 SYSTEM_PROMPT，
#   没有 guard 的话，光是 import 就会送出一次真实 API 调用、而且是拿占位字符串去问）
if __name__ == "__main__":
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": PAPER_TEXT}]
    )
    print(response.content[0].text)
```

**学到什么**：system prompt 跟 user message 分工、明确格式要求、防 hallucinate 的“不知道就说没提到”。

---

## Stage 3 — Tool use：自动抓论文

```python
# step3_tool_use.py
import requests
from anthropic import Anthropic
from step2_paper_summary import SYSTEM_PROMPT  # 上一个 stage 写的

client = Anthropic()

# 定义 tool
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
    """Tool 实现。"""
    arxiv_id = arxiv_url.split("/")[-1].replace(".pdf", "")
    api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    r = requests.get(api_url)
    # 简化：实际要 parse XML
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
            system=SYSTEM_PROMPT,  # 从 Stage 2 来
        )
        
        # 没有更多 tool 要调用 → done
        if response.stop_reason == "end_turn":
            return response.content[-1].text
        
        # 处理 tool call
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

# 跑（同样要 guard：Stage 7 的 eval_provider / step7 都会 import run_agent，
#   没 guard 的话每次 import 都会多跑一轮完整 agent）
if __name__ == "__main__":
    print(run_agent("摘要这篇论文：https://arxiv.org/abs/2210.03629"))
```

**学到什么**：tool schema 怎么写、ReAct loop 怎么运作、`stop_reason` 怎么判定结束、tool_result 怎么回传给 LLM。

**这是 Stage 3 最大的跃进——你的程序从“调用 LLM”变成“LLM 调用你的程序”。**

---

## Stage 4 — 用 framework + 加 reflection

> **装套件**：`pip install langgraph langchain-anthropic langchain-core`

用 LangGraph 重写，加一个“self-review”node：

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
    # 同 Stage 3 的实现
    import requests
    arxiv_id = arxiv_url.split("/")[-1].replace(".pdf", "")
    r = requests.get(f"http://export.arxiv.org/api/query?id_list={arxiv_id}")
    return r.text[:5000]

class State(TypedDict):
    messages: Annotated[list, add_messages]
    revisions: int  # 防止无限 loop

llm = ChatAnthropic(model="claude-sonnet-5")
react_agent = create_react_agent(llm, tools=[fetch_arxiv])

MAX_REVISIONS = 2

def reflect(state: State) -> State:
    """让 LLM 评估前一轮的摘要，并决定是否要再改。"""
    last_summary = state["messages"][-1].content
    
    # 用一个明确的 yes/no 判定，不要靠关键字 match
    review_prompt = (
        f"以下摘要是否符合：3 段、各 ≤60 字、5 个英文关键词、不瞎掰？\n\n"
        f"{last_summary}\n\n"
        "请只回答 PASS 或 NEEDS_REVISION，不要解释。"
    )
    verdict = llm.invoke(review_prompt).content.strip().upper()
    
    return {
        "messages": [HumanMessage(content=f"[Reviewer 判定: {verdict}]")],
        "revisions": state.get("revisions", 0) + 1,
    }

def should_continue(state: State) -> str:
    """判断下一步去 agent 还是 END。"""
    last_msg = state["messages"][-1].content
    if state["revisions"] >= MAX_REVISIONS:
        return END  # 达到上限，无条件退出
    if "NEEDS_REVISION" in last_msg:
        return "agent"  # 回去重做
    return END  # PASS 就退出

# 组 graph
graph = StateGraph(State)
graph.add_node("agent", react_agent)
graph.add_node("reflect", reflect)
graph.add_edge("agent", "reflect")
graph.add_conditional_edges("reflect", should_continue, {"agent": "agent", END: END})
graph.set_entry_point("agent")
app = graph.compile()

# 跑（同样要 guard：Stage 6 会 import 这个文件的 State / react_agent / reflect）
if __name__ == "__main__":
    result = app.invoke({
        "messages": [HumanMessage(content="摘要 https://arxiv.org/abs/2210.03629")],
        "revisions": 0,
    })
    # 同理：messages[-1] 是 reviewer 判定，要看摘要得往回找最后一则 AI 消息
    print(next(m.content for m in reversed(result["messages"]) if m.type == "ai"))
```

**学到什么**：framework 抽掉的东西（while loop、message 结构、tool 注册）、graph 怎么定义条件分支跟正确的终止条件、reflection pattern 怎么让 agent 在限定回合内 self-correct（不会无限 loop）。

**注意**：Stage 4 之后不再示范 LangGraph 内部 state 细节——后面 stage 把 LangGraph agent 当黑盒用即可。

---

## Stage 5 — 包成 Claude Code Project Skill

> 这一步**不是** Python，是把前面 Stage 1-4 的逻辑，重新包成 Claude Code 自己会加载的 **project skill**。`description` 写得清楚的话，Claude 会在用户提到相关需求时自动触发。

在你 repo 内创建：

```
your-repo/
└── .claude/
    └── skills/
        └── paper-summary/
            └── SKILL.md
```

`SKILL.md` 内容：

```markdown
---
name: paper-summary
description: 摘要 arXiv 论文。当用户贴 arXiv URL、提到论文 ID（如 2210.03629），或要求「summarize this paper / 摘要论文」时触发。输出 3 段摘要 + 5 个关键词 + 与主流方法差别。
---

# Paper Summary Skill

## What this does
摘要 arXiv 论文成结构化的 3 段 + 关键词 + 差异点。

## When Claude should use this
用户：
- 贴 arXiv URL（`https://arxiv.org/abs/...` 或 `arxiv.org/pdf/...`）
- 提到具体论文（标题或 ID）并要 summary / 摘要 / 要点
- 问「这篇论文跟其他方法差在哪」

## How to do it
1. 从 URL 抓 paper 内容（用 Claude Code 内建的 WebFetch tool；或在用户贴了 PDF 时用 Read tool）
2. 套用以下 prompt 结构：
   - 动机（≤60 字）
   - 方法（≤60 字）
   - 结果（≤60 字）
   - 5 个英文 keyword
   - 2-3 点跟主流方法的差别
3. 不确定的内容回「论文没提到」，不要瞎掰

## References
- `references/example-summaries.md` — 3 个范例输出，照这个风格写
```

放好后，**在这个 repo 里开 Claude Code**——project-level skill 会自动加载（不需要安装指令）。Claude 看到 description 跟用户输入吻合就会用这个 skill。

验证它是否生效：在 Claude Code 对话里贴 `https://arxiv.org/abs/2210.03629`，看 Claude 是不是按你定义的格式响应。

**学到什么**：project skill 跟 plugin marketplace skill 的差别（这个是 project-level、进到 repo 就生效；plugin 是另一个层级的安装）、`description` 是触发机制（不是 magic 的 trigger_phrases 字段）、references/ 怎么支持更长的 example。

**进阶**：如果想把这个 skill 包成可分享的 plugin（让别人也能装在自己的 Claude Code），参考 [Stage 5.4 Plugins & Marketplaces](../stages/05-claude-code-ecosystem.zh-Hans.md#54--plugins-与-marketplaces)。本 walkthrough 不展开 plugin 打包流程。

---

## Stage 6 — 加 RAG memory

让 agent **记得它看过的论文**，新论文进来时跟过去的比较。

```python
# step6_memory.py
import chromadb
from chromadb.utils import embedding_functions
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-5")

# 开一个本地 vector DB
chroma = chromadb.PersistentClient(path="./paper_memory")
embed_fn = embedding_functions.DefaultEmbeddingFunction()
collection = chroma.get_or_create_collection(
    name="papers",
    embedding_function=embed_fn,
)

def store_paper(arxiv_id: str, summary: str):
    """把摘要存进 vector DB。用 upsert：同一篇重跑时覆盖，
    而不是像 add() 那样被静默忽略。"""
    collection.upsert(
        documents=[summary],
        ids=[arxiv_id],
        metadatas=[{"arxiv_id": arxiv_id}],
    )

def find_similar(query_summary: str, top_k: int = 3) -> list[dict]:
    """找跟新论文最像的 3 篇。"""
    results = collection.query(query_texts=[query_summary], n_results=top_k)
    return [
        {"id": id_, "summary": doc}
        for id_, doc in zip(results["ids"][0], results["documents"][0])
    ]

# 修改 Stage 4 的 agent，加上 compare_with_memory step：
def compare_with_memory(state):
    # compare 这个 node 跑在 reflect 之后，所以 messages[-1] 是 reflect 塞进去的
    # “[Reviewer 判定: …]”，不是摘要。要往回找最后一则 AI 消息才是 agent 的产出。
    new_summary = next(m.content for m in reversed(state["messages"]) if m.type == "ai")
    similar = find_similar(new_summary, top_k=3)
    
    if not similar:
        # 先存再返回。第一篇论文进来时 DB 是空的，如果这里直接 return，
        # store_paper 永远不会被调用，memory 会一直是空的。
        store_paper(arxiv_id=state["arxiv_id"], summary=new_summary)
        return {"comparison": "（数据库里没有相关论文，这是第一篇）"}
    
    compare_prompt = f"""新论文摘要：{new_summary}
    
数据库中最像的 3 篇：
{chr(10).join(f"- {p['id']}: {p['summary'][:200]}" for p in similar)}

请点出新论文的 2-3 个 unique contribution（跟以上不重叠的部分）。"""
    
    response = llm.invoke(compare_prompt)
    
    # 存新论文进 memory
    store_paper(arxiv_id=state["arxiv_id"], summary=new_summary)
    
    return {"comparison": response.content}
```

把 `compare_with_memory` 接进 Stage 4 的 graph：

```python
# step6_memory.py 接续上面
from step4_langgraph import State, react_agent, reflect, should_continue, MAX_REVISIONS
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

# State 只声明 messages / revisions，而 LangGraph 会把没声明的 key 丢掉。
# compare_with_memory 要返回 comparison，就得先在 schema 里有位子，
# 否则那次 LLM 调用照样计费、结果却拿不到。
class MemoryState(State):
    arxiv_id: str      # 存进 vector DB 用的 key；不要写死
    comparison: str    # compare_with_memory 的输出

graph = StateGraph(MemoryState)
graph.add_node("agent", react_agent)
graph.add_node("reflect", reflect)
graph.add_node("compare", compare_with_memory)  # 新加的 node
graph.add_edge("agent", "reflect")
graph.add_conditional_edges("reflect", should_continue, {"agent": "agent", END: "compare"})
graph.add_edge("compare", END)
graph.set_entry_point("agent")
app_with_memory = graph.compile()

# 跑（arxiv_id 一定要传：store_paper 拿它当 vector DB 的 key）
if __name__ == "__main__":
    result = app_with_memory.invoke({
        "messages": [HumanMessage(content="摘要 https://arxiv.org/abs/2210.03629")],
        "revisions": 0,
        "arxiv_id": "2210.03629",
    })
    print(result["comparison"])   # 注意读的是 comparison，不是 messages[-1]
```

**学到什么**：vector DB 怎么用、embedding 跟相似度查询、把 agent 从“stateless”变成“有记忆”、persistent storage 的设计、graph 怎么扩新 node 而不重写前面的逻辑。

---

## Stage 7 — Eval + Observability + Deploy

### 7.1 Eval (`promptfoo`)

> **装**：`npm install -g promptfoo`

Promptfoo 的 Python provider 要的是“可调用的 function”，不是 module 变量。所以先包一个薄 wrapper：

```python
# eval_provider.py
"""Promptfoo Python provider — 给 promptfoo 调用的 function。"""
from step2_paper_summary import SYSTEM_PROMPT
from step3_tool_use import run_agent  # Stage 3 写的 ReAct loop


def call_api(prompt: str, options: dict, context: dict) -> dict:
    """Promptfoo 会传 vars（context['vars']）+ prompt 进来。"""
    paper_url = context["vars"]["paper_url"]
    output = run_agent(f"请摘要这篇论文：{paper_url}")
    return {"output": output}
```

```yaml
# promptfooconfig.yaml
prompts:
  - "请摘要：{{paper_url}}"

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
        value: "回应包含 5 个英文关键词、每段不超过 60 字"
  - description: "RAG paper"
    vars:
      paper_url: "https://arxiv.org/abs/2104.08663"
    assert:
      - type: contains
        value: "retrieval"
```

跑：`promptfoo eval && promptfoo view`

### 7.2 Observability (`langfuse`)

> **装**：`pip install langfuse`
> **环境变量**（去 [cloud.langfuse.com](https://cloud.langfuse.com) 申请）：
> ```bash
> export LANGFUSE_PUBLIC_KEY="pk-lf-..."
> export LANGFUSE_SECRET_KEY="sk-lf-..."
> export LANGFUSE_HOST="https://cloud.langfuse.com"  # 或自架的 URL
> ```

```python
# step7_observability.py
# langfuse **3.0** 起 observe 就在包顶层；只有 2.x 是 `from langfuse.decorators import observe`。
# 3.x / 4.x 都用下面这行；装到 2.x 才需要改回旧路径。
from langfuse import observe
from step3_tool_use import run_agent  # 前面 stage 的 agent

@observe(name="paper-summary-agent")
def run_paper_agent(arxiv_url: str) -> str:
    return run_agent(f"摘要 {arxiv_url}")

if __name__ == "__main__":
    out = run_paper_agent("https://arxiv.org/abs/2210.03629")
    print(out)
```

跑完之后到 Langfuse dashboard 看每次调用的 trace、cost、latency、tool use。

### 7.3 Deploy（Docker + FastAPI）

> **装**：`pip install fastapi uvicorn pydantic`

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from step7_observability import run_paper_agent  # 用 Langfuse 包过的版本

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
# 或 deploy 到 Cloud Run / Fly.io / Railway / 自家 K8s
```

**学到什么**：eval 怎么当回归测试、observability 怎么让你 debug production agent、把 agent 从 script 变成 service。

---

## ✅ 完整 walkthrough 之后你应该能：

- [ ] 从零打造 ReAct agent（Stage 3）
- [ ] 用 framework 重写并加进阶 pattern（Stage 4）
- [ ] 把 agent 包成 Claude Code skill（Stage 5）
- [ ] 加 RAG memory 让 agent 变成有状态（Stage 6）
- [ ] 写 eval + 接 observability + deploy（Stage 7）

这份 walkthrough 比单一 framework 小练习长，因为它要让你看见同一个 agent 怎么一层一层长大；每一步仍应该能单独运行与检查。

---

## ➡️ 下一站：把这个 Agent 接回主路线

1. 读 [Stage 7.5 — 进阶 Agentic 概念](../stages/07.5-advanced-agentic-concepts.zh-Hans.md)，给刚完成的系统选择真正需要的进阶做法。
2. 再读 [Stage 8 — Agent 操作界面](../stages/08-agent-interfaces.zh-Hans.md)，决定它需要 Search、Browser Use、Computer Use 还是 Sandbox，并补上安全边界。
3. 想改走另一条路时，回到[主路线 README](../README.zh-Hans.md)。

---

## 🚧 进阶延伸

如果你想再玩更深，这个 paper-summary-bot 可以延伸成：

- **Multi-agent paper review**：两个 agent 分别当 supportive reviewer 跟 adversarial reviewer，第三个 agent 当 area chair → [研究人员路径](../branches/for-researcher.zh-Hans.md)
- **Conference report generator**：给定一个 conference proceedings URL，产出每个 track 的高层摘要 → [知识工作者路径](../branches/for-knowledge-worker.zh-Hans.md)
- **同主题论文趋势追踪**：每周扫 arXiv，找新论文跟现有 Memory 比较，产出 weekly digest → [日常用户路径](../branches/for-everyday-users.zh-Hans.md)

每条都对应一个 specialized branch。

---

## 💡 维护这个 walkthrough

这个范例会随时间更新——SDK 接口变化、framework 演进、最佳实践改变。如果你发现某段代码跑不起来：

1. 先在 issue 里回报具体错误信息 + 你的环境（Python 版本、套件版本）
2. PR 修正请说明“为什么这样改”
3. 不要把这份文件改成只 demo 你最熟悉的 framework——这份是给**多元 framework 学习**用的
