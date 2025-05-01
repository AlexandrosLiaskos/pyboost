# Usage

PyBoost provides several command-line tools for maintaining Python code.

## PyBoost

The main `pyboost` command applies multiple tools to clean, optimize, and improve Python code.

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

## PyBackup

The `pybackup` command creates backups of Python files with timestamps.

### Basic Usage

```bash
pybackup /path/to/your/python/project
```

### Options

```
usage: pybackup [-h] [--backup-dir BACKUP_DIR] [--no-backup] [--verbose]
                [--log-file LOG_FILE] [--extensions EXTENSIONS]
                [--exclude EXCLUDE]
                codebase_root

Python File Backup Utility

positional arguments:
  codebase_root         Root directory of the codebase to backup

options:
  -h, --help            show this help message and exit
  --backup-dir BACKUP_DIR
                        Directory to store backups (default:
                        <codebase_root>/backup)
  --no-backup           Don't create backups (dry run)
  --verbose, -v         Enable verbose output
  --log-file LOG_FILE   Path to log file (default:
                        <codebase_root>/logs/pybackup.log)
  --extensions EXTENSIONS
                        Comma-separated list of file extensions to include
                        (default: .py)
  --exclude EXCLUDE     Comma-separated list of regex patterns to exclude
```

## PyRMCM (Remove Comments)

The `pyrmcm` command removes comments and docstrings from Python files.

### Basic Usage

```bash
pyrmcm input_file.py output_file.py
```

If output_file is not specified, the result will be printed to stdout.

### Options

```
usage: pyrmcm [-h] [input_file] [output_file]

Remove comments and docstrings from Python files

positional arguments:
  input_file   Input Python file
  output_file  Output file (if not specified, prints to stdout)

options:
  -h, --help   show this help message and exit
```

## PyFormat

The `pyformat` command formats Python files by removing comments and applying Black.

### Basic Usage

```bash
pyformat /path/to/your/python/project
```

### Options

```
usage: pyformat [-h] [--backup] [--no-black] [--verbose] directory

Process all Python files in a directory by removing comments and formatting with Black.

positional arguments:
  directory     Directory containing Python files to process

options:
  -h, --help    show this help message and exit
  --backup      Create backup files with .bak extension before processing
  --no-black    Skip Black formatting step, only remove comments
  --verbose, -v  Enable verbose output
```
