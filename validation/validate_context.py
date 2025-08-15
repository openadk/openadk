#!/usr/bin/env python
"""
OpenADK Context Validation System
Validates PROJECT_CONTEXT.yaml and provides detailed feedback
"""

import yaml
import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

class ContextValidator:
    def __init__(self, context_path: str):
        self.context_path = context_path
        self.errors = []
        self.warnings = []
        self.info = []
        
    def validate(self) -> bool:
        """Main validation method"""
        if not os.path.exists(self.context_path):
            self.warnings.append("PROJECT_CONTEXT.yaml not found (will be created on initialization)")
            return True
            
        # Load and parse YAML
        try:
            with open(self.context_path, 'r') as f:
                self.data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML syntax: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error reading file: {e}")
            return False
            
        # Validate structure
        self._validate_structure()
        self._validate_project_section()
        self._validate_repositories()
        self._validate_goals()
        
        return len(self.errors) == 0
    
    def _validate_structure(self):
        """Validate top-level structure"""
        required_sections = ['project', 'repositories', 'conventions', 
                           'development_guidelines', 'quick_reference']
        
        missing = [s for s in required_sections if s not in self.data]
        if missing:
            self.errors.append(f"Missing required sections: {', '.join(missing)}")
    
    def _validate_project_section(self):
        """Validate project section"""
        if 'project' not in self.data:
            return
            
        project = self.data['project']
        required_fields = ['name', 'type', 'description', 'initialized_at']
        
        missing = [f for f in required_fields if f not in project]
        if missing:
            self.errors.append(f"Project section missing fields: {', '.join(missing)}")
        
        # Validate type field
        if 'type' in project:
            valid_types = ['single-repository', 'single-repository-focus', 
                          'multi-repository', 'monorepo']
            if project['type'] not in valid_types:
                self.errors.append(f"Invalid project type: {project['type']}")
    
    def _validate_repositories(self):
        """Validate repositories section"""
        if 'repositories' not in self.data:
            return
            
        repos = self.data['repositories']
        if not isinstance(repos, dict):
            self.errors.append("Repositories section must be a dictionary")
            return
            
        for repo_name, repo_data in repos.items():
            required = ['path', 'description', 'technology_stack', 'status', 'has_git']
            missing = [f for f in required if f not in repo_data]
            if missing:
                self.warnings.append(f"Repository '{repo_name}' missing fields: {', '.join(missing)}")
            
            # Validate status
            if 'status' in repo_data:
                valid_statuses = ['active', 'inactive', 'archived', 'maintenance']
                if repo_data['status'] not in valid_statuses:
                    self.errors.append(f"Invalid status for {repo_name}: {repo_data['status']}")
    
    def _validate_goals(self):
        """Validate goals section (new requirement)"""
        if 'project' not in self.data:
            return
            
        project = self.data['project']
        if 'goals' not in project:
            self.warnings.append("Missing 'goals' section in project (required for goal alignment)")
            self.info.append("Consider adding goals with: primary_objective, success_metrics, constraints")
        else:
            goals = project['goals']
            required_goal_fields = ['primary_objective', 'success_metrics', 'constraints']
            missing = [f for f in required_goal_fields if f not in goals]
            if missing:
                self.warnings.append(f"Goals section missing recommended fields: {', '.join(missing)}")
    
    def print_results(self):
        """Print validation results"""
        print(f"{Colors.BLUE}Validating PROJECT_CONTEXT.yaml{Colors.NC}")
        
        if self.errors:
            for error in self.errors:
                print(f"{Colors.RED}ERROR:{Colors.NC} {error}")
        
        if self.warnings:
            for warning in self.warnings:
                print(f"{Colors.YELLOW}WARNING:{Colors.NC} {warning}")
        
        if self.info:
            for info in self.info:
                print(f"{Colors.BLUE}INFO:{Colors.NC} {info}")
        
        if not self.errors and not self.warnings:
            print(f"{Colors.GREEN}VALID:{Colors.NC} PROJECT_CONTEXT.yaml is valid")
        elif not self.errors:
            print(f"{Colors.GREEN}VALID:{Colors.NC} PROJECT_CONTEXT.yaml is valid with warnings")

def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    context_path = project_root / "_project" / "PROJECT_CONTEXT.yaml"
    
    validator = ContextValidator(str(context_path))
    is_valid = validator.validate()
    validator.print_results()
    
    return 0 if is_valid else 1

if __name__ == "__main__":
    sys.exit(main())