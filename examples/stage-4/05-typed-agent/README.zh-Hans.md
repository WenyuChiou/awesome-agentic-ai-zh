<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 5：型别安全 agent（Pydantic AI structured output）

对应 [Stage 4 — Agent Frameworks](../../../stages/04-agent-frameworks.zh-Hans.md) 练习 5。
> 🎓 **学习模式**：这份 `starter.py` 是**完整解答**、不是 TODO skeleton。建议用**主动模式**——`mv starter.py starter_reference.py`、看 signature 不看 body、自己重写一份 `starter.py`、跑 `python test.py` 验证；卡 20 分钟再回去对照 reference。完整方法论看 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 两条 SDK path，不是进阶深度教材。深度教材推荐：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章节式 + 16 种 production 能力。**本练习对应 hello-agents 的 structured output / type-safe 章节**
> - [Pydantic AI 官方 docs](https://ai.pydantic.dev/) + [Instructor library](https://github.com/567-labs/instructor)（另一条 typed-output 路线）
> - 完整 references 见 [Stage 4 精选 Projects](../../../stages/04-agent-frameworks.zh-Hans.md#-精选-projects)


## 任务

Agent 回问题、**强制** return `AnswerWithConfidence`：

```python
class AnswerWithConfidence(BaseModel):
    answer: str
    confidence: float = Field(ge=0.0, le=1.0) # runtime 验证 0-1
    sources: list[str]
```

Pydantic AI 把 **schema validation（格式规则检查）** 放进程序：LLM 不照 schema 时，framework 可以拒绝或重试。它能检查形状，**不能证明答案内容是真的**。

## 怎么跑 — 两条路径

> ⚠️ **每个练习都要有自己的 Python 3.11 `.venv`。** 不要把这题的 Pydantic 需求与 CrewAI 练习混装。

### Path A（默认、本机免费）

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
.\.venv\Scripts\python.exe starter.py
```

预算：模型 API 是 **$0**；本机硬体、电力与重试时间仍有成本。

### Path B（Anthropic、比较云端结果）

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py
```

预设固定型号：`claude-haiku-4-5-20251001`。若一次请求用 2,000 input + 1,000 output tokens：`2,000 / 1,000,000 × $1 + 1,000 / 1,000,000 × $5 = $0.007`。验证失败可能重试；先设供应商支出上限 **$0.05**。

<details markdown="1">
<summary>macOS／Linux 指令与查核资讯</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
./.venv/bin/python test.py
```

官方来源：[Pydantic AI output](https://ai.pydantic.dev/output/)｜[Pydantic AI testing](https://ai.pydantic.dev/testing/)｜[Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>套件、model ID、价格与官方连结查核：2026-08-28 UTC。</small>
</details>

## 不花钱验证程序逻辑

```powershell
.\.venv\Scripts\python.exe test.py # 官方 TestModel + schema 边界
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic 设定 + 相同输出契约
```

`test.py` 直接验 `AnswerWithConfidence` 对非法资料（confidence > 1.0、type 不对、sources 不是 list）的 ValidationError——不需要打 LLM、纯 type 层测试。

## 为什么 type-safe agent 重要

```
Stage 3 练习 6：schema = JSON Schema in prompt
    LLM 看到、但回什么是 LLM 决定（可能违反）

Stage 4 练习 5：schema = Pydantic model in code
    LLM 违反 → framework 自动 raise → retry / 修
    成功回传的 output 已通过 runtime 格式检查
    内容是否正确仍要另外验证
```

对 production：

| 需求 | 纯 prompt schema | Pydantic AI |
|---|---|---|
| LLM 偶尔少栏位 | 你的下游 code 要 try/except | 自动 retry 直到符合 |
| 型别错（confidence="high"） | 下游 crash | Pydantic ValidationError、retry |
| 边界错（confidence=1.5） | 下游用错误值 | 拒绝、retry |
| 多余栏位 | 依你的 parser 而定 | 依 Pydantic model 设定处理 |

**结论**：下游程序需要固定栏位时，typed output 很有用。Stage 3 练习 6 教 schema 设计；这题把 schema 变成 runtime contract，再提醒你补上事实查核。

## Pydantic AI 核心观念

### Agent + output_type

```python
agent = Agent(
    model=...,
    output_type=AnswerWithConfidence, # ← 强制 LLM 回这个 shape
    system_prompt="..."
)
result = agent.run_sync(question)
answer: AnswerWithConfidence = result.output # 已验证的物件
```

**重点**：framework 把 Pydantic schema 转成 structured output 指示，执行 validation，失败时依设定重试。重试成功只表示格式合格。

### Field constraints

```python
confidence: float = Field(ge=0.0, le=1.0, description="...")
```

`ge` / `le` 是 Pydantic 的 numeric bound。LLM 回 `1.5` 会被 ValidationError 挡下、retry。

### 自动 retry

```python
Agent(..., retries=3) # default 1，可调
```

Pydantic AI 看到 ValidationError、会把错误讯息塞回 prompt、要求 LLM 重产。

## 两个 path 观察重点

| 观察项 | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| 一次产对 schema | 用相同题组量测 | 用相同题组量测 |
| retry 次数 | 记录实际结果 | 记录实际结果 |
| confidence 边界 | 由 Pydantic 验证 | 由 Pydantic 验证 |
| sources 是 list | 由 Pydantic 验证 | 由 Pydantic 验证 |
| 成本 | 依 tokens 与重试次数 | 模型 API $0 |

**教学重点**：比较模型时要一起记录成功率、重试次数、延迟与费用；不要只看单次 token 价格，也不要先假设大模型一定比较省。

## 常见坑

- **`output_type` 太复杂**：nested model 越深越难产生与维护。先用最少必要栏位，再用评测决定是否拆分
- **缺 `description`**：`Field(...)` 没写 `description=`、LLM 看不到栏位用途、易误填
- **`retries=0`**：失败就 raise。重试次数要依费用、延迟与失败模式设定，并保留上限
- **小 model + 深 nested**：qwen2.5:3b 可能 retry 多次仍不对。换大 model 或扁平 schema

## 想看更聪明的答案？

```powershell
$env:MODEL="claude-sonnet-5"; .\.venv\Scripts\python.exe starter_anthropic.py
$env:MODEL="qwen2.5:7b"; .\.venv\Scripts\python.exe starter.py
```

## 延伸

- **加 tools**：Pydantic AI agent 可以同时有 tools + structured output、`@agent.tool` 装饰函数
- **stream typed output**：`agent.run_stream(...)` 边跑边验
- **跨 model 比较**：同一个 schema 跑 Claude / GPT / Gemini / 本机 model，比较通过率、重试与成本
- **接 production**：Pydantic AI 跟 FastAPI 整合很好、output 直接当 API response model
