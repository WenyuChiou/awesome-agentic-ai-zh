<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 练习 5：让 Agent 下次还记得

← 回到 [Stage 6 — Memory & RAG](../../../stages/06-memory-rag.zh-Hans.md#练习-5long-term-memory)

普通聊天记录像写在白板上：程序关掉，白板可能就擦掉了。**Long-term memory（长期记忆）**会把值得保留的事写进磁盘，下次开程序还能找回来。

## 📌 学习目标

- 分清楚 **chat history**、**working memory**、**long-term memory**。
- 把一条用户事实写入 Chroma `PersistentClient`。
- 重新打开同一个数据库后找回记忆。
- 把相关记忆放进 system prompt，而不是把全部历史都塞进去。

## 🔑 核心词

| 核心词 | 白话意思 |
|---|---|
| **Working memory** | 这次任务眼前正在用的少量信息 |
| **Long-term memory** | 跨程序重开或跨 session 仍保留的信息 |
| **Recall** | 用现在的问题找回相关记忆 |
| **Memory policy** | 决定什么能记、要更新、要忘记、谁能读 |

## 📚 必读与学习资源

- ★★★★★ [Chroma `PersistentClient` 官方文档](https://docs.trychroma.com/reference/python/client)：本练习真正保存到磁盘的基础。
- ★★★★★ [LangGraph Memory 官方概念页](https://docs.langchain.com/oss/python/concepts/memory)：分清楚 thread 与跨 thread 记忆。
- ★★★★☆ [Mem0](https://github.com/mem0ai/mem0)：fact extraction、更新与删除的成熟项目。
- ★★★★☆ [Letta Code](https://github.com/letta-ai/letta-code)：现行 stateful agent 与 working／archival memory 的完整实现。
- ★★★★☆ [`datawhalechina/hello-agents`](https://github.com/datawhalechina/hello-agents)：较完整的 Agent memory 教材。

<sub>资料查核：2026-08-30 UTC。</sub>

## ▶️ Path A（Ollama、本机免费）

```powershell
pip install -r requirements.txt
ollama pull qwen2.5:3b
ollama serve
python starter.py
```

程序会把 Chroma 数据放在 `.stage06-memory`。再次执行时，之前写入的记忆仍在。API 费用是 **$0**。

<details markdown="1">
<summary>Path B（Anthropic）</summary>

```powershell
pip install -r requirements.txt
$env:ANTHROPIC_API_KEY = Read-Host "Anthropic API key"
python starter_anthropic.py
```

默认 `claude-haiku-4-5` 的费用按 token 计算：每百万输入 token **$1**、输出 token **$5**。执行前请核对 [Anthropic 官方价格页](https://platform.claude.com/docs/en/about-claude/pricing)并设定小额上限。

</details>

**Stage 06 总预算**：五个 Path A 全部跑完，API 费用仍是 **$0**（不含下载、磁盘与电费）。选跑云端 Path 时，费用依 embedding／输入／输出 token 实际用量计算；先设小额账户上限，成功跑一次就停。

## ✅ 不写入项目文件夹、不连 API 的检查

```powershell
python test.py
python test_anthropic.py
```

大多数测试注入小型记忆库与假 LLM；持久化检查会在系统临时文件夹建立真正的 `PersistentClient`，让两个全新的 Python process 一写一读，完成后自动删除。

## 记忆流程

```text
用户说话
  → 判断值不值得记
  → remember() 写入磁盘
  → 下次问题先 recall()
  → 只把相关记忆放进 prompt
```

```python
memory = MemoryStore(path=".stage06-memory")
memory.remember("User prefers Python.")
recalled = memory.recall("Which language should I learn?")
```

## Chat history 和长期记忆不是同一件事

| 比较 | Chat history | Long-term memory |
|---|---|---|
| 用途 | 保持眼前对话连续 | 下次还记得重要事实 |
| 放哪里 | 当前 messages | 磁盘或外部数据库 |
| 怎么读 | 最近几轮直接放进 prompt | 先搜索，再取少量相关内容 |
| 风险 | prompt 变太长 | 记错人、记过期数据、删不干净 |

本练习用简单规则找 `I am`、`I like`、`I prefer` 等句子，只是为了看懂流程。正式系统要有清楚的 **memory policy**：用户同意、user ID 隔离、更新、删除、期限与审计。

<details>
<summary>常见问题与 production 下一步</summary>

- 不要每句都存；先判断是否真的值得长期保留。
- 同一事实重复出现时，要去重或更新，不要一直新增。
- 用户搬家或改偏好时，要让新记忆取代旧记忆。
- 每位用户必须有独立 namespace，不能互相看到数据。
- 用户要求删除时，要能找到所有副本并确实删除。
- 需要完整生命周期时，再评估 Mem0、Letta 或 LangGraph persistence。

</details>

完成后，回到 [Stage 6](../../../stages/06-memory-rag.zh-Hans.md)做成功检查，再前往 Stage 7。
