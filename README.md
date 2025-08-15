# OpenADK (Open Agent Development Kit)

A development toolkit that enhances Claude Code with specialized AI agents and multi-repository workflows for professional software development.

## ⚡ Get Started with OpenADK

### Setup Options

**Option 1: For Multiple Repositories** - Clone OpenADK in a shared parent directory:
```bash
cd your-workspace
git clone https://github.com/openadk/openadk.git
```

Your structure:
```
your-workspace/
├── openadk/         # OpenADK toolkit
├── repo-1/          # Your repositories
├── repo-2/
└── .../
```

**Option 2: For a Single Repository** - Clone OpenADK next to your specific repository:
```bash
cd my-repo/..
git clone https://github.com/openadk/openadk.git
```

Your structure:
```
parent-folder/
├── openadk/         # OpenADK toolkit
└── my-repo/         # Your single repository
```

This works with any folder structure - no GitHub organization required. OpenADK will discover and work with any git repositories in the same parent directory.

### Start Claude Code

```bash
cd openadk
claude
```

**Alternative**: If you prefer, you can also start from the parent directory:
```bash
cd parent-directory  # Go to the parent of openadk
claude openadk       # Start Claude with openadk as target
```

### Initialize Your Workspace

**Option A: Work with all discovered repositories**
Type `start` and Claude will:
- Discover all git repositories in the parent directory
- Check their status
- Provide intelligent assistance across all repositories

**Option B: Work with specific repositories only**
Type `start [repo1] [repo2]` (e.g., `start backend frontend`) and Claude will:
- Work only with the specified repositories
- Ignore other repositories in the parent directory
- Focus assistance on your selected repositories

### Analyze Repository Health

Type `analyze` or `health` to get a comprehensive evaluation of your code:
- **8 Dimensions**: Maintainability, Scalability, Reliability, Security, Performance, Testability, Documentation, Operational Readiness
- **Multi-Agent Analysis**: Leverages all specialized agents for deep insights
- **Actionable Reports**: Get prioritized recommendations with effort estimates
- **Clean Output**: Reports stored in `_project/reports/` for easy access

## 🎯 Vision

**Our vision is to enhance AI-assisted development by providing a free, open-source toolkit that brings enterprise-grade multi-agent workflows to developers using AI coding assistants.**

We believe that:
- Developers using AI assistants should have access to sophisticated multi-agent workflows without additional costs
- Your AI configuration and workflows should be portable, customizable, and under your control
- The future of development is multi-agent collaboration, where specialized AI agents work together on different aspects of your code
- Open-source tools can dramatically amplify the capabilities of existing AI assistants

### Current Focus: Claude Code
OpenADK is currently optimized for Claude Code users, providing deep integration and specialized workflows. *Requires a Claude Code subscription.*

### Future: Model-Agnostic Platform
Our long-term vision is to make OpenADK a **universal enhancement layer** that works with any AI coding assistant:
- Support for multiple AI CLIs (Codex CLI, Gemini CLI, and others)
- Unified agent definitions that adapt to different models
- Consistent multi-repository workflows across platforms
- Write once, enhance any AI assistant

This model-agnostic approach ensures your investment in workflows and configurations remains valuable regardless of which AI assistant you choose.

## Key Features

- **🔍 Repository Health Analysis** - Comprehensive 8-dimensional code evaluation
- **Multi-Repository Management** - Seamlessly work across multiple repos
- **Specialized Agents** - Pre-configured agents for different development tasks
- **Automated Code Review** - AI-powered pre-commit reviews
- **Dynamic Discovery** - Zero configuration needed
- **Project Agnostic** - Works with any tech stack

## Specialized AI Agents

OpenADK includes pre-configured agents for:

- **🏗️ system-architect** - Technology decisions and architecture design
- **👔 project-manager** - Task breakdown and project management
- **📝 requirements-analyst** - Requirements gathering and specification
- **🔒 security-expert** - Security reviews and vulnerability assessment
- **🧪 test-engineer** - Test creation and coverage analysis
- **📊 code-reviewer** - Code quality and best practices
- **⚙️ devops-engineer** - Infrastructure and deployment

## Why OpenADK?

**Amplify Your AI Assistant**
- Enhance your existing Claude Code subscription with multi-agent workflows
- No additional subscription fees beyond your AI assistant
- Own your configuration and workflows

**Open Source Benefits**
- Complete transparency - see exactly how it works
- Customize to your needs
- Contribute improvements back to the community
- No vendor lock-in

**Enterprise Features for Everyone**
- Multi-repository context management
- Specialized AI agents
- Automated code review
- Professional development workflows

## Prerequisites

- **Claude Code subscription** (Required)
- Git installed on your system
- Your project repositories in a common parent directory


## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.