> **繁體中文** | [简体中文](./build-first-agent-in-7-steps.zh-Hans.md) | [English](./build-first-agent-in-7-steps.en.md)

# 7 步打造你的第一個 AI Agent

> [← 回主路線 README](../README.md)

> 📌 **這份是給 Track B（Agent Builder）的**——教你**從零寫**一個 agent。
> 走 [Track A（CLI Power User）](../tracks/cli/A1-cli-intro.md) 的人**不需要跑**這份；但讀過之後對「**agent 從 LLM API 到 production 怎麼一步步組起來**」會有更深的理解，可作為 optional 進階補充。

這是一份**跨 7 個 stage 的具體 walkthrough**——同一個 agent，從 Stage 1 寫到 Stage 7，每個 stage 都附可執行的程式碼骨架。

> **怎麼讀這份**：每一節都是上一節的延伸。後面 stage 的 snippet 預設你已經有前面 stage 的檔案在同一個資料夾。要實際跑：
> 1. 照 Stage 0 設好環境
> 2. 每個 stage 開新檔案（`step1_*.py`、`step2_*.py`...）
> 3. 後面 stage 用 `from step1_xxx import ...` 引用前面寫的東西
>
> 所有依賴一次裝完：`pip install anthropic openai requests beautifulsoup4 langgraph langchain-anthropic langchain-core chromadb langfuse fastapi uvicorn pydantic`

要做的 agent：**Paper Summary Bot** — 給定一個 arXiv 論文 URL，輸出 3 段摘要 + 5 個關鍵詞 + 跟相關論文的比較。

每個 Stage 都會替同一個 agent **加一層能力**。最後它會使用多個 LLM、記得需要的資料，也能部署成服務。

---

## 📋 全程概覽

| Stage | 你會加的能力 | 這一步有多大 |
|---|---|---|
| 0 | 環境準備（Python、API key、git） | 準備工作 |
| 1 | 第一次呼叫 LLM API | 小 |
| 2 | 寫一個專業的 prompt | 小 |
| 3 | Tool use：自動抓取 arXiv 論文 | 中 |
| 4 | 用 framework 重寫，加上反思檢查（reflection） | 中；framework 會包住部分細節 |
| 5 | 包成 Claude Code Skill | 一份設定檔 + 一個小程式 |
| 6 | 加 RAG 與 Memory：找回舊論文，再做比較 | 中 |
| 7 | 加 Eval（評測）、Observability（執行紀錄）與 Deploy（部署） | 較大 |

**最後成果**：一個從最小 Python 程式一路長成可評測、可查看執行紀錄、可部署服務的具體例子。

---

## Stage 0 — 環境準備

```bash
# 安裝 Python 3.11+
python --version

# 建虛擬環境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安裝所有 stage 會用到的套件（一次裝完，後面 stage 不會再 pip install）
pip install anthropic openai requests beautifulsoup4 \
            langgraph langchain-anthropic langchain-core \
            chromadb langfuse fastapi uvicorn pydantic

# Claude API key（去 console.anthropic.com 申請）
export ANTHROPIC_API_KEY="sk-ant-..."

# 建 repo
mkdir paper-summary-bot && cd paper-summary-bot
git init
echo ".env\n.venv/\n__pycache__/" > .gitignore
```

**檢查點**：你應該能跑 `python -c "from anthropic import Anthropic; print('OK')"` 而不報錯。

---

## Stage 1 — 第一次呼叫 LLM

```python
# step1_hello_llm.py
from anthropic import Anthropic

client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=500,
    messages=[{
        "role": "user",
        "content": "請用 3 句話介紹什麼是 ReAct agent。"
    }]
)

print(response.content[0].text)
print(f"\n--- Tokens: input={response.usage.input_tokens}, "
      f"output={response.usage.output_tokens} ---")
```

跑：`python step1_hello_llm.py`

**學到什麼**：API call 的長相、`messages` 結構、`usage` 怎麼算 token。

---

## Stage 2 — 寫專業的 prompt

```python
# step2_paper_summary.py
from anthropic import Anthropic

client = Anthropic()

SYSTEM_PROMPT = """你是學術論文摘要助手。你的任務：

1. 用 3 段摘要描述論文：(a) 動機、(b) 方法、(c) 結果。
2. 列出 5 個關鍵詞。
3. 用條列點出 2-3 個跟主流方法的差別。

格式要求：
- 每段摘要 ≤ 60 字
- 關鍵詞用英文（technical term）
- 整體 300 字以內
- 不要瞎掰；不知道就說「論文沒提到」"""

PAPER_TEXT = """[論文 abstract 貼這裡]"""

# 跑（包在 __main__ guard 裡：後面的 stage 會 import 這個檔案拿 SYSTEM_PROMPT，
#   沒有 guard 的話，光是 import 就會送出一次真實 API 呼叫、而且是拿佔位字串去問）
if __name__ == "__main__":
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=800,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": PAPER_TEXT}]
    )
    print(response.content[0].text)
```

**學到什麼**：system prompt 跟 user message 分工、明確格式要求、防 hallucinate 的「不知道就說沒提到」。

---

## Stage 3 — Tool use：自動抓論文

```python
# step3_tool_use.py
import requests
from anthropic import Anthropic
from step2_paper_summary import SYSTEM_PROMPT  # 上一個 stage 寫的

client = Anthropic()

# 定義 tool
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
    """Tool 實作。"""
    arxiv_id = arxiv_url.split("/")[-1].replace(".pdf", "")
    api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
    r = requests.get(api_url)
    # 簡化：實際要 parse XML
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
            system=SYSTEM_PROMPT,  # 從 Stage 2 來
        )
        
        # 沒有更多 tool 要呼叫 → done
        if response.stop_reason == "end_turn":
            return response.content[-1].text
        
        # 處理 tool call
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

# 跑（同樣要 guard：Stage 7 的 eval_provider / step7 都會 import run_agent，
#   沒 guard 的話每次 import 都會多跑一輪完整 agent）
if __name__ == "__main__":
    print(run_agent("摘要這篇論文：https://arxiv.org/abs/2210.03629"))
```

**學到什麼**：tool schema 怎麼寫、ReAct loop 怎麼運作、`stop_reason` 怎麼判定結束、tool_result 怎麼回傳給 LLM。

**這是 Stage 3 最大的躍進——你的程式從「呼叫 LLM」變成「LLM 呼叫你的程式」。**

---

## Stage 4 — 用 framework + 加 reflection

> **裝套件**：`pip install langgraph langchain-anthropic langchain-core`

用 LangGraph 重寫，加一個「self-review」node：

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
    # 同 Stage 3 的實作
    import requests
    arxiv_id = arxiv_url.split("/")[-1].replace(".pdf", "")
    r = requests.get(f"http://export.arxiv.org/api/query?id_list={arxiv_id}")
    return r.text[:5000]

class State(TypedDict):
    messages: Annotated[list, add_messages]
    revisions: int  # 防止無限 loop

llm = ChatAnthropic(model="claude-sonnet-5")
react_agent = create_react_agent(llm, tools=[fetch_arxiv])

MAX_REVISIONS = 2

def reflect(state: State) -> State:
    """讓 LLM 評估前一輪的摘要，並決定是否要再改。"""
    last_summary = state["messages"][-1].content
    
    # 用一個明確的 yes/no 判定，不要靠關鍵字 match
    review_prompt = (
        f"以下摘要是否符合：3 段、各 ≤60 字、5 個英文關鍵詞、不瞎掰？\n\n"
        f"{last_summary}\n\n"
        "請只回答 PASS 或 NEEDS_REVISION，不要解釋。"
    )
    verdict = llm.invoke(review_prompt).content.strip().upper()
    
    return {
        "messages": [HumanMessage(content=f"[Reviewer 判定: {verdict}]")],
        "revisions": state.get("revisions", 0) + 1,
    }

def should_continue(state: State) -> str:
    """判斷下一步去 agent 還是 END。"""
    last_msg = state["messages"][-1].content
    if state["revisions"] >= MAX_REVISIONS:
        return END  # 達到上限，無條件退出
    if "NEEDS_REVISION" in last_msg:
        return "agent"  # 回去重做
    return END  # PASS 就退出

# 組 graph
graph = StateGraph(State)
graph.add_node("agent", react_agent)
graph.add_node("reflect", reflect)
graph.add_edge("agent", "reflect")
graph.add_conditional_edges("reflect", should_continue, {"agent": "agent", END: END})
graph.set_entry_point("agent")
app = graph.compile()

# 跑（同樣要 guard：Stage 6 會 import 這個檔案的 State / react_agent / reflect）
if __name__ == "__main__":
    result = app.invoke({
        "messages": [HumanMessage(content="摘要 https://arxiv.org/abs/2210.03629")],
        "revisions": 0,
    })
    # 同理：messages[-1] 是 reviewer 判定，要看摘要得往回找最後一則 AI 訊息
    print(next(m.content for m in reversed(result["messages"]) if m.type == "ai"))
```

**學到什麼**：framework 抽掉的東西（while loop、message 結構、tool 註冊）、graph 怎麼定義條件分支跟正確的終止條件、reflection pattern 怎麼讓 agent 在限定回合內 self-correct（不會無限 loop）。

**注意**：Stage 4 之後不再示範 LangGraph 內部 state 細節——後面 stage 把 LangGraph agent 當黑盒用即可。

---

## Stage 5 — 包成 Claude Code Project Skill

> 這一步**不是** Python，是把前面 Stage 1-4 的邏輯，重新包成 Claude Code 自己會載入的 **project skill**。`description` 寫得清楚的話，Claude 會在使用者提到相關需求時自動觸發。

在你 repo 內建立：

```
your-repo/
└── .claude/
    └── skills/
        └── paper-summary/
            └── SKILL.md
```

`SKILL.md` 內容：

```markdown
---
name: paper-summary
description: 摘要 arXiv 論文。當使用者貼 arXiv URL、提到論文 ID（如 2210.03629），或要求「summarize this paper / 摘要論文」時觸發。輸出 3 段摘要 + 5 個關鍵詞 + 與主流方法差別。
---

# Paper Summary Skill

## What this does
摘要 arXiv 論文成結構化的 3 段 + 關鍵詞 + 差異點。

## When Claude should use this
使用者：
- 貼 arXiv URL（`https://arxiv.org/abs/...` 或 `arxiv.org/pdf/...`）
- 提到具體論文（標題或 ID）並要 summary / 摘要 / 重點
- 問「這篇論文跟其他方法差在哪」

## How to do it
1. 從 URL 抓 paper 內容（用 Claude Code 內建的 WebFetch tool；或在使用者貼了 PDF 時用 Read tool）
2. 套用以下 prompt 結構：
   - 動機（≤60 字）
   - 方法（≤60 字）
   - 結果（≤60 字）
   - 5 個英文 keyword
   - 2-3 點跟主流方法的差別
3. 不確定的內容回「論文沒提到」，不要瞎掰

## References
- `references/example-summaries.md` — 3 個範例輸出，照這個風格寫
```

放好後，**在這個 repo 裡開 Claude Code**——project-level skill 會自動載入（不需要安裝指令）。Claude 看到 description 跟使用者輸入吻合就會用這個 skill。

驗證它是否生效：在 Claude Code 對話裡貼 `https://arxiv.org/abs/2210.03629`，看 Claude 是不是按你定義的格式回應。

**學到什麼**：project skill 跟 plugin marketplace skill 的差別（這個是 project-level、進到 repo 就生效；plugin 是另一個層級的安裝）、`description` 是觸發機制（不是 magic 的 trigger_phrases 欄位）、references/ 怎麼支援更長的 example。

**進階**：如果想把這個 skill 包成可分享的 plugin（讓別人也能裝在自己的 Claude Code），參考 [Stage 5.4 Plugins & Marketplaces](../stages/05-claude-code-ecosystem.md#54--plugins-與-marketplaces)。本 walkthrough 不展開 plugin 打包流程。

---

## Stage 6 — 加 RAG memory

讓 agent **記得它看過的論文**，新論文進來時跟過去的比較。

```python
# step6_memory.py
import chromadb
from chromadb.utils import embedding_functions
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model="claude-sonnet-5")

# 開一個本地 vector DB
chroma = chromadb.PersistentClient(path="./paper_memory")
embed_fn = embedding_functions.DefaultEmbeddingFunction()
collection = chroma.get_or_create_collection(
    name="papers",
    embedding_function=embed_fn,
)

def store_paper(arxiv_id: str, summary: str):
    """把摘要存進 vector DB。用 upsert：同一篇重跑時覆蓋，
    而不是像 add() 那樣被靜默忽略。"""
    collection.upsert(
        documents=[summary],
        ids=[arxiv_id],
        metadatas=[{"arxiv_id": arxiv_id}],
    )

def find_similar(query_summary: str, top_k: int = 3) -> list[dict]:
    """找跟新論文最像的 3 篇。"""
    results = collection.query(query_texts=[query_summary], n_results=top_k)
    return [
        {"id": id_, "summary": doc}
        for id_, doc in zip(results["ids"][0], results["documents"][0])
    ]

# 修改 Stage 4 的 agent，加上 compare_with_memory step：
def compare_with_memory(state):
    # compare 這個 node 跑在 reflect 之後，所以 messages[-1] 是 reflect 塞進去的
    # 「[Reviewer 判定: …]」，不是摘要。要往回找最後一則 AI 訊息才是 agent 的產出。
    new_summary = next(m.content for m in reversed(state["messages"]) if m.type == "ai")
    similar = find_similar(new_summary, top_k=3)
    
    if not similar:
        # 先存再回傳。第一篇論文進來時 DB 是空的，如果這裡直接 return，
        # store_paper 永遠不會被呼叫，memory 會一直是空的。
        store_paper(arxiv_id=state["arxiv_id"], summary=new_summary)
        return {"comparison": "（資料庫裡沒有相關論文，這是第一篇）"}
    
    compare_prompt = f"""新論文摘要：{new_summary}
    
資料庫中最像的 3 篇：
{chr(10).join(f"- {p['id']}: {p['summary'][:200]}" for p in similar)}

請點出新論文的 2-3 個 unique contribution（跟以上不重疊的部分）。"""
    
    response = llm.invoke(compare_prompt)
    
    # 存新論文進 memory
    store_paper(arxiv_id=state["arxiv_id"], summary=new_summary)
    
    return {"comparison": response.content}
```

把 `compare_with_memory` 接進 Stage 4 的 graph：

```python
# step6_memory.py 接續上面
from step4_langgraph import State, react_agent, reflect, should_continue, MAX_REVISIONS
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage

# State 只宣告 messages / revisions，而 LangGraph 會把沒宣告的 key 丟掉。
# compare_with_memory 要回傳 comparison，就得先在 schema 裡有位子，
# 否則那次 LLM 呼叫照樣計費、結果卻拿不到。
class MemoryState(State):
    arxiv_id: str      # 存進 vector DB 用的 key；不要寫死
    comparison: str    # compare_with_memory 的輸出

graph = StateGraph(MemoryState)
graph.add_node("agent", react_agent)
graph.add_node("reflect", reflect)
graph.add_node("compare", compare_with_memory)  # 新加的 node
graph.add_edge("agent", "reflect")
graph.add_conditional_edges("reflect", should_continue, {"agent": "agent", END: "compare"})
graph.add_edge("compare", END)
graph.set_entry_point("agent")
app_with_memory = graph.compile()

# 跑（arxiv_id 一定要傳：store_paper 拿它當 vector DB 的 key）
if __name__ == "__main__":
    result = app_with_memory.invoke({
        "messages": [HumanMessage(content="摘要 https://arxiv.org/abs/2210.03629")],
        "revisions": 0,
        "arxiv_id": "2210.03629",
    })
    print(result["comparison"])   # 注意讀的是 comparison，不是 messages[-1]
```

**學到什麼**：vector DB 怎麼用、embedding 跟相似度查詢、把 agent 從「stateless」變成「有記憶」、persistent storage 的設計、graph 怎麼擴新 node 而不重寫前面的邏輯。

---

## Stage 7 — Eval + Observability + Deploy

### 7.1 Eval (`promptfoo`)

> **裝**：`npm install -g promptfoo`

Promptfoo 的 Python provider 要的是「可呼叫的 function」，不是 module 變數。所以先包一個薄 wrapper：

```python
# eval_provider.py
"""Promptfoo Python provider — 給 promptfoo 呼叫的 function。"""
from step2_paper_summary import SYSTEM_PROMPT
from step3_tool_use import run_agent  # Stage 3 寫的 ReAct loop


def call_api(prompt: str, options: dict, context: dict) -> dict:
    """Promptfoo 會傳 vars（context['vars']）+ prompt 進來。"""
    paper_url = context["vars"]["paper_url"]
    output = run_agent(f"請摘要這篇論文：{paper_url}")
    return {"output": output}
```

```yaml
# promptfooconfig.yaml
prompts:
  - "請摘要：{{paper_url}}"

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
        value: "回應包含 5 個英文關鍵詞、每段不超過 60 字"
  - description: "RAG paper"
    vars:
      paper_url: "https://arxiv.org/abs/2104.08663"
    assert:
      - type: contains
        value: "retrieval"
```

跑：`promptfoo eval && promptfoo view`

### 7.2 Observability (`langfuse`)

> **裝**：`pip install langfuse`
> **環境變數**（去 [cloud.langfuse.com](https://cloud.langfuse.com) 申請）：
> ```bash
> export LANGFUSE_PUBLIC_KEY="pk-lf-..."
> export LANGFUSE_SECRET_KEY="sk-lf-..."
> export LANGFUSE_HOST="https://cloud.langfuse.com"  # 或自架的 URL
> ```

```python
# step7_observability.py
# langfuse **3.0** 起 observe 就在套件頂層；只有 2.x 是 `from langfuse.decorators import observe`。
# 3.x / 4.x 都用下面這行；裝到 2.x 才需要改回舊路徑。
from langfuse import observe
from step3_tool_use import run_agent  # 前面 stage 的 agent

@observe(name="paper-summary-agent")
def run_paper_agent(arxiv_url: str) -> str:
    return run_agent(f"摘要 {arxiv_url}")

if __name__ == "__main__":
    out = run_paper_agent("https://arxiv.org/abs/2210.03629")
    print(out)
```

跑完之後到 Langfuse dashboard 看每次呼叫的 trace、cost、latency、tool use。

### 7.3 Deploy（Docker + FastAPI）

> **裝**：`pip install fastapi uvicorn pydantic`

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from step7_observability import run_paper_agent  # 用 Langfuse 包過的版本

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

**學到什麼**：eval 怎麼當回歸測試、observability 怎麼讓你 debug production agent、把 agent 從 script 變成 service。

---

## ✅ 完整 walkthrough 之後你應該能：

- [ ] 從零打造 ReAct agent（Stage 3）
- [ ] 用 framework 重寫並加進階 pattern（Stage 4）
- [ ] 把 agent 包成 Claude Code skill（Stage 5）
- [ ] 加 RAG memory 讓 agent 變成有狀態（Stage 6）
- [ ] 寫 eval + 接 observability + deploy（Stage 7）

這份 walkthrough 比單一 framework 小練習長，因為它要讓你看見同一個 agent 如何一層一層長大；每一步仍應該能單獨執行與檢查。

---

## ➡️ 下一站：把這個 Agent 接回主路線

1. 讀 [Stage 7.5 — 進階 Agentic 概念](../stages/07.5-advanced-agentic-concepts.md)，替剛完成的系統選真正需要的進階做法。
2. 再讀 [Stage 8 — Agent Interfaces](../stages/08-agent-interfaces.md)，決定它需要 Search、Browser Use、Computer Use 還是 Sandbox，並補上安全邊界。
3. 想改走另一條路時，回到[主路線 README](../README.md)。

---

## 🚧 進階延伸

如果你想再玩更深，這個 paper-summary-bot 可以延伸成：

- **Multi-agent paper review**：兩個 agent 分別當 supportive reviewer 跟 adversarial reviewer，第三個 agent 當 area chair → [研究人員路徑](../branches/for-researcher.md)
- **Conference report generator**：給定一個 conference proceedings URL，產出每個 track 的高層摘要 → [知識工作者路徑](../branches/for-knowledge-worker.md)
- **同主題論文趨勢追蹤**：每週掃 arXiv，找新論文跟現有 Memory 比較，產出 weekly digest → [日常使用者路徑](../branches/for-everyday-users.md)

每條都對應一個 specialized branch。

---

## 💡 維護這個 walkthrough

這個範例會隨時間更新——SDK 介面變化、framework 演進、最佳實踐改變。如果你發現某段程式碼跑不起來：

1. 先在 issue 裡回報具體錯誤訊息 + 你的環境（Python 版本、套件版本）
2. PR 修正請說明「為什麼這樣改」
3. 不要把這份檔案改成只 demo 你最熟悉的 framework——這份是給**多元 framework 學習**用的
