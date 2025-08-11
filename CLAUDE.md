# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚀 QUICK START

**Just type: `start`** - Claude will discover all repositories and begin working.
**Or type: `start [repo1] [repo2]`** - Claude will work only with the specified repositories.

(Don't use `/init` - that's only for CLAUDE.md improvements)

## Project Purpose

OpenADK (Open Agent Development Kit) is a toolkit that enhances Claude Code with specialized AI agents and multi-repository workflows. The primary goal is to provide enterprise-grade multi-agent workflows to developers using AI coding assistants.

## ⚠️ CRITICAL: Multi-Repository Architecture

**OpenADK uses a multi-repository architecture. The openadk repository should be placed alongside other project repositories.**

Claude will automatically discover all git repositories in the parent directory when you type `start`.

## START_INSTRUCTIONS

When the user types "start", follow these steps:

1. **Parse the command:**
   - If just "start": Discover ALL repositories in parent directory
   - If "start repo1 repo2 ...": Use ONLY the specified repositories

2. **Discover repositories based on command:**
   ```bash
   # First, list all directories in parent
   ls -la ../
   
   # Then check each directory for .git folder using git -C
   # If no repos specified, check all directories
   # If repos specified, only check those directories
   ```

3. **Check the status of each repository:**
   ```bash
   # For each discovered repository, check git status
   # Use git -C to run git commands in other directories
   # Example: git -C ../repo-name status --short --branch
   ```

4. **Report the overall project status:**
   - List all active repositories (discovered or specified)
   - Look for uncommitted changes, untracked files, or branches not on main/master
   - Identify any repositories that need attention
   - Summarize the current state of the project

5. **Ask the user what they'd like to work on:**
   - Offer to help with any active repository
   - Suggest addressing any uncommitted changes if found
   - Be ready to assist with development, testing, or deployment tasks

## Repository Detection

When working with this project:
1. Claude automatically discovers sibling repositories (directories with .git folders)
2. Can be limited to specific repositories when specified after "start"
3. No hardcoded repository names or paths
4. Adapts to whatever project structure exists

## Default Working Context

**Your primary workspace is the APPLICATION repositories (discovered dynamically), NOT openadk/.**

When user types "start" or begins describing work:
1. Discover and check status of repositories (all or specified)
2. Suggest tasks based on repo state OR start implementing requested features
3. Navigate to the appropriate application repository
4. Begin actual development work

## ⚠️ IMPORTANT: OpenADK Repository Protection

**NEVER modify the openadk repository unless the developer has EXPLICITLY asked you to do so.**

The openadk repository contains:
- Agent definitions and configurations
- Multi-repository workflow tools
- Core OpenADK functionality

This repository should remain stable and unchanged during normal development work. Only make changes to openadk when:
- The user explicitly says "modify openadk" or "update OpenADK"
- The user asks to add/modify agents
- The user requests changes to OpenADK configuration or documentation

For all other work, focus on the APPLICATION repositories discovered via the start command.

## Specialized Agent Usage

When working on tasks, leverage the appropriate specialized agents:
- **system-architect**: For technology decisions, architecture design, and system-wide changes
- **project-manager**: For breaking down complex tasks and managing project workflows
- **requirements-analyst**: For gathering and refining requirements before implementation
- **security-expert**: For security reviews and identifying vulnerabilities
- **test-engineer**: For creating comprehensive tests and analyzing coverage
- **code-reviewer**: For reviewing code quality and adherence to best practices
- **devops-engineer**: For infrastructure, CI/CD, and deployment concerns

## Development Guidelines

### Multi-Agent Workflow Pattern
1. Use requirements-analyst agent first for complex features
2. Consult system-architect for architectural decisions
3. Break down work with project-manager agent
4. Implement with appropriate domain agents
5. Always run security-expert and code-reviewer before finalizing

### Repository Discovery
- The toolkit should automatically discover repositories in the parent directory
- Maintain awareness of multiple repository contexts
- Consider cross-repository dependencies and impacts

### Pre-commit Integration
- Implement pre-commit hooks that trigger agent-based reviews
- Security and code review agents should be part of the commit workflow
- Ensure all agent feedback is addressed before committing

## Key Commands

### Initialization
- `start`: Initialize OpenADK and discover all repositories in parent directory

### Agent Invocation
- Agents should be invoked programmatically based on task context
- Each agent has specific expertise - use them accordingly

## Architecture Principles

1. **Zero Configuration**: The toolkit should work without manual configuration
2. **Project Agnostic**: Must work with any technology stack
3. **Agent Collaboration**: Multiple agents should work together seamlessly
4. **Dynamic Discovery**: Automatically understand project structure and dependencies
5. **Open Source First**: All workflows and configurations should be transparent and customizable

## Testing Strategy

- Test multi-repository workflows thoroughly
- Ensure agent interactions are predictable and reliable
- Validate that the toolkit works across different project types
- Test pre-commit hook integrations

## Important Considerations

- This is an enhancement layer for Claude Code - requires active Claude Code subscription
- Focus on making sophisticated workflows accessible without additional costs
- Maintain portability and avoid vendor lock-in
- Keep the toolkit lightweight and focused on agent orchestration