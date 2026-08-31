# Related Resources

> [繁體中文](./RESOURCES.md) | [简体中文](./RESOURCES.zh-Hans.md) | **English**

> [← Back to main README](README.en.md)

## 📌 Choose what you want to do now

You do not need to read the whole list. Pick the task you want to do now:

| I want to… | Start here | Editorial rating |
|---|---|---|
| Learn AI agents from the beginning | [Stage 0](stages/00-foundations.en.md) | ⭐⭐⭐⭐⭐ |
| Understand how models learn and how they are used | [Model training guide](resources/model-training-guide.en.md) | ⭐⭐⭐⭐⭐ |
| Look up an unfamiliar term | [Glossary](resources/glossary.en.md) | ⭐⭐⭐⭐ |
| Choose a CLI agent | [CLI Agents Guide](resources/cli-agents-guide.en.md) | ⭐⭐⭐⭐⭐ |
| Connect an Agent to external tools | [MCP / Skills Catalog](resources/mcp-skills-catalog.en.md) | ⭐⭐⭐⭐⭐ |
| Build a small project step by step | [Cookbook](resources/cookbook.en.md) | ⭐⭐⭐⭐⭐ |

<a id="three-core-terms-mcp--skills--plugins"></a>
## 🧩 Three core terms: MCP, Skill, and Plugin

**MCP (Model Context Protocol)**: an open protocol that lets AI applications connect to external data and tools through a shared method. What it can do still depends on the server, account permissions, and user approval.

**Skill**: a reusable package of instructions that may also include scripts, templates, and references. Different products place and load Skills differently.

**Plugin**: an installable package provided by a host. It may bundle Skills, commands, hooks, or MCP configuration; Plugins are not part of the MCP specification.

For a hands-on example, go to [Stage 5](stages/05-claude-code-ecosystem.en.md). To separate Apps / Connectors, CLI Agents, and MCP Servers, see the [CLI Agents Guide](resources/cli-agents-guide.en.md).

## 📚 Five safe starting points

Start with official entry points or complete learning materials, then evaluate community projects. These are editorial ratings, not GitHub stars.

| Starting point | Learn first | Editorial rating |
|---|---|---|
| [Official MCP Registry](https://registry.modelcontextprotocol.io/) | Find published MCP Servers; still check the maintainer, permissions, and source | ⭐⭐⭐⭐⭐ |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | See educational reference implementations; they are not a production recommendation | ⭐⭐⭐⭐⭐ |
| [anthropics/skills](https://github.com/anthropics/skills) | See how Agent Skill folders, instructions, and resources fit together | ⭐⭐⭐⭐⭐ |
| [github/github-mcp-server](https://github.com/github/github-mcp-server) | Learn OAuth, tool groups, and repository permissions from an official implementation | ⭐⭐⭐⭐⭐ |
| [datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents) | Learn Agent principles and implementation through a Chinese-language course | ⭐⭐⭐⭐⭐ |

> ⚠️ **Start with fewer keys**: an MCP Server may read, create, send, or delete real data. Begin with read-only access, least privilege, and a test workspace; keep **Human Approval** before write, send, or delete actions.

<a id="daily-tool-integrations"></a>
<a id="daily-tool-integrations-mcp-servers--skills"></a>
## 🔌 Common integration groups

The table below shows selected projects and official entry points directly. Start with the group you need; only the longer supplemental list is collapsed.

<table class="resource-table">
<thead><tr><th scope="col">Group</th><th scope="col">Resource</th><th scope="col">What it helps with</th><th scope="col">Status / limits</th><th scope="col">Editorial rating</th></tr></thead>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Notes / Knowledge Bases</th><td><a href="https://developers.notion.com/guides/mcp/overview">Notion MCP</a></td><td>Search, create, and update Notion content</td><td>Official hosted MCP; user OAuth required and permissions follow the signed-in user</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/MarkusPfundstein/mcp-obsidian">MarkusPfundstein/mcp-obsidian</a></td><td>Read and write an Obsidian vault</td><td>Community project; grant only the vault and write scope needed</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://support.google.com/gemininotebook/answer/16164461">Gemini Notebook (formerly NotebookLM)</a></td><td>Summarize and ask questions about your own sources</td><td>Google service; availability varies by region, account, and feature</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/teng-lin/notebooklm-py">teng-lin/notebooklm-py</a></td><td>Operate Gemini Notebook through Python / CLI</td><td>Unofficial interface; Google changes may break it</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="3">Office Documents</th><td><a href="https://github.com/anthropics/skills">anthropics/skills</a></td><td>Read Agent Skill examples and document workflows</td><td>Official examples; built-in Skills vary by Claude surface</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/tfriedel/claude-office-skills">tfriedel/claude-office-skills</a></td><td>Extend Office document automation workflows</td><td>Community Skills; back up files and verify outputs</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://developers.google.com/workspace/guides/configure-mcp-servers">Google Workspace MCP</a></td><td>Connect Gmail, Drive, Docs, Sheets, Slides, Calendar, and Chat</td><td>Official <strong>Developer Preview</strong>; each product has a dedicated server, with OAuth 2.0 and user / organization governance</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Dev Collaboration</th><td><a href="https://github.com/github/github-mcp-server">GitHub MCP Server</a></td><td>Query and work with issues, PRs, and repositories</td><td>Official MCP; use OAuth or a least-privilege token and approve high-impact writes</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/">Atlassian Rovo MCP</a></td><td>Search or update Jira, Confluence, and Bitbucket</td><td>Official hosted remote MCP; OAuth 2.1 and signed-in user permissions apply; require human approval before writing real data</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://linear.app/docs/mcp">Linear MCP</a></td><td>Search and update Linear issues / projects</td><td>Official hosted remote MCP over Streamable HTTP; an official read-only option exists</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://docs.slack.dev/ai/mcp-overview/">Slack MCP</a></td><td>Search Slack, send messages, and manage canvases</td><td>Official MCP; it is not read-only, so confirm before sending or changing content</td><td>⭐⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="4">Research Workflow</th><td><a href="https://github.com/WenyuChiou/ai-research-skills">WenyuChiou/ai-research-skills</a></td><td>Turn research steps into reusable Skills</td><td>Community project; install only Skills relevant to the current task</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/WenyuChiou/research-hub">WenyuChiou/research-hub</a></td><td>Connect Zotero, Obsidian, and research workflows</td><td>Community workspace; check data location, backups, and permissions</td><td>⭐⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/WenyuChiou/zotero-skills">WenyuChiou/zotero-skills</a></td><td>Organize Zotero data with Skills</td><td>Community Skill; back up the library before batch changes</td><td>⭐⭐⭐⭐</td></tr>
<tr><td><a href="https://github.com/WenyuChiou/codex-delegate">WenyuChiou/codex-delegate</a></td><td>Delegate clearly scoped repetitive work to another Agent</td><td>Community tool; lock files, acceptance criteria, and stop conditions first</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
<tbody>
<tr><th scope="rowgroup" rowspan="1">Chinese Ecosystem</th><td><a href="https://github.com/leemysw/feishu-docx">leemysw/feishu-docx</a></td><td>Convert between Feishu (Lark) documents and Markdown</td><td>Community tool; confirm sharing and write permissions</td><td>⭐⭐⭐⭐</td></tr>
</tbody>
</table>

<a id="research-workflow"></a>
<a id="research-workflow-by-the-repo-maintainer"></a>
<a id="topic-awesome-lists"></a>
<a id="topic-based-awesome-lists"></a>
<details markdown="1">
<summary>Expand more lists, courses, and design tools</summary>

- [MCP Registry](https://registry.modelcontextprotocol.io/): the official discovery entry point for published Servers.
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers): browse community Servers by category; review before installing.
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code): Claude Code community resources.
- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills): Agent Skills community list.
- [Canva MCP](https://www.canva.dev/docs/mcp/): official remote MCP; features, plans, and permissions depend on the account, so no fixed tool count is stated.
- [Course list](resources/courses.en.md): choose courses by learning goal; a certificate is not a degree.
- [Agent paradigms](resources/agent-paradigms.en.md): compare common Agent shapes with diagrams.

</details>

<a id="what-else"></a>
## ✅ Next stop

- Unclear term: open [`resources/glossary.en.md`](resources/glossary.en.md).
- Want to build now: open [`resources/cookbook.en.md`](resources/cookbook.en.md).
- Want to understand training choices: open [`resources/model-training-guide.en.md`](resources/model-training-guide.en.md).
- Want to contribute or translate: read [`resources/style-guide.en.md`](resources/style-guide.en.md) and [`CONTRIBUTING.en.md`](CONTRIBUTING.en.md).
