#!/bin/bash

# OpenADK Validation System
# Validates agent templates and PROJECT_CONTEXT.yaml against defined schemas

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
AGENTS_DIR="$PROJECT_ROOT/.claude/agents"
PROJECT_CONTEXT="$PROJECT_ROOT/_project/PROJECT_CONTEXT.yaml"
SCHEMAS_FILE="$SCRIPT_DIR/schemas.yaml"

# Validation results
VALIDATION_PASSED=true
ERRORS=()
WARNINGS=()

# Function to print colored output
print_error() {
    echo -e "${RED}✗${NC} $1"
    ERRORS+=("$1")
    VALIDATION_PASSED=false
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
    WARNINGS+=("$1")
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Function to validate agent template
validate_agent_template() {
    local agent_file="$1"
    local agent_name="$(basename "$agent_file" .md)"
    
    print_info "Validating agent: $agent_name"
    
    # Check if file exists
    if [[ ! -f "$agent_file" ]]; then
        print_error "Agent file not found: $agent_file"
        return 1
    fi
    
    # Extract frontmatter
    local frontmatter=$(sed -n '/^---$/,/^---$/p' "$agent_file" | sed '1d;$d')
    
    if [[ -z "$frontmatter" ]]; then
        print_error "No frontmatter found in $agent_name"
        return 1
    fi
    
    # Check required fields
    local has_name=$(echo "$frontmatter" | grep -c "^name:" || true)
    local has_description=$(echo "$frontmatter" | grep -c "^description:" || true)
    local has_model=$(echo "$frontmatter" | grep -c "^model:" || true)
    local has_color=$(echo "$frontmatter" | grep -c "^color:" || true)
    
    if [[ $has_name -eq 0 ]]; then
        print_error "$agent_name: Missing 'name' field in frontmatter"
    fi
    
    if [[ $has_description -eq 0 ]]; then
        print_error "$agent_name: Missing 'description' field in frontmatter"
    fi
    
    if [[ $has_model -eq 0 ]]; then
        print_error "$agent_name: Missing 'model' field in frontmatter"
    fi
    
    if [[ $has_color -eq 0 ]]; then
        print_error "$agent_name: Missing 'color' field in frontmatter"
    fi
    
    # Validate model value
    local model=$(echo "$frontmatter" | grep "^model:" | cut -d: -f2 | tr -d ' ')
    if [[ -n "$model" ]] && [[ "$model" != "sonnet" ]] && [[ "$model" != "opus" ]] && [[ "$model" != "haiku" ]]; then
        print_error "$agent_name: Invalid model '$model'. Must be: sonnet, opus, or haiku"
    fi
    
    # Check description contains required text
    local description=$(echo "$frontmatter" | grep "^description:" | cut -d: -f2-)
    if [[ -n "$description" ]]; then
        if ! echo "$description" | grep -q "Use this agent"; then
            print_warning "$agent_name: Description should contain 'Use this agent'"
        fi
        if ! echo "$description" | grep -q "Examples:"; then
            print_warning "$agent_name: Description should contain 'Examples:'"
        fi
    fi
    
    # Check content length
    local content_length=$(wc -l < "$agent_file")
    if [[ $content_length -lt 20 ]]; then
        print_warning "$agent_name: Agent content seems too short (less than 20 lines)"
    fi
    
    print_success "$agent_name validated"
}

# Function to validate PROJECT_CONTEXT.yaml
validate_project_context() {
    print_info "Validating PROJECT_CONTEXT.yaml"
    
    if [[ ! -f "$PROJECT_CONTEXT" ]]; then
        print_warning "PROJECT_CONTEXT.yaml not found (will be created on initialization)"
        return 0
    fi
    
    # Check YAML syntax
    if ! python -c "import yaml; yaml.safe_load(open('$PROJECT_CONTEXT'))" 2>/dev/null; then
        print_error "PROJECT_CONTEXT.yaml has invalid YAML syntax"
        return 1
    fi
    
    # Check required sections using Python
    python <<EOF
import yaml
import sys

with open('$PROJECT_CONTEXT', 'r') as f:
    data = yaml.safe_load(f)

required_sections = ['project', 'repositories', 'conventions', 'development_guidelines', 'quick_reference']
missing_sections = []

for section in required_sections:
    if section not in data:
        missing_sections.append(section)

if missing_sections:
    print(f"MISSING:{','.join(missing_sections)}")
    sys.exit(1)

# Check project section
project = data.get('project', {})
required_project_fields = ['name', 'type', 'description', 'initialized_at']
missing_project_fields = []

for field in required_project_fields:
    if field not in project:
        missing_project_fields.append(field)

if missing_project_fields:
    print(f"PROJECT_MISSING:{','.join(missing_project_fields)}")
    sys.exit(1)

# Check for goals (new requirement)
if 'goals' not in project:
    print("NO_GOALS")

# Validate type field
valid_types = ['single-repository', 'single-repository-focus', 'multi-repository', 'monorepo']
if project.get('type') not in valid_types:
    print(f"INVALID_TYPE:{project.get('type')}")

print("OK")
EOF

    local result=$?
    local output=$(python <<EOF 2>/dev/null
import yaml
import sys

with open('$PROJECT_CONTEXT', 'r') as f:
    data = yaml.safe_load(f)

required_sections = ['project', 'repositories', 'conventions', 'development_guidelines', 'quick_reference']
missing_sections = []

for section in required_sections:
    if section not in data:
        missing_sections.append(section)

if missing_sections:
    print(f"MISSING:{','.join(missing_sections)}")
    sys.exit(0)

# Check project section
project = data.get('project', {})
required_project_fields = ['name', 'type', 'description', 'initialized_at']
missing_project_fields = []

for field in required_project_fields:
    if field not in project:
        missing_project_fields.append(field)

if missing_project_fields:
    print(f"PROJECT_MISSING:{','.join(missing_project_fields)}")
    sys.exit(0)

# Check for goals (new requirement)
if 'goals' not in project:
    print("NO_GOALS")
    sys.exit(0)

# Validate type field
valid_types = ['single-repository', 'single-repository-focus', 'multi-repository', 'monorepo']
if project.get('type') not in valid_types:
    print(f"INVALID_TYPE:{project.get('type')}")
    sys.exit(0)

print("OK")
EOF
)
    
    if [[ "$output" == "OK" ]]; then
        print_success "PROJECT_CONTEXT.yaml structure is valid"
    elif [[ "$output" == "NO_GOALS" ]]; then
        print_warning "PROJECT_CONTEXT.yaml missing 'goals' section (required for goal alignment)"
    elif [[ "$output" == MISSING:* ]]; then
        local missing=$(echo "$output" | cut -d: -f2)
        print_error "PROJECT_CONTEXT.yaml missing sections: $missing"
    elif [[ "$output" == PROJECT_MISSING:* ]]; then
        local missing=$(echo "$output" | cut -d: -f2)
        print_error "PROJECT_CONTEXT.yaml project section missing fields: $missing"
    elif [[ "$output" == INVALID_TYPE:* ]]; then
        local type=$(echo "$output" | cut -d: -f2)
        print_error "PROJECT_CONTEXT.yaml has invalid type: $type"
    fi
}

# Function to check for duplicate agent names
check_duplicate_agents() {
    print_info "Checking for duplicate agent names"
    
    local agent_names=()
    for agent_file in "$AGENTS_DIR"/*.md; do
        if [[ -f "$agent_file" ]]; then
            local name=$(sed -n '/^name:/p' "$agent_file" | head -1 | cut -d: -f2 | tr -d ' ')
            if [[ -n "$name" ]]; then
                agent_names+=("$name")
            fi
        fi
    done
    
    # Check for duplicates
    local duplicates=$(printf '%s\n' "${agent_names[@]}" | sort | uniq -d)
    if [[ -n "$duplicates" ]]; then
        print_error "Duplicate agent names found: $duplicates"
    else
        print_success "No duplicate agent names"
    fi
}

# Main validation process
main() {
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}           OpenADK Validation System v1.0${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo
    
    # Validate all agent templates
    if [[ -d "$AGENTS_DIR" ]]; then
        for agent_file in "$AGENTS_DIR"/*.md; do
            if [[ -f "$agent_file" ]]; then
                validate_agent_template "$agent_file"
            fi
        done
        check_duplicate_agents
    else
        print_warning "Agents directory not found: $AGENTS_DIR"
    fi
    
    echo
    
    # Validate PROJECT_CONTEXT.yaml
    validate_project_context
    
    echo
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    
    # Summary
    if [[ $VALIDATION_PASSED == true ]] && [[ ${#WARNINGS[@]} -eq 0 ]]; then
        echo -e "${GREEN}           Validation Passed Successfully!${NC}"
    elif [[ $VALIDATION_PASSED == true ]]; then
        echo -e "${YELLOW}      Validation Passed with Warnings${NC}"
        echo
        echo "Warnings (${#WARNINGS[@]}):"
        for warning in "${WARNINGS[@]}"; do
            echo "  - $warning"
        done
    else
        echo -e "${RED}           Validation Failed${NC}"
        echo
        if [[ ${#ERRORS[@]} -gt 0 ]]; then
            echo "Errors (${#ERRORS[@]}):"
            for error in "${ERRORS[@]}"; do
                echo "  - $error"
            done
        fi
        if [[ ${#WARNINGS[@]} -gt 0 ]]; then
            echo
            echo "Warnings (${#WARNINGS[@]}):"
            for warning in "${WARNINGS[@]}"; do
                echo "  - $warning"
            done
        fi
        exit 1
    fi
    
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
}

# Run main function
main "$@"