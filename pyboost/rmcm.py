"""
rmcm - A tool to remove comments and docstrings from Python files.

This module uses Python's tokenize module to properly parse Python code and
remove comments and docstrings while preserving the code's functionality.
"""

import argparse
import io
import os
import sys
import tokenize
from pathlib import Path
from typing import Optional


def remove_comments_and_docstrings(source: str) -> str:
    """
    Returns source code with comments and docstrings removed.

    Args:
        source (str): Source code as a string

    Returns:
        str: Source code with comments and docstrings removed
    """
    io_obj = io.StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0

    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]

        # Handle new lines
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))

        # Remove comments
        if token_type == tokenize.COMMENT:
            pass
        # Remove docstrings
        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                # This is likely a regular string, not a docstring
                if prev_toktype != tokenize.NEWLINE:
                    # Catch whole-module docstrings
                    if start_col > 0:
                        # Not a docstring
                        out += token_string
            else:
                # This is a docstring
                pass
        # Keep everything else
        else:
            out += token_string

        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line

    # Remove empty lines
    return '\n'.join(line for line in out.splitlines() if line.strip())


def process_file(input_file: str, output_file: Optional[str] = None) -> bool:
    """
    Process a single file to remove comments and docstrings.

    Args:
        input_file (str): Path to the input file
        output_file (str, optional): Path to the output file. If None, prints to stdout.

    Returns:
        bool: True if successful, False otherwise
    """
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"Error: Input file '{input_file}' not found.")
        return False

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            source = f.read()

        cleaned_source = remove_comments_and_docstrings(source)

        if output_file:
            output_path = Path(output_file)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_source)
            print(f"Comments and docstrings removed. Output written to '{output_file}'")
        else:
            print(cleaned_source)

        return True

    except Exception as e:
        print(f"Error processing file: {e}")
        return False


def main():
    """Main function to handle command line arguments and process files."""
    parser = argparse.ArgumentParser(
        description="Remove comments and docstrings from Python files",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="Input Python file"
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        help="Output file (if not specified, prints to stdout)"
    )
    parser.add_argument(
        "--help-full",
        action="store_true",
        help="Show full help message and exit"
    )

    # Show help if no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    # Show full help if requested
    if args.help_full:
        print(__doc__)
        sys.exit(0)

    # Check if input file is provided
    if not args.input_file:
        parser.print_help()
        sys.exit(1)

    success = process_file(args.input_file, args.output_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
