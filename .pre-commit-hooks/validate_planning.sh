#!/bin/bash
# Pre-commit hook to validate planning compliance in staged files

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Running planning compliance validation..."

# Get list of staged markdown and yaml files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(md|yaml|yml)$' || true)

if [ -z "$STAGED_FILES" ]; then
    echo -e "${GREEN}✓${NC} No markdown or YAML files to validate"
    exit 0
fi

VALIDATION_FAILED=false

for file in $STAGED_FILES; do
    # Skip certain files that are allowed to have examples
    if [[ "$file" == "AGENT_GUIDELINES.md" ]] || [[ "$file" == *"example"* ]]; then
        continue
    fi
    
    # Run Python validation
    if python validation/check_time_estimates.py "$file" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} $file"
    else
        echo -e "${RED}✗${NC} $file contains time-based estimates"
        VALIDATION_FAILED=true
        
        # Show specific violations
        python validation/check_time_estimates.py "$file" 2>&1 | grep "Line" | head -5
    fi
done

if [ "$VALIDATION_FAILED" = true ]; then
    echo
    echo -e "${RED}Planning validation failed!${NC}"
    echo "Please replace time-based estimates with:"
    echo "  - Priority levels (Critical, High, Medium, Low)"
    echo "  - Complexity ratings (Simple, Moderate, Complex)"
    echo "  - Relative sizing (Small, Medium, Large)"
    echo
    echo "Run 'python validation/check_time_estimates.py <file>' for details"
    exit 1
fi

echo -e "${GREEN}✓${NC} All files pass planning compliance validation"
exit 0