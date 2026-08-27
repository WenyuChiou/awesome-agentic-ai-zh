<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 1：一个工具、一次完整来回

对应 [Stage 3 — Tool Use & Hello Agent](../../../stages/03-tool-use-and-hello-agent.zh-Hans.md) 练习 1。

这题只做一件事：模型说“请调用 `get_weather`”，你的 Python 程序检查参数、执行工具，再把结果交回模型。跑完后，你会亲眼看到：

`问题 → Tool Call → 程序检查并执行 → Tool Result → 最后回答`

**Tool Call** 是模型提出的工具请求。**Tool Result** 是你的程序执行后交回去的结果。模型提出请求，不代表它有权直接执行程序。

## 第一个动作

先在 PowerShell 复制并执行：

```powershell
ollama pull qwen2.5:3b
```

## Path A：Ollama（本机，API 费用 `$0`）

```powershell
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
ollama serve
python starter.py
```

如果 `ollama serve` 说端口已被使用，通常代表 Ollama 已经在运行；保留那个窗口，再开一个 PowerShell 执行 `python starter.py`。

这条路径使用 OpenAI Python SDK 连接到 `http://localhost:11434/v1`，数据不会发送到 OpenAI 云端。

## Path B：Anthropic（需要 API key）

```powershell
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = "你的-key"
python starter_anthropic.py
```

程序使用固定模型 ID `claude-haiku-4-5-20251001`，避免模型 alias 之后移动时教学结果悄悄改变。

**预算提醒**：每次正式运行先预留 `$0.05` 上限。实际费用按 token 数计算：

`输入 token × $1 / 1,000,000 + 输出 token × $5 / 1,000,000`

Tool Use 还会加入系统提示 token；不要把基于无 token 假设的小数写成保证价格。价格查核日：`2026-08-27`。

<details markdown="1">
<summary>macOS/Linux 命令</summary>

```bash
cd examples/stage-3/01-function-calling
python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY="你的-key"
python starter_anthropic.py
```

</details>

## 不花钱的自我检查

这两个测试使用假的模型响应，不连接 Ollama，也不调用 Anthropic API：

```powershell
python test.py
python test_anthropic.py
```

你应该看到两次 `all pass`。测试也会故意送入坏 JSON、多余字段与不存在的工具，确认程序会先挡下它们。

## 你正在保护什么

- **Allowlist**：只有 `get_weather` 可以执行；模型乱说别的工具名称也不行。
- **参数验证**：`city` 不能是空字符串，`unit` 只能是 `celsius`，多余字段也会被拒绝。
- **结果配对**：每个结果都带回原本的 `tool_call_id` 或 `tool_use_id`。
- **错误标记**：Anthropic 路径失败时会加上 `is_error: true`，让模型知道这不是正常结果。

## 完成条件

- [ ] Path A 或 Path B 至少成功运行一次。
- [ ] 两个离线测试都显示 `all pass`。
- [ ] 你能用自己的话说出“模型只提出请求，程序才真正执行”。
- [ ] 你能指出程序在哪里检查工具名称与参数。

## 官方参考

- [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling)
- [Anthropic：How tool use works](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)
- [Anthropic：Handle tool calls](https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls)
- [Ollama OpenAI compatibility](https://docs.ollama.com/api/openai-compatibility)

文档与 SDK 查核日：`2026-08-27`。

> 📚 **想看完整章节？** 这里仅教学第一个最小循环。接着读：
> - [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：章节式中文 Agent 课程；把这题当成 tool calling 的起点。
> - [Anthropic Tool Use Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/tool_use)：从单一工具走到多工具的官方 notebook。
> - [Stage 3 精选 Projects](../../../stages/03-tool-use-and-hello-agent.zh-Hans.md#-精选-projects)：回到学习地图选择下一个资源。
