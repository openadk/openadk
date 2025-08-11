# Contributing to OpenADK

First off, thank you for considering contributing to OpenADK! It's people like you that make OpenADK such a great tool for enhancing Claude Code with specialized AI agents.

## Code of Conduct

This project and everyone participating in it is governed by the [OpenADK Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title** for the issue to identify the problem
* **Describe the exact steps which reproduce the problem** in as many details as possible
* **Provide specific examples to demonstrate the steps** (include links to files or GitHub projects, or copy/pasteable snippets)
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior
* **Explain which behavior you expected to see instead and why**
* **Include details about your configuration and environment**:
  * Which version of Claude Code are you using?
  * What's the name and version of the OS you're using?
  * Which repositories are you working with?

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title** for the issue to identify the suggestion
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible
* **Provide specific examples to demonstrate the steps** or provide mockups/diagrams
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why
* **Explain why this enhancement would be useful** to most OpenADK users

### Creating New Agents

OpenADK thrives on specialized agents! To contribute a new agent:

1. **Identify a clear use case** - What specific task will this agent excel at?
2. **Define the agent's expertise** - What makes this agent unique?
3. **Document usage patterns** - When should developers use this agent?
4. **Provide examples** - Show real-world scenarios where the agent adds value

Agent contributions should include:
* Agent definition in the appropriate configuration file
* Clear documentation of the agent's capabilities
* Example usage scenarios
* Integration with existing agent workflows

### Pull Requests

The process described here has several goals:
- Maintain OpenADK's quality
- Fix problems that are important to users
- Engage the community in working toward the best possible OpenADK
- Enable a sustainable system for OpenADK's maintainers to review contributions

Please follow these steps:

1. **Fork the repo and create your branch from `main`**
2. **If you've added code that should be tested, add tests**
3. **If you've added or modified agents, update the documentation**
4. **Ensure the test suite passes** (if applicable)
5. **Make sure your code follows the existing style**
6. **Issue that pull request!**

#### Pull Request Guidelines

* Fill in the required template
* Do not include issue numbers in the PR title
* Include screenshots and animated GIFs in your pull request whenever possible
* Follow the style guides
* Document new code
* End all files with a newline

## Development Process

### Model-Agnostic Architecture

While OpenADK currently focuses on Claude Code, we're building toward a **model-agnostic future** that will support multiple AI CLIs (Codex, Gemini, etc.). When contributing:

1. **Avoid Model-Specific Features** - Design agents and workflows that can work with any LLM
2. **Abstract Model Differences** - Use configuration layers to handle model-specific adaptations
3. **Document Claude Dependencies** - Clearly note any features that are Claude-specific
4. **Consider Portability** - Think about how your contribution would work with other AI assistants
5. **Test with Future in Mind** - Consider how features would adapt to different models

### Working with Multiple Repositories

OpenADK is designed to work across multiple repositories. When developing:

1. **Test multi-repository scenarios** - Ensure your changes work with various project structures
2. **Consider cross-repository impacts** - How do your changes affect multi-repo workflows?
3. **Maintain backward compatibility** - Don't break existing workflows

### Agent Development Guidelines

When creating or modifying agents:

1. **Single Responsibility** - Each agent should have one clear area of expertise
2. **Composability** - Agents should work well together in workflows
3. **Clear Communication** - Agent outputs should be actionable and clear
4. **Error Handling** - Agents should gracefully handle edge cases
5. **Performance** - Consider token usage and response times
6. **Model Agnostic** - Write prompts that work across different LLMs, avoiding model-specific syntax

### Testing

* Write tests for any new agents or workflows
* Test multi-repository scenarios
* Verify agent interactions work as expected
* Check for edge cases and error conditions

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
    * 🎨 `:art:` when improving the format/structure of the code
    * 🚀 `:rocket:` when adding new agents or features
    * 📝 `:memo:` when writing docs
    * 🐛 `:bug:` when fixing a bug
    * 🔥 `:fire:` when removing code or files
    * 💚 `:green_heart:` when fixing CI build
    * ✅ `:white_check_mark:` when adding tests
    * 🔒 `:lock:` when dealing with security
    * ⬆️ `:arrow_up:` when upgrading dependencies
    * ⬇️ `:arrow_down:` when downgrading dependencies

### Documentation Styleguide

* Use [Markdown](https://guides.github.com/features/mastering-markdown/)
* Reference agents using backticks: `system-architect`
* Include code examples when possible
* Keep line length to 80 characters when possible
* Use clear, concise language

### Code Styleguide

* Follow the existing code style in the repository
* Comment complex logic
* Keep functions focused and small
* Use descriptive variable and function names
* Write self-documenting code where possible

## Community

### Getting Help

* Check the [documentation](README.md)
* Search existing issues
* Join community discussions in GitHub Discussions
* Ask questions in issues with the "question" label

### Recognition

Contributors who make significant improvements will be recognized in:
* The project README
* Release notes
* Special contributors section (if established)

## Questions?

Feel free to open an issue with the tag "question" if you have any questions about contributing!

Thank you for contributing to OpenADK! 🚀