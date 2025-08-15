# Agent Guidelines and Best Practices

This document defines critical guidelines that ALL agents must follow when working on OpenADK projects.

## 🚫 Critical Rules - MANDATORY FOR ALL AGENTS

### 1. NO TIME-BASED ESTIMATES
**NEVER create estimates using actual time units. This is non-negotiable.**

❌ **FORBIDDEN:**
- "This will take 2 days"
- "Complete in week 1"
- "Month 1-2 timeline"
- "3 hours of work"
- "Q1 2025 delivery"
- Any reference to days, weeks, months, quarters, or years

✅ **REQUIRED APPROACH:**
- Use priority levels: Critical, High, Medium, Low
- Use complexity ratings: Simple, Moderate, Complex
- Use relative sizing: Small, Medium, Large, XL
- Use ordered lists: Priority 1, Priority 2, Priority 3
- Focus on dependencies and sequencing, not duration

### 2. GOAL ALIGNMENT
**Every recommendation and task must align with project goals defined in PROJECT_CONTEXT.yaml**

Before creating any plan or recommendation:
1. Check the `project.goals` section in PROJECT_CONTEXT.yaml
2. Ensure alignment with `primary_objective`
3. Verify contribution to `success_metrics`
4. Respect defined `constraints`
5. Avoid anything listed in `non_goals`

### 3. INCREMENTAL CONTEXT UPDATES
**Never rewrite entire PROJECT_CONTEXT.yaml - only update what has changed**

When updating project context:
1. Use the validation system first: `python validation/validate_context.py`
2. Use incremental updates: `python validation/update_context.py`
3. Preserve existing goals and configurations
4. Only modify fields that have actually changed
5. Add `current_focus` to track active work

## 📋 Planning and Estimation Guidelines

### For project-manager Agent

When creating project plans:
- **Structure**: Break work into prioritized items, not time-boxed sprints
- **Sequencing**: Focus on dependencies and logical order
- **Capacity**: Use story points or complexity ratings, not hours
- **Milestones**: Define by achievement, not by date
- **Risk**: Assess by probability and impact, not by timeline

Example sprint planning:
```markdown
## Sprint Focus
Primary Objective: Implement authentication system

## Prioritized Backlog
1. [CRITICAL] Core authentication service
2. [CRITICAL] User session management  
3. [HIGH] Password reset flow
4. [MEDIUM] Remember me functionality
5. [LOW] Social login integration

## Complexity Assessment
- Authentication service: COMPLEX (multiple integrations)
- Session management: MODERATE (standard patterns)
- Password reset: SIMPLE (well-defined flow)
```

### For system-architect Agent

When providing implementation timelines:
- Focus on technical complexity and dependencies
- Describe phases by functionality, not duration
- Use priority-based rollout strategies

Example:
```markdown
## Implementation Phases
Priority 1: Core Infrastructure
- Database schema setup
- API gateway configuration
- Authentication middleware

Priority 2: Feature Implementation  
- User management endpoints
- Role-based access control
- Audit logging

Priority 3: Optimization
- Caching layer
- Performance tuning
- Monitoring setup
```

### For requirements-analyst Agent

When gathering requirements:
- Define success by outcomes, not deadlines
- Prioritize features by value, not by sprint
- Set acceptance criteria by functionality, not timing

### For test-engineer Agent

When planning test strategies:
- Organize by test priority, not test phases
- Define coverage by risk level, not by sprint
- Structure test suites by complexity, not duration

### For devops-engineer Agent

When planning deployments:
- Sequence by dependencies, not calendar
- Define rollout by risk tolerance, not dates
- Structure migrations by complexity, not timeline

### For code-reviewer Agent

When reviewing code:
- Prioritize issues by severity, not fix time
- Categorize findings by impact, not effort
- Order recommendations by importance, not sequence

### For security-expert Agent

When assessing security:
- Rank vulnerabilities by risk, not remediation time
- Prioritize fixes by exposure, not effort
- Structure audits by criticality, not schedule

## 🎯 Output Format Requirements

### Task Lists
Always format tasks with priority indicators:
```markdown
## Task Prioritization
🔴 Critical Priority
- Task 1
- Task 2

🟡 Important Priority  
- Task 3
- Task 4

🟢 Strategic Priority
- Task 5
- Task 6
```

### Roadmaps
Structure roadmaps by priority, not timeline:
```markdown
## Development Roadmap

### Immediate Focus (Critical)
- Core functionality implementation
- Security vulnerabilities patching

### Secondary Focus (Important)
- Performance optimization
- User experience improvements

### Future Enhancements (Strategic)
- Advanced features
- Platform expansions
```

### Progress Tracking
Track progress by completion, not by time:
```markdown
## Progress Status
- Authentication: 75% complete
- Database migration: Complete ✓
- API development: In Progress
- Testing: Not Started
```

## 🔄 Context and Validation

### Before Any Work
1. Validate current context: `python validation/validate_context.py`
2. Check agent templates: `./validation/validate.sh`
3. Review project goals in PROJECT_CONTEXT.yaml
4. Understand current focus areas

### During Work
1. Align all recommendations with project goals
2. Use priority-based planning exclusively
3. Update context incrementally as work progresses
4. Maintain focus on value delivery over time tracking

### After Work
1. Update PROJECT_CONTEXT.yaml with current focus
2. Document decisions by priority and rationale
3. Track progress by completion percentage
4. Review alignment with success metrics

## 📝 Communication Standards

### With Users
- Present options by priority and impact
- Explain complexity without time estimates
- Focus on value delivery and outcomes
- Use relative comparisons for effort

### In Documentation
- Structure guides by workflow, not timeline
- Organize tutorials by complexity level
- Present examples by use case priority
- Define success by achievement metrics

### In Reports
- Summarize by accomplishment, not duration
- Measure by impact, not time spent
- Prioritize findings by severity
- Recommend actions by importance

## ⚠️ Enforcement

These guidelines are **mandatory** for all agents. The validation system will check for compliance, and any outputs violating these rules should be rejected and regenerated.

Remember: **Quality and priority over time estimates. Always.**