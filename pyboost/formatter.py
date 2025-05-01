"""
Formatter module - Process Python files by removing comments and formatting with Black.

This module finds Python files, removes comments using rmcm,
and then formats the code with Black to maintain readability.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from .rmcm import remove_comments_and_docstrings


def find_python_files(directory: str) -> List[Path]:
    """
    Find all Python files in the given directory recursively.
    
    Args:
        directory (str): Directory to search for Python files
        
    Returns:
        List[Path]: List of Python file paths
    """
    return list(Path(directory).rglob("*.py"))


def process_file(
    file_path: Path, 
    create_backup: bool = False, 
    use_black: bool = True,
    verbose: bool = False
) -> bool:
    """
    Process a single Python file by removing comments and formatting with Black.
    
    Args:
        file_path (Path): Path to the Python file
        create_backup (bool, optional): Whether to create a backup. Defaults to False.
        use_black (bool, optional): Whether to format with Black. Defaults to True.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.
        
    Returns:
        bool: True if successful, False otherwise
    """
    file_path = Path(file_path)
    
    # Create backup if requested
    if create_backup:
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        try:
            with open(file_path, 'r', encoding='utf-8') as src:
                with open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            if verbose:
                print(f"Created backup: {backup_path}")
        except Exception as e:
            print(f"Error creating backup for {file_path}: {e}")
            return False
    
    # Create a temporary file for the intermediate result
    temp_file = file_path.with_suffix(file_path.suffix + '.temp')
    
    try:
        # Read the source file
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Remove comments and docstrings
        cleaned_source = remove_comments_and_docstrings(source)
        
        # Write to temporary file
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(cleaned_source)
            
        if verbose:
            print(f"Removed comments from {file_path}")
            
        # Format with Black if requested
        if use_black:
            try:
                result = subprocess.run(
                    ['black', str(temp_file)],
                    capture_output=True,
                    text=True,
                    check=True
                )
                if verbose:
                    print(f"Formatted {file_path} with Black")
            except subprocess.CalledProcessError as e:
                print(f"Error formatting {file_path} with Black: {e.stderr}")
                if temp_file.exists():
                    temp_file.unlink()
                return False
        
        # Replace the original file with the processed one
        with open(temp_file, 'r', encoding='utf-8') as src:
            with open(file_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        temp_file.unlink()  # Remove the temporary file
        return True
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        if temp_file.exists():
            temp_file.unlink()
        return False


def format_directory(
    directory: str, 
    create_backup: bool = False, 
    use_black: bool = True,
    verbose: bool = False
) -> tuple[int, int]:
    """
    Format all Python files in a directory.
    
    Args:
        directory (str): Directory containing Python files
        create_backup (bool, optional): Whether to create backups. Defaults to False.
        use_black (bool, optional): Whether to format with Black. Defaults to True.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.
        
    Returns:
        tuple[int, int]: (success_count, total_count)
    """
    # Check if directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return 0, 0
    
    # Check if Black is available if requested
    if use_black:
        try:
            subprocess.run(['black', '--version'], capture_output=True, check=False)
        except FileNotFoundError:
            print("Error: 'black' command not found. Install with 'pip install black' or use use_black=False.")
            return 0, 0
    
    # Find all Python files
    python_files = find_python_files(directory)
    if not python_files:
        print(f"No Python files found in '{directory}'.")
        return 0, 0
    
    if verbose:
        print(f"Found {len(python_files)} Python files to process.")
    
    # Process each file
    success_count = 0
    for file_path in python_files:
        if verbose:
            print(f"Processing {file_path}...")
        if process_file(file_path, create_backup, use_black, verbose):
            success_count += 1
    
    if verbose:
        print(f"Processed {success_count} of {len(python_files)} files successfully.")
    
    return success_count, len(python_files)


def main():
    """Main function to parse arguments and process files."""
    parser = argparse.ArgumentParser(
        description="Process all Python files in a directory by removing comments and formatting with Black."
    )
    parser.add_argument(
        "directory",
        help="Directory containing Python files to process"
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create backup files with .bak extension before processing"
    )
    parser.add_argument(
        "--no-black",
        action="store_true",
        help="Skip Black formatting step, only remove comments"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    success_count, total_count = format_directory(
        args.directory,
        args.backup,
        not args.no_black,
        args.verbose
    )
    
    sys.exit(0 if success_count == total_count else 1)


if __name__ == "__main__":
    main()
