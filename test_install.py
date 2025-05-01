#!/usr/bin/env python3
"""
Test script to verify the PyBoost package installation.

This script imports all the main modules from PyBoost and prints their versions.
"""

import sys
from importlib import import_module

def test_import(module_name):
    """Test importing a module and print its version if available."""
    try:
        module = import_module(module_name)
        version = getattr(module, "__version__", "unknown")
        print(f"✅ Successfully imported {module_name} (version: {version})")
        return True
    except ImportError as e:
        print(f"❌ Failed to import {module_name}: {e}")
        return False

def main():
    """Main function to test PyBoost installation."""
    print("Testing PyBoost installation...\n")
    
    # List of modules to test
    modules = [
        "pyboost",
        "pyboost.core",
        "pyboost.backup",
        "pyboost.rmcm",
        "pyboost.formatter",
        "pyboost.utils"
    ]
    
    # Test importing each module
    success_count = 0
    for module_name in modules:
        if test_import(module_name):
            success_count += 1
    
    # Print summary
    print(f"\nImported {success_count} of {len(modules)} modules successfully.")
    
    if success_count == len(modules):
        print("\n🎉 PyBoost is installed correctly!")
        return 0
    else:
        print("\n⚠️ Some PyBoost modules could not be imported.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
