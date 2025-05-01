# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-05-02

### Added
- Initial release of PyBoost
- Integrated PyBackup for creating backups of Python files
- Integrated RMCM for removing comments and docstrings
- Support for multiple external tools:
  - autoflake for removing unused imports and variables
  - pyupgrade for upgrading to modern Python syntax
  - isort for sorting imports
  - black for formatting code
  - ruff for linting and fixing code
  - mypy for static type checking
  - bandit for security checks
  - vulture for finding dead code
- Command-line interface with multiple options
- Documentation and tests
