#!/usr/bin/env python
"""
OpenADK Context Update System
Handles incremental updates to PROJECT_CONTEXT.yaml
Only updates changed elements instead of full rewrites
"""

import yaml
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import json

class ContextUpdater:
    def __init__(self, context_path: str):
        self.context_path = context_path
        self.existing_data = None
        self.updated_data = None
        self.changes = []
        
    def load_existing(self) -> bool:
        """Load existing PROJECT_CONTEXT.yaml if it exists"""
        if not os.path.exists(self.context_path):
            print(f"Creating new PROJECT_CONTEXT.yaml at {self.context_path}")
            self.existing_data = self._get_default_structure()
            return False
            
        try:
            with open(self.context_path, 'r') as f:
                self.existing_data = yaml.safe_load(f)
            return True
        except Exception as e:
            print(f"Error loading existing context: {e}")
            self.existing_data = self._get_default_structure()
            return False
    
    def _get_default_structure(self) -> Dict:
        """Get default PROJECT_CONTEXT structure"""
        return {
            'project': {
                'name': 'OpenADK Workspace',
                'type': 'single-repository',
                'description': 'AI agent enhancement toolkit',
                'initialized_at': datetime.now().strftime('%Y-%m-%d'),
                'goals': {
                    'primary_objective': 'Enhance AI-assisted development with specialized agents',
                    'success_metrics': [
                        'Agent invocation accuracy',
                        'Code quality improvement',
                        'Developer productivity gains'
                    ],
                    'constraints': [
                        'Must work with Claude Code',
                        'Zero-configuration philosophy',
                        'Model-agnostic future compatibility'
                    ],
                    'milestones': [],
                    'non_goals': []
                }
            },
            'repositories': {},
            'conventions': {
                'commit_style': 'conventional-commits',
                'branch_strategy': 'main-branch',
                'documentation': 'markdown'
            },
            'development_guidelines': {
                'testing': 'Project-specific testing frameworks',
                'security': 'Follow security best practices',
                'code_style': 'Match existing project conventions'
            },
            'quick_reference': {
                'available_agents': {},
                'working_directories': {},
                'key_commands': {}
            }
        }
    
    def update_project_info(self, updates: Dict[str, Any]):
        """Update project information only if changed"""
        if not self.updated_data:
            self.updated_data = self.existing_data.copy()
            
        project = self.updated_data.get('project', {})
        
        for key, value in updates.items():
            if key not in project or project[key] != value:
                old_value = project.get(key, 'Not set')
                project[key] = value
                self.changes.append(f"Updated project.{key}: {old_value} -> {value}")
        
        self.updated_data['project'] = project
    
    def update_repository(self, repo_name: str, repo_data: Dict[str, Any]):
        """Update repository information only if changed"""
        if not self.updated_data:
            self.updated_data = self.existing_data.copy()
            
        repos = self.updated_data.get('repositories', {})
        
        if repo_name not in repos:
            repos[repo_name] = repo_data
            self.changes.append(f"Added new repository: {repo_name}")
        else:
            existing_repo = repos[repo_name]
            for key, value in repo_data.items():
                if key not in existing_repo or existing_repo[key] != value:
                    old_value = existing_repo.get(key, 'Not set')
                    existing_repo[key] = value
                    self.changes.append(f"Updated {repo_name}.{key}")
            repos[repo_name] = existing_repo
        
        self.updated_data['repositories'] = repos
    
    def update_goals(self, goals: Dict[str, Any]):
        """Update project goals"""
        if not self.updated_data:
            self.updated_data = self.existing_data.copy()
            
        project = self.updated_data.get('project', {})
        
        if 'goals' not in project:
            project['goals'] = goals
            self.changes.append("Added goals section to project")
        else:
            existing_goals = project['goals']
            for key, value in goals.items():
                if key not in existing_goals or existing_goals[key] != value:
                    existing_goals[key] = value
                    self.changes.append(f"Updated goals.{key}")
            project['goals'] = existing_goals
        
        self.updated_data['project'] = project
    
    def add_current_focus(self, repo_name: str, focus: str):
        """Add current focus to a repository"""
        if not self.updated_data:
            self.updated_data = self.existing_data.copy()
            
        repos = self.updated_data.get('repositories', {})
        if repo_name in repos:
            repos[repo_name]['current_focus'] = focus
            self.changes.append(f"Updated current focus for {repo_name}")
            self.updated_data['repositories'] = repos
    
    def save(self, dry_run: bool = False) -> bool:
        """Save updated context to file"""
        if not self.updated_data:
            print("No updates to save")
            return True
            
        if not self.changes:
            print("No changes detected")
            return True
        
        # Add metadata
        self.updated_data['# Last updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if dry_run:
            print("DRY RUN - Changes that would be made:")
            for change in self.changes:
                print(f"  - {change}")
            return True
        
        try:
            # Create backup of existing file
            if os.path.exists(self.context_path):
                backup_path = f"{self.context_path}.backup"
                with open(self.context_path, 'r') as src:
                    with open(backup_path, 'w') as dst:
                        dst.write(src.read())
            
            # Write updated context
            with open(self.context_path, 'w') as f:
                yaml.dump(self.updated_data, f, default_flow_style=False, 
                         sort_keys=False, allow_unicode=True)
            
            print(f"Successfully updated PROJECT_CONTEXT.yaml with {len(self.changes)} changes:")
            for change in self.changes:
                print(f"  - {change}")
            return True
            
        except Exception as e:
            print(f"Error saving context: {e}")
            return False
    
    def get_diff(self) -> Dict[str, Any]:
        """Get differences between existing and updated data"""
        if not self.updated_data:
            return {}
            
        diff = {}
        # This is a simplified diff - could be enhanced with deep comparison
        for key in self.updated_data:
            if key not in self.existing_data:
                diff[key] = {'status': 'added', 'value': self.updated_data[key]}
            elif self.existing_data[key] != self.updated_data[key]:
                diff[key] = {
                    'status': 'modified',
                    'old': self.existing_data[key],
                    'new': self.updated_data[key]
                }
        
        return diff

def main():
    """Example usage and testing"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    context_path = project_root / "_project" / "PROJECT_CONTEXT.yaml"
    
    updater = ContextUpdater(str(context_path))
    updater.load_existing()
    
    # Example: Add goals if missing
    goals = {
        'primary_objective': 'Enhance AI-assisted development with specialized agents',
        'success_metrics': [
            'Agent invocation accuracy > 95%',
            'Code quality scores > 8/10',
            'Developer productivity improvement > 30%',
            'Zero-configuration setup time < 1 minute'
        ],
        'constraints': [
            'Must work with Claude Code',
            'Maintain zero-configuration philosophy',
            'Ensure model-agnostic future compatibility',
            'Keep resource usage minimal'
        ],
        'milestones': [
            'Priority 1: Core validation system complete',
            'Priority 2: Multi-model support beta',
            'Priority 3: Enterprise features release'
        ],
        'non_goals': [
            'Replacing human developers',
            'Automated code generation without review',
            'Vendor lock-in to specific tools'
        ]
    }
    
    updater.update_goals(goals)
    
    # Example: Update repository current focus
    updater.add_current_focus('openadk', 'Implementing validation and incremental updates')
    
    # Save changes
    updater.save(dry_run=False)

if __name__ == "__main__":
    main()