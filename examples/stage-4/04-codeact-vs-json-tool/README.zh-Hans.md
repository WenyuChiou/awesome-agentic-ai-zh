<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 4：CodeAct vs JSON tool（Smolagents）

对应 [Stage 4 — Workflow Graph 与 Agent 框架](../../../stages/04-agent-frameworks.zh-Hans.md) 练习 4。
> 🎓 **学习模式**：先运行提供的 `starter.py`（`python starter.py`），然后只改一个小地方，再重新运行现有测试 `python test.py`。如果测试失败，就撤销或修正这一个改动，再试一次。不需要重命名文件，也不需要重写整份解答。完整方法见 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 illustrative 版、聚焦核心 pattern + 两条 SDK path，不是进阶深度教材。深度教材推荐：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章节式 + 16 种 production 能力。**本练习对应 hello-agents 的 CodeAct vs JSON tool 章节**
> - [Smolagents 官方 cookbook](https://github.com/huggingface/smolagents/tree/main/examples) + [QuantaLogic/quantalogic](https://github.com/quantalogic/quantalogic)（另一个 CodeAct framework）
> - 完整 references 见 [Stage 4 精选 Projects](../../../stages/04-agent-frameworks.zh-Hans.md#-精选-projects)


## 两种 agent action 路线对照

| 路线 | 怎么 act | 范例 framework |
|---|---|---|
| **JSON tool** | LLM 回 `{"name": "tool_x", "arguments": {...}}` | OpenAI function calling、LangGraph、CrewAI |
| **CodeAct** | LLM 写 Python code、直接执行 | HuggingFace Smolagents |

**这题用 CodeAct 解同题（人口比例）、跟练习 1 / 3 的 JSON tool 路线对照**。

## 怎么跑 — 两条路径

> ⚠️ **每个练习都要有自己的 Python 3.11 `.venv`。** 这题还需要 Docker；不要把模型产生的程序码直接放到主机执行。这个教学容器仍可能连网，所以里面不要放密码或私密数据。

### Path A（默认、本机免费）

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
docker version
.\.venv\Scripts\python.exe test_docker_smoke.py
.\.venv\Scripts\python.exe starter.py
```

预算：模型 API 是 **$0**；本机硬体、电力与 Docker 资源仍有成本。小模型可能需要更多修正步骤，所以程序把 `max_steps` 限制为 4。

### Path B（Anthropic、比较云端结果）

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
.\.venv\Scripts\python.exe starter_anthropic.py
```

预设固定型号：`anthropic/claude-haiku-4-5-20251001`。单次 2,000 input + 1,000 output tokens 的例子为 `$0.007`；CodeAct 可能多轮调用，因此先设供应商支出上限 **$0.10**。实际费用看 tokens 与步数。

<details markdown="1">
<summary>macOS／Linux 指令与查核资讯</summary>

```bash
python3.11 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."
docker version
./.venv/bin/python test.py
./.venv/bin/python test_docker_smoke.py
```

价格公式：`input_tokens / 1,000,000 × $1 + output_tokens / 1,000,000 × $5`。

官方来源：[Secure code execution](https://huggingface.co/docs/smolagents/tutorials/secure_code_execution)｜[Python executors](https://huggingface.co/docs/smolagents/reference/python_executors)｜[Docker port publishing](https://docs.docker.com/engine/network/port-publishing/)｜[Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing)

<small>套件、model ID、价格与官方连结查核：2026-08-28 UTC。</small>
</details>

## 不花钱验证程序逻辑

```powershell
.\.venv\Scripts\python.exe test.py # AST、JSON allowlist、loopback 控制端口与资源限制
.\.venv\Scripts\python.exe test_anthropic.py # Anthropic 设定 + 相同安全边界
```

这两个离线测试**不会**执行模型产生的程序码，也不需要 Docker daemon。`test_docker_smoke.py` 是另一个手动 smoke test：它真的启动 Jupyter executor，确认主机控制通道可用，而且控制端口只绑定到 `127.0.0.1`；先让 `docker version` 成功再运行。它不会假装容器不能连网。

## CodeAct 是怎么运作的

LLM 不回 JSON、而是**回 Python code block**：

````
（user）Find Taipei population, divide by NYC, give ratio.

（LLM 回应）
```python
pop_taipei = lookup_fact(query="Taipei population") # 2602000
pop_nyc = lookup_fact(query="New York population") # 8336000
ratio = calculator(expression=f"{pop_taipei}/{pop_nyc}") # 0.3122
print(ratio)
```

（Smolagents 执行这段 code、把 print 结果接回去给 LLM 继续）
````

这份示例明确使用 Docker executor。Jupyter 控制端口只绑定到主机的 `127.0.0.1`，并移除 Linux capabilities、禁止提权与 pickle，再限制内存、process 数与 agent 步数。一般 Docker bridge **仍可能让容器连接外部网络或主机服务**，所以这只是受控教学示例，不是 production sandbox。需要执行不可信程序码时，还要加真正的 egress／host 防火墙，或改用有正式隔离边界的远程 sandbox。

## CodeAct vs JSON tool 对照

| 维度 | JSON tool | CodeAct |
|---|---|---|
| LLM 输出形式 | 结构化 JSON | Python 程序码 |
| 变数绑定 | LLM 要自己记得 / 重复调用 | 自然有 variable（`pop_taipei = ...`） |
| 多步运算 | 每步一次 LLM call | 一次写好几行 code |
| 一轮 token 数 | 较少 | 较多（code 较长） |
| 对小 model | 较友善（稳定的 JSON） | 较吃力（要产正确 Python） |
| Debug 友善 | tool call 看得清楚 | 看 code execution log |
| 安全考量 | allowlist + 参数验证 | 不可信程序码，必须隔离、限权、限资源 |
| 哪些题目擅长 | 单步、边界明确 | 多步运算、需要中间 variable |

**HuggingFace 的观点**：CodeAct 更贴近“人类怎么解问题”——你也是用变数记中间结果、不是每步都重新查。

## 两个 path 观察重点

| 观察项 | Anthropic Claude haiku | Ollama qwen2.5:3b |
|---|---|---|
| 产出可执行 Python | 用相同测试题量测 | 用相同测试题量测 |
| 变数命名 / 重用 | 看 execution log | 看 execution log |
| 比例是否算对 | 验证最终值 | 验证最终值 |
| 步数 | 由 `max_steps=4` 限制 | 由 `max_steps=4` 限制 |
| 模型 API 成本 | 依 tokens 与步数 | $0 |

**punchline**：CodeAct 比 JSON tool 多了一个“执行程序码”的风险面。不要先假设哪个模型或路线较好；用相同任务比较成功率、步数、成本与安全边界。

## 常见坑

- **`@tool` 函数 docstring 是 prompt 的一部分**：Smolagents 把 docstring 当 tool description 给 LLM 看。**docstring 没写好、LLM 不知道何时用这 tool**
- **把 Docker 当完整 sandbox**：错。这份示例只缩小权限并把控制端口绑定到 loopback；上线前还要做镜像、权限、egress、host access、资源与记录审查
- **`max_steps` 不够**：先看错在哪一步，不要只把数字调大；较大上限会增加费用与 loop 风险
- **模型程序码有 syntax error**：Smolagents 可以把错误接回模型修正，但会增加步数；是否换模型要看评测结果

## 想看更聪明的答案？

```powershell
$env:MODEL="anthropic/claude-sonnet-5"; .\.venv\Scripts\python.exe starter_anthropic.py
$env:MODEL="qwen2.5:7b"; .\.venv\Scripts\python.exe starter.py
```

## 延伸

- **加更多 tools**：`@tool` 装饰函数即自动 wrap、Smolagents 自动拿 docstring 当 description
- **改 ToolCallingAgent**：Smolagents 也有非 CodeAct 的 `ToolCallingAgent`、用 JSON tool 路线。对照看
- **接 Hugging Face Hub**：使用现行 `InferenceClientModel` 调用 HF inference（不需要本机 Ollama）
- **看 [Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)**：Anthropic 的观点是两条路线都合理、看任务
