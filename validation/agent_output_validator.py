#!/usr/bin/env python
"""
OpenADK Agent Output Validator
Enforces strict rules on agent outputs programmatically
"""

import re
import json
import yaml
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class Priority(Enum):
    """Allowed priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    
class Complexity(Enum):
    """Allowed complexity ratings"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    
class Size(Enum):
    """Allowed relative sizes"""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    XL = "extra_large"

@dataclass
class ValidationRule:
    """Defines a validation rule"""
    name: str
    pattern: str
    severity: str  # "error", "warning"
    message: str
    
class AgentOutputValidator:
    def __init__(self):
        # Forbidden patterns that should NEVER appear
        self.forbidden_patterns = [
            # Time estimates
            ValidationRule(
                name="time_estimate_days",
                pattern=r'\b\d+\s*(day|days)\b',
                severity="error",
                message="Time estimates in days are forbidden. Use priority levels."
            ),
            ValidationRule(
                name="time_estimate_weeks",
                pattern=r'\b\d+\s*(week|weeks)\b',
                severity="error",
                message="Time estimates in weeks are forbidden. Use priority levels."
            ),
            ValidationRule(
                name="time_estimate_months",
                pattern=r'\b\d+\s*(month|months)\b',
                severity="error",
                message="Time estimates in months are forbidden. Use priority levels."
            ),
            ValidationRule(
                name="time_estimate_hours",
                pattern=r'\b\d+\s*(hour|hours)\b',
                severity="error",
                message="Time estimates in hours are forbidden. Use complexity ratings."
            ),
            ValidationRule(
                name="time_estimate_quarters",
                pattern=r'\bQ[1-4]\s+20\d{2}\b',
                severity="error",
                message="Quarter-based timelines are forbidden. Use priority sequencing."
            ),
            ValidationRule(
                name="time_estimate_ranges",
                pattern=r'\b\d+\s*-\s*\d+\s*(days|weeks|months|hours)\b',
                severity="error",
                message="Time range estimates are forbidden. Use priority levels."
            ),
            ValidationRule(
                name="deadline_references",
                pattern=r'\b(deadline|due date|due by|complete by|finish by)\b',
                severity="error",
                message="Deadline references are forbidden. Use priority indicators."
            ),
        ]
        
        # Required patterns that MUST appear for certain outputs
        self.required_patterns = {
            "project_plan": [
                ValidationRule(
                    name="priority_levels",
                    pattern=r'(critical|high|medium|low|priority\s+\d+)',
                    severity="error",
                    message="Project plans must use priority levels"
                )
            ],
            "task_breakdown": [
                ValidationRule(
                    name="complexity_or_size",
                    pattern=r'(simple|moderate|complex|small|medium|large|xl)',
                    severity="error",
                    message="Task breakdowns must use complexity or size ratings"
                )
            ]
        }
        
    def validate_output(self, output: str, output_type: str = "general") -> Tuple[bool, List[Dict]]:
        """
        Validate agent output against rules
        
        Returns:
            (is_valid, violations)
        """
        violations = []
        
        # Check forbidden patterns
        for rule in self.forbidden_patterns:
            pattern = re.compile(rule.pattern, re.IGNORECASE)
            matches = pattern.findall(output)
            if matches:
                violations.append({
                    "rule": rule.name,
                    "severity": rule.severity,
                    "message": rule.message,
                    "matches": matches
                })
        
        # Check required patterns if applicable
        if output_type in self.required_patterns:
            for rule in self.required_patterns[output_type]:
                pattern = re.compile(rule.pattern, re.IGNORECASE)
                if not pattern.search(output):
                    violations.append({
                        "rule": rule.name,
                        "severity": rule.severity,
                        "message": rule.message,
                        "matches": []
                    })
        
        # Check goal alignment if PROJECT_CONTEXT exists
        goal_violations = self._check_goal_alignment(output)
        violations.extend(goal_violations)
        
        is_valid = not any(v["severity"] == "error" for v in violations)
        return is_valid, violations
    
    def _check_goal_alignment(self, output: str) -> List[Dict]:
        """Check if output aligns with project goals"""
        violations = []
        
        try:
            # Load project context
            with open("_project/PROJECT_CONTEXT.yaml", "r") as f:
                context = yaml.safe_load(f)
            
            if "project" in context and "goals" in context["project"]:
                goals = context["project"]["goals"]
                
                # Check for non-goals
                if "non_goals" in goals:
                    for non_goal in goals["non_goals"]:
                        # Simple keyword check - could be made more sophisticated
                        if non_goal.lower() in output.lower():
                            violations.append({
                                "rule": "non_goal_violation",
                                "severity": "warning",
                                "message": f"Output may violate non-goal: {non_goal}",
                                "matches": [non_goal]
                            })
        except:
            # If we can't load context, skip goal checking
            pass
            
        return violations
    
    def transform_output(self, output: str) -> str:
        """
        Transform output to comply with rules
        Replaces forbidden patterns with compliant alternatives
        """
        transformations = {
            r'\b1\s*day\b': 'Priority: Critical',
            r'\b2-3\s*days\b': 'Complexity: Simple',
            r'\b1\s*week\b': 'Priority: High',
            r'\b2\s*weeks\b': 'Priority: Medium',
            r'\b1\s*month\b': 'Priority: Low',
            r'\b(\d+)\s*hours?\b': 'Complexity: Moderate',
            r'Q1 2025': 'Priority 1',
            r'Q2 2025': 'Priority 2',
            r'Q3 2025': 'Priority 3',
            r'Q4 2025': 'Priority 4',
            r'deadline': 'priority target',
            r'due date': 'priority milestone',
            r'complete by': 'prioritize for',
        }
        
        transformed = output
        for pattern, replacement in transformations.items():
            transformed = re.sub(pattern, replacement, transformed, flags=re.IGNORECASE)
            
        return transformed

class StructuredPlanGenerator:
    """Generate compliant structured plans"""
    
    @staticmethod
    def create_task_list(tasks: List[Dict[str, Any]]) -> Dict:
        """
        Create a structured task list that's inherently compliant
        
        Args:
            tasks: List of task dictionaries with 'name', 'complexity', 'priority'
        """
        structured = {
            "type": "task_list",
            "format_version": "1.0",
            "priorities": {
                "critical": [],
                "high": [],
                "medium": [],
                "low": []
            },
            "metadata": {
                "uses_time_estimates": False,
                "uses_priority_system": True
            }
        }
        
        for task in tasks:
            priority = task.get("priority", "medium").lower()
            if priority in structured["priorities"]:
                structured["priorities"][priority].append({
                    "name": task["name"],
                    "complexity": task.get("complexity", "moderate"),
                    "dependencies": task.get("dependencies", []),
                    "id": task.get("id", "")
                })
        
        return structured
    
    @staticmethod
    def create_roadmap(phases: List[Dict[str, Any]]) -> Dict:
        """
        Create a structured roadmap without timelines
        """
        return {
            "type": "roadmap",
            "format_version": "1.0",
            "phases": [
                {
                    "sequence": i + 1,
                    "name": phase["name"],
                    "priority": phase.get("priority", "medium"),
                    "objectives": phase.get("objectives", []),
                    "success_criteria": phase.get("success_criteria", []),
                    "dependencies": phase.get("dependencies", [])
                }
                for i, phase in enumerate(phases)
            ],
            "metadata": {
                "uses_time_estimates": False,
                "uses_sequencing": True
            }
        }

def validate_agent_output(output: str, output_type: str = "general") -> Dict:
    """
    Main validation function to be called by agents
    
    Returns dict with:
        - valid: bool
        - violations: list
        - transformed: str (compliant version)
        - structured: dict (if applicable)
    """
    validator = AgentOutputValidator()
    
    # Validate
    is_valid, violations = validator.validate_output(output, output_type)
    
    # Transform if needed
    transformed = output
    if not is_valid:
        transformed = validator.transform_output(output)
        # Re-validate transformed version
        is_valid_after, _ = validator.validate_output(transformed, output_type)
    
    return {
        "valid": is_valid,
        "violations": violations,
        "transformed": transformed if not is_valid else None,
        "requires_transformation": not is_valid
    }

# Example usage for testing
if __name__ == "__main__":
    # Test with non-compliant output
    test_output = """
    Project Plan:
    - Phase 1: Complete in 2 weeks
    - Phase 2: 1 month timeline
    - Deadline: Q1 2025
    """
    
    result = validate_agent_output(test_output, "project_plan")
    print("Validation Result:")
    print(f"Valid: {result['valid']}")
    print(f"Violations: {result['violations']}")
    if result['transformed']:
        print(f"Transformed:\n{result['transformed']}")
    
    # Test structured plan generation
    tasks = [
        {"name": "Setup infrastructure", "priority": "critical", "complexity": "complex"},
        {"name": "Implement API", "priority": "high", "complexity": "moderate"},
        {"name": "Add documentation", "priority": "low", "complexity": "simple"}
    ]
    
    generator = StructuredPlanGenerator()
    structured_plan = generator.create_task_list(tasks)
    print("\nStructured Plan:")
    print(json.dumps(structured_plan, indent=2))