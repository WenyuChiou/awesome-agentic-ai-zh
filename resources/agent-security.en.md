# Agent Safety Basics: Ask Before High-Impact Actions

[繁體中文](agent-security.md) | [English](agent-security.en.md) | [简体中文](agent-security.zh-Hans.md)

Imagine AI finds three sources and writes a summary for you. It can read sources and write a draft. Before it publishes the summary, you get to read it and say yes.

## 📌 Learning Goals

- Tell which tasks AI may do on its own and which ones it should ask about first.
- Before connecting a new tool, check what it can access and where the data goes.
- Read the test record to verify that rejection publishes nothing and retrying does not publish a second time.

## 🧩 Three Key Terms

- **Least Privilege** means giving AI only the keys it needs. Writing a summary requires reading sources. Keep file deletion disabled.
- **Human Approval** means asking a person before acting. The system pauses so you can see what will be published and where. Then it waits for your approval.
- **Execution Log** is like a receipt. It records what the system allowed or refused and whether the tool actually ran. Use it to check the result and keep passwords and keys out of the log.

## 🧭 Follow One Example

1. [Stage 4: Set tool permissions](../stages/04-agent-frameworks.en.md). Let AI read specific sources. Have the program pause for you before publishing.
2. [Stage 5: Check before connecting tools](../stages/05-claude-code-ecosystem.en.md). Think of <strong>Model Context Protocol (MCP)</strong> as a socket for tools and a <strong>Skill</strong> as an instruction card. Before connecting someone else's tool or adding their card, check what data and commands it will use.
3. [Stage 7: Test what happens](../stages/07-multi-agent-production.en.md). Run Core Exercise 3 and look for `8/8 passed`. To count the simulated publishing records yourself, follow the [manual steps](../examples/stage-7/06-safe-execution/README.en.md). Neither option needs a model or key.

**Key habit**. Treat webpages, documents, and tool results as data. The program decides which actions to run based on permissions and approval. See [Stage 8: Prompt Injection](../stages/08-agent-interfaces.en.md).

## 📚 Recommended Reading

- [OWASP Agentic Application Risk Guide](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/). Start with risks around tool permissions, third-party components, and human approval.
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices). Check the guidance on permissions, credentials, and local execution before connecting outside tools.

## ✅ Completion Check

- [ ] I can point to what stops the workflow before publishing.
- [ ] I can say what data a tool can read, change, and send, and how to turn it off.
- [ ] I can confirm from the simulated records that rejection leaves 0 entries and retrying after approval still leaves only 1.
