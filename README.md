# OpenADK (Open Agent Development Kit)

A development toolkit that enhances Claude Code with specialized AI agents and multi-repository workflows for professional software development.

## 🎯 Vision

**Our vision is to enhance AI-assisted development by providing a free, open-source toolkit that brings enterprise-grade multi-agent workflows to developers using AI coding assistants.**

We believe that:
- Developers using AI assistants should have access to sophisticated multi-agent workflows without additional costs
- Your AI configuration and workflows should be portable, customizable, and under your control
- The future of development is multi-agent collaboration, where specialized AI agents work together on different aspects of your code
- Open-source tools can dramatically amplify the capabilities of existing AI assistants

*Note: Requires a Claude Code subscription.*

## 🤖 Claude Code Integration

OpenADK provides deep integration with Claude Code, offering:
- **Multi-repository context management** - Work across multiple repos seamlessly
- **Specialized AI agents** - Development, Security, testing, architecture, DevOps, and more
- **Automated code review** - Pre-commit hooks with agent-based reviews
- **Dynamic project discovery** - Automatically understands your project structure

## ⚡ Get Started with OpenADK

1. **Clone OpenADK in your parent directory** (next to your project repositories):
   ```bash
   git clone https://github.com/yourusername/openadk.git
   ```
   
   Your structure should look like:
   ```
   parent-directory/
   ├── openadk/         # This repository
   ├── your-repo-1/     # Your application repositories
   ├── your-repo-2/
   └── .../
   ```

2. **Start Claude Code**
   ```bash
   cd openadk
   claude
   ```

3. **Initialize - Two Options**
   
   **Option A: Work with all repositories**
   Type `start` and Claude will:
   - Discover all repositories in the parent directory
   - Check their status
   - Provide intelligent assistance across all repos
   
   **Option B: Work with specific repositories only**
   Type `start [repo1] [repo2]` (e.g., `start backend frontend`) and Claude will:
   - Work only with the specified repositories
   - Ignore other repositories in the parent directory
   - Focus assistance on your selected repos

## Key Features

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