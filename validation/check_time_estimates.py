#!/usr/bin/env python
"""
OpenADK Time Estimate Checker
Validates that documents don't contain time-based estimates
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple

class TimeEstimateChecker:
    def __init__(self):
        # Patterns that indicate time-based estimates
        self.time_patterns = [
            r'\b\d+\s*(day|days|week|weeks|month|months|year|years|hour|hours|minute|minutes)\b',
            r'\b(one|two|three|four|five|six|seven|eight|nine|ten)\s*(day|days|week|weeks|month|months|hour|hours)\b',
            r'\bQ[1-4]\s+20\d{2}\b',  # Q1 2025, etc.
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+20\d{2}\b',
            r'\b(Week|Month|Day)\s+\d+\b',  # Week 1, Month 2, etc.
            r'\b\d+\s*-\s*\d+\s*(days|weeks|months)\b',  # 2-3 days, 1-2 weeks
            r'\btimeline\s*:\s*\d+',  # timeline: 3
            r'\b(first|second|third)\s+(week|month|quarter)\b',
            r'\b(early|mid|late)\s+(January|February|March|April|May|June|July|August|September|October|November|December)\b',
            r'\bby\s+(end of|beginning of)\s+(week|month|quarter|year)\b',
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.time_patterns]
        
        # Exceptions - contexts where time references are acceptable
        self.exception_contexts = [
            r'copyright\s+\d{4}',  # Copyright years
            r'version\s+\d+\.\d+',  # Version numbers
            r'RFC\s+\d+',  # RFC references
            r'ISO\s+\d+',  # ISO standards
            r'port\s+\d+',  # Port numbers
            r'\d+\s*ms',  # Milliseconds (technical)
            r'\d+\s*seconds?\s+(timeout|delay|interval)',  # Technical timeouts
        ]
        
        self.exception_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.exception_contexts]
        
    def check_file(self, filepath: str) -> List[Tuple[int, str, str]]:
        """Check a file for time-based estimates
        
        Returns: List of (line_number, matched_text, context) tuples
        """
        violations = []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, 1):
                # Skip comments in code files
                if filepath.endswith(('.py', '.js', '.ts')) and line.strip().startswith(('#', '//', '/*')):
                    continue
                    
                # Check for violations
                for pattern in self.compiled_patterns:
                    matches = pattern.finditer(line)
                    for match in matches:
                        # Check if this match is an exception
                        is_exception = False
                        for exception in self.exception_patterns:
                            if exception.search(line):
                                is_exception = True
                                break
                        
                        if not is_exception:
                            violations.append((
                                line_num,
                                match.group(),
                                line.strip()
                            ))
                            
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            
        return violations
    
    def check_directory(self, directory: str, patterns: List[str] = None) -> dict:
        """Check all matching files in a directory
        
        Args:
            directory: Directory to check
            patterns: File patterns to check (default: markdown files)
            
        Returns: Dictionary of filepath -> violations
        """
        if patterns is None:
            patterns = ['*.md', '*.yaml', '*.yml']
            
        results = {}
        path = Path(directory)
        
        for pattern in patterns:
            for filepath in path.rglob(pattern):
                # Skip certain directories
                if any(skip in str(filepath) for skip in ['node_modules', '.git', 'venv', '__pycache__']):
                    continue
                    
                violations = self.check_file(str(filepath))
                if violations:
                    results[str(filepath)] = violations
                    
        return results
    
    def print_results(self, results: dict):
        """Print violations in a readable format"""
        if not results:
            print("SUCCESS: No time-based estimates found!")
            return
            
        print("WARNING: Time-based estimates detected:\n")
        
        total_violations = 0
        for filepath, violations in results.items():
            print(f"FILE: {filepath}")
            for line_num, matched, context in violations:
                print(f"   Line {line_num}: '{matched}'")
                print(f"   Context: {context[:100]}...")
            print()
            total_violations += len(violations)
            
        print(f"\nERROR: Total violations: {total_violations}")
        print("\nRECOMMENDATION: Replace time estimates with:")
        print("   - Priority levels (Critical, High, Medium, Low)")
        print("   - Complexity ratings (Simple, Moderate, Complex)")
        print("   - Relative sizing (Small, Medium, Large, XL)")
        print("   - Sequencing (Priority 1, Priority 2, Priority 3)")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Check for time-based estimates in documentation')
    parser.add_argument('path', nargs='?', default='.', help='Path to check (file or directory)')
    parser.add_argument('--patterns', nargs='+', default=['*.md', '*.yaml', '*.yml'],
                       help='File patterns to check')
    parser.add_argument('--fix', action='store_true', help='Suggest fixes for violations')
    
    args = parser.parse_args()
    
    checker = TimeEstimateChecker()
    
    path = Path(args.path)
    if path.is_file():
        violations = checker.check_file(str(path))
        if violations:
            results = {str(path): violations}
            checker.print_results(results)
            sys.exit(1)
        else:
            print(f"SUCCESS: {path} contains no time-based estimates")
            sys.exit(0)
    elif path.is_dir():
        results = checker.check_directory(str(path), args.patterns)
        checker.print_results(results)
        sys.exit(1 if results else 0)
    else:
        print(f"ERROR: Path not found: {path}")
        sys.exit(1)

if __name__ == "__main__":
    main()