# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚀 Quick Start

**Just type: `start`** - Claude will discover all repositories and begin working.
**Or type: `start [repo1] [repo2]`** - Claude will work only with the specified repositories.

**Important for Claude:** When you see "start", do not use any bash commands during initialization. Use only the Read and LS tools to understand the project context. The specific sequence is detailed in START_INSTRUCTIONS below.

(Don't use `/init` - that's only for CLAUDE.md improvements)

## Project Context Auto-Discovery

When working in any repository, automatically build understanding from:
1. **README.md** - Project purpose, features, and usage
2. **package.json/pyproject.toml/go.mod** - Technology stack and dependencies  
3. **CONTRIBUTING.md** - Development guidelines
4. **.claude/** directory - If present, this is an enhancement toolkit
5. **Documentation files** - Any *.md files that provide context

This automatic discovery means:
- No manual context files needed
- Projects document themselves through standard files
- When a toolkit works on itself, it uses its own documentation as context

## 🎯 CRITICAL: Project-Native Development

**You MUST adapt to each project's specific practices and culture. Before writing ANY code:**

### 1. Study Project Conventions
- **Code Style**: Check for .editorconfig, .prettierrc, .eslintrc, rustfmt.toml, etc.
- **Language Idioms**: Follow the project's specific patterns (functional vs OOP, async patterns, error handling)
- **Naming Conventions**: Match existing naming for files, functions, variables, and types
- **Project Structure**: Respect existing directory organization and module patterns

### 2. Testing Practices
- **Test Framework**: Identify what's used (Jest, pytest, go test, etc.)
- **Test Structure**: Match existing test file locations and naming
- **Test Style**: Follow project's approach (TDD, BDD, unit vs integration)
- **Coverage Requirements**: Check for coverage thresholds in CI/CD configs
- **ALWAYS** run existing tests before making changes
- **ALWAYS** add tests for new functionality

### 3. Security Practices
- **Authentication**: Use project's existing auth patterns
- **Secret Management**: Follow established patterns for API keys, tokens
- **Input Validation**: Match project's validation approach
- **Dependencies**: Check for security policies on third-party packages
- **NEVER** commit secrets, keys, or sensitive data

### 4. Development Workflow
- **Branch Strategy**: Check if it's git-flow, GitHub flow, or trunk-based
- **Commit Messages**: Follow project's commit convention (conventional commits, etc.)
- **PR Process**: Understand review requirements, CI checks
- **Documentation**: Update relevant docs with code changes

### 5. Build & Dependencies
- **Package Manager**: Use the project's chosen tool (npm, yarn, pip, cargo, etc.)
- **Lock Files**: Always respect and update lock files properly
- **Version Constraints**: Follow project's dependency versioning strategy
- **Build Scripts**: Understand and use existing build/deploy scripts

### 6. Communication Style
- **Code Comments**: Match the project's comment density and style
- **Documentation**: Follow existing tone (formal vs casual, detailed vs concise)
- **PR Descriptions**: Match the team's PR description format
- **Issue Responses**: Align with project's communication culture

### 7. API & Database Conventions
- **API Style**: REST vs GraphQL vs gRPC - match existing patterns
- **Endpoint Naming**: Follow URL structure and versioning conventions
- **Response Formats**: Match existing error and success response structures
- **Database Patterns**: ORMs vs raw SQL, migration strategies
- **Query Patterns**: Understand pagination, filtering, sorting approaches

### 8. Performance & Monitoring
- **Performance Budgets**: Check for existing performance requirements
- **Profiling Tools**: Use project's performance monitoring setup
- **Metrics & Telemetry**: Follow established observability patterns
- **Caching Strategy**: Understand and use existing cache layers
- **Optimization Patterns**: Match project's approach to optimization

### 9. Internationalization & Accessibility
- **i18n Framework**: Use project's localization approach if present
- **Date/Time Handling**: Follow project's timezone and format conventions
- **Accessibility Standards**: Maintain WCAG compliance if established
- **RTL Support**: Consider if project supports right-to-left languages

### 10. Domain-Specific Patterns
- **Business Logic**: Understand domain models and business rules
- **Industry Standards**: Follow regulatory requirements (HIPAA, PCI, GDPR)
- **Domain Language**: Use established ubiquitous language from the domain
- **Integration Patterns**: Follow existing third-party integration approaches

### 11. DevOps & Deployment
- **Environment Management**: Understand dev, staging, prod configurations
- **Container Patterns**: Follow Dockerfile and compose conventions
- **Infrastructure as Code**: Respect Terraform, CloudFormation patterns
- **Deployment Process**: Understand rollback and feature flag strategies
- **Monitoring & Alerts**: Follow existing observability setup

### 12. Team-Specific Practices
- **Code Review Culture**: Understand team's review depth and style
- **Pair Programming**: Check if team practices pairing or mob programming
- **Documentation Standards**: Follow team's doc requirements (ADRs, wikis)
- **Meeting Artifacts**: Update relevant meeting notes or decision logs
- **Tool Preferences**: Use team's preferred tools and extensions

### Pre-Implementation Checklist
Before writing code, ALWAYS:
- [ ] Read CONTRIBUTING.md thoroughly
- [ ] Check for style guides and linters
- [ ] Review recent PRs to understand standards
- [ ] Identify test patterns from existing tests
- [ ] Look for CI/CD configurations
- [ ] Study error handling patterns
- [ ] Understand logging conventions
- [ ] Check for feature flags or environment configs
- [ ] Review API documentation and patterns
- [ ] Understand domain models and business rules
- [ ] Check performance and security requirements
- [ ] Identify team-specific practices and tools

## ⚠️ CRITICAL: Multi-Repository Architecture

**This project may use a multi-repository architecture with related repositories in the parent directory.**

Claude will automatically discover all git repositories in the parent directory when you type `start`.

## Working on Enhancement Toolkits

If the current repository contains a `.claude/` directory with agent configurations:
1. This is an enhancement toolkit (like the one providing these instructions)
2. Use README.md and other docs to understand the toolkit's purpose
3. Ensure CLAUDE.md remains project-agnostic
4. Test changes against other project types
5. Never put project-specific information in CLAUDE.md
6. The toolkit's own documentation serves as its development guide

## Start Instructions

When the user types "start", follow these steps in order:

### Step 1: Parse the command
Understand what the user is asking for:
- If just "start": Work with all repositories in parent directory
- If "start repo1 repo2 ...": Work only with specified repositories

### Step 2: Read current project context (no bash commands)
Use the Read tool and LS tool (only within openadk directory):
1. Read tool: README.md in current directory
2. Read tool: CONTRIBUTING.md for development guidelines
3. Read tool: _project/PROJECT_CONTEXT.yaml if it exists
4. LS tool: Check .claude directory within openadk
5. LS tool: Check _project directory within openadk

### Step 3: Understand project from existing context
Since LS tool for parent directory would require user approval:
1. Check if PROJECT_CONTEXT.yaml already lists known repositories
2. If user specified repositories (e.g., "start repo1 repo2"), note those names
3. If just "start", assume working with openadk and any repos mentioned in PROJECT_CONTEXT.yaml

### Step 4: Read known repositories (using Read tool only)
For repositories identified in Step 3:
1. Read tool: Try to read ../repo-name/README.md
2. Read tool: Try to read configuration files like ../repo-name/package.json
3. If files don't exist, that's fine - the repository may not exist

### Step 5: Generate/Update PROJECT_CONTEXT.yaml
Create or update a structured context store in `_project/` with:
- Project metadata and purpose
- Repository information and tech stacks
- Available agents (if .claude/ exists)
- Workflow patterns and development guidelines
- Project-specific practices discovered
- Quick access facts for agents

### Step 6: Report project status
Provide a clear summary to the user:
- List all active repositories discovered
- Note their purpose and technology stack
- Mention available agents and tools
- Be ready to help with any development task

### Step 7: After initialization - working phase
Only now, after all context is gathered, you may use bash commands for actual development work:
- Checking git status with `git status --short --branch`
- Running git commands with `git -C ../repo-name status`
- Building, testing, or other development tasks

### Important notes
- During initialization (steps 1-6): Use only Read tool and LS tool (within openadk only)
- LS tool on directories outside openadk requires user approval - don't use during initialization
- After initialization (step 7+): Bash commands are allowed for actual work
- Never use bash to read file contents - always use the Read tool
- The initialization phase is about understanding, not executing

### Step 8: Ask the user what they'd like to work on
   - Offer to help with any active repository
   - Suggest addressing any uncommitted changes if found
   - Be ready to assist with development, testing, or deployment tasks

## Example: Correct Initialization Sequence

Here's what Claude should do when the user types "start":

```
User: start

Claude's process:

1. Read current openadk project files:
   - Read tool: README.md
   - Read tool: CONTRIBUTING.md  
   - Read tool: _project/PROJECT_CONTEXT.yaml (if exists)
   - LS tool: .claude directory (within openadk)
   - LS tool: _project directory (within openadk)

2. Identify repositories from context:
   - Check PROJECT_CONTEXT.yaml for known repositories
   - Note any repository names from user's command

3. Read identified repositories (may fail if they don't exist):
   - Read tool: ../repo-name/README.md
   - Read tool: ../repo-name/package.json
   - Note: No LS tool outside openadk (would require approval)

4. Generate or update PROJECT_CONTEXT.yaml

5. Report status to user based on what was found

6. Only now can bash commands be used for actual work
```

Key principles: 
- No bash commands during initialization
- LS tool only within openadk directory (other directories need approval)
- Read tool can try to read files anywhere (will fail gracefully if not found)
- Bash is for doing work after initialization is complete

## Repository Detection

When working with this project:
1. Claude automatically discovers sibling repositories (directories with .git folders)
2. Can be limited to specific repositories when specified after "start"
3. No hardcoded repository names or paths
4. Adapts to whatever project structure exists

## Default Working Context

**Your primary workspace is the APPLICATION repositories discovered dynamically.**

When user types "start" or begins describing work:
1. Discover and check status of repositories (all or specified)
2. Suggest tasks based on repo state OR start implementing requested features
3. Navigate to the appropriate application repository
4. Begin actual development work

## ⚠️ IMPORTANT: Configuration Repository Protection

**If a `.claude/` configuration directory exists in any repository, NEVER modify it unless explicitly requested.**

Configuration directories may contain:
- Agent definitions and configurations
- Settings and permissions
- Workflow tools

These should remain stable during normal development. Only modify configuration when:
- The user explicitly requests configuration changes
- The user asks to add/modify agents
- The user requests changes to workflow settings

For all other work, focus on the APPLICATION code and features.

## Context Store & Artifacts

### Context Store Usage
**_project/PROJECT_CONTEXT.yaml** is your quick reference for project understanding:
- Generated automatically by the `start` command
- Updated when project structure changes
- Agents should read this FIRST before diving into individual files
- Provides instant context without expensive file scanning
- Human-readable for debugging

### Project Working Directory
**All agent-generated content goes in `_project/` directory:**
- `_project/requirements/` - Requirements specifications
- `_project/reviews/` - Code and security review reports
- `_project/architecture/` - Architecture decision records
- `_project/tests/` - Test reports and coverage
- `_project/planning/` - Sprint plans and task breakdowns
- `_project/reports/` - General analysis reports

**Important**: These directories are git-ignored. They're working spaces for agents to store their outputs without cluttering the repository.

## Specialized Agent Usage

When working on tasks, leverage the appropriate specialized agents:
- **system-architect**: For technology decisions, architecture design, and system-wide changes
- **project-manager**: For breaking down complex tasks and managing project workflows
- **requirements-analyst**: For gathering and refining requirements before implementation
- **security-expert**: For security reviews and identifying vulnerabilities
- **test-engineer**: For creating comprehensive tests and analyzing coverage
- **code-reviewer**: For reviewing code quality and adherence to best practices
- **devops-engineer**: For infrastructure, CI/CD, and deployment concerns

**IMPORTANT**: All agents MUST follow the project-native development practices identified above. When invoking any agent, ensure they:
1. Read _project/PROJECT_CONTEXT.yaml for project conventions
2. Follow the discovered code style, testing, and security practices
3. Adapt their output to match the project's culture and standards
4. Use project-specific tools and frameworks
5. Respect team conventions and domain language

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
- `start`: Initialize and discover all repositories in parent directory

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