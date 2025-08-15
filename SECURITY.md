# Security Policy

## Supported Versions

OpenADK is currently in active development. We provide security updates for:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |
| < main  | :x:                |

## Reporting a Vulnerability

The OpenADK team takes the security of our software seriously. If you believe you have found a security vulnerability in OpenADK, please report it to us as described below.

### Please do NOT:

* Open a public issue
* Disclose the vulnerability publicly before it has been addressed

### Please DO:

* Email the maintainers directly with details
* Allow reasonable time for the vulnerability to be fixed before public disclosure
* Provide sufficient information to reproduce the issue

### What to include in your report:

* Type of issue (e.g., agent manipulation, prompt injection, data exposure)
* Full paths of source file(s) related to the issue
* Location of the affected source code (tag/branch/commit or direct URL)
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit it

### What to expect:

* Priority acknowledgment of your report
* Swift assessment of the issue and resolution planning
* Regular updates on the progress of fixing the vulnerability
* Credit in the release notes (unless you prefer to remain anonymous)

## Security Best Practices for Users

When using OpenADK with Claude Code:

### 1. Repository Access
* Only use OpenADK with repositories you trust
* Review agent actions before allowing them to proceed
* Be cautious when working with repositories containing sensitive data

### 2. Environment Variables
* Never commit `.env` files or credentials to version control
* Use proper secret management for API keys and tokens
* Review the `.gitignore` file to ensure sensitive files are excluded

### 3. Agent Permissions
* Understand what each agent can do before invoking it
* Review generated code before committing
* Be especially careful with agents that can modify multiple files

### 4. Multi-Repository Operations
* Be aware that OpenADK can discover and work with sibling repositories
* Ensure you intend to work with all discovered repositories
* Use the `start [specific-repo]` command to limit scope when needed

### 5. Code Review
* Always review agent-generated code before deployment
* Use the `code-reviewer` and `security-expert` agents for additional validation
* Enable pre-commit hooks for automatic security checks

## Security Features

OpenADK includes several security-focused features:

1. **Security Expert Agent**: Specialized agent for identifying vulnerabilities
2. **Code Review Agent**: Automatic code quality and security checks
3. **Pre-commit Integration**: Hooks for security validation before commits
4. **Scoped Operations**: Ability to limit operations to specific repositories

## Known Security Considerations

### Agent Interactions
* Agents operate with the same permissions as Claude Code
* Multiple agents can interact, potentially amplifying actions
* Always review agent suggestions before implementation

### Multi-Repository Access
* OpenADK can discover and access sibling repositories
* Ensure your directory structure doesn't expose unintended repositories
* Use repository-specific start commands when working with sensitive projects

### Data Handling
* Agents may process code and data from your repositories
* Sensitive data in code could be included in agent context
* Consider data classification before using agents on sensitive codebases

## Compliance

OpenADK itself does not store or transmit data. However, when using with Claude Code:

* Follow your organization's AI usage policies
* Ensure compliance with data residency requirements
* Review Claude's data handling practices
* Consider enterprise agreements for sensitive workloads

## Updates and Patches

* Security updates are released as soon as possible after discovery
* Check the [CHANGELOG](CHANGELOG.md) for security-related updates
* We recommend always using the latest version from the main branch
* Enable GitHub notifications to receive security alerts

## Contact

For security concerns, please contact the maintainers through:
* GitHub Security Advisories (preferred for GitHub users)
* Direct message to repository maintainers
* Email (if provided in repository information)

## Acknowledgments

We thank the security researchers and users who responsibly disclose vulnerabilities and help make OpenADK more secure.

---

*This security policy is adapted from best practices recommended by the Open Source Security Foundation (OpenSSF).*