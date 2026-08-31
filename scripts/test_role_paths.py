"""Reader, fact, resource, and mirror contracts for role-path migrations."""

from __future__ import annotations

import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "researcher": {
        "zh-TW": ROOT / "branches/for-researcher.md",
        "en": ROOT / "branches/for-researcher.en.md",
        "zh-Hans": ROOT / "branches/for-researcher.zh-Hans.md",
    },
    "developer": {
        "zh-TW": ROOT / "branches/for-developer.md",
        "en": ROOT / "branches/for-developer.en.md",
        "zh-Hans": ROOT / "branches/for-developer.zh-Hans.md",
    },
    "teacher": {
        "zh-TW": ROOT / "branches/for-teacher.md",
        "en": ROOT / "branches/for-teacher.en.md",
        "zh-Hans": ROOT / "branches/for-teacher.zh-Hans.md",
    },
    "knowledge-worker": {
        "zh-TW": ROOT / "branches/for-knowledge-worker.md",
        "en": ROOT / "branches/for-knowledge-worker.en.md",
        "zh-Hans": ROOT / "branches/for-knowledge-worker.zh-Hans.md",
    },
    "everyday-user": {
        "zh-TW": ROOT / "branches/for-everyday-users.md",
        "en": ROOT / "branches/for-everyday-users.en.md",
        "zh-Hans": ROOT / "branches/for-everyday-users.zh-Hans.md",
    },
}

CORE_TERMS = {
    "researcher": (
        "Source",
        "Claim",
        "Citation",
        "Source Verification",
        "Literature RAG",
        "Reproducibility",
        "Private Data",
        "Human Review",
    ),
    "developer": (
        "IDE／Surface",
        "Coding Agent／Harness",
        "Provider／Router",
        "Model／Runtime",
        "Sandbox",
        "Approval",
        "Diff／Rollback",
        "Eval／Observability",
    ),
    "teacher": (
        "Learning Objective",
        "Scaffolding",
        "Rubric",
        "Formative Assessment",
        "AI Literacy",
        "Student Data",
        "Human Review",
        "Academic Integrity",
    ),
    "knowledge-worker": (
        "Source",
        "Action Item",
        "Knowledge Base",
        "Private Data",
        "Human Review",
        "App／Connector",
        "MCP Server",
        "Workflow Automation",
        "Approval Gate",
    ),
    "everyday-user": (
        "Prompt",
        "Source",
        "Private Data",
        "Hallucination",
        "Human Review",
        "App／Connector",
        "CLI Agent",
        "Local LLM／Runtime",
        "Approval Gate",
    ),
}

RESOURCE_PAIRS = {
    "researcher": (
        ("https://notebooklm.google.com/", "⭐⭐⭐⭐⭐"),
        ("https://www.zotero.org/", "⭐⭐⭐⭐⭐"),
        ("https://github.com/Future-House/paper-qa", "⭐⭐⭐⭐⭐"),
        ("https://github.com/assafelovic/gpt-researcher", "⭐⭐⭐⭐"),
        ("https://github.com/stanford-oval/storm", "⭐⭐⭐⭐"),
        ("https://github.com/kaixindelele/ChatPaper", "⭐⭐⭐⭐⭐"),
        ("https://github.com/MuiseDestiny/zotero-gpt", "⭐⭐⭐⭐"),
        ("https://github.com/asreview/asreview", "⭐⭐⭐⭐"),
        ("https://github.com/treeverse/dvc", "⭐⭐⭐⭐⭐"),
        ("https://github.com/mlflow/mlflow", "⭐⭐⭐⭐⭐"),
        ("https://zenodo.org/", "⭐⭐⭐⭐⭐"),
        ("https://github.com/jupyterhub/repo2docker", "⭐⭐⭐⭐"),
        ("https://github.com/flonat/flonat-research", "⭐⭐⭐"),
        ("https://github.com/SakanaAI/AI-Scientist-v2", "⭐⭐⭐⭐"),
        ("https://github.com/langchain-ai/open_deep_research", "⭐⭐⭐"),
    ),
    "developer": (
        ("https://code.claude.com/docs/en/overview", "⭐⭐⭐⭐⭐"),
        ("https://github.com/openai/codex", "⭐⭐⭐⭐⭐"),
        ("https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent", "⭐⭐⭐⭐⭐"),
        ("https://cursor.com/docs", "⭐⭐⭐⭐⭐"),
        ("https://github.com/anomalyco/opencode", "⭐⭐⭐⭐⭐"),
        ("https://github.com/earendil-works/pi", "⭐⭐⭐⭐"),
        ("https://github.com/Aider-AI/aider", "⭐⭐⭐⭐⭐"),
        ("https://github.com/aaif-goose/goose", "⭐⭐⭐⭐"),
        ("https://github.com/cline/cline", "⭐⭐⭐⭐⭐"),
        ("https://github.com/OpenHands/OpenHands", "⭐⭐⭐⭐"),
        ("https://github.com/obra/superpowers", "⭐⭐⭐⭐"),
        ("https://github.com/yamadashy/repomix", "⭐⭐⭐⭐⭐"),
        ("https://github.com/continuedev/continue", "⭐⭐⭐⭐"),
        ("https://github.com/RooCodeInc/Roo-Code", "⭐⭐⭐"),
    ),
    "teacher": (
        ("https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research?hub=387", "⭐⭐⭐⭐⭐"),
        ("https://education.ec.europa.eu/focus-topics/digital-education/actions/plan/ethical-guidelines-for-educators-on-using-artificial-intelligence", "⭐⭐⭐⭐⭐"),
        ("https://www.teachai.org/toolkit", "⭐⭐⭐⭐⭐"),
        ("https://www.anthropic.com/news/claude-for-teachers", "⭐⭐⭐⭐"),
        ("https://openai.com/index/chatgpt-for-teachers/", "⭐⭐⭐⭐"),
        ("https://support.google.com/gemininotebook/answer/16337734?hl=en", "⭐⭐⭐⭐⭐"),
        ("https://github.com/huggingface/agents-course", "⭐⭐⭐⭐⭐"),
        ("https://github.com/datawhalechina/hello-agents", "⭐⭐⭐⭐⭐"),
        ("https://github.com/microsoft/ai-agents-for-beginners", "⭐⭐⭐⭐"),
        ("https://github.com/anthropics/skills", "⭐⭐⭐⭐⭐"),
        ("https://github.com/obra/superpowers", "⭐⭐⭐⭐"),
        ("https://github.com/f/prompts.chat", "⭐⭐⭐"),
    ),
    "knowledge-worker": (
        ("https://help.openai.com/en/articles/11487775-connectors-in", "⭐⭐⭐⭐⭐"),
        ("https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory", "⭐⭐⭐⭐⭐"),
        ("https://support.google.com/gemini/answer/14959807?co=GENIE.Platform%3DDesktop&hl=en", "⭐⭐⭐⭐⭐"),
        ("https://support.microsoft.com/en-us/microsoft-365-copilot/understand-copilot-connectors", "⭐⭐⭐⭐⭐"),
        ("https://github.com/n8n-io/n8n", "⭐⭐⭐⭐⭐"),
        ("https://academy.make.com/courses/FoundationC01?pc=workflow", "⭐⭐⭐⭐"),
        ("https://learn.microsoft.com/en-us/training/powerplatform/power-automate", "⭐⭐⭐⭐"),
        ("https://help.zapier.com/hc/en-us/articles/22234847450893-Zap-workflows-quick-start-guide", "⭐⭐⭐⭐"),
        ("https://github.com/langflow-ai/langflow", "⭐⭐⭐⭐"),
        ("https://github.com/langgenius/dify", "⭐⭐⭐⭐"),
        ("https://github.com/khoj-ai/khoj", "⭐⭐⭐⭐"),
        ("https://github.com/lobehub/lobehub", "⭐⭐⭐⭐⭐"),
        ("https://github.com/Mintplex-Labs/anything-llm", "⭐⭐⭐⭐⭐"),
        ("https://github.com/obra/superpowers", "⭐⭐⭐⭐"),
        ("https://modelcontextprotocol.io/registry/about", "⭐⭐⭐⭐"),
    ),
    "everyday-user": (
        ("https://claude.ai", "⭐⭐⭐⭐⭐"),
        ("https://chatgpt.com", "⭐⭐⭐⭐⭐"),
        ("https://gemini.google.com", "⭐⭐⭐⭐"),
        ("https://perplexity.ai", "⭐⭐⭐⭐"),
        ("https://help.openai.com/en/articles/10032626-how-do-i-prompt-chatgpt-effectively", "⭐⭐⭐⭐⭐"),
        ("https://support.claude.com/en/articles/8114491-get-started-with-claude", "⭐⭐⭐⭐⭐"),
        ("https://help.openai.com/en/articles/11487775-connectors-in", "⭐⭐⭐⭐⭐"),
        ("https://support.google.com/gemini/answer/13594961?hl=en", "⭐⭐⭐⭐⭐"),
        ("https://github.com/anthropics/claude-code", "⭐⭐⭐⭐⭐"),
        ("https://github.com/openai/codex", "⭐⭐⭐⭐⭐"),
        ("https://github.com/anomalyco/opencode", "⭐⭐⭐⭐⭐"),
        ("https://github.com/google-gemini/gemini-cli", "⭐⭐⭐⭐"),
        ("https://github.com/ollama/ollama", "⭐⭐⭐⭐⭐"),
        ("https://lmstudio.ai/", "⭐⭐⭐⭐"),
        ("https://github.com/f/prompts.chat", "⭐⭐⭐⭐"),
    ),
}

ROWGROUPS = {
    "researcher": (3, 4, 5, 2, 1),
    "developer": (4, 6, 2, 2),
    "teacher": (3, 3, 3, 3),
    "knowledge-worker": (4, 4, 2, 3, 2),
    "everyday-user": (4, 4, 4, 2, 1),
}

VISIBLE_STARTING_URLS = {
    "researcher": (
        *(url for url, _rating in RESOURCE_PAIRS["researcher"]),
    ),
    "developer": (
        *(url for url, _rating in RESOURCE_PAIRS["developer"]),
    ),
    "teacher": tuple(url for url, _rating in RESOURCE_PAIRS["teacher"]),
    "knowledge-worker": tuple(url for url, _rating in RESOURCE_PAIRS["knowledge-worker"]),
    "everyday-user": tuple(url for url, _rating in RESOURCE_PAIRS["everyday-user"]),
}

VISIBLE_FIVE_STAR_COUNTS = {
    "researcher": 10,
    "developer": 8,
    "teacher": 10,
    "knowledge-worker": 7,
    "everyday-user": 10,
}

DETAIL_COUNTS = {
    "researcher": 3,
    "developer": 3,
    "teacher": 5,
    "knowledge-worker": 3,
    "everyday-user": 3,
}

RESEARCHER_REQUIRED_READING_URLS = (
    "https://support.google.com/gemininotebook/answer/16179559",
    "https://support.google.com/gemininotebook/answer/17004255",
    "https://www.zotero.org/support/quick_start_guide",
    "https://github.com/Future-House/paper-qa",
    "https://doc.dvc.org/command-reference",
    "https://help.zenodo.org/docs/get-started/quickstart/",
)

DEVELOPER_REQUIRED_READING_URLS = (
    "https://code.claude.com/docs/en/permissions",
    "https://learn.chatgpt.com/docs/agent-approvals-security",
    "https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent",
    "https://github.com/earendil-works/pi#permissions--containerization",
    "https://openrouter.ai/docs/guides/routing/provider-selection",
    "https://docs.ollama.com/",
)

KNOWLEDGE_WORKER_REQUIRED_READING_URLS = (
    "https://help.openai.com/en/articles/11487775-connectors-in",
    "https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory",
    "https://support.google.com/gemini/answer/14959807?co=GENIE.Platform%3DDesktop&hl=en",
    "https://support.microsoft.com/en-us/microsoft-365-copilot/understand-copilot-connectors",
    "https://modelcontextprotocol.io/registry/about",
    "https://help.zapier.com/hc/en-us/articles/22234847450893-Zap-workflows-quick-start-guide",
)

EVERYDAY_USER_REQUIRED_READING_URLS = (
    "https://help.openai.com/en/articles/10032626-how-do-i-prompt-chatgpt-effectively",
    "https://support.claude.com/en/articles/8114491-get-started-with-claude",
    "https://help.openai.com/en/articles/11487775-connectors-in",
    "https://support.claude.com/en/articles/11725091-when-to-use-desktop-and-web-connectors",
    "https://support.google.com/gemini/answer/13594961?hl=en",
    "https://docs.ollama.com/faq",
)

DEVELOPER_EXERCISE_SAFETY = {
    "zh-TW": (
        "在我明確人工批准前，不要寫檔。",
        "不要 push、merge 或 deploy。",
        "不要用會清掉整個工作區的指令。",
    ),
    "en": (
        "Before my explicit human Approval, do not write files.",
        "Do not push, merge, or deploy.",
        "never clear the whole worktree.",
    ),
    "zh-Hans": (
        "在我明确人工 Approval 前不要写文件。",
        "不要 push、merge 或 deploy。",
        "不要清空整个工作区。",
    ),
}

DEVELOPER_EXERCISE_BOUNDS = {
    "zh-TW": ("## 🛠 第一個練習", "## 📚 先選一個入口"),
    "en": ("## 🛠 First exercise", "## 📚 Choose an entry point"),
    "zh-Hans": ("## 🛠 第一个练习", "## 📚 先选一个入口"),
}

DEVELOPER_NON_SYNONYM_TEXT = {
    "zh-TW": (
        "不代表它只能在 IDE 裡工作",
        "兩者常放在同一產品裡，但不是同一個意思",
    ),
    "en": (
        "does not mean it only works in an IDE",
        "They may be in one product but are not the same thing",
    ),
    "zh-Hans": (
        "不代表它只能在 IDE 中工作",
        "两者常在同一产品中，但含义不同",
    ),
}

PI_NO_BUILT_IN_SANDBOX = {
    "zh-TW": "沒有內建 sandbox，要自行隔離",
    "en": "no built-in Sandbox, so isolate it yourself",
    "zh-Hans": "没有内置 sandbox，需自行隔离",
}

VISIBLE_LANDMARKS = {
    "researcher": ("## 📌", "## 🎯", "## 🧩", "## 🛠", "## 📚", "## 📖", "## ⭐", "## ✅"),
    "developer": ("## 📌", "## 🎯", "## 🧩", "## 🛠", "## 📚", "## 📖", "## ⭐", "## ✅"),
    "teacher": ("## 📌", "## 🎯", "## 🧩", "## 🛡", "## 🛠", "## 📚", "## ⭐", "## ✅"),
    "knowledge-worker": ("## 📌", "## 🎯", "## 🧩", "## 🛠", "## 📚", "## 📖", "## ⭐", "## ✅"),
    "everyday-user": ("## 📌", "## 🎯", "## 🧩", "## 🛠", "## 🚪", "## 📖", "## ⭐", "## ✅"),
}

RESOURCE_STATUS = {
    "https://notebooklm.google.com/": "available",
    "https://www.zotero.org/": "available",
    "https://github.com/Future-House/paper-qa": "active",
    "https://github.com/assafelovic/gpt-researcher": "active",
    "https://github.com/stanford-oval/storm": "usable",
    "https://github.com/kaixindelele/ChatPaper": "usable",
    "https://github.com/MuiseDestiny/zotero-gpt": "usable",
    "https://github.com/asreview/asreview": "active",
    "https://github.com/treeverse/dvc": "active",
    "https://github.com/mlflow/mlflow": "active",
    "https://zenodo.org/": "available",
    "https://github.com/jupyterhub/repo2docker": "active",
    "https://github.com/flonat/flonat-research": "active",
    "https://github.com/SakanaAI/AI-Scientist-v2": "research",
    "https://github.com/langchain-ai/open_deep_research": "archived",
    "https://code.claude.com/docs/en/overview": "commercial",
    "https://github.com/openai/codex": "active",
    "https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent": "commercial",
    "https://github.com/anomalyco/opencode": "active",
    "https://github.com/earendil-works/pi": "active",
    "https://github.com/Aider-AI/aider": "active",
    "https://github.com/aaif-goose/goose": "active",
    "https://cursor.com/docs": "commercial",
    "https://github.com/cline/cline": "active",
    "https://github.com/continuedev/continue": "read-only",
    "https://github.com/OpenHands/OpenHands": "active",
    "https://github.com/obra/superpowers": "active",
    "https://github.com/yamadashy/repomix": "active",
    "https://github.com/RooCodeInc/Roo-Code": "archived",
    "https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research?hub=387": "current",
    "https://education.ec.europa.eu/focus-topics/digital-education/actions/plan/ethical-guidelines-for-educators-on-using-artificial-intelligence": "current",
    "https://www.teachai.org/toolkit": "current",
    "https://www.anthropic.com/news/claude-for-teachers": "limited",
    "https://openai.com/index/chatgpt-for-teachers/": "limited",
    "https://support.google.com/gemininotebook/answer/16337734?hl=en": "available",
    "https://github.com/huggingface/agents-course": "active",
    "https://github.com/datawhalechina/hello-agents": "active",
    "https://github.com/microsoft/ai-agents-for-beginners": "active",
    "https://github.com/anthropics/skills": "active",
    "https://github.com/f/prompts.chat": "active",
    "https://help.openai.com/en/articles/11487775-connectors-in": "commercial",
    "https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory": "commercial",
    "https://support.google.com/gemini/answer/14959807?co=GENIE.Platform%3DDesktop&hl=en": "commercial",
    "https://support.microsoft.com/en-us/microsoft-365-copilot/understand-copilot-connectors": "commercial",
    "https://github.com/n8n-io/n8n": "active",
    "https://academy.make.com/courses/FoundationC01?pc=workflow": "commercial",
    "https://learn.microsoft.com/en-us/training/powerplatform/power-automate": "commercial",
    "https://help.zapier.com/hc/en-us/articles/22234847450893-Zap-workflows-quick-start-guide": "commercial",
    "https://github.com/langflow-ai/langflow": "active",
    "https://github.com/langgenius/dify": "active",
    "https://github.com/khoj-ai/khoj": "active",
    "https://github.com/lobehub/lobehub": "active",
    "https://github.com/Mintplex-Labs/anything-llm": "active",
    "https://modelcontextprotocol.io/registry/about": "preview",
    "https://claude.ai": "available",
    "https://chatgpt.com": "available",
    "https://gemini.google.com": "available",
    "https://perplexity.ai": "available",
    "https://help.openai.com/en/articles/10032626-how-do-i-prompt-chatgpt-effectively": "current",
    "https://support.claude.com/en/articles/8114491-get-started-with-claude": "current",
    "https://support.google.com/gemini/answer/13594961?hl=en": "current",
    "https://github.com/anthropics/claude-code": "active",
    "https://github.com/google-gemini/gemini-cli": "active",
    "https://github.com/ollama/ollama": "active",
    "https://lmstudio.ai/": "commercial",
}

STATUS_TOKENS = {
    "available": {"zh-TW": "正式可用", "en": "Available", "zh-Hans": "正式可用"},
    "active": {"zh-TW": "活躍", "en": "Active", "zh-Hans": "活跃"},
    "usable": {"zh-TW": "可用", "en": "Usable", "zh-Hans": "可用"},
    "research": {"zh-TW": "研究參考", "en": "Research reference", "zh-Hans": "研究参考"},
    "archived": {"zh-TW": "已封存", "en": "archived", "zh-Hans": "已封存"},
    "commercial": {"zh-TW": "商業", "en": "Commercial", "zh-Hans": "商业"},
    "read-only": {"zh-TW": "read-only", "en": "Read-only", "zh-Hans": "read-only"},
    "current": {"zh-TW": "現行", "en": "Current", "zh-Hans": "现行"},
    "limited": {"zh-TW": "限區可用", "en": "Region-limited", "zh-Hans": "限区可用"},
    "preview": {"zh-TW": "Preview", "en": "Preview", "zh-Hans": "Preview"},
}

RESOURCE_LICENSE_OR_SERVICE = {
    "https://notebooklm.google.com/": {"zh-TW": "雲端服務", "en": "cloud service", "zh-Hans": "云服务"},
    "https://www.zotero.org/": {"zh-TW": "桌面", "en": "desktop", "zh-Hans": "桌面"},
    "https://github.com/Future-House/paper-qa": "Apache-2.0",
    "https://github.com/assafelovic/gpt-researcher": "Apache-2.0",
    "https://github.com/stanford-oval/storm": "MIT",
    "https://github.com/kaixindelele/ChatPaper": "CC BY-NC-ND 4.0",
    "https://github.com/MuiseDestiny/zotero-gpt": "AGPL-3.0",
    "https://github.com/asreview/asreview": "Apache-2.0",
    "https://github.com/treeverse/dvc": "Apache-2.0",
    "https://github.com/mlflow/mlflow": "Apache-2.0",
    "https://zenodo.org/": {"zh-TW": "雲端服務", "en": "cloud service", "zh-Hans": "云服务"},
    "https://github.com/jupyterhub/repo2docker": "BSD-3-Clause",
    "https://github.com/flonat/flonat-research": "MIT",
    "https://github.com/SakanaAI/AI-Scientist-v2": "source-code license",
    "https://github.com/langchain-ai/open_deep_research": "MIT",
    "https://code.claude.com/docs/en/overview": {"zh-TW": "商業", "en": "Commercial", "zh-Hans": "商业"},
    "https://github.com/openai/codex": {
        "zh-TW": "repo 程式碼為 Apache-2.0，app／cloud 依服務條款",
        "en": "repository code is Apache-2.0, while app/cloud follow their service terms",
        "zh-Hans": "repo 代码为 Apache-2.0，app／cloud 依服务条款",
    },
    "https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent": {"zh-TW": "商業", "en": "Commercial", "zh-Hans": "商业"},
    "https://github.com/anomalyco/opencode": "MIT",
    "https://github.com/earendil-works/pi": "MIT",
    "https://github.com/Aider-AI/aider": "Apache-2.0",
    "https://github.com/aaif-goose/goose": "Apache-2.0",
    "https://cursor.com/docs": {"zh-TW": "商業", "en": "Commercial", "zh-Hans": "商业"},
    "https://github.com/cline/cline": "Apache-2.0",
    "https://github.com/continuedev/continue": "Apache-2.0",
    "https://github.com/OpenHands/OpenHands": "MIT",
    "https://github.com/obra/superpowers": "MIT",
    "https://github.com/yamadashy/repomix": "MIT",
    "https://github.com/RooCodeInc/Roo-Code": "Apache-2.0",
    "https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research?hub=387": {"zh-TW": "官方指引", "en": "official guidance", "zh-Hans": "官方指南"},
    "https://education.ec.europa.eu/focus-topics/digital-education/actions/plan/ethical-guidelines-for-educators-on-using-artificial-intelligence": {"zh-TW": "官方指引", "en": "official guidance", "zh-Hans": "官方指南"},
    "https://www.teachai.org/toolkit": {"zh-TW": "教育工具包", "en": "education toolkit", "zh-Hans": "教育工具包"},
    "https://www.anthropic.com/news/claude-for-teachers": {"zh-TW": "雲端服務", "en": "cloud service", "zh-Hans": "云服务"},
    "https://openai.com/index/chatgpt-for-teachers/": {"zh-TW": "雲端服務", "en": "cloud service", "zh-Hans": "云服务"},
    "https://support.google.com/gemininotebook/answer/16337734?hl=en": {"zh-TW": "雲端服務", "en": "cloud service", "zh-Hans": "云服务"},
    "https://github.com/huggingface/agents-course": "Apache-2.0",
    "https://github.com/datawhalechina/hello-agents": "CC BY-NC-SA 4.0",
    "https://github.com/microsoft/ai-agents-for-beginners": "MIT",
    "https://github.com/anthropics/skills": {"zh-TW": "各資料夾授權", "en": "per-folder licenses", "zh-Hans": "各文件夹授权"},
    "https://github.com/f/prompts.chat": {"zh-TW": "MIT／CC0", "en": "MIT / CC0", "zh-Hans": "MIT／CC0"},
    "https://help.openai.com/en/articles/11487775-connectors-in": {"zh-TW": "商業雲端服務", "en": "commercial cloud service", "zh-Hans": "商业云服务"},
    "https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory": {"zh-TW": "商業雲端服務", "en": "commercial cloud service", "zh-Hans": "商业云服务"},
    "https://support.google.com/gemini/answer/14959807?co=GENIE.Platform%3DDesktop&hl=en": {"zh-TW": "商業雲端服務", "en": "commercial cloud service", "zh-Hans": "商业云服务"},
    "https://support.microsoft.com/en-us/microsoft-365-copilot/understand-copilot-connectors": {"zh-TW": "商業雲端服務", "en": "commercial cloud service", "zh-Hans": "商业云服务"},
    "https://github.com/n8n-io/n8n": "Sustainable Use License",
    "https://academy.make.com/courses/FoundationC01?pc=workflow": {"zh-TW": "商業雲端服務", "en": "commercial cloud service", "zh-Hans": "商业云服务"},
    "https://learn.microsoft.com/en-us/training/powerplatform/power-automate": {"zh-TW": "商業雲端服務", "en": "commercial cloud service", "zh-Hans": "商业云服务"},
    "https://help.zapier.com/hc/en-us/articles/22234847450893-Zap-workflows-quick-start-guide": {"zh-TW": "商業雲端服務", "en": "commercial cloud service", "zh-Hans": "商业云服务"},
    "https://github.com/langflow-ai/langflow": "MIT",
    "https://github.com/langgenius/dify": {"zh-TW": "修改版 Apache-2.0", "en": "modified Apache-2.0", "zh-Hans": "修改版 Apache-2.0"},
    "https://github.com/khoj-ai/khoj": "AGPL-3.0",
    "https://github.com/lobehub/lobehub": "LobeHub Community License",
    "https://github.com/Mintplex-Labs/anything-llm": "MIT",
    "https://modelcontextprotocol.io/registry/about": {"zh-TW": "官方 metadata 服務", "en": "official metadata service", "zh-Hans": "官方 metadata 服务"},
    "https://claude.ai": {"zh-TW": "商業雲端服務", "en": "commercial cloud service", "zh-Hans": "商业云服务"},
    "https://chatgpt.com": {"zh-TW": "商業雲端服務", "en": "commercial cloud service", "zh-Hans": "商业云服务"},
    "https://gemini.google.com": {"zh-TW": "商業雲端服務", "en": "commercial cloud service", "zh-Hans": "商业云服务"},
    "https://perplexity.ai": {"zh-TW": "商業雲端服務", "en": "commercial cloud service", "zh-Hans": "商业云服务"},
    "https://help.openai.com/en/articles/10032626-how-do-i-prompt-chatgpt-effectively": {"zh-TW": "官方指引", "en": "official guidance", "zh-Hans": "官方指南"},
    "https://support.claude.com/en/articles/8114491-get-started-with-claude": {"zh-TW": "官方指引", "en": "official guidance", "zh-Hans": "官方指南"},
    "https://support.google.com/gemini/answer/13594961?hl=en": {"zh-TW": "官方隱私指引", "en": "official privacy guidance", "zh-Hans": "官方隐私指南"},
    "https://github.com/anthropics/claude-code": {"zh-TW": "商業服務；repo 未標示標準開源授權", "en": "commercial service; repository has no standard open-source license", "zh-Hans": "商业服务；repo 未标示标准开源许可证"},
    "https://github.com/google-gemini/gemini-cli": "Apache-2.0",
    "https://github.com/ollama/ollama": "MIT",
    "https://lmstudio.ai/": {"zh-TW": "商業桌面應用程式", "en": "commercial desktop application", "zh-Hans": "商业桌面应用程序"},
}

RESOURCE_LIMIT_TOKENS = {
    "https://notebooklm.google.com/": {"zh-TW": "citation", "en": "citations", "zh-Hans": "引用"},
    "https://www.zotero.org/": {"zh-TW": "研究品質", "en": "research quality", "zh-Hans": "研究质量"},
    "https://github.com/Future-House/paper-qa": {"zh-TW": "評測", "en": "evaluate", "zh-Hans": "评测"},
    "https://github.com/assafelovic/gpt-researcher": {"zh-TW": "引用", "en": "citation", "zh-Hans": "引用"},
    "https://github.com/stanford-oval/storm": {"zh-TW": "依賴", "en": "dependencies", "zh-Hans": "依赖"},
    "https://github.com/kaixindelele/ChatPaper": {"zh-TW": "商業", "en": "commercial", "zh-Hans": "商业"},
    "https://github.com/MuiseDestiny/zotero-gpt": {"zh-TW": "模型", "en": "model", "zh-Hans": "模型"},
    "https://github.com/asreview/asreview": {"zh-TW": "人工篩選", "en": "human screening", "zh-Hans": "人工筛选"},
    "https://github.com/treeverse/dvc": {"zh-TW": "資料版本", "en": "data versions", "zh-Hans": "数据版本"},
    "https://github.com/mlflow/mlflow": {"zh-TW": "run", "en": "runs", "zh-Hans": "run"},
    "https://zenodo.org/": {"zh-TW": "私人資料", "en": "private data", "zh-Hans": "私人资料"},
    "https://github.com/jupyterhub/repo2docker": {"zh-TW": "container", "en": "container", "zh-Hans": "container"},
    "https://github.com/flonat/flonat-research": {"zh-TW": "領域", "en": "field", "zh-Hans": "领域"},
    "https://github.com/SakanaAI/AI-Scientist-v2": {"zh-TW": "作者", "en": "authors", "zh-Hans": "作者"},
    "https://github.com/langchain-ai/open_deep_research": {"zh-TW": "現行預設", "en": "current default", "zh-Hans": "现行默认"},
    "https://code.claude.com/docs/en/overview": {"zh-TW": "permission", "en": "permission", "zh-Hans": "permission"},
    "https://github.com/openai/codex": {"zh-TW": "approval", "en": "approval", "zh-Hans": "approval"},
    "https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent": {"zh-TW": "人工", "en": "human", "zh-Hans": "人工"},
    "https://github.com/anomalyco/opencode": {"zh-TW": "AGENTS.md", "en": "AGENTS.md", "zh-Hans": "AGENTS.md"},
    "https://github.com/earendil-works/pi": {"zh-TW": "sandbox", "en": "sandbox", "zh-Hans": "sandbox"},
    "https://github.com/Aider-AI/aider": {"zh-TW": "hook", "en": "hooks", "zh-Hans": "hook"},
    "https://github.com/aaif-goose/goose": {"zh-TW": "權限", "en": "privilege", "zh-Hans": "权限"},
    "https://cursor.com/docs": {"zh-TW": "權限", "en": "permissions", "zh-Hans": "权限"},
    "https://github.com/cline/cline": {"zh-TW": "安全", "en": "safety", "zh-Hans": "安全"},
    "https://github.com/continuedev/continue": {"zh-TW": "2.0.0", "en": "2.0.0", "zh-Hans": "2.0.0"},
    "https://github.com/OpenHands/OpenHands": {"zh-TW": "人工", "en": "human", "zh-Hans": "人工"},
    "https://github.com/obra/superpowers": {"zh-TW": "gate", "en": "gate", "zh-Hans": "gate"},
    "https://github.com/yamadashy/repomix": {"zh-TW": "secret", "en": "secrets", "zh-Hans": "secrets"},
    "https://github.com/RooCodeInc/Roo-Code": {"zh-TW": "仍在維護", "en": "maintained", "zh-Hans": "仍在维护"},
    "https://www.unesco.org/en/articles/guidance-generative-ai-education-and-research?hub=387": {"zh-TW": "年齡", "en": "age", "zh-Hans": "年龄"},
    "https://education.ec.europa.eu/focus-topics/digital-education/actions/plan/ethical-guidelines-for-educators-on-using-artificial-intelligence": {"zh-TW": "AI Act", "en": "AI Act", "zh-Hans": "AI Act"},
    "https://www.teachai.org/toolkit": {"zh-TW": "校方政策", "en": "school policy", "zh-Hans": "校方政策"},
    "https://www.anthropic.com/news/claude-for-teachers": {"zh-TW": "美國 K-12", "en": "U.S. K-12", "zh-Hans": "美国 K-12"},
    "https://openai.com/index/chatgpt-for-teachers/": {"zh-TW": "美國 K-12", "en": "U.S. K-12", "zh-Hans": "美国 K-12"},
    "https://support.google.com/gemininotebook/answer/16337734?hl=en": {"zh-TW": "學校政策", "en": "school policy", "zh-Hans": "学校政策"},
    "https://github.com/huggingface/agents-course": {"zh-TW": "日常工具", "en": "daily tool for teachers", "zh-Hans": "日常工具"},
    "https://github.com/datawhalechina/hello-agents": {"zh-TW": "非商業", "en": "noncommercial", "zh-Hans": "非商业"},
    "https://github.com/microsoft/ai-agents-for-beginners": {"zh-TW": "版本", "en": "versions", "zh-Hans": "版本"},
    "https://github.com/anthropics/skills": {"zh-TW": "授權", "en": "license", "zh-Hans": "授权"},
    "https://github.com/f/prompts.chat": {"zh-TW": "品質", "en": "quality", "zh-Hans": "质量"},
    "https://help.openai.com/en/articles/11487775-connectors-in": {"zh-TW": "人工確認", "en": "human confirmation", "zh-Hans": "人工确认"},
    "https://support.claude.com/en/articles/14328846-browse-skills-connectors-and-plugins-in-one-directory": {"zh-TW": "管理員", "en": "administrator", "zh-Hans": "管理员"},
    "https://support.google.com/gemini/answer/14959807?co=GENIE.Platform%3DDesktop&hl=en": {"zh-TW": "來源", "en": "sources", "zh-Hans": "来源"},
    "https://support.microsoft.com/en-us/microsoft-365-copilot/understand-copilot-connectors": {"zh-TW": "權限", "en": "permissions", "zh-Hans": "权限"},
    "https://github.com/n8n-io/n8n": {"zh-TW": "自架安全", "en": "self-hosting security", "zh-Hans": "自架安全"},
    "https://academy.make.com/courses/FoundationC01?pc=workflow": {"zh-TW": "費用", "en": "cost", "zh-Hans": "费用"},
    "https://learn.microsoft.com/en-us/training/powerplatform/power-automate": {"zh-TW": "管理員", "en": "administrator", "zh-Hans": "管理员"},
    "https://help.zapier.com/hc/en-us/articles/22234847450893-Zap-workflows-quick-start-guide": {"zh-TW": "無限迴圈", "en": "infinite loop", "zh-Hans": "无限循环"},
    "https://github.com/langflow-ai/langflow": {"zh-TW": "production 安全", "en": "production security", "zh-Hans": "production 安全"},
    "https://github.com/langgenius/dify": {"zh-TW": "多租戶", "en": "multi-tenant", "zh-Hans": "多租户"},
    "https://github.com/khoj-ai/khoj": {"zh-TW": "資料設定", "en": "data configuration", "zh-Hans": "数据设置"},
    "https://github.com/lobehub/lobehub": {"zh-TW": "衍生作品", "en": "derivative work", "zh-Hans": "衍生作品"},
    "https://github.com/Mintplex-Labs/anything-llm": {"zh-TW": "模型供應商", "en": "model provider", "zh-Hans": "模型供应商"},
    "https://modelcontextprotocol.io/registry/about": {"zh-TW": "不是安全審查", "en": "not a security review", "zh-Hans": "不是安全审查"},
    "https://claude.ai": {"zh-TW": "方案與地區", "en": "plan and region", "zh-Hans": "方案与地区"},
    "https://chatgpt.com": {"zh-TW": "仍會出錯", "en": "can still be wrong", "zh-Hans": "仍会出错"},
    "https://gemini.google.com": {"zh-TW": "人工審查", "en": "human review", "zh-Hans": "人工审查"},
    "https://perplexity.ai": {"zh-TW": "逐一打開來源", "en": "open each source", "zh-Hans": "逐一打开来源"},
    "https://help.openai.com/en/articles/10032626-how-do-i-prompt-chatgpt-effectively": {"zh-TW": "仍要查證", "en": "still verify", "zh-Hans": "仍要查证"},
    "https://support.claude.com/en/articles/8114491-get-started-with-claude": {"zh-TW": "使用限制", "en": "usage limits", "zh-Hans": "使用限制"},
    "https://support.google.com/gemini/answer/13594961?hl=en": {"zh-TW": "機密資料", "en": "confidential data", "zh-Hans": "机密数据"},
    "https://github.com/anthropics/claude-code": {"zh-TW": "permission", "en": "permissions", "zh-Hans": "permission"},
    "https://github.com/google-gemini/gemini-cli": {"zh-TW": "sandbox", "en": "sandbox", "zh-Hans": "sandbox"},
    "https://github.com/ollama/ollama": {"zh-TW": "cloud model", "en": "cloud models", "zh-Hans": "cloud model"},
    "https://lmstudio.ai/": {"zh-TW": "雲端功能", "en": "cloud features", "zh-Hans": "云功能"},
}

DEVELOPER_ROW_FACTS = {
    "https://code.claude.com/docs/en/overview": (("coding agent",), ("CLI", "IDE", "desktop", "cloud")),
    "https://github.com/openai/codex": (("coding agent",), ("app", "CLI", "IDE", "cloud")),
    "https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent": (("coding agent", "code assistant"), ("GitHub", "IDE", "CLI", "app")),
    "https://cursor.com/docs": (("coding agent", "AI editor"), ("IDE", "CLI", "cloud", "SDK")),
    "https://github.com/anomalyco/opencode": (("coding agent", "harness"), ("terminal", "desktop")),
    "https://github.com/earendil-works/pi": (("coding agent", "harness"), ("terminal", "SDK", "RPC")),
    "https://github.com/Aider-AI/aider": (("coding agent", "pair programmer"), ("CLI",)),
    "https://github.com/aaif-goose/goose": (("coding", "general agent"), ("CLI", "desktop", "API")),
    "https://github.com/cline/cline": (("coding agent",), ("IDE", "CLI", "SDK")),
    "https://github.com/continuedev/continue": (("coding agent",), ("CLI", "VS Code", "JetBrains")),
    "https://github.com/OpenHands/OpenHands": (("software-development agent platform",), ("web", "CLI", "SDK", "cloud")),
    "https://github.com/obra/superpowers": (("workflow collection",), ("agent plugin", "skills")),
    "https://github.com/yamadashy/repomix": (("repo context packer",), ("CLI", "MCP")),
    "https://github.com/RooCodeInc/Roo-Code": (("coding agent",), ("VS Code extension",)),
}
FRESHNESS = {
    "researcher": (
        "<!-- freshness: canonical=branches/for-researcher.md; "
        "verified_on=2026-08-29; "
        "scope=research-tools,citations,privacy,reproducibility,project-status; "
        "max_age_days=90 -->"
    ),
    "developer": (
        "<!-- freshness: canonical=branches/for-developer.md; "
        "verified_on=2026-08-29; "
        "scope=coding-agents,tool-identity,permissions,sandboxing,project-status; "
        "max_age_days=90 -->"
    ),
    "teacher": (
        "<!-- freshness: canonical=branches/for-teacher.md; "
        "verified_on=2026-08-29; "
        "scope=education-guidance,student-data,assessment,tool-availability,project-status; "
        "max_age_days=90 -->"
    ),
    "knowledge-worker": (
        "<!-- freshness: canonical=branches/for-knowledge-worker.md; "
        "verified_on=2026-08-29; "
        "scope=apps,connectors,mcp,workflow-automation,permissions,project-status; "
        "max_age_days=90 -->"
    ),
    "everyday-user": (
        "<!-- freshness: canonical=branches/for-everyday-users.md; "
        "verified_on=2026-08-29; "
        "scope=chat-apps,connectors,cli-agents,local-runtimes,privacy,project-status; "
        "max_age_days=90 -->"
    ),
}

LEGACY_ANCHORS = {
    "researcher": {
        "zh-TW": (
            "使用情境研究階段-ai-怎麼幫",
            "精選-projects",
            "研究流程-marketplace",
            "文獻-rag--qa",
            "大綱與寫作",
            "文獻管理整合",
            "multi-llm-研究組合本-repo-維護者的研究-setup",
            "multi-agent-for-research",
            "必修閱讀",
            "必練流程按使用頻率",
            "層級建議",
        ),
        "en": (
            "use-cases",
            "curated-projects",
            "research-workflow-marketplaces",
            "literature-rag--qa",
            "outline--writing",
            "citation-manager-integrations",
            "multi-llm-research-stack-maintainer-setup",
            "multi-agent-for-research",
            "required-reading",
            "workflows-to-master",
            "tier-recommendations",
        ),
        "zh-Hans": (
            "使用场景研究阶段-ai-怎么帮",
            "精选-projects",
            "研究流程-marketplace",
            "文献-rag--qa",
            "大纲与写作",
            "文献管理集成",
            "multi-llm-研究组合本-repo-维护者的研究-setup",
            "multi-agent-for-research",
            "必修阅读",
            "必练流程按使用频率",
            "层级建议",
        ),
    },
    "developer": {
        "zh-TW": (
            "使用情境開發場景-ai-怎麼幫",
            "精選-projects",
            "coding-agents",
            "code-review",
            "推薦工具",
            "必練流程按使用頻率",
            "3-個具體-workflow-recipe",
            "常見踩坑anti-patterns",
            "tier-升級路徑",
            "也適用其他分支",
            "社群備註",
        ),
        "en": (
            "use-cases-developer-scenarios--how-ai-helps",
            "curated-projects",
            "coding-agents",
            "code-review",
            "recommended-tools",
            "workflows-to-master-by-frequency",
            "3-concrete-workflow-recipes",
            "common-pitfalls-anti-patterns",
            "tier-progression",
            "other-branches-also-apply",
            "community-note",
        ),
        "zh-Hans": (
            "使用场景开发场景-ai-怎么帮",
            "精选-projects",
            "coding-agents",
            "code-review",
            "推荐工具",
            "必练流程按使用频率",
            "3-个具体-workflow-recipe",
            "常见踩坑anti-patterns",
            "tier-升级路径",
            "也适用其他分支",
            "社群备注",
        ),
    },
    "teacher": {
        "zh-TW": (
            "使用情境",
            "教師使用-ai-輔助時要注意什麼",
            "備課與上課素材製作",
            "教學現場與學習輔助",
            "其他應用場景",
            "參考文獻",
            "精選-projects",
            "教學流程-skills",
            "可用的基礎元件",
            "教學課程素材給教師備課用",
            "prompt-素材庫",
            "閱讀材料",
            "可以建的流程按教學階段",
            "3-個可直接複製的-prompt-範本",
            "隱私--倫理重要",
            "給教師的層級建議",
            "也適用其他分支",
            "社群備註",
        ),
        "en": (
            "use-cases",
            "what-teachers-should-watch-for-when-using-ai",
            "lesson-prep-and-class-material-creation",
            "classroom-and-learning-support",
            "other-use-cases",
            "references",
            "curated-projects",
            "teaching-workflow-skills",
            "available-building-blocks",
            "course-materials-for-teaching",
            "prompt-libraries",
            "reading-materials",
            "workflows-you-can-build-by-teaching-stage",
            "3-copy-ready-prompt-templates",
            "privacy--ethics-important",
            "tier-recommendations-for-teachers",
            "other-branches-that-also-apply",
            "community-note",
        ),
        "zh-Hans": (
            "使用场景",
            "教师使用-ai-辅助时要注意什么",
            "备课与上课素材制作",
            "教学现场与学习辅助",
            "其他应用场景",
            "参考文献",
            "精选-projects",
            "教学流程-skills",
            "可用的基础组件",
            "教学课程素材给教师备课用",
            "prompt-素材库",
            "阅读材料",
            "可以构建的流程按教学阶段",
            "3-个可直接复制的-prompt-模板",
            "隐私--伦理重要",
            "给教师的层级建议",
            "也适用其他分支",
            "社群备注",
        ),
    },
    "knowledge-worker": {
        "zh-TW": (
            "使用情境辦公場景--ai-怎麼幫",
            "精選-projects",
            "工作流工具",
            "知識工作者-skills",
            "知識管理--個人-ai",
            "對知識工作者有用的-mcp-server",
            "可以建的流程按使用頻率",
            "層級建議",
            "閱讀",
        ),
        "en": (
            "use-cases-office-scenarios--how-ai-helps",
            "curated-projects",
            "workflow-tools",
            "knowledge-worker-skills",
            "knowledge-management--personal-ai",
            "mcp-servers-useful-for-knowledge-workers",
            "workflows-you-can-build-by-frequency",
            "tier-recommendations",
            "reading",
        ),
        "zh-Hans": (
            "使用场景办公场景--ai-怎么帮",
            "精选-projects",
            "工作流工具",
            "知识工作者-skills",
            "知识管理--个人-ai",
            "对知识工作者有用的-mcp-server",
            "可以建的流程按使用频率",
            "层级建议",
            "阅读",
        ),
    },
    "everyday-user": {
        "zh-TW": (
            "使用情境生活場景--ai-怎麼幫",
            "起步你應該從哪一層進來",
            "-精選-projects",
            "tier-2--cli-agent願意學命令列的進階使用者",
            "必修閱讀",
            "可以建的流程按使用頻率",
            "給日常使用者的層級建議",
            "社群備註",
        ),
        "en": (
            "use-cases-life-scenarios--how-ai-helps",
            "where-to-start-4-tiers-by-how-hands-on-are-you",
            "-curated-projects",
            "tier-2--cli-agents-advanced-users-willing-to-learn-the-command-line",
            "required-reading",
            "workflows-you-can-build-by-frequency",
            "tier-recommendations-for-everyday-users",
            "community-notes",
        ),
        "zh-Hans": (
            "使用场景生活场景--ai-怎么帮",
            "起步你应该从哪一层进入",
            "-精选-projects",
            "tier-2--cli-agent愿意学命令行的进阶用户",
            "必修阅读",
            "可以建的流程按使用频率",
            "给日常用户的层级建议",
            "社群备注",
        ),
    },
}


def _without_details(text: str) -> str:
    return re.sub(r"<details\b[^>]*>.*?</details>", "", text, flags=re.DOTALL)


def _resource_table(text: str, first_url: str) -> str:
    tables = re.findall(r"<table>.*?</table>", text, flags=re.DOTALL)
    matches = [table for table in tables if first_url in table]
    assert len(matches) == 1
    return matches[0]


def _resource_rows(table: str) -> list[str]:
    rows: list[str] = []
    for group in re.findall(r"<tbody>(.*?)</tbody>", table, flags=re.DOTALL):
        rows.extend(re.findall(r"<tr>(.*?)</tr>", group, flags=re.DOTALL))
    return rows


def _row_for_url(text: str, url: str) -> str:
    rows = [row for row in re.findall(r"<tr>(.*?)</tr>", text, flags=re.DOTALL) if url in row]
    assert len(rows) == 1, (url, len(rows))
    return rows[0]


def _localized_token(value: str | dict[str, str], locale: str) -> str:
    return value[locale] if isinstance(value, dict) else value


@pytest.mark.parametrize("role", PAGES)
@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_visible_path_is_progressive_and_keeps_core_terms(role: str, locale: str) -> None:
    text = PAGES[role][locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    landmarks = VISIBLE_LANDMARKS[role]
    positions = [visible.index(icon) for icon in landmarks]
    assert positions == sorted(positions)
    for term in CORE_TERMS[role]:
        assert f"**{term}" in visible
        assert visible.index(f"**{term}") < visible.index("## 🛠")
    for url in VISIBLE_STARTING_URLS[role]:
        assert url in visible
    assert visible.count("⭐⭐⭐⭐⭐") == VISIBLE_FIVE_STAR_COUNTS[role]

    openings = re.findall(r"^<details\b[^>]*>", text, flags=re.MULTILINE)
    assert len(openings) == DETAIL_COUNTS[role]
    assert openings == ['<details markdown="1">'] * len(openings)


@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_research_copy_block_teaches_source_verification(locale: str) -> None:
    visible = _without_details(PAGES["researcher"][locale].read_text(encoding="utf-8"))
    assert "https://arxiv.org/abs/1706.03762" in visible
    assert len(re.findall(r"^[123]\. ", visible, flags=re.MULTILINE)) >= 3
    for token in ("citation", "original", "unsupported"):
        assert token.casefold() in visible.casefold()


@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_research_required_reading_and_complete_resource_table_are_visible(locale: str) -> None:
    text = PAGES["researcher"][locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    for url in RESEARCHER_REQUIRED_READING_URLS:
        assert url in visible
    for url, _rating in RESOURCE_PAIRS["researcher"]:
        assert url in visible
    assert "open_deep_research" in visible
    assert re.search(r"open_deep_research.{0,300}(archived|封存|历史|歷史)", visible, re.DOTALL | re.IGNORECASE)


@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_developer_copy_block_is_small_reviewable_and_human_gated(locale: str) -> None:
    visible = _without_details(PAGES["developer"][locale].read_text(encoding="utf-8"))
    start, end = DEVELOPER_EXERCISE_BOUNDS[locale]
    exercise = visible[visible.index(start):visible.index(end)]
    for token in (
        "read-only plan",
        "README.md",
        "git diff -- README.md",
        "test",
        "rollback",
        "push",
        "merge",
        "deploy",
    ):
        assert token.casefold() in exercise.casefold()
    assert re.search(r"human|人工", exercise, flags=re.IGNORECASE)
    for sentence in DEVELOPER_EXERCISE_SAFETY[locale]:
        assert sentence.casefold() in exercise.casefold(), (locale, sentence)
    for sentence in DEVELOPER_NON_SYNONYM_TEXT[locale]:
        assert sentence.casefold() in visible.casefold(), (locale, sentence)
    assert PI_NO_BUILT_IN_SANDBOX[locale].casefold() in visible.casefold()
    for url in DEVELOPER_REQUIRED_READING_URLS:
        assert url in visible


@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_teacher_copy_block_uses_fictional_data_and_teacher_review(locale: str) -> None:
    text = PAGES["teacher"][locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    required = {
        "zh-TW": ("虛構", "不要放學生資料", "Learning Objective", "Exit Ticket", "Human Review"),
        "en": ("fictional", "no student data", "Learning Objective", "Exit Ticket", "Human Review"),
        "zh-Hans": ("虚构", "不要放学生数据", "Learning Objective", "Exit Ticket", "Human Review"),
    }[locale]
    for token in required:
        assert token.casefold() in visible.casefold(), (locale, token)
    assert "teacher-ai-review-loop" in visible
    assert "teacher-ai-classroom-use-cases" not in text


@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_teacher_page_rejects_autonomous_grading_and_diagnosis_claims(locale: str) -> None:
    text = PAGES["teacher"][locale].read_text(encoding="utf-8")
    forbidden = (
        "即時批改",
        "即时批改",
        "instant grading",
        "推測近側發展區",
        "推测最近发展区",
        "infer the zone of proximal development",
        "AI 最終評分",
        "AI 最终评分",
        "AI makes the final grade",
        "AI diagnoses the student",
        "AI 診斷學生",
        "AI 诊断学生",
    )
    assert not any(token.casefold() in text.casefold() for token in forbidden)


@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_knowledge_worker_first_exercise_is_copyable_grounded_and_human_gated(locale: str) -> None:
    visible = _without_details(PAGES["knowledge-worker"][locale].read_text(encoding="utf-8"))
    exercise = visible[visible.index("## 🛠"):visible.index("## 📚")]
    for token in (
        "fictional",
        "Decision",
        "Action Item",
        "Owner",
        "Due date",
        "Source sentence",
        "Needs confirmation",
        "Private Data",
        "Human Review",
    ):
        assert token.casefold() in exercise.casefold(), (locale, token)
    grounded_rules = {
        "zh-TW": ("不要補猜沒有寫出的名字或日期", "填「未知」", "Needs confirmation 填「是」"),
        "en": ("do not invent names or dates", "write “unknown”", "mark Needs confirmation “yes”"),
        "zh-Hans": ("不要补猜没有写出的名字或日期", "填“未知”", "Needs confirmation 填“是”"),
    }[locale]
    for rule in grounded_rules:
        assert rule.casefold() in exercise.casefold(), (locale, rule)
    assert re.search(r"do not (send|post|write)|不要.{0,10}(寄出|發送|发送|寫回|写回)", exercise, re.IGNORECASE)


@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_knowledge_worker_distinguishes_apps_mcp_and_automation(locale: str) -> None:
    text = PAGES["knowledge-worker"][locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    for url in KNOWLEDGE_WORKER_REQUIRED_READING_URLS:
        assert url in visible
    for term in ("App／Connector", "MCP Server", "Workflow Automation", "Approval Gate"):
        assert f"**{term}" in visible
    assert re.search(r"App.{0,220}MCP Server.{0,220}Workflow Automation", visible, re.DOTALL | re.IGNORECASE)
    assert re.search(r"connector.{0,120}(app|renam)|連接器.{0,120}(App|改稱)|连接器.{0,120}(App|改称)", visible, re.DOTALL | re.IGNORECASE)
    non_interchangeable = {
        "zh-TW": "名稱不能互換",
        "en": "names are not interchangeable",
        "zh-Hans": "名称不能互换",
    }[locale]
    assert non_interchangeable.casefold() in visible.casefold(), (locale, non_interchangeable)
    assert "https://modelcontextprotocol.io/registry/about" in visible


def test_knowledge_worker_page_drops_stale_counts_unsafe_defaults_and_archived_flowise() -> None:
    forbidden = (
        "81+",
        "36k+",
        "81k+",
        "147k+",
        "64k+",
        "on-device by default",
        "預設 on-device",
        "默认 on-device",
        "NotebookLM 的私有 self-hosted 替代方案",
        "A self-hosted alternative to NotebookLM",
        "Claude Desktop + Gmail MCP",
        "https://github.com/FlowiseAI/Flowise",
        "https://github.com/punkpeye/awesome-mcp-servers",
        "https://github.com/wong2/awesome-mcp-servers",
        "30-45",
        "30–45",
        "Half a day",
        "1 week of setup",
        "Several weeks",
        "半天裝好",
        "1 週 setup",
        "數週",
        "半天装好",
        "1 周 setup",
        "数周",
    )
    for page in PAGES["knowledge-worker"].values():
        text = page.read_text(encoding="utf-8")
        assert not any(token.casefold() in text.casefold() for token in forbidden)
        assert not re.search(r"★\s*[\d,.]+[kKmM]?\+?", text)


@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_everyday_user_first_exercise_is_copyable_grounded_and_does_not_act(locale: str) -> None:
    visible = _without_details(PAGES["everyday-user"][locale].read_text(encoding="utf-8"))
    exercise = visible[visible.index("## 🛠"):visible.index("## 🚪")]
    localized = {
        "zh-TW": ("虛構", "只能使用來源訊息裡的事實", "不要猜", "不要替我傳送"),
        "en": ("fictional", "Use only facts in the source message", "Do not guess", "Do not send"),
        "zh-Hans": ("虚构", "只能使用来源消息里的事实", "不要猜", "不要替我发送"),
    }[locale]
    for token in (*localized, "Draft", "Facts copied", "Needs confirmation"):
        assert token.casefold() in exercise.casefold(), (locale, token)
    assert "9 月 12 日" in exercise or "September 12" in exercise or "9 月 12 日" in exercise


@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_everyday_user_uses_four_job_based_doors_not_an_upgrade_ladder(locale: str) -> None:
    text = PAGES["everyday-user"][locale].read_text(encoding="utf-8")
    visible = _without_details(text)
    for term in ("Chat surface", "App／Connector", "CLI Agent", "Local LLM／Runtime"):
        assert term in visible
    not_levels = {
        "zh-TW": "這四扇門不是等級",
        "en": "These four doors are not levels",
        "zh-Hans": "这四扇门不是等级",
    }[locale]
    assert not_levels in visible
    assert "Tier 0" not in visible and "Tier 1" not in visible
    assert "Tier 2" not in visible and "Tier 3" not in visible
    for url in EVERYDAY_USER_REQUIRED_READING_URLS:
        assert url in visible


@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_everyday_user_teaches_permission_and_local_cloud_boundaries(locale: str) -> None:
    text = PAGES["everyday-user"][locale].read_text(encoding="utf-8")
    required = {
        "zh-TW": ("方案、地區、workspace", "寫入動作", "人工確認", "cloud model", "local-only", "雲端功能"),
        "en": ("plan, region, and workspace", "write action", "human confirmation", "cloud models", "local-only", "cloud features"),
        "zh-Hans": ("方案、地区、workspace", "写入动作", "人工确认", "cloud model", "local-only", "云功能"),
    }[locale]
    for token in required:
        assert token.casefold() in text.casefold(), (locale, token)
    assert re.search(r"Ollama.{0,700}cloud", text, re.DOTALL | re.IGNORECASE)
    assert re.search(r"LM Studio.{0,500}(cloud|雲端|云)", text, re.DOTALL | re.IGNORECASE)


def test_everyday_user_drops_stale_rankings_counts_times_and_high_risk_starters() -> None:
    forbidden = (
        "runoob.com",
        "platform.openai.com/docs/guides/prompt-engineering",
        "docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview",
        "81+",
        "90%",
        "30 分鐘",
        "30 minutes",
        "半小時",
        "half an hour",
        "1-2 days",
        "1–2 days",
        "1-2 天",
        "1–2 天",
        "最容易上手",
        "easiest CLI",
        "最大生態",
        "largest ecosystem",
        "每個答案都附引用",
        "every answer includes citations",
        "較收斂、不太瞎掰",
        "less prone to hallucination",
        "本地醫療 / 法律 / 財務",
        "local medical / legal / financial",
        "本地医疗 / 法律 / 财务",
    )
    for page in PAGES["everyday-user"].values():
        text = page.read_text(encoding="utf-8")
        assert not any(token.casefold() in text.casefold() for token in forbidden)
        assert not re.search(r"★\s*[\d,.]+[kKmM]?\+?", text)


@pytest.mark.parametrize("role", PAGES)
def test_resource_tables_have_structured_trilingual_parity(role: str) -> None:
    expected_pairs = RESOURCE_PAIRS[role]
    expected_groups = ROWGROUPS[role]
    observed_tables: list[tuple[tuple[str, str], ...]] = []

    for page in PAGES[role].values():
        text = page.read_text(encoding="utf-8")
        table = _resource_table(text, expected_pairs[0][0])
        groups = re.findall(r"<tbody>(.*?)</tbody>", table, flags=re.DOTALL)
        assert len(groups) == len(expected_groups)
        for group, size in zip(groups, expected_groups):
            assert len(re.findall(r"<tr>", group)) == size
            assert f'scope="rowgroup" rowspan="{size}"' in group

        pairs = []
        for row in _resource_rows(table):
            url = re.search(r'<a href="(https?://[^"]+)">', row)
            rating = re.search(r"⭐{3,5}", row)
            assert url and rating
            pairs.append((url.group(1), rating.group()))
        assert tuple(pairs) == expected_pairs
        observed_tables.append(tuple(pairs))

    assert len(set(observed_tables)) == 1


@pytest.mark.parametrize("role", PAGES)
@pytest.mark.parametrize("locale", ("zh-TW", "en", "zh-Hans"))
def test_each_resource_row_keeps_status_license_and_limitation(role: str, locale: str) -> None:
    text = PAGES[role][locale].read_text(encoding="utf-8")
    for url, _rating in RESOURCE_PAIRS[role]:
        row = _row_for_url(text, url)
        expected_status = STATUS_TOKENS[RESOURCE_STATUS[url]][locale]
        expected_license = _localized_token(RESOURCE_LICENSE_OR_SERVICE[url], locale)
        expected_limit = RESOURCE_LIMIT_TOKENS[url][locale]
        for token in (expected_status, expected_license, expected_limit):
            assert token.casefold() in row.casefold(), (url, locale, token)

        if role == "developer":
            identities, surfaces = DEVELOPER_ROW_FACTS[url]
            for token in identities + surfaces:
                assert token.casefold() in row.casefold(), (url, locale, token)


def test_row_lookup_does_not_borrow_facts_from_an_earlier_row() -> None:
    text = """
<table><tbody>
<tr><td>coding agent</td><td>CLI／cloud／SDK</td><td>permission gate</td></tr>
<tr><td><a href="https://example.com/target">Target</a></td><td>IDE only</td></tr>
</tbody></table>
"""
    row = _row_for_url(text, "https://example.com/target")
    for leaked_token in ("coding agent", "CLI", "cloud", "SDK", "permission gate"):
        assert leaked_token.casefold() not in row.casefold()


@pytest.mark.parametrize("role", PAGES)
def test_freshness_urls_and_legacy_landings_are_mirrored(role: str) -> None:
    expected_urls: list[str] | None = None
    for locale, page in PAGES[role].items():
        text = page.read_text(encoding="utf-8")
        assert text.count(FRESHNESS[role]) == 1
        landing_markers = {
            "researcher": (
                "## 📌", "## ⭐", "<summary>🧪", "## 🛠", "## ⭐",
                "## ⭐", "<summary>🧪", "<summary>🧪", "## 📖",
                "<summary>🧪", "## 📚",
            ),
            "developer": (
                "## 📌", "## ⭐", "## 🧩", "## 🛠", "## 📚",
                "<summary>🧪", "<summary>🧪", "<summary>🧯", "## 📚",
                "## ✅", "## ⭐",
            ),
            "teacher": (
                "## 📌", "## 🛡", "<summary>🧪", "<summary>🧪", "<summary>🧪",
                "## 📚", "## ⭐", "## ⭐", "## ⭐", "## ⭐", "## ⭐",
                "## 📚", "<summary>🧪", "<summary>🧪", "## 🛡", "<summary>⏱",
                "## ✅", "<summary>🤝",
            ),
            "knowledge-worker": (
                "## 📌", "## ⭐", "<strong>工作流", "<strong>知識工作者",
                "<strong>知識管理", "<strong>MCP", "<summary>🧪", "## 📚", "## 📖",
            ) if locale == "zh-TW" else (
                "## 📌", "## ⭐", "<strong>Workflow", "<strong>Knowledge-worker",
                "<strong>Knowledge", "<strong>MCP", "<summary>🧪", "## 📚", "## 📖",
            ) if locale == "en" else (
                "## 📌", "## ⭐", "<strong>工作流", "<strong>知识工作者",
                "<strong>知识管理", "<strong>MCP", "<summary>🧪", "## 📚", "## 📖",
            ),
            "everyday-user": (
                "## 📌", "## 🚪", "## ⭐", "<strong>CLI Agent",
                "## 📖", "<summary>🧰", "## 🚪", "## ✅",
            ),
        }[role]
        anchor_positions = []
        for anchor, marker in zip(LEGACY_ANCHORS[role][locale], landing_markers, strict=True):
            anchor_text = f'<a id="{anchor}"></a>'
            assert text.count(anchor_text) == 1
            anchor_at = text.index(anchor_text)
            marker_at = text.index(marker, anchor_at)
            assert 0 < marker_at - anchor_at < 240, (anchor, marker, marker_at - anchor_at)
            anchor_positions.append(anchor_at)
        assert min(anchor_positions) > text.index("<!-- freshness:")
        assert len(set(anchor_positions)) >= 8

        expected_return = {
            "zh-TW": "[← 回主路線](../README.md)",
            "en": "[← Back to the main route](../README.en.md)",
            "zh-Hans": "[← 回到主路线](../README.zh-Hans.md)",
        }[locale]
        visible = _without_details(text)
        assert expected_return in visible
        assert visible.index(expected_return) < visible.index("## 📌")
        urls = re.findall(r"https?://[^)\s<>\"]+", text)
        if expected_urls is None:
            expected_urls = urls
        else:
            assert urls == expected_urls


def test_current_research_name_privacy_status_and_curation_rules() -> None:
    for page in PAGES["researcher"].values():
        text = page.read_text(encoding="utf-8")
        assert "Gemini Notebook" in text and "NotebookLM" in text
        assert "https://support.google.com/gemininotebook/answer/17004255" in text
        assert re.search(
            r"open_deep_research.{0,300}(archived|封存|历史|歷史)",
            text,
            re.DOTALL | re.IGNORECASE,
        )
        assert "WenyuChiou/" not in text
        assert "1M context" not in text and "1M token" not in text
        assert not re.search(r"★\s*[\d,.]+[kKmM]?\+?", text)


def test_teacher_tools_require_school_approval_and_use_current_product_names() -> None:
    approval_labels = {
        "zh-TW": "需由學校核准的教師雲端工具",
        "en": "Teacher cloud tools requiring school approval",
        "zh-Hans": "需由学校核准的教师云工具",
    }
    misleading_labels = {
        "zh-TW": "學校核准工具",
        "en": "School-approved tools",
        "zh-Hans": "学校核准工具",
    }
    current_url = "https://support.google.com/gemininotebook/answer/16337734?hl=en"
    for locale, page in PAGES["teacher"].items():
        text = page.read_text(encoding="utf-8")
        assert approval_labels[locale] in text
        assert misleading_labels[locale] not in text
        assert "Gemini Notebook" in text and "NotebookLM" in text
        assert "Gemini Notebooks" not in text
        assert current_url in text
        assert "support.google.com/notebooklm/" not in text


def test_public_access_is_not_treated_as_upload_permission() -> None:
    required = {
        "zh-TW": ("授權或著作權", "工具條款", "公開可讀，不等於"),
        "en": ("license or copyright", "tool's terms", "not permission to upload"),
        "zh-Hans": ("许可或版权", "工具条款", "公开可读，不代表"),
    }
    forbidden = {
        "zh-TW": "公開 paper 可以直接使用",
        "en": "A public paper is fine to use",
        "zh-Hans": "公开 paper 可以直接使用",
    }
    import_action = {
        "zh-TW": "把 paper 加進",
        "en": "Add the paper",
        "zh-Hans": "把 paper 加到",
    }
    for locale, page in PAGES["researcher"].items():
        text = page.read_text(encoding="utf-8")
        visible = _without_details(text)
        assert all(token in visible for token in required[locale])
        assert visible.index(required[locale][0]) < visible.index(import_action[locale])
        assert forbidden[locale] not in text


def test_developer_identity_and_surface_are_separate_axes() -> None:
    for page in PAGES["developer"].values():
        text = page.read_text(encoding="utf-8")
        assert "OpenRouter" in text and "Ollama" in text
        assert re.search(r"OpenRouter.{0,250}(Router|router)", text, re.DOTALL)
        assert re.search(
            r"Ollama.{0,250}(runtime|執行環境|运行环境)",
            text,
            re.DOTALL | re.IGNORECASE,
        )
        assert "核心身分" in text or "Core identity" in text or "核心身份" in text
        assert "surface" in text.casefold()
        for url, surfaces in (
            ("https://cursor.com/docs", ("IDE", "CLI", "cloud", "SDK")),
            ("https://github.com/cline/cline", ("IDE", "CLI", "SDK")),
            ("https://github.com/continuedev/continue", ("CLI", "VS Code", "JetBrains")),
        ):
            row = _row_for_url(text, url)
            assert "coding agent" in row.casefold()
            for surface in surfaces:
                assert surface.casefold() in row.casefold()
        assert re.search(
            r"Roo Code.{0,300}(archived|封存|历史|歷史)",
            text,
            re.DOTALL | re.IGNORECASE,
        )
        assert re.search(
            r"continuedev/continue.{0,500}(read-only|不再積極維護|不再积极维护)",
            text,
            re.DOTALL | re.IGNORECASE,
        )
        assert not re.search(r"★\s*[\d,.]+[kKmM]?\+?", text)


@pytest.mark.parametrize("page", tuple(path for role in PAGES.values() for path in role.values()))
def test_role_pages_drop_known_stale_or_unsafe_claims(page: Path) -> None:
    text = page.read_text(encoding="utf-8")
    forbidden = (
        "採用度最高",
        "highest adoption",
        "采用度最高",
        "< 50 LOC",
        "read:user",
        "classic PAT",
        "首選",
        "首选",
        '""',
        "“”",
    )
    assert not any(token in text for token in forbidden)
