# PyBoost - Ultimate Python Code Maintenance Toolkit

[![PyPI version](https://img.shields.io/pypi/v/pyboost-toolkit.svg)](https://pypi.org/project/pyboost-toolkit/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyboost-toolkit.svg)](https://pypi.org/project/pyboost-toolkit/)
[![License](https://img.shields.io/github/license/AlexandrosLiaskos/pyboost.svg)](https://github.com/AlexandrosLiaskos/pyboost/blob/main/LICENSE)

PyBoost is a comprehensive toolkit for cleaning, optimizing, and improving Python code. It integrates multiple tools into a single, easy-to-use package.

## Features

PyBoost combines the following tools:

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

## Installation

The package is available on [PyPI](https://pypi.org/project/pyboost-toolkit/) as `pyboost-toolkit`.

> **Note:** While the package name is `pyboost-toolkit`, the command-line tools are still named `pyboost`, `pybackup`, etc.

### Basic Installation

```bash
pip install pyboost-toolkit
```

### Full Installation (with all optional tools)

```bash
pip install pyboost-toolkit[all]
```

### Development Installation

```bash
pip install pyboost-toolkit[dev]
```

## Usage

### Basic Usage

```bash
pyboost /path/to/your/python/project
```

### Options

```
usage: pyboost [-h] [--no-bak] [--backup-dir BACKUP_DIR] [--skip SKIP]
               [--aggressive] [--backup-only] [--list-tools] [--verbose]
               directory

Ultimate Python Code Maintenance Toolkit

positional arguments:
  directory             Directory containing Python files to process

options:
  -h, --help            show this help message and exit
  --no-bak              Skip creating backup files (backups are stored in the
                        codebase by default)
  --backup-dir BACKUP_DIR
                        Directory to store backups (default: <codebase>/backup)
  --skip SKIP           Comma-separated list of tools to skip (e.g.,
                        'rmcm,mypy,bandit')
  --aggressive          Enable aggressive mode (includes comment removal and
                        other potentially destructive operations)
  --backup-only         Only create backups, don't process files
  --list-tools          List all available tools and exit
  --verbose, -v         Enable verbose output
```

### Examples

#### Basic Usage

```bash
pyboost ~/projects/my_python_project
```

#### Skip Optional Tools

```bash
pyboost ~/projects/my_python_project --skip=mypy,bandit,vulture
```

#### Aggressive Mode (includes comment removal)

```bash
pyboost ~/projects/my_python_project --aggressive
```

#### Backup Only

```bash
pyboost ~/projects/my_python_project --backup-only
```

#### Custom Backup Directory

```bash
pyboost ~/projects/my_python_project --backup-dir ~/backups/python_projects
```

## Individual Tools

PyBoost also provides access to individual tools:

### PyBackup

Create backups of Python files with timestamps.

```bash
pybackup /path/to/your/python/project
```

### PyRMCM (Remove Comments)

Remove comments and docstrings from Python files.

```bash
pyrmcm input_file.py output_file.py
```

### PyFormat

Format Python files by removing comments and applying Black.

```bash
pyformat /path/to/your/python/project
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository from [GitHub](https://github.com/AlexandrosLiaskos/pyboost)
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
