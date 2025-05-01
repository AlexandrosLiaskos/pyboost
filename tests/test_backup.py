"""
Tests for the backup module.
"""

import os
import tempfile
from pathlib import Path

import pytest

from pyboost.backup import PyBackup


def test_pybackup_initialization():
    """Test PyBackup initialization."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a PyBackup instance
        backup = PyBackup(
            codebase_root=temp_dir,
            verbose=True
        )
        
        # Check that the backup directory was created
        assert (Path(temp_dir) / "backup").exists()
        
        # Check that the logs directory was created
        assert (Path(temp_dir) / "logs").exists()
        
        # Check that the log file was created
        assert (Path(temp_dir) / "logs" / "pybackup.log").exists()


def test_backup_file():
    """Test backing up a file."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test file
        test_file = Path(temp_dir) / "test.py"
        with open(test_file, "w") as f:
            f.write("print('Hello, world!')")
        
        # Create a PyBackup instance
        backup = PyBackup(
            codebase_root=temp_dir,
            verbose=True
        )
        
        # Backup the file
        result = backup.backup_file(test_file)
        
        # Check that the backup was successful
        assert result is True
        
        # Check that a backup file was created
        backup_files = list(Path(temp_dir).glob("backup/test.py.*"))
        assert len(backup_files) == 1


def test_find_files():
    """Test finding files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some test files
        (Path(temp_dir) / "test1.py").touch()
        (Path(temp_dir) / "test2.py").touch()
        (Path(temp_dir) / "test3.txt").touch()
        
        # Create a subdirectory with a Python file
        subdir = Path(temp_dir) / "subdir"
        subdir.mkdir()
        (subdir / "test4.py").touch()
        
        # Create a PyBackup instance
        backup = PyBackup(
            codebase_root=temp_dir,
            verbose=True
        )
        
        # Find Python files
        files = backup.find_files()
        
        # Check that we found the right files
        assert len(files) == 3
        assert any(f.name == "test1.py" for f in files)
        assert any(f.name == "test2.py" for f in files)
        assert any(f.name == "test4.py" for f in files)
        assert not any(f.name == "test3.txt" for f in files)


def test_exclude_patterns():
    """Test excluding files with patterns."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some test files
        (Path(temp_dir) / "test1.py").touch()
        (Path(temp_dir) / "test2.py").touch()
        (Path(temp_dir) / "exclude_me.py").touch()
        
        # Create a PyBackup instance with exclude patterns
        backup = PyBackup(
            codebase_root=temp_dir,
            verbose=True,
            exclude_patterns=["exclude_me"]
        )
        
        # Find Python files
        files = backup.find_files()
        
        # Check that we found the right files
        assert len(files) == 2
        assert any(f.name == "test1.py" for f in files)
        assert any(f.name == "test2.py" for f in files)
        assert not any(f.name == "exclude_me.py" for f in files)
