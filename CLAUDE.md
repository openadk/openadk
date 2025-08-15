# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Configuration Note**: Parent directory access is pre-configured in `.claude/settings.local.json` with explicit permissions for `Read(../**)` and `List(..)`. This eliminates all approval prompts during repository discovery.

## 🚀 Quick Start

**Just type: `start`** - Claude will discover all repositories and begin working.
**Or type: `start [repo1] [repo2]`** - Claude will work only with the specified repositories.

**Important for Claude:** When you see "start", do not use any bash commands during initialization. Use only the Read and LS tools to understand the project context. The parent directory (..) is a working directory, so LS tool can be used there without approval. The specific sequence is detailed below.

(Don't use `/init` - that's only for CLAUDE.md improvements)

## 🤖 MANDATORY: Agent Invocation Protocol

**STOP: Before proceeding with ANY user request, you MUST apply these rules:**

### Automatic Agent Invocation Rules (NO EXCEPTIONS)

**Rule 1: Complex Task Detection**
```
IF user request involves 3+ steps OR mentions multiple components
THEN immediately invoke project-manager agent FIRST
EXAMPLES: "implement feature X", "set up system Y", "improve performance", "add authentication"
```

**Rule 2: Planning and Strategy Requests** 
```
IF user asks "what should we work on" OR "what's next" OR similar planning questions
THEN immediately invoke project-manager agent
NO DIRECT ANSWERS - agent invocation is MANDATORY
```

**Rule 3: Requirements and Specifications**
```
IF user request is vague OR missing details OR asks for recommendations
THEN invoke requirements-analyst agent BEFORE any other work
EXAMPLES: "add user management", "improve security", "optimize the app"
```

**Rule 4: Architecture and Design**
```
IF user mentions: architecture, design, scalability, integration, system, structure
THEN invoke system-architect agent
```

**Rule 5: Pre-Commit MANDATORY Review**
```
BEFORE any git commit OR file modification completion:
- invoke security-expert agent (security review)
- invoke code-reviewer agent (code quality review)
THIS IS NON-NEGOTIABLE
```

### Instant Agent Selection by Keywords

**PROJECT PLANNING KEYWORDS** → project-manager agent:
- plan, planning, roadmap, sprint, breakdown, organize, prioritize, timeline, tasks, workflow, "what should we", "what's next", manage, coordinate

**REQUIREMENTS KEYWORDS** → requirements-analyst agent:  
- requirements, specs, clarify, define, criteria, constraints, "what exactly", unclear, vague, recommendation, "how should we"

**ARCHITECTURE KEYWORDS** → system-architect agent:
- architecture, design, structure, scalable, integration, system, technology choice, patterns, framework, performance optimization

**SECURITY KEYWORDS** → security-expert agent:
- security, vulnerability, auth, authentication, authorization, encryption, permission, access, secure, compliance

**TESTING KEYWORDS** → test-engineer agent:
- test, testing, coverage, quality, validate, verification, QA, quality assurance

**CODE REVIEW KEYWORDS** → code-reviewer agent:
- review, refactor, quality, best practices, clean code, maintainability, standards

**INFRASTRUCTURE KEYWORDS** → devops-engineer agent:
- deploy, deployment, infrastructure, CI/CD, pipeline, build, docker, kubernetes

### Agent Invocation Command Format

When you detect a trigger, immediately use this format:
```
I need to invoke the [agent-name] agent for this task.

IMPORTANT: This agent must follow AGENT_GUIDELINES.md - no time estimates, only priorities.

Let me start by using the [agent-name] agent to [specific purpose].
```

Then immediately invoke the agent using the proper agent tool.

**IMPORTANT: Do not attempt to handle complex requests directly. Always use the appropriate agent first.**

**CRITICAL: All agents MUST use the structured planning API:**
- Use `python validation/planning_api.py` for creating plans (enforces compliance)
- Use `python validation/enforce_planning.py` to validate any text output
- Use `python validation/check_time_estimates.py` to verify compliance
- FORBIDDEN: Time-based estimates (automatically rejected by validation)
- REQUIRED: Priority-based planning using ONLY: critical, high, medium, low
- REQUIRED: Complexity ratings using ONLY: simple, moderate, complex
- All outputs are validated against `validation/planning_rules.yaml`

### VALIDATION CHECKLIST - Apply to Every User Request

Before responding to ANY user request, complete this checklist:

- [ ] **Step 1**: Does this request contain planning keywords? → If YES, invoke project-manager agent
- [ ] **Step 2**: Does this request contain requirements keywords? → If YES, invoke requirements-analyst agent  
- [ ] **Step 3**: Does this request contain architecture keywords? → If YES, invoke system-architect agent
- [ ] **Step 4**: Does this request involve 3+ steps or multiple components? → If YES, invoke project-manager agent
- [ ] **Step 5**: Is the request vague or missing details? → If YES, invoke requirements-analyst agent
- [ ] **Step 6**: Only after completing steps 1-5, proceed with implementation
- [ ] **Step 7**: Before any commits, ALWAYS invoke security-expert AND code-reviewer agents

**If ANY checkbox is checked, you MUST invoke the corresponding agent BEFORE doing anything else.**

### Examples of MANDATORY Agent Invocation

**User says: "What should we work on next?"**
- ✅ CORRECT: "I need to invoke the project-manager agent for this planning question. Let me start by using the project-manager agent to assess current project status and recommend next steps."
- ❌ WRONG: "Based on your repositories, I suggest..."

**User says: "Add user authentication to the app"**  
- ✅ CORRECT: "I need to invoke the requirements-analyst agent for this complex feature. Let me start by using the requirements-analyst agent to clarify authentication requirements and scope."
- ❌ WRONG: "I'll help you add authentication. First, let me check..."

**User says: "How should we architect the payment system?"**
- ✅ CORRECT: "I need to invoke the system-architect agent for this design question. Let me start by using the system-architect agent to evaluate payment system architecture options."
- ❌ WRONG: "For payment systems, I recommend..."

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

### Step 2: Validate and read current project context (no bash commands)
Use the Read tool and LS tool:
1. Read tool: README.md in current directory
2. Read tool: CONTRIBUTING.md for development guidelines
3. Read tool: _project/PROJECT_CONTEXT.yaml (only if it exists from a previous run)
4. If PROJECT_CONTEXT.yaml exists, validate it: `python validation/validate_context.py`
5. LS tool: Check .claude directory
6. LS tool: Check _project directory
7. Run agent validation: `./validation/validate.sh` (checks all agent templates)
Note: PROJECT_CONTEXT.yaml is generated, not tracked in git

### Step 3: Discover repositories (using LS tool)
Since the parent directory is a working directory:
1. LS tool: List parent directory (..) to see all directories
2. For each directory found, use LS to check if it has a .git folder
3. Build a list of actual git repositories

### Step 4: Read discovered repositories (using Read tool)
For each repository discovered in Step 3:
1. Read tool: Read ../repo-name/README.md to understand purpose
2. Read tool: Read configuration files like ../repo-name/package.json
3. Build understanding of each repository's technology and purpose

### Step 5: Generate/Update PROJECT_CONTEXT.yaml (Incremental Updates)
**IMPORTANT: Use incremental updates, not full rewrites**
1. First run validation: `python validation/validate_context.py`
2. Use `python validation/update_context.py` for incremental changes:
   - Only update fields that have changed
   - Preserve existing goals and configurations
   - Add new repositories without overwriting existing ones
   - Update current_focus for active work
3. Context should include:
   - Project metadata with **goals** section (primary_objective, success_metrics, constraints)
   - Repository information and tech stacks
   - Available agents from .claude/ directory
   - Workflow patterns and development guidelines
   - Current focus for each repository
Note: PROJECT_CONTEXT.yaml is .gitignored and unique to each user's setup

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
- The parent directory (..) is automatically a working directory via settings.local.json
- During initialization (steps 1-6): Use only Read and LS tools, no bash commands
- LS tool can be used on parent directory and its subdirectories without approval
- After initialization (step 7+): Bash commands are allowed for actual work
- Never use bash to read file contents - always use the Read tool
- The initialization phase is about understanding, not executing

### Step 8: Ask the user what they'd like to work on + MANDATORY Agent Protocol
   - Offer to help with any active repository
   - Suggest addressing any uncommitted changes if found
   - **CRITICAL**: Inform the user that specialized agents are ready:
     - "I have specialized agents ready for different tasks: project planning, requirements analysis, architecture design, security reviews, testing, and code reviews."
     - "What would you like to work on? I'll automatically invoke the appropriate agents based on your request using the Mandatory Agent Invocation Protocol."
   - Be ready to assist with development, testing, or deployment tasks
   - **MANDATORY**: Apply the Agent Invocation Protocol rules to the user's response - no exceptions
   - **REMEMBER**: Questions like "what should we work on" automatically trigger project-manager agent invocation

## Example: Correct Initialization Sequence

Here's what Claude should do when the user types "start":

```
User: start

Claude's process:

1. Read current openadk project files:
   - Read tool: README.md
   - Read tool: CONTRIBUTING.md  
   - Read tool: _project/PROJECT_CONTEXT.yaml (if exists from previous run - likely won't exist)
   - LS tool: .claude directory
   - LS tool: _project directory

2. Discover repositories:
   - LS tool: List parent directory (..)
   - LS tool: Check ../repo1/.git, ../repo2/.git etc.
   - Build list of actual git repositories

3. Read discovered repositories:
   - Read tool: ../repo-name/README.md
   - Read tool: ../repo-name/package.json or similar
   - Understand each repository's purpose and tech stack

4. Generate or update PROJECT_CONTEXT.yaml

5. Report status to user with all discovered repositories

6. Only now can bash commands be used for actual work
```

Key principles: 
- No bash commands during initialization
- Parent directory is accessible via LS tool (configured in settings.local.json)
- Read tool can read files from any discovered repository
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

## 🔍 Repository Analysis System

### Overview
OpenADK includes a comprehensive repository analysis system that evaluates code health across 8 critical dimensions. This system leverages all specialized agents to provide deep insights and actionable recommendations.

### The `analyze` Command
When the user types `analyze` or `health`:

1. **Run Basic Analysis**: Execute `./analyze-repo.sh` to gather repository metrics
2. **Invoke Specialized Agents**: Automatically use agents for deep analysis:
   - **code-reviewer** + **system-architect** → Maintainability assessment
   - **system-architect** + **devops-engineer** → Scalability evaluation
   - **test-engineer** + **devops-engineer** → Reliability analysis
   - **security-expert** → Security vulnerability scan
   - **code-reviewer** → Performance and Documentation review
   - **test-engineer** → Testability assessment
   - **devops-engineer** → Operational readiness check
3. **Generate Comprehensive Report**: Combine all agent findings into unified report
4. **Store in _project/reports/**: Save both markdown and YAML versions

### Analysis Dimensions
Each dimension provides specific insights:
- **Maintainability**: Code quality, technical debt, refactoring needs
- **Scalability**: Architecture patterns, bottlenecks, growth capacity
- **Reliability**: Error handling, fault tolerance, recovery mechanisms
- **Security**: Vulnerabilities, authentication, data protection
- **Performance**: Optimization opportunities, resource usage
- **Testability**: Coverage, test quality, CI/CD integration
- **Documentation**: Completeness, clarity, maintenance
- **Operational Readiness**: Deployment, monitoring, incident response

### Analysis Workflow
```
User: analyze
Claude: 
1. Runs ./analyze-repo.sh for basic metrics
2. Invokes multiple agents in parallel for deep analysis
3. Aggregates findings into comprehensive report
4. Provides prioritized recommendations
5. Stores report in _project/reports/
```

### Report Structure
Reports are stored in simplified _project structure:
- `_project/reports/` - Current analysis reports
- `_project/archive/` - Historical reports for trend analysis
- No cluttered subdirectories - just clean, accessible outputs

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

## 🔄 Multi-Agent Coordination Patterns

**REMINDER: All agents must follow AGENT_GUIDELINES.md - NO time estimates, only priority-based planning**

**Standard Workflows for Complex Tasks:**

### Pattern 1: New Feature Development (7-step process)
1. **requirements-analyst** → Gather and clarify requirements
2. **system-architect** → Design approach and integration
3. **project-manager** → Break down work and plan sprints
4. **Implementation** → Code the feature
5. **test-engineer** → Create comprehensive tests
6. **security-expert** → Security review
7. **code-reviewer** → Final quality review

### Pattern 2: Complex Project Management (5-step process)
1. **project-manager** → Initial assessment and breakdown
2. **system-architect** → Technical feasibility and architecture
3. **requirements-analyst** → Detailed requirements per component
4. **devops-engineer** → Infrastructure and deployment strategy
5. **Iterative implementation with regular reviews**

### Pattern 3: Code Quality Improvement (5-step process)
1. **code-reviewer** → Identify quality issues
2. **test-engineer** → Analyze test coverage gaps
3. **security-expert** → Security vulnerability assessment
4. **system-architect** → Architectural improvements
5. **project-manager** → Prioritize and plan improvements

### Agent Coordination Rules

**CRITICAL COORDINATION RULES:**

1. **Never implement without planning** → If user asks for implementation, FIRST use project-manager to break it down
2. **Never commit without review** → ALWAYS run security-expert and code-reviewer before any commit
3. **Never design without requirements** → If architecture is needed, FIRST clarify requirements with requirements-analyst
4. **Always test what you build** → After implementation, ALWAYS use test-engineer for comprehensive testing

**IMPORTANT**: All agents MUST follow the project-native development practices identified above. When invoking any agent, ensure they:
1. Read AGENT_GUIDELINES.md for mandatory planning and estimation rules
2. Read _project/PROJECT_CONTEXT.yaml for project conventions and goals
3. Follow the discovered code style, testing, and security practices
4. Adapt their output to match the project's culture and standards
5. Use project-specific tools and frameworks
6. Respect team conventions and domain language
7. NEVER provide time-based estimates - use priority levels only
8. ALWAYS align work with project goals defined in PROJECT_CONTEXT.yaml

## Development Guidelines

### Multi-Agent Workflow Pattern

**DEPRECATED**: This section has been replaced by the "Mandatory Agent Invocation Protocol" at the top of this document and the "Multi-Agent Coordination Patterns" above.

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
- `start [repo1] [repo2]`: Initialize with specific repositories only

### Repository Analysis
- `analyze`: Run comprehensive repository health analysis with multi-dimensional evaluation
- `health`: Quick health check of current repository (alias for analyze)

### Agent Invocation
- **MANDATORY**: Follow the "Mandatory Agent Invocation Protocol" at the top of this document for EVERY task
- Apply the automatic invocation rules without exception
- Use the keyword-based triggers to instantly select appropriate agents
- Always invoke multiple agents for complex tasks using the coordination patterns

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