"""
Python File Backup Utility

A utility module for backing up Python files in a codebase with timestamps.
Creates backups within the codebase structure and logs operations.
"""

import argparse
import datetime
import logging
import os
import re
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Set, Tuple

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
    from rich.prompt import Confirm
    from rich.rule import Rule
    from rich.table import Table
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None
    print("Rich library not available. Install with: pip install rich")
    print("Falling back to standard output.")


class PyBackup:
    """Python file backup utility class"""

    def __init__(
        self,
        codebase_root: str,
        backup_dir: Optional[str] = None,
        no_backup: bool = False,
        verbose: bool = False,
        log_file: Optional[str] = None,
        extensions: List[str] = None,
        exclude_patterns: List[str] = None
    ):
        """
        Initialize the backup utility

        Args:
            codebase_root: Root directory of the codebase
            backup_dir: Directory to store backups (default: <codebase_root>/backup)
            no_backup: If True, don't create backups (dry run)
            verbose: If True, print verbose output
            log_file: Path to log file (default: <codebase_root>/logs/pybackup.log)
            extensions: List of file extensions to include (default: ['.py'])
            exclude_patterns: List of regex patterns to exclude
        """
        self.codebase_root = Path(codebase_root).resolve()

        if not self.codebase_root.is_dir():
            self._error(f"Codebase root directory not found: {self.codebase_root}")
            sys.exit(1)

        # Set up backup directory
        if backup_dir:
            self.backup_dir = Path(backup_dir).resolve()
        else:
            self.backup_dir = self.codebase_root / "backup"

        # Create backup directory if it doesn't exist
        if not no_backup and not self.backup_dir.exists():
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            self._info(f"Created backup directory: {self.backup_dir}")

        # Set up logs directory
        self.logs_dir = self.codebase_root / "logs"
        if not self.logs_dir.exists():
            self.logs_dir.mkdir(parents=True, exist_ok=True)
            self._info(f"Created logs directory: {self.logs_dir}")

        # Set up logging
        if log_file:
            self.log_file = Path(log_file).resolve()
        else:
            self.log_file = self.logs_dir / "pybackup.log"

        # Create parent directory for log file if it doesn't exist
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Create empty log file if it doesn't exist
        if not self.log_file.exists():
            self.log_file.touch()

        logging.basicConfig(
            filename=self.log_file,
            level=logging.DEBUG if verbose else logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Set other properties
        self.no_backup = no_backup
        self.verbose = verbose
        self.extensions = extensions or ['.py']
        self.exclude_patterns = exclude_patterns or []
        self.exclude_regexes = [re.compile(pattern) for pattern in self.exclude_patterns]

        # Timestamp for this backup session
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Log initialization
        logging.info(f"Initialized PyBackup for codebase: {self.codebase_root}")
        logging.info(f"Backup directory: {self.backup_dir}")
        logging.info(f"Extensions filter: {self.extensions}")
        logging.info(f"Exclude patterns: {self.exclude_patterns}")
        if self.no_backup:
            logging.info("Running in dry-run mode (no backups will be created)")

    def _info(self, message: str) -> None:
        """Print info message using rich if available, otherwise print normally"""
        if RICH_AVAILABLE and console:
            console.print(f"[blue]{message}[/]")
        else:
            print(message)
        logging.info(message)

    def _warning(self, message: str) -> None:
        """Print warning message using rich if available, otherwise print normally"""
        if RICH_AVAILABLE and console:
            console.print(f"[yellow]{message}[/]")
        else:
            print(f"Warning: {message}")
        logging.warning(message)

    def _error(self, message: str) -> None:
        """Print error message using rich if available, otherwise print normally"""
        if RICH_AVAILABLE and console:
            console.print(f"[red]{message}[/]")
        else:
            print(f"Error: {message}")
        logging.error(message)

    def _success(self, message: str) -> None:
        """Print success message using rich if available, otherwise print normally"""
        if RICH_AVAILABLE and console:
            console.print(f"[green]{message}[/]")
        else:
            print(message)
        logging.info(message)

    def _should_exclude(self, file_path: Path) -> bool:
        """Check if a file should be excluded based on patterns"""
        file_str = str(file_path)
        return any(regex.search(file_str) for regex in self.exclude_regexes)

    def find_files(self) -> List[Path]:
        """Find all files in the codebase matching the extension filter"""
        files = []
        for ext in self.extensions:
            files.extend(self.codebase_root.rglob(f"*{ext}"))

        # Filter out excluded files
        files = [f for f in files if not self._should_exclude(f)]

        return sorted(files)

    def backup_file(self, file_path: Path) -> bool:
        """
        Create a backup of a single file

        Args:
            file_path: Path to the file to backup

        Returns:
            bool: True if backup was successful, False otherwise
        """
        file_path = Path(file_path).resolve()

        if not file_path.exists():
            self._error(f"File not found: {file_path}")
            return False

        if not file_path.is_file():
            self._error(f"Not a file: {file_path}")
            return False

        # Skip if extension not in filter
        if file_path.suffix not in self.extensions:
            if self.verbose:
                self._info(f"Skipping file with non-matching extension: {file_path}")
            return True

        # Skip if matches exclude pattern
        if self._should_exclude(file_path):
            if self.verbose:
                self._info(f"Skipping excluded file: {file_path}")
            return True

        # Create relative path for backup
        try:
            rel_path = file_path.relative_to(self.codebase_root)
        except ValueError:
            # If file is not in codebase_root, use the filename only
            rel_path = file_path.name

        # Create backup path with timestamp
        backup_path = self.backup_dir / f"{rel_path}.{self.timestamp}"

        # Create parent directories if they don't exist
        if not self.no_backup:
            backup_path.parent.mkdir(parents=True, exist_ok=True)

        # Create backup
        if not self.no_backup:
            try:
                shutil.copy2(file_path, backup_path)
                if self.verbose:
                    self._success(f"Created backup: {backup_path}")
                logging.info(f"Backed up {file_path} to {backup_path}")
                return True
            except Exception as e:
                self._error(f"Failed to backup {file_path}: {e}")
                logging.exception(f"Backup failed for {file_path}")
                return False
        else:
            if self.verbose:
                self._info(f"Would backup {file_path} to {backup_path} (dry run)")
            return True

    def backup_all(self) -> Tuple[int, int]:
        """
        Backup all files in the codebase matching the extension filter

        Returns:
            Tuple[int, int]: (success_count, total_count)
        """
        files = self.find_files()
        total_count = len(files)

        if total_count == 0:
            self._warning(f"No files found matching extensions: {self.extensions}")
            return 0, 0

        self._info(f"Found {total_count} files to backup")

        if RICH_AVAILABLE and console:
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TextColumn("({task.completed}/{task.total})"),
                TimeElapsedColumn(),
                console=console
            ) as progress:
                task = progress.add_task(f"Backing up files", total=total_count)
                success_count = 0

                for file_path in files:
                    if self.backup_file(file_path):
                        success_count += 1
                    progress.update(task, advance=1)
        else:
            success_count = 0
            for i, file_path in enumerate(files, 1):
                print(f"Backing up file {i}/{total_count}: {file_path}")
                if self.backup_file(file_path):
                    success_count += 1

        self._info(f"Backup complete: {success_count}/{total_count} files backed up successfully")
        return success_count, total_count


def main():
    """Main function to parse arguments and run the backup utility"""
    parser = argparse.ArgumentParser(
        description="Python File Backup Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "codebase_root",
        help="Root directory of the codebase to backup"
    )
    parser.add_argument(
        "--backup-dir",
        help="Directory to store backups (default: <codebase_root>/backup)"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backups (dry run)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--log-file",
        help="Path to log file (default: <codebase_root>/logs/pybackup.log)"
    )
    parser.add_argument(
        "--extensions",
        help="Comma-separated list of file extensions to include (default: .py)",
        default=".py"
    )
    parser.add_argument(
        "--exclude",
        help="Comma-separated list of regex patterns to exclude",
        default=""
    )

    args = parser.parse_args()

    # Parse extensions
    extensions = [ext.strip() for ext in args.extensions.split(",")]
    # Ensure extensions start with a dot
    extensions = [ext if ext.startswith(".") else f".{ext}" for ext in extensions]

    # Parse exclude patterns
    exclude_patterns = [pat.strip() for pat in args.exclude.split(",") if pat.strip()]

    # Create backup utility
    backup = PyBackup(
        codebase_root=args.codebase_root,
        backup_dir=args.backup_dir,
        no_backup=args.no_backup,
        verbose=args.verbose,
        log_file=args.log_file,
        extensions=extensions,
        exclude_patterns=exclude_patterns
    )

    # Run backup
    success_count, total_count = backup.backup_all()

    # Exit with success if all files were backed up successfully
    sys.exit(0 if success_count == total_count else 1)


if __name__ == "__main__":
    main()
