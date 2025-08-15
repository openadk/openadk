#!/bin/bash

# OpenADK Repository Analysis System
# Performs comprehensive multi-dimensional analysis of repositories

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_DIR="_project/reports"
ARCHIVE_DIR="_project/archive"
ANALYSIS_FILE="${REPORT_DIR}/repository_analysis_${TIMESTAMP}.md"
YAML_FILE="${REPORT_DIR}/repository_analysis_${TIMESTAMP}.yaml"

# Ensure directories exist
mkdir -p "$REPORT_DIR" "$ARCHIVE_DIR"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[$(date +"%H:%M:%S")]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to get repository info
get_repo_info() {
    local repo_path="${1:-.}"
    local repo_name=$(basename "$(cd "$repo_path" && pwd)")
    
    # Get git info if available
    local branch="N/A"
    local last_commit="N/A"
    local uncommitted_changes="No"
    
    if [[ -d "${repo_path}/.git" ]]; then
        branch=$(cd "$repo_path" && git branch --show-current 2>/dev/null || echo "N/A")
        last_commit=$(cd "$repo_path" && git log -1 --format="%h - %s" 2>/dev/null || echo "N/A")
        if [[ -n $(cd "$repo_path" && git status --porcelain 2>/dev/null) ]]; then
            uncommitted_changes="Yes"
        fi
    fi
    
    echo "Repository: $repo_name"
    echo "Path: $(cd "$repo_path" && pwd)"
    echo "Branch: $branch"
    echo "Last Commit: $last_commit"
    echo "Uncommitted Changes: $uncommitted_changes"
}

# Function to detect technology stack
detect_tech_stack() {
    local repo_path="${1:-.}"
    local tech_stack=""
    
    # Check for various technology indicators
    [[ -f "${repo_path}/package.json" ]] && tech_stack="${tech_stack}Node.js/JavaScript "
    [[ -f "${repo_path}/requirements.txt" || -f "${repo_path}/setup.py" || -f "${repo_path}/pyproject.toml" ]] && tech_stack="${tech_stack}Python "
    [[ -f "${repo_path}/go.mod" ]] && tech_stack="${tech_stack}Go "
    [[ -f "${repo_path}/Cargo.toml" ]] && tech_stack="${tech_stack}Rust "
    [[ -f "${repo_path}/pom.xml" || -f "${repo_path}/build.gradle" ]] && tech_stack="${tech_stack}Java "
    [[ -f "${repo_path}/composer.json" ]] && tech_stack="${tech_stack}PHP "
    [[ -f "${repo_path}/Gemfile" ]] && tech_stack="${tech_stack}Ruby "
    [[ -f "${repo_path}/.csproj" || -f "${repo_path}/.sln" ]] && tech_stack="${tech_stack}C#/.NET "
    [[ -f "${repo_path}/Dockerfile" ]] && tech_stack="${tech_stack}Docker "
    [[ -f "${repo_path}/docker-compose.yml" || -f "${repo_path}/docker-compose.yaml" ]] && tech_stack="${tech_stack}Docker-Compose "
    [[ -d "${repo_path}/.github/workflows" ]] && tech_stack="${tech_stack}GitHub-Actions "
    [[ -f "${repo_path}/.gitlab-ci.yml" ]] && tech_stack="${tech_stack}GitLab-CI "
    [[ -f "${repo_path}/Jenkinsfile" ]] && tech_stack="${tech_stack}Jenkins "
    
    echo "${tech_stack:-Unknown}"
}

# Function to count files and lines
get_repo_metrics() {
    local repo_path="${1:-.}"
    
    # Count files (excluding common non-code directories)
    local file_count=$(find "$repo_path" -type f \
        -not -path "*/\.*" \
        -not -path "*/node_modules/*" \
        -not -path "*/venv/*" \
        -not -path "*/vendor/*" \
        -not -path "*/target/*" \
        -not -path "*/dist/*" \
        -not -path "*/build/*" \
        -not -path "*/out/*" \
        2>/dev/null | wc -l)
    
    # Count total lines (rough estimate, excluding binaries)
    local total_lines=$(find "$repo_path" -type f \
        -not -path "*/\.*" \
        -not -path "*/node_modules/*" \
        -not -path "*/venv/*" \
        -not -path "*/vendor/*" \
        -not -path "*/target/*" \
        -not -path "*/dist/*" \
        -not -path "*/build/*" \
        -not -path "*/out/*" \
        \( -name "*.js" -o -name "*.ts" -o -name "*.py" -o -name "*.go" \
           -o -name "*.java" -o -name "*.c" -o -name "*.cpp" -o -name "*.rs" \
           -o -name "*.php" -o -name "*.rb" -o -name "*.sh" -o -name "*.md" \
           -o -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o -name "*.xml" \) \
        -exec wc -l {} + 2>/dev/null | tail -n 1 | awk '{print $1}')
    
    echo "Files: $file_count"
    echo "Lines of Code (approx): ${total_lines:-0}"
}

# Initialize analysis
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}       OpenADK Repository Analysis System v1.0${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo

# Start analysis timer
START_TIME=$(date +%s)

# Determine repositories to analyze
if [[ $# -eq 0 ]]; then
    # No arguments, analyze current directory
    REPOS=(.)
    print_status "Analyzing current repository..."
else
    # Analyze specified repositories
    REPOS=("$@")
    print_status "Analyzing ${#REPOS[@]} specified repository(ies)..."
fi

# Create analysis report header
cat > "$ANALYSIS_FILE" << EOF
# Repository Analysis Report

**Generated**: $(date "+%Y-%m-%d %H:%M:%S")  
**Analysis Tool**: OpenADK Repository Analysis System v1.0

---

## Executive Summary

This comprehensive analysis evaluates repository health across 8 critical dimensions:
- **Maintainability**: Code quality, organization, and technical debt
- **Scalability**: Architecture patterns and growth capacity
- **Reliability**: Error handling and system stability
- **Security**: Vulnerability assessment and secure practices
- **Performance**: Optimization opportunities and bottlenecks
- **Testability**: Test coverage and quality assurance
- **Documentation**: Knowledge sharing and onboarding
- **Operational Readiness**: Deployment and monitoring capabilities

---

## Repository Overview

EOF

# Create YAML report header
cat > "$YAML_FILE" << EOF
# OpenADK Repository Analysis Report
metadata:
  timestamp: "$(date -Iseconds)"
  version: "1.0"
  analysis_tool: "OpenADK Repository Analysis System"

repositories:
EOF

# Analyze each repository
for repo in "${REPOS[@]}"; do
    if [[ ! -d "$repo" ]]; then
        print_error "Directory not found: $repo"
        continue
    fi
    
    repo_name=$(basename "$(cd "$repo" && pwd)")
    print_status "Analyzing repository: ${CYAN}$repo_name${NC}"
    
    # Gather basic repository information
    echo -e "\n### Repository: $repo_name\n" >> "$ANALYSIS_FILE"
    echo -e "\`\`\`" >> "$ANALYSIS_FILE"
    get_repo_info "$repo" >> "$ANALYSIS_FILE"
    echo -e "Technology Stack: $(detect_tech_stack "$repo")" >> "$ANALYSIS_FILE"
    get_repo_metrics "$repo" >> "$ANALYSIS_FILE"
    echo -e "\`\`\`\n" >> "$ANALYSIS_FILE"
    
    # Add to YAML
    echo "  - name: \"$repo_name\"" >> "$YAML_FILE"
    echo "    path: \"$(cd "$repo" && pwd)\"" >> "$YAML_FILE"
    echo "    technology_stack: \"$(detect_tech_stack "$repo")\"" >> "$YAML_FILE"
    
    print_success "Basic analysis complete for $repo_name"
done

# Placeholder for agent-based analysis results
cat >> "$ANALYSIS_FILE" << 'EOF'

---

## Dimensional Analysis

### 🔧 Maintainability
**Score**: Pending agent analysis  
**Status**: Requires code-reviewer and system-architect agents

Key areas to evaluate:
- Code complexity and organization
- Naming conventions and consistency
- Code duplication
- Technical debt indicators

### 📈 Scalability  
**Score**: Pending agent analysis  
**Status**: Requires system-architect and devops-engineer agents

Key areas to evaluate:
- Architecture patterns
- Database design
- Caching strategies
- Load handling capacity

### 🛡️ Reliability
**Score**: Pending agent analysis  
**Status**: Requires test-engineer and devops-engineer agents

Key areas to evaluate:
- Error handling patterns
- Fault tolerance mechanisms
- Recovery procedures
- System monitoring

### 🔒 Security
**Score**: Pending agent analysis  
**Status**: Requires security-expert agent

Key areas to evaluate:
- Vulnerability assessment
- Authentication/authorization
- Data protection
- Security best practices

### ⚡ Performance
**Score**: Pending agent analysis  
**Status**: Requires code-reviewer and system-architect agents

Key areas to evaluate:
- Algorithm efficiency
- Database query optimization
- Resource usage
- Caching implementation

### 🧪 Testability
**Score**: Pending agent analysis  
**Status**: Requires test-engineer agent

Key areas to evaluate:
- Test coverage
- Test quality
- Testing patterns
- CI/CD integration

### 📚 Documentation
**Score**: Pending agent analysis  
**Status**: Requires code-reviewer agent

Key areas to evaluate:
- README completeness
- Code comments
- API documentation
- Architecture docs

### 🚀 Operational Readiness
**Score**: Pending agent analysis  
**Status**: Requires devops-engineer agent

Key areas to evaluate:
- Deployment automation
- Monitoring setup
- Logging practices
- Incident response

---

## Recommendations

### Immediate Actions
*Agent analysis required to generate specific recommendations*

### Short-term Improvements
*Agent analysis required to generate specific recommendations*

### Long-term Strategic Items
*Agent analysis required to generate specific recommendations*

---

## Next Steps

To complete the comprehensive analysis:

1. **Run specialized agent analysis**:
   ```bash
   # This will invoke OpenADK agents for deep analysis
   claude analyze --agents all
   ```

2. **Review critical findings** in the detailed report

3. **Prioritize improvements** based on your team's capacity

4. **Track progress** with regular re-analysis

---

## Analysis Metadata

EOF

# Calculate analysis duration
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Add metadata to report
cat >> "$ANALYSIS_FILE" << EOF
- **Analysis Duration**: ${DURATION} seconds
- **Timestamp**: $(date -Iseconds)
- **Report Location**: $ANALYSIS_FILE
- **YAML Data**: $YAML_FILE

---

*This report provides a foundation for comprehensive repository analysis. The full power of OpenADK's specialized agents can provide deeper insights into each dimension.*
EOF

# Complete YAML report
cat >> "$YAML_FILE" << EOF

analysis_summary:
  duration_seconds: $DURATION
  dimensions_analyzed:
    - name: "Maintainability"
      status: "Pending agent analysis"
    - name: "Scalability"
      status: "Pending agent analysis"
    - name: "Reliability"
      status: "Pending agent analysis"
    - name: "Security"
      status: "Pending agent analysis"
    - name: "Performance"
      status: "Pending agent analysis"
    - name: "Testability"
      status: "Pending agent analysis"
    - name: "Documentation"
      status: "Pending agent analysis"
    - name: "Operational Readiness"
      status: "Pending agent analysis"
EOF

# Print summary
echo
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}           Analysis Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo
print_success "Basic repository analysis completed in ${DURATION} seconds"
print_success "Markdown report: ${CYAN}$ANALYSIS_FILE${NC}"
print_success "YAML data: ${CYAN}$YAML_FILE${NC}"
echo
print_warning "Note: For deep analysis with OpenADK agents, run:"
echo -e "  ${CYAN}claude analyze --agents all${NC}"
echo
echo "To view the report:"
echo -e "  ${CYAN}cat $ANALYSIS_FILE${NC}"