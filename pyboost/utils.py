"""
Utility functions for pyboost.

This module contains utility functions used across the pyboost package.
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set


def find_python_files(directory: str) -> List[Path]:
    """
    Find all Python files in the given directory recursively.
    
    Args:
        directory (str): Directory to search for Python files
        
    Returns:
        List[Path]: List of Python file paths
    """
    return list(Path(directory).rglob("*.py"))


def check_command_availability(command: str) -> bool:
    """
    Check if a command is available in the system PATH.
    
    Args:
        command (str): Command to check
        
    Returns:
        bool: True if command is available, False otherwise
    """
    try:
        result = subprocess.run(
            ["which", command] if os.name != "nt" else ["where", command],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except Exception:
        return False


def create_backup_path(file_path: Path, timestamp: Optional[str] = None) -> Path:
    """
    Create a backup path for a file with an optional timestamp.
    
    Args:
        file_path (Path): Path to the file
        timestamp (str, optional): Timestamp to append to the backup file. 
                                  If None, uses current time. Defaults to None.
        
    Returns:
        Path: Backup path
    """
    import datetime
    
    if timestamp is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
    return file_path.with_suffix(f"{file_path.suffix}.{timestamp}")


def run_command(
    command: List[str], 
    input_file: Optional[str] = None, 
    output_file: Optional[str] = None,
    verbose: bool = False
) -> bool:
    """
    Run a command with optional input and output files.
    
    Args:
        command (List[str]): Command to run
        input_file (str, optional): Input file path. Defaults to None.
        output_file (str, optional): Output file path. Defaults to None.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.
        
    Returns:
        bool: True if command succeeded, False otherwise
    """
    # Replace placeholders in command
    cmd = []
    for part in command:
        if part == "{input}" and input_file:
            cmd.append(input_file)
        elif part == "{output}" and output_file:
            cmd.append(output_file)
        else:
            cmd.append(part)
    
    if verbose:
        print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode != 0:
            if verbose:
                print(f"Command failed with exit code {result.returncode}")
                print(f"Error: {result.stderr}")
            return False
        
        if verbose:
            print(f"Command succeeded")
            if result.stdout:
                print(f"Output: {result.stdout}")
        
        return True
    except Exception as e:
        if verbose:
            print(f"Exception running command: {e}")
        return False
