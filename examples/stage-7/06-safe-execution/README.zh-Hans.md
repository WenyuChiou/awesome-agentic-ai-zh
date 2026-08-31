<div align="right">
  <a href="./README.md">繁體中文</a> | <strong>简体中文</strong> | <a href="./README.en.md">English</a>
</div>

# 核心练习：先停下、存好，再安全地继续

这题不用模型，也不会真的寄信或改资料。程序只把“假动作”写进本机 JSON ledger，让你先看懂安全骨架。

对应 [Stage 7 — Agent Production Engineering：Harness、Loop 与 Graph](../../../stages/07-multi-agent-production.zh-Hans.md) 核心练习 3。

## 🎯 学习目标

- **Human Approval（人工批准）**：敏感动作先暂停；人可以 approve 或 reject。
- **Checkpoint（检查点）**：在等待批准时保存工作状态。
- **Resume（续跑）**：程序重开后，从同一个 task ID 接着做。
- **Recovery（恢复）**：状态损坏或不相符时 fail closed，不猜下一步。
- **Idempotency（幂等）**：同一个 key 重跑很多次，假动作仍只执行一次。

## 先跑不花模型费用的测试

在这个文件夹打开 PowerShell，直接复制：

```powershell
py -3.11 test.py
```

看到 `8/8 passed`，代表暂停、拒绝、批准、重开续跑、ledger 对账、损坏状态与“最多执行一次”都有离线测试。

## 亲手走一次 pause → approve → resume

第一步只建立 checkpoint，**不执行假动作**：

```powershell
py -3.11 starter.py start --action "publish draft" --key demo-001
```

你会看到 `status` 是 `waiting_for_approval`。现在关掉终端机也没关系；状态在 `.cache/safe-execution-state.json`。

第二步由人决定。批准：

```powershell
py -3.11 starter.py resume --decision approve
```

再次执行同一行，ledger 仍只有一笔 `demo-001`。这就是最小的 idempotency 证据。

要练拒绝，先删除这个练习自己建立的两个 `.cache/safe-execution-*.json`，再用新 key start，最后执行：

```powershell
py -3.11 starter.py resume --decision reject
```

## 看懂两份文件

| 文件 | 它保存什么 | 不应该放什么 |
|---|---|---|
| checkpoint state | task ID、动作、状态、批准结果、schema version | API key、密码、未遮罩的客户资料 |
| side-effect ledger | 已执行的 idempotency key 与假动作 | 把“写入成功”当成业务 Outcome 已正确 |

真实系统通常把 state 放进有权限、备份、保留期限与版本控制的数据库或 queue。这个 JSON 示例只教责任边界，不是 production 存储方案。

## 只改一件事

把 `publish draft` 改成 `send reviewed summary`，并换一个新的 key。先 reject，再确认 ledger 没增加；重新 start 后 approve，再确认只增加一笔。

## 成功检查

- [ ] 没有人批准时，ledger 不会出现假动作。
- [ ] reject 后状态是 `cancelled`，而且没有副作用。
- [ ] approve 后状态是 `completed`。
- [ ] 同一个 key resume 两次，ledger 仍只有一笔。
- [ ] ledger 与 checkpoint 冲突时，程序会修复可证明的完成状态，或停止请人处理；不会把已执行的动作标成 `cancelled`。
- [ ] JSON 损坏或 key／action 不相符时，程序停止而不是猜测。

## 📚 必读与学习资源

- ⭐⭐⭐⭐⭐ [OpenAI Agents SDK — Human-in-the-loop](https://openai.github.io/openai-agents-python/human_in_the_loop/)：tool approval、`RunState` 保存与 resume。
- ⭐⭐⭐⭐⭐ [LangGraph — Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)：pause、approve／reject、checkpoint、resume 与 interrupt 前的幂等副作用。
- ⭐⭐⭐⭐⭐ [LangGraph — Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)：checkpointer、store、thread state 与 fault tolerance 的边界。
- ⭐⭐⭐⭐⭐ [Anthropic — Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)：不要只看 Agent 说了什么，也要检查外部 Outcome 与完整 Trajectory。

<small>官方文件与链接查核：2026-08-31 UTC。</small>

<details markdown="1">
<summary>展开：为什么 ledger 要先写，checkpoint 才标成完成？</summary>

如果程序在两次写入中间中断，下次 resume 会先在 ledger 找同一个 idempotency key。找到就不重做假动作，只补上 `completed` checkpoint。这是教学用的最小 write-ahead 想法；真实跨服务交易仍要依数据库、queue 或供应商 API 的一致性保证设计。

</details>

<details markdown="1">
<summary>展开：常见错误与安全边界</summary>

- 把 approval 写在工具执行后：已经寄出或付款，再问人就太晚了。
- 只有 retry，没有 idempotency key：网络 timeout 后重试可能重复副作用。
- checkpoint 没有 schema／程序版本：隔天部署新程序，旧 state 可能无法安全读取。
- 把完整 Prompt、token 或客户资料塞进 state：state 也要做最小化、加密、权限与删除设计。
- 只看 `status=completed`：仍要用 Outcome Eval 确认外部结果真的正确。

</details>

下一步：回到 [Stage 7 上线四步](../../../stages/07-multi-agent-production.zh-Hans.md#-上线四步eval--observability--approvalrecovery--deploy)，再做 Deploy 练习。
