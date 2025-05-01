"""
pyboost core module - Ultimate Python Code Maintenance Toolkit

This module applies multiple tools to clean, optimize, and improve Python code:
1. pybackup - Create backups of Python files with timestamps
2. rmcm - Remove comments and docstrings (optional)
3. autoflake - Remove unused imports and variables
4. pyupgrade - Upgrade to modern Python syntax
5. isort - Sort imports
6. black - Format code
7. ruff - Lint and check for errors
8. mypy - Static type checking (optional)
9. bandit - Security checks (optional)
10. vulture - Find dead code (optional)
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Set

from .backup import PyBackup
from .utils import check_command_availability, find_python_files, run_command

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


# Define the tools and their commands
TOOLS = {
    "pybackup": {
        "command": None,  # Handled internally
        "install": "Included in pyboost",
        "description": "Creates backups of Python files with timestamps",
        "optional": False,
        "aggressive_only": False
    },
    "rmcm": {
        "command": ["rmcm", "{input}", "{output}"],
        "install": "pip install pyboost[rmcm]",
        "description": "Removes comments and docstrings",
        "optional": True,
        "aggressive_only": True
    },
    "autoflake": {
        "command": ["autoflake", "--in-place", "--remove-all-unused-imports", "--remove-unused-variables", "{input}"],
        "install": "pip install autoflake",
        "description": "Removes unused imports and variables",
        "optional": False,
        "aggressive_only": False
    },
    "pyupgrade": {
        "command": ["pyupgrade", "--py310-plus", "{input}"],
        "install": "pip install pyupgrade",
        "description": "Upgrades to modern Python syntax",
        "optional": False,
        "aggressive_only": False
    },
    "isort": {
        "command": ["isort", "{input}"],
        "install": "pip install isort",
        "description": "Sorts imports",
        "optional": False,
        "aggressive_only": False
    },
    "black": {
        "command": ["black", "{input}"],
        "install": "pip install black",
        "description": "Formats code",
        "optional": False,
        "aggressive_only": False
    },
    "ruff": {
        "command": ["ruff", "check", "--fix", "{input}"],
        "install": "pip install ruff",
        "description": "Lints and fixes code",
        "optional": False,
        "aggressive_only": False
    },
    "mypy": {
        "command": ["mypy", "{input}"],
        "install": "pip install mypy",
        "description": "Performs static type checking",
        "optional": True,
        "aggressive_only": False
    },
    "bandit": {
        "command": ["bandit", "-r", "{input}"],
        "install": "pip install bandit",
        "description": "Checks for security issues",
        "optional": True,
        "aggressive_only": False
    },
    "vulture": {
        "command": ["vulture", "{input}"],
        "install": "pip install vulture",
        "description": "Finds dead code",
        "optional": True,
        "aggressive_only": False
    }
}


def check_tool_availability(skip_tools: Set[str], aggressive: bool) -> Dict[str, bool]:
    """
    Check which tools are available and return a dictionary of tool availability.
    
    Args:
        skip_tools (Set[str]): Set of tools to skip
        aggressive (bool): Whether aggressive mode is enabled
        
    Returns:
        Dict[str, bool]: Dictionary of tool availability
    """
    available_tools = {}
    
    for tool_name, tool_info in TOOLS.items():
        # Skip tools that are in the skip list
        if tool_name in skip_tools:
            available_tools[tool_name] = False
            continue
            
        # Skip tools that are only for aggressive mode if not in aggressive mode
        if tool_info["aggressive_only"] and not aggressive:
            available_tools[tool_name] = False
            continue
            
        # pybackup is always available since it's integrated
        if tool_name == "pybackup":
            available_tools[tool_name] = True
            continue
            
        # Check if the tool is available
        if tool_info["command"] is None:
            available_tools[tool_name] = True
            continue
            
        cmd = tool_info["command"][0]
        available_tools[tool_name] = check_command_availability(cmd)
        
        if not available_tools[tool_name] and not tool_info["optional"]:
            print(f"Warning: Required tool '{tool_name}' not found. Install with: {tool_info['install']}")
                
    return available_tools


def process_file(
    file_path: Path, 
    available_tools: Dict[str, bool], 
    create_backup: bool = True,
    backup_only: bool = False,
    backup_dir: Optional[str] = None,
    verbose: bool = False
) -> bool:
    """
    Process a single Python file with all available tools.
    
    Args:
        file_path (Path): Path to the Python file
        available_tools (Dict[str, bool]): Dictionary of tool availability
        create_backup (bool, optional): Whether to create a backup. Defaults to True.
        backup_only (bool, optional): Whether to only create a backup. Defaults to False.
        backup_dir (Optional[str], optional): Directory to store backups. Defaults to None.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.
        
    Returns:
        bool: True if successful, False otherwise
    """
    file_path = Path(file_path)
    
    # Create backup if requested
    if create_backup and available_tools.get("pybackup", False):
        # Use the integrated PyBackup for backups
        codebase_root = file_path.parent
        backup = PyBackup(
            codebase_root=codebase_root,
            backup_dir=backup_dir,
            no_backup=False,
            verbose=verbose,
            extensions=[file_path.suffix],
            exclude_patterns=[]
        )
        backup.backup_file(file_path)
    
    # If backup_only is True, skip the rest of the processing
    if backup_only:
        return True
    
    # Process with each available tool
    success = True
    
    for tool_name, is_available in available_tools.items():
        if not is_available or tool_name == "pybackup":
            continue
            
        tool_info = TOOLS[tool_name]
        if verbose:
            print(f"Applying {tool_name} to {file_path}...")
        
        try:
            # Special handling for rmcm which needs an output file
            if tool_name == "rmcm":
                with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as temp:
                    temp_path = Path(temp.name)
                
                success = run_command(
                    tool_info["command"],
                    str(file_path),
                    str(temp_path),
                    verbose
                )
                
                if success:
                    # Copy the temp file back to the original
                    with open(temp_path, 'r', encoding='utf-8') as src:
                        with open(file_path, 'w', encoding='utf-8') as dst:
                            dst.write(src.read())
                    os.unlink(temp_path)
                else:
                    print(f"Error applying {tool_name} to {file_path}")
                    if temp_path.exists():
                        os.unlink(temp_path)
                    success = False
            else:
                # For other tools, just run the command
                cmd_success = run_command(
                    tool_info["command"],
                    str(file_path),
                    None,
                    verbose
                )
                
                if not cmd_success:
                    print(f"Error applying {tool_name} to {file_path}")
                    success = False
                    
        except Exception as e:
            print(f"Exception applying {tool_name} to {file_path}: {e}")
            success = False
            
    return success


def process_directory(
    directory: str,
    skip_tools: Set[str] = None,
    aggressive: bool = False,
    create_backup: bool = True,
    backup_only: bool = False,
    backup_dir: Optional[str] = None,
    verbose: bool = False
) -> tuple[int, int]:
    """
    Process all Python files in a directory.
    
    Args:
        directory (str): Directory containing Python files
        skip_tools (Set[str], optional): Set of tools to skip. Defaults to None.
        aggressive (bool, optional): Whether aggressive mode is enabled. Defaults to False.
        create_backup (bool, optional): Whether to create backups. Defaults to True.
        backup_only (bool, optional): Whether to only create backups. Defaults to False.
        backup_dir (Optional[str], optional): Directory to store backups. Defaults to None.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.
        
    Returns:
        tuple[int, int]: (success_count, total_count)
    """
    skip_tools = skip_tools or set()
    
    # Check if directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return 0, 0
    
    # Check tool availability
    available_tools = check_tool_availability(skip_tools, aggressive)
    
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
            print(f"\nProcessing {file_path}...")
        if process_file(
            file_path, 
            available_tools, 
            create_backup,
            backup_only,
            backup_dir,
            verbose
        ):
            success_count += 1
    
    if verbose:
        print(f"\nProcessed {success_count} of {len(python_files)} files successfully.")
    
    return success_count, len(python_files)


def main():
    """Main function to parse arguments and process files."""
    parser = argparse.ArgumentParser(
        description="Ultimate Python Code Maintenance Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__  # Use the module docstring as epilog
    )
    parser.add_argument(
        "directory",
        help="Directory containing Python files to process"
    )
    parser.add_argument(
        "--no-bak",
        action="store_true",
        help="Skip creating backup files (backups are stored in the codebase by default)"
    )
    parser.add_argument(
        "--backup-dir",
        type=str,
        help="Directory to store backups (default: <codebase>/backup)"
    )
    parser.add_argument(
        "--skip",
        type=str,
        default="",
        help="Comma-separated list of tools to skip (e.g., 'rmcm,mypy,bandit')"
    )
    parser.add_argument(
        "--aggressive",
        action="store_true",
        help="Enable aggressive mode (includes comment removal and other potentially destructive operations)"
    )
    parser.add_argument(
        "--backup-only",
        action="store_true",
        help="Only create backups, don't process files"
    )
    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="List all available tools and exit"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Handle --list-tools
    if args.list_tools:
        print("Available tools:")
        for tool_name, tool_info in TOOLS.items():
            status = "Optional" if tool_info["optional"] else "Required"
            if tool_info["aggressive_only"]:
                status += " (aggressive mode only)"
            print(f"  {tool_name}: {tool_info['description']} - {status}")
        sys.exit(0)
    
    # Parse skip list
    skip_tools = set(args.skip.split(",")) if args.skip else set()
    
    # If backup_only is True, skip all tools except pybackup
    if args.backup_only:
        for tool_name in TOOLS.keys():
            if tool_name != "pybackup":
                skip_tools.add(tool_name)
    
    success_count, total_count = process_directory(
        args.directory,
        skip_tools,
        args.aggressive,
        not args.no_bak,
        args.backup_only,
        args.backup_dir,
        args.verbose
    )
    
    sys.exit(0 if success_count == total_count else 1)


if __name__ == "__main__":
    main()
