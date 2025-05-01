# PyBoost Documentation

Welcome to the PyBoost documentation. PyBoost is a comprehensive toolkit for cleaning, optimizing, and improving Python code.

## Overview

PyBoost integrates multiple tools into a single, easy-to-use package:

1. **pybackup** - Create backups of Python files with timestamps
2. **rmcm** - Remove comments and docstrings (optional)
3. **autoflake** - Remove unused imports and variables
4. **pyupgrade** - Upgrade to modern Python syntax
5. **isort** - Sort imports
6. **black** - Format code
7. **ruff** - Lint and check for errors
8. **mypy** - Static type checking (optional)
9. **bandit** - Security checks (optional)
10. **vulture** - Find dead code (optional)

## Contents

- [Installation](installation.md)
- [Usage](usage.md)
- [Contributing](contributing.md)

## Quick Start

```bash
# Install PyBoost
pip install pyboost

# Process a Python project
pyboost /path/to/your/python/project

# List available tools
pyboost --list-tools

# Use aggressive mode (includes comment removal)
pyboost /path/to/your/python/project --aggressive

# Only create backups
pyboost /path/to/your/python/project --backup-only
```
