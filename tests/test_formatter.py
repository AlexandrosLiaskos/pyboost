"""
Tests for the formatter module.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from pyboost.formatter import find_python_files, process_file


def test_find_python_files():
    """Test find_python_files function."""
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


def test_process_file():
    """Test process_file function."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test file
        test_file = Path(temp_dir) / "test.py"
        with open(test_file, "w") as f:
            f.write("""
# This is a comment
def hello():
    '''This is a docstring'''
    print('Hello, world!')  # This is another comment
""")
        
        # Create a backup of the original content
        original_content = test_file.read_text()
        
        # Process the file without Black
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            result = process_file(
                test_file,
                create_backup=True,
                use_black=False,
                verbose=True
            )
            
            # Check that the file was processed successfully
            assert result is True
            
            # Check that a backup was created
            backup_file = Path(temp_dir) / "test.py.bak"
            assert backup_file.exists()
            assert backup_file.read_text() == original_content
            
            # Check that comments and docstrings were removed
            processed_content = test_file.read_text()
            assert "# This is a comment" not in processed_content
            assert "'''This is a docstring'''" not in processed_content
            assert "# This is another comment" not in processed_content
            assert "def hello():" in processed_content
            assert "print('Hello, world!')" in processed_content
