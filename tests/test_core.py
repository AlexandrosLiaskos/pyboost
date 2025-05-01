"""
Tests for the core module.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from pyboost.core import check_tool_availability, process_file


def test_check_tool_availability():
    """Test check_tool_availability function."""
    # Test with no skip tools and no aggressive mode
    with patch('pyboost.core.check_command_availability', return_value=True):
        available_tools = check_tool_availability(set(), False)
        
        # pybackup should always be available
        assert available_tools["pybackup"] is True
        
        # rmcm should not be available in non-aggressive mode
        assert available_tools["rmcm"] is False
        
        # Other tools should be available
        assert available_tools["autoflake"] is True
        assert available_tools["pyupgrade"] is True
        assert available_tools["isort"] is True
        assert available_tools["black"] is True
        assert available_tools["ruff"] is True
        assert available_tools["mypy"] is True
        assert available_tools["bandit"] is True
        assert available_tools["vulture"] is True
    
    # Test with skip tools
    with patch('pyboost.core.check_command_availability', return_value=True):
        available_tools = check_tool_availability({"autoflake", "black"}, False)
        
        # Skipped tools should not be available
        assert available_tools["autoflake"] is False
        assert available_tools["black"] is False
        
        # Other tools should be available
        assert available_tools["pybackup"] is True
        assert available_tools["pyupgrade"] is True
        assert available_tools["isort"] is True
        assert available_tools["ruff"] is True
    
    # Test with aggressive mode
    with patch('pyboost.core.check_command_availability', return_value=True):
        available_tools = check_tool_availability(set(), True)
        
        # rmcm should be available in aggressive mode
        assert available_tools["rmcm"] is True


def test_process_file():
    """Test process_file function."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a test file
        test_file = Path(temp_dir) / "test.py"
        with open(test_file, "w") as f:
            f.write("print('Hello, world!')")
        
        # Mock available tools
        available_tools = {
            "pybackup": True,
            "rmcm": False,
            "autoflake": False,
            "pyupgrade": False,
            "isort": False,
            "black": False,
            "ruff": False,
            "mypy": False,
            "bandit": False,
            "vulture": False
        }
        
        # Process the file (only backup)
        with patch('pyboost.core.PyBackup') as mock_pybackup:
            mock_instance = mock_pybackup.return_value
            mock_instance.backup_file.return_value = True
            
            result = process_file(
                test_file,
                available_tools,
                create_backup=True,
                backup_only=True,
                verbose=True
            )
            
            # Check that the backup was created
            assert result is True
            mock_instance.backup_file.assert_called_once_with(test_file)
