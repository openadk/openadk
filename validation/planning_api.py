#!/usr/bin/env python
"""
OpenADK Planning API
Structured API for agents to create compliant plans
No free-form text allowed - only structured data
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import yaml

# Import enforcement
from enforce_planning import PlanningPriority, PlanningComplexity, Task, Milestone

class OutputFormat(Enum):
    """Allowed output formats"""
    JSON = "json"
    YAML = "yaml"
    MARKDOWN = "markdown"

class PlanType(Enum):
    """Types of plans that can be created"""
    TASK_LIST = "task_list"
    ROADMAP = "roadmap"
    SPRINT = "sprint"
    ARCHITECTURE = "architecture"
    REQUIREMENTS = "requirements"

@dataclass
class PlanBuilder:
    """
    Structured plan builder that prevents non-compliant outputs
    Agents MUST use this instead of generating free text
    """
    
    plan_type: PlanType
    tasks: List[Task] = field(default_factory=list)
    milestones: List[Milestone] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_task(self,
                 name: str,
                 priority: str,
                 complexity: str,
                 dependencies: Optional[List[str]] = None) -> 'PlanBuilder':
        """Add a task to the plan - enforces valid values"""
        # This will raise exception if invalid
        task = Task(
            name=name,
            priority=PlanningPriority.from_string(priority),
            complexity=PlanningComplexity.from_string(complexity),
            dependencies=dependencies or []
        )
        
        # Validate task
        is_valid, errors = task.validate()
        if not is_valid:
            raise ValueError(f"Invalid task: {errors}")
            
        self.tasks.append(task)
        return self
    
    def add_milestone(self,
                     name: str,
                     priority: str,
                     success_criteria: List[str],
                     prerequisites: Optional[List[str]] = None) -> 'PlanBuilder':
        """Add a milestone to the plan"""
        milestone = Milestone(
            name=name,
            priority=PlanningPriority.from_string(priority),
            success_criteria=success_criteria,
            prerequisites=prerequisites or []
        )
        
        is_valid, errors = milestone.validate()
        if not is_valid:
            raise ValueError(f"Invalid milestone: {errors}")
            
        self.milestones.append(milestone)
        return self
    
    def set_metadata(self, key: str, value: Any) -> 'PlanBuilder':
        """Set metadata - validates against forbidden terms"""
        # Check value for forbidden terms if it's a string
        if isinstance(value, str):
            forbidden_terms = ["day", "week", "month", "hour", "deadline", "due date"]
            for term in forbidden_terms:
                if term in value.lower():
                    raise ValueError(f"Forbidden term '{term}' in metadata value")
        
        self.metadata[key] = value
        return self
    
    def build(self, format: OutputFormat = OutputFormat.YAML) -> str:
        """Build the final plan in specified format"""
        
        # Create structured data
        plan_data = {
            "type": self.plan_type.value,
            "version": "1.0",
            "compliance": {
                "uses_time_estimates": False,
                "uses_priority_system": True,
                "validated": True
            },
            "metadata": self.metadata
        }
        
        # Organize tasks by priority
        if self.tasks:
            priority_groups = {
                "critical": [],
                "high": [],
                "medium": [],
                "low": []
            }
            
            for task in self.tasks:
                priority_groups[task.priority.value].append({
                    "name": task.name,
                    "complexity": task.complexity.value,
                    "dependencies": task.dependencies
                })
            
            plan_data["prioritized_tasks"] = priority_groups
        
        # Add milestones if present
        if self.milestones:
            plan_data["milestones"] = [
                {
                    "name": m.name,
                    "priority": m.priority.value,
                    "success_criteria": m.success_criteria,
                    "prerequisites": m.prerequisites
                }
                for m in self.milestones
            ]
        
        # Format output
        if format == OutputFormat.JSON:
            return json.dumps(plan_data, indent=2)
        elif format == OutputFormat.YAML:
            return yaml.dump(plan_data, default_flow_style=False, sort_keys=False)
        elif format == OutputFormat.MARKDOWN:
            return self._to_markdown(plan_data)
        else:
            raise ValueError(f"Unknown format: {format}")
    
    def _to_markdown(self, data: Dict) -> str:
        """Convert to markdown format"""
        lines = []
        lines.append(f"# {data['type'].replace('_', ' ').title()}")
        lines.append("")
        
        if "prioritized_tasks" in data:
            for priority in ["critical", "high", "medium", "low"]:
                tasks = data["prioritized_tasks"][priority]
                if tasks:
                    lines.append(f"## {priority.upper()} Priority")
                    for task in tasks:
                        complexity = task['complexity'].upper()
                        lines.append(f"- **{task['name']}** [Complexity: {complexity}]")
                        if task['dependencies']:
                            lines.append(f"  - Dependencies: {', '.join(task['dependencies'])}")
                    lines.append("")
        
        if "milestones" in data:
            lines.append("## Milestones")
            for m in data["milestones"]:
                lines.append(f"### {m['name']} (Priority: {m['priority'].upper()})")
                lines.append("**Success Criteria:**")
                for criterion in m['success_criteria']:
                    lines.append(f"- {criterion}")
                if m['prerequisites']:
                    lines.append("**Prerequisites:**")
                    for prereq in m['prerequisites']:
                        lines.append(f"- {prereq}")
                lines.append("")
        
        return "\n".join(lines)

# Agent-specific builders with pre-configured rules
class ProjectManagerPlan(PlanBuilder):
    """Specialized builder for project-manager agent"""
    def __init__(self):
        super().__init__(PlanType.SPRINT)
        self.set_metadata("agent", "project-manager")
        self.set_metadata("focus", "task_breakdown_and_prioritization")

class SystemArchitectPlan(PlanBuilder):
    """Specialized builder for system-architect agent"""
    def __init__(self):
        super().__init__(PlanType.ARCHITECTURE)
        self.set_metadata("agent", "system-architect")
        self.set_metadata("focus", "technical_design_and_dependencies")

class RequirementsAnalystPlan(PlanBuilder):
    """Specialized builder for requirements-analyst agent"""
    def __init__(self):
        super().__init__(PlanType.REQUIREMENTS)
        self.set_metadata("agent", "requirements-analyst")
        self.set_metadata("focus", "success_criteria_and_acceptance")

# Simple API functions for agents
def create_task_list(tasks: List[Dict[str, str]]) -> str:
    """
    Create a compliant task list
    
    Args:
        tasks: List of dicts with 'name', 'priority', 'complexity'
    
    Returns:
        YAML formatted task list
    """
    builder = PlanBuilder(PlanType.TASK_LIST)
    
    for task in tasks:
        builder.add_task(
            name=task['name'],
            priority=task['priority'],
            complexity=task['complexity'],
            dependencies=task.get('dependencies', [])
        )
    
    return builder.build(OutputFormat.YAML)

def create_roadmap(phases: List[Dict[str, Any]]) -> str:
    """
    Create a compliant roadmap
    
    Args:
        phases: List of phase dictionaries
    
    Returns:
        YAML formatted roadmap
    """
    builder = PlanBuilder(PlanType.ROADMAP)
    
    for i, phase in enumerate(phases):
        # Add phase as milestone
        builder.add_milestone(
            name=phase['name'],
            priority=phase['priority'],
            success_criteria=phase.get('success_criteria', []),
            prerequisites=phase.get('prerequisites', [])
        )
        
        # Add phase tasks if present
        if 'tasks' in phase:
            for task in phase['tasks']:
                builder.add_task(
                    name=f"Phase {i+1}: {task['name']}",
                    priority=task['priority'],
                    complexity=task.get('complexity', 'moderate'),
                    dependencies=task.get('dependencies', [])
                )
    
    return builder.build(OutputFormat.YAML)

# Example usage
if __name__ == "__main__":
    # Project manager creating a sprint plan
    pm_plan = ProjectManagerPlan()
    pm_plan.add_task("Setup CI/CD pipeline", "critical", "complex", ["DevOps approval"])
    pm_plan.add_task("Implement user auth", "high", "moderate", ["Database schema"])
    pm_plan.add_task("Add documentation", "low", "simple", [])
    
    print("Project Manager Sprint Plan:")
    print(pm_plan.build(OutputFormat.MARKDOWN))
    print("\n" + "="*50 + "\n")
    
    # System architect creating a roadmap
    architect_plan = SystemArchitectPlan()
    architect_plan.add_milestone(
        "Core Infrastructure",
        "critical",
        ["Database configured", "API gateway operational", "Auth service deployed"],
        []
    )
    architect_plan.add_milestone(
        "Feature Implementation",
        "high",
        ["All endpoints functional", "Data validation complete"],
        ["Core Infrastructure"]
    )
    
    print("System Architect Roadmap:")
    print(architect_plan.build(OutputFormat.YAML))