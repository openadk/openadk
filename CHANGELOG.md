# Changelog

All notable changes to OpenADK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2024-08-11

### Added
- Initial release of OpenADK
- Core agent definitions for software development lifecycle
  - `system-architect` - Technology and architecture decisions
  - `project-manager` - Task breakdown and workflow management
  - `requirements-analyst` - Requirements gathering and refinement
  - `security-expert` - Security reviews and vulnerability detection
  - `test-engineer` - Test creation and coverage analysis
  - `code-reviewer` - Code quality and best practices review
  - `devops-engineer` - Infrastructure and CI/CD concerns
  - `software-developer` - Code implementation and development
- Multi-repository discovery and management
- Dynamic repository detection with `start` command
- Repository-specific scoping with `start [repo1] [repo2]`
- CLAUDE.md for Claude Code integration
- Pre-commit hook configuration for automated reviews
- MIT License
- Security policy documentation (SECURITY.md)
- Contributing guidelines (CONTRIBUTING.md)
- Comprehensive .gitignore file
- Version history tracking (CHANGELOG.md)

### Features
- Zero-configuration setup
- Automatic repository discovery in parent directory
- Project-agnostic design works with any technology stack
- Seamless agent collaboration for complex workflows
- Open source implementation with no vendor lock-in

### Documentation
- Comprehensive README with quick start guide
- CLAUDE.md with detailed Claude Code instructions
- Agent usage examples and best practices
- Multi-repository workflow documentation
- Security best practices and vulnerability reporting process
- Contribution guidelines and development workflow
- Clear versioning strategy and change tracking

## Version History

### Versioning Strategy
- **Major** (X.0.0): Breaking changes to agent APIs or core functionality
- **Minor** (0.X.0): New agents, features, or significant enhancements
- **Patch** (0.0.X): Bug fixes, documentation updates, minor improvements

---

For detailed commit history, see the [git log](https://github.com/yourusername/openadk/commits/main).

[Unreleased]: https://github.com/yourusername/openadk/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/openadk/releases/tag/v0.1.0