#!/usr/bin/env python
"""
OpenADK Planning Enforcement System
Strict enforcement wrapper for agent outputs
"""

import yaml
import json
import re
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path
from enum import Enum
from dataclasses import dataclass, asdict

# Load planning rules
RULES_PATH = Path(__file__).parent / "planning_rules.yaml"
with open(RULES_PATH, 'r') as f:
    RULES = yaml.safe_load(f)

class PlanningPriority(Enum):
    """Strictly enforced priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value.lower() in [p.value for p in cls]
    
    @classmethod
    def from_string(cls, value: str) -> Optional['PlanningPriority']:
        value = value.lower()
        for priority in cls:
            if priority.value == value:
                return priority
        return None

class PlanningComplexity(Enum):
    """Strictly enforced complexity levels"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    
    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value.lower() in [c.value for c in cls]
    
    @classmethod
    def from_string(cls, value: str) -> Optional['PlanningComplexity']:
        value = value.lower()
        for complexity in cls:
            if complexity.value == value:
                return complexity
        return None

@dataclass
class Task:
    """Enforced task structure"""
    name: str
    priority: PlanningPriority
    complexity: PlanningComplexity
    dependencies: List[str]
    id: Optional[str] = None
    acceptance_criteria: Optional[List[str]] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary with enum values as strings"""
        result = {
            "name": self.name,
            "priority": self.priority.value,
            "complexity": self.complexity.value,
            "dependencies": self.dependencies
        }
        if self.id:
            result["id"] = self.id
        if self.acceptance_criteria:
            result["acceptance_criteria"] = self.acceptance_criteria
        return result
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate task against rules"""
        errors = []
        
        if not self.name:
            errors.append("Task name is required")
        
        if not isinstance(self.priority, PlanningPriority):
            errors.append(f"Invalid priority: must be one of {[p.value for p in PlanningPriority]}")
            
        if not isinstance(self.complexity, PlanningComplexity):
            errors.append(f"Invalid complexity: must be one of {[c.value for c in PlanningComplexity]}")
            
        # Check for forbidden terms in name
        for term in RULES["forbidden_terms"]["time_units"]:
            if term in self.name.lower():
                errors.append(f"Forbidden time term '{term}' in task name")
                
        return len(errors) == 0, errors

@dataclass
class Milestone:
    """Enforced milestone structure"""
    name: str
    priority: PlanningPriority
    success_criteria: List[str]
    prerequisites: List[str]
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate milestone"""
        errors = []
        
        if not self.name:
            errors.append("Milestone name is required")
            
        if not self.success_criteria:
            errors.append("Success criteria are required")
            
        if not isinstance(self.priority, PlanningPriority):
            errors.append("Invalid priority level")
            
        return len(errors) == 0, errors

class PlanningEnforcer:
    """Main enforcement class for planning outputs"""
    
    def __init__(self, agent_name: Optional[str] = None):
        self.agent_name = agent_name
        self.rules = RULES
        self.enforcement_level = self.rules["enforcement"]["level"]
        
    def create_task(self, 
                   name: str,
                   priority: Union[str, PlanningPriority],
                   complexity: Union[str, PlanningComplexity],
                   dependencies: List[str] = None) -> Task:
        """Create a validated task - will raise exception if invalid"""
        
        # Convert strings to enums
        if isinstance(priority, str):
            priority_enum = PlanningPriority.from_string(priority)
            if not priority_enum:
                raise ValueError(f"Invalid priority '{priority}'. Must be one of: {[p.value for p in PlanningPriority]}")
            priority = priority_enum
            
        if isinstance(complexity, str):
            complexity_enum = None
            for c in PlanningComplexity:
                if c.value == complexity.lower():
                    complexity_enum = c
                    break
            if not complexity_enum:
                raise ValueError(f"Invalid complexity '{complexity}'. Must be one of: {[c.value for c in PlanningComplexity]}")
            complexity = complexity_enum
        
        task = Task(
            name=name,
            priority=priority,
            complexity=complexity,
            dependencies=dependencies or []
        )
        
        # Validate
        is_valid, errors = task.validate()
        if not is_valid:
            raise ValueError(f"Task validation failed: {'; '.join(errors)}")
            
        return task
    
    def create_priority_list(self, tasks: List[Task]) -> Dict[str, List[Dict]]:
        """Create a priority-organized task list"""
        priority_list = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": []
        }
        
        for task in tasks:
            priority_list[task.priority.value].append(task.to_dict())
            
        return priority_list
    
    def validate_text_output(self, text: str) -> Tuple[bool, List[str]]:
        """Validate any text output for forbidden terms"""
        violations = []
        
        # Check for forbidden time units
        for term in self.rules["forbidden_terms"]["time_units"]:
            pattern = r'\b\d+\s*' + re.escape(term) + r's?\b'
            if re.search(pattern, text, re.IGNORECASE):
                violations.append(f"Forbidden time unit: {term}")
        
        # Check for deadline terms
        for term in self.rules["forbidden_terms"]["deadline_terms"]:
            if term.lower() in text.lower():
                violations.append(f"Forbidden deadline term: {term}")
                
        # Check for temporal references
        for term in self.rules["forbidden_terms"]["temporal_references"]:
            if term.lower() in text.lower():
                violations.append(f"Forbidden temporal reference: {term}")
                
        return len(violations) == 0, violations
    
    def transform_text(self, text: str) -> str:
        """Transform text to be compliant"""
        transformed = text
        
        # Apply transformation rules
        for old, new in self.rules["transformations"].items():
            transformed = re.sub(re.escape(old), new, transformed, flags=re.IGNORECASE)
            
        return transformed
    
    def enforce_output(self, output: Any) -> Dict[str, Any]:
        """
        Main enforcement function
        Returns enforced output or raises exception in strict mode
        """
        result = {
            "original": output,
            "valid": False,
            "transformed": None,
            "violations": [],
            "structured": None
        }
        
        # If output is already structured (Task, Milestone, etc), validate it
        if isinstance(output, (Task, Milestone)):
            is_valid, errors = output.validate()
            result["valid"] = is_valid
            result["violations"] = errors
            result["structured"] = output.to_dict() if hasattr(output, 'to_dict') else asdict(output)
            
        # If output is text, validate and potentially transform
        elif isinstance(output, str):
            is_valid, violations = self.validate_text_output(output)
            result["valid"] = is_valid
            result["violations"] = violations
            
            if not is_valid:
                if self.enforcement_level == "strict":
                    raise ValueError(f"Output validation failed: {'; '.join(violations)}")
                else:
                    # Transform the output
                    result["transformed"] = self.transform_text(output)
                    
        # If output is a list of tasks
        elif isinstance(output, list) and all(isinstance(t, Task) for t in output):
            all_valid = True
            all_errors = []
            for task in output:
                is_valid, errors = task.validate()
                if not is_valid:
                    all_valid = False
                    all_errors.extend(errors)
            
            result["valid"] = all_valid
            result["violations"] = all_errors
            result["structured"] = self.create_priority_list(output)
            
        return result

# Convenience functions for agents to use
def create_compliant_task(name: str, priority: str, complexity: str, dependencies: List[str] = None) -> Dict:
    """Helper function to create a compliant task"""
    enforcer = PlanningEnforcer()
    task = enforcer.create_task(name, priority, complexity, dependencies)
    return task.to_dict()

def validate_output(output: str, agent_name: Optional[str] = None) -> bool:
    """Helper function to validate output"""
    enforcer = PlanningEnforcer(agent_name)
    is_valid, _ = enforcer.validate_text_output(output)
    return is_valid

def get_allowed_values() -> Dict[str, List[str]]:
    """Get all allowed values for planning"""
    return {
        "priorities": [p.value for p in PlanningPriority],
        "complexities": [c.value for c in PlanningComplexity],
        "forbidden_terms": RULES["forbidden_terms"]
    }

# Example usage
if __name__ == "__main__":
    # Test enforcement
    enforcer = PlanningEnforcer("project-manager")
    
    # Create compliant tasks
    try:
        task1 = enforcer.create_task(
            name="Implement authentication",
            priority="critical",
            complexity="complex",
            dependencies=[]
        )
        print(f"Valid task created: {task1.to_dict()}")
    except ValueError as e:
        print(f"Task creation failed: {e}")
    
    # Test text validation
    bad_text = "Complete this in 2 weeks with a deadline of Q1 2025"
    is_valid, violations = enforcer.validate_text_output(bad_text)
    print(f"\nText validation: Valid={is_valid}")
    if violations:
        print(f"Violations: {violations}")
        transformed = enforcer.transform_text(bad_text)
        print(f"Transformed: {transformed}")
    
    # Show allowed values
    print(f"\nAllowed values: {get_allowed_values()}")