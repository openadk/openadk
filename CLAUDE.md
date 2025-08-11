# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚀 QUICK START

**Just type: `start`** - Claude will discover all repositories and begin working.
**Or type: `start [repo1] [repo2]`** - Claude will work only with the specified repositories.

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


Claude will automatically discover all git repositories in the parent directory when you type `start`.

## START_INSTRUCTIONS

When the user types "start", follow these steps:

1. **Parse the command:**
   - If just "start": Discover ALL repositories in parent directory
   - If "start repo1 repo2 ...": Use ONLY the specified repositories

2. **Auto-discover project context:**
   ```bash
   # For each repository, read key files to understand:
   # - Project purpose (README.md)
   # - Tech stack (package.json, go.mod, etc.)
   # - Special configurations (.claude/ directory)
   # Build internal model of what each repository does
   ```

3. **Discover repositories based on command:**
   ```bash
   # First, list all directories in parent
   ls -la ../
   
   # Then check each directory for .git folder using git -C
   # If no repos specified, check all directories
   # If repos specified, only check those directories
   ```

4. **Understand each repository automatically:**
   For each discovered repository:
   - Read README.md to understand its purpose
   - Check for package.json, go.mod, pyproject.toml to identify tech stack
   - Look for .claude/ directory (indicates enhancement toolkit)
   - Scan for API definitions, test directories, CI/CD configs
   - Build mental model: "This is a React frontend" or "This is a Go microservice"
   
5. **Generate/Update _project/PROJECT_CONTEXT.yaml:**
   Create or update a structured context store in `_project/` with:
   - Project metadata and purpose
   - Repository information and tech stacks
   - Available agents (if .claude/ exists)
   - Workflow patterns
   - Development guidelines
   - **Project-specific practices discovered**:
     - Code style and linting rules
     - Testing framework and patterns
     - API conventions and patterns
     - Security and compliance requirements
     - Build and deployment processes
     - Team conventions and tools
   - Quick access facts for agents
   
   This file provides agents with instant context without re-reading everything, including all project-specific conventions.

6. **Check the status of each repository:**
   ```bash
   # For each discovered repository, check git status
   # Use git -C to run git commands in other directories
   # Example: git -C ../repo-name status --short --branch
   ```

7. **Report the overall project status:**
   - List all active repositories (discovered or specified)
   - Look for uncommitted changes, untracked files, or branches not on main/master
   - Identify any repositories that need attention
   - Summarize the current state of the project

8. **Ask the user what they'd like to work on:**
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