<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 3：从零实现 ReAct（不用 framework）

对应 [Stage 3 — 工具使用与第一个 Agent Loop](../../../stages/03-tool-use-and-hello-agent.zh-Hans.md) 练习 3。
> 🎓 **学习模式**：先运行提供的 `starter.py`（`python starter.py`），然后只改一个小地方，再重新运行现有测试 `python test.py`。如果测试失败，就撤销或修正这一个改动，再试一次。不需要重命名文件，也不需要重写整份解答。完整方法见 [`docs/HOW_TO_USE.md`](../../../docs/HOW_TO_USE.md)。

> 📚 **想要 chapter-length 深入版？** 本 folder 的 starter 是 70-150 行 illustrative 版、聚焦 `核心 pattern + 两条 SDK path`，不是进阶深度教材。深度教材推荐：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents) ⭐ 中文圈最完整、章节式 + 16 种 production 能力。**本练习对应 hello-agents 的 ReAct 章节（搭配 [`learn_version` 分支](https://github.com/jjyaoao/HelloAgents/tree/learn_version)）**
> - [ReAct 原论文](https://arxiv.org/abs/2210.03629)（Yao et al. 2022 第 3 节） + [pguso/ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch)（本机 LLM 从零实现）
> - 完整 references 见 [Stage 3 精选 Projects](../../../stages/03-tool-use-and-hello-agent.zh-Hans.md#-精选-projects)


## 为什么从零写

ReAct（Reasoning + Acting）是现代 agent 的基础 pattern：

```
while not done:
    thought    = LLM 看完目前 context、讲出下一步要做什么
    action     = LLM 调用一个 tool
    observation = tool 执行结果、喂回去给 LLM
```

LangGraph / CrewAI 把这个 loop 藏起来了。你**自己写过一次**才知道：

- 为什么 messages array 一直长
- tool_use_id 跟 tool_result 怎么配对
- stop_reason 为什么是 `tool_use` 或 `end_turn`
- max_iter 为什么是 safety net

70 行 Python 全交代清楚。

## 怎么跑 — 两条路径

### Path A（默认、本机免费）

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

预算：**$0 API 费用**；不包含硬件、内存与电力成本。

### Path B（Anthropic、云端比较）

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "your-key"
python starter_anthropic.py
```

预算：每次先预留 **$0.05**。实际费用按 `输入 tokens × $1 / 1,000,000 + 输出 tokens × $5 / 1,000,000` 计算，Tool Use 还会加入 prompt tokens；价格查核日：`2026-08-27`。

预期看到（Path A、本机）：

```
❓ 问题：'台北人口' 除以 '纽约人口'、答案保留 4 位小数。
------------------------------------------------------------
[step 0] thought: 我先查台北人口...
           tool: lookup_fact({'query': '台北人口'}) → 2602000
[step 1] thought: 接着查纽约人口...
           tool: lookup_fact({'query': '纽约人口'}) → 8336000
[step 2] thought: 计算比例...
           tool: calculator({'expression': '2602000 / 8336000'}) → 0.3121...
[step 3] thought: 答案是 0.3122
------------------------------------------------------------
✅ 最终答案：台北人口除以纽约人口约 0.3122
   共 4 轮
✅ 练习 3 通过 — ReAct loop 自己连用了 lookup_fact 跟 calculator
```

## 不花钱验证程序逻辑

```powershell
python test.py            # 验 Path A (Ollama) starter.py 逻辑
python test_anthropic.py  # 验 Path B (Anthropic) starter_anthropic.py 逻辑
```

两条 test 都用 `unittest.mock`、不打真 API、$0/run。Path A 用 OpenAI-compat response shape、Path B 用 Anthropic content blocks。

`test.py` 用 `unittest.mock.MagicMock` 取代 Anthropic client、塞固定 response、验证你的 loop 逻辑。预期：

```
✅ test_calculator_basic
✅ test_calculator_rejects_eval_injection
✅ test_lookup_fact
✅ test_react_loop_single_tool_call
✅ test_react_loop_multi_step
✅ test_react_loop_respects_max_iter

🎉 全部通过 — 你的 ReAct loop 逻辑正确
```

## 程序结构走查

| 段 | 行 | 在做什么 |
|---|---|---|
| `tool_calculator` | ~30-40 | 安全的计算器（whitelist 过滤、避免 `eval` 漏洞） |
| `tool_lookup_fact` | ~42-50 | 假事实库（教学用、避免依赖外部 API） |
| `TOOLS_SPEC` | ~52-75 | tool schema 给 LLM 看 |
| `TOOL_IMPL` | ~77-80 | name → callable 对应表（dispatch） |
| `react_loop` | ~85-130 | 主循环、含 max_iter safety、`messages` 累积、tool result 接回去 |

## 常见坑

1. **忘记把 assistant response 加进 messages**：下一轮 LLM 就看不到自己上一轮讲过什么、会 loop forever
2. **tool_result 没带 `tool_use_id`**：LLM 无法配对哪个 result 对应哪个 call
3. **`while True` 没 max_iter**：tool 结果写得不好、LLM 会无限调用；safety net 一定要设
4. **未过滤的 eval**：不要把 model text 送进 `eval`，否则可能造成 RCE；不要靠字符 whitelist 或 `ast.literal_eval` 做算术。改用明确的 AST operator allowlist，并限制输入长度、AST 深度、节点数与数字／结果大小。

## 想看更聪明的答案？

预设用固定 ID `claude-haiku-4-5-20251001`。想比较 sonnet 时：

```powershell
$env:MODEL = "claude-sonnet-5"; python starter_anthropic.py
```

或在 `starter_anthropic.py` 改 `MODEL = ...` 那行。

## 延伸

- **加更多 tool**：在 `TOOLS_SPEC` + `TOOL_IMPL` 补一个 entry 即可
- **加 streaming**：把 `client.messages.create(...)` 换成 `with client.messages.stream(...) as s:`、边跑边印
- **加 prompt cache**：在 `system=` 或 `tools=` 带 `cache_control={"type":"ephemeral"}` 重复 call 省 90% token
- **接 [LangGraph](https://langchain-ai.github.io/langgraph/) 或 [Pydantic AI](https://ai.pydantic.dev/) 看 framework 怎么帮你藏掉这 70 行**
