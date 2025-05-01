"""
Tests for the utils module.
"""

import os
import tempfile
from pathlib import Path

import pytest

from pyboost.utils import check_command_availability, create_backup_path, find_python_files


def test_check_command_availability():
    """Test check_command_availability function."""
    # Python should be available
    assert check_command_availability("python") is True
    
    # A non-existent command should not be available
    assert check_command_availability("non_existent_command_12345") is False


def test_create_backup_path():
    """Test create_backup_path function."""
    # Create a test file path
    file_path = Path("/tmp/test.py")
    
    # Test with a custom timestamp
    timestamp = "20230101_120000"
    backup_path = create_backup_path(file_path, timestamp)
    assert str(backup_path) == "/tmp/test.py.20230101_120000"
    
    # Test without a timestamp (uses current time)
    backup_path = create_backup_path(file_path)
    assert str(backup_path).startswith("/tmp/test.py.")
    assert len(str(backup_path)) > len("/tmp/test.py.")


def test_find_python_files():
    """Test find_python_files function."""
    # Create a temporary directory with some Python files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some Python files
        (Path(temp_dir) / "file1.py").touch()
        (Path(temp_dir) / "file2.py").touch()
        
        # Create a subdirectory with a Python file
        subdir = Path(temp_dir) / "subdir"
        subdir.mkdir()
        (subdir / "file3.py").touch()
        
        # Create a non-Python file
        (Path(temp_dir) / "file4.txt").touch()
        
        # Find Python files
        python_files = find_python_files(temp_dir)
        
        # Check that we found the right files
        assert len(python_files) == 3
        assert any(f.name == "file1.py" for f in python_files)
        assert any(f.name == "file2.py" for f in python_files)
        assert any(f.name == "file3.py" for f in python_files)
        assert not any(f.name == "file4.txt" for f in python_files)
