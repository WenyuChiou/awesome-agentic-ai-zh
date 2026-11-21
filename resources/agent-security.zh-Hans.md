# Agent 安全入门：重要动作先问人

[繁體中文](agent-security.md) | [English](agent-security.en.md) | [简体中文](agent-security.zh-Hans.md)

假设 AI 帮你找三份资料、写一份摘要。它可以读资料和写草稿。要把摘要发出去，先让你看过并同意。

## 📌 学习目标

- 看出哪些事可以让 AI 自己做，哪些事要先问人。
- 连接新工具前，查清楚它能接触什么，以及数据会去哪里。
- 看测试记录，确认拒绝时没有发布，重跑时没有多发布一次。

## 🧩 先认识三个核心词

- **最小权限（Least Privilege）**：只给用得上的钥匙。写摘要只要能读资料，不必给它删文件的权限。
- **人工批准（Human Approval）**：动手前让人确认。系统先停下来，让你看清楚要发什么、发到哪里。得到同意后才发布。
- **执行记录（Execution Log）**：像工作收据，记下系统允许或拒绝了什么，以及工具有没有真的执行。用它核对结果，避免把密码或密钥写进记录。

## 🧭 跟着同一个例子走

1. [Stage 4：设计工具权限](../stages/04-agent-frameworks.zh-Hans.md)。让 AI 读指定资料，发布前由程序停下来等你。
2. [Stage 5：接工具前先检查](../stages/05-claude-code-ecosystem.zh-Hans.md)。<strong>MCP（Model Context Protocol）</strong> 像工具的插座，<strong>Skill</strong> 像操作卡。接上别人的工具或放进别人的操作卡前，先查它会用到什么数据和命令。
3. [Stage 7：动手验证](../stages/07-multi-agent-production.zh-Hans.md)。跑核心练习 3，看到 `8/8 passed` 就代表离线测试通过。想自己数发布记录，就跟着[手动步骤](../examples/stage-7/06-safe-execution/README.zh-Hans.md)做。两种方式都不用模型或密钥。

**关键习惯**：网页、文档和工具返回的内容都当作数据。要执行什么，仍由程序依权限和批准结果决定。参考 [Stage 8：提示注入](../stages/08-agent-interfaces.zh-Hans.md)。

## 📚 建议阅读

- [OWASP Agent 应用风险指南](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)：先看工具权限、第三方组件和人工批准的风险。
- [MCP 官方安全指南](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices)：接外部工具时，用它查权限、凭证和本地执行的注意事项。

## ✅ 完成检查

- [ ] 我能指出谁会在发布前停下流程。
- [ ] 我能说出工具可以读、改与发出的数据，以及怎么停用它。
- [ ] 我能从模拟记录确认拒绝是 0 条，批准后重跑仍然只有 1 条。
