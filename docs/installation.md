# Installation

PyBoost can be installed using pip, the Python package manager.

## Basic Installation

The basic installation includes the core functionality and the integrated tools (pybackup and rmcm).

```bash
pip install pyboost
```

## Full Installation

To install PyBoost with all optional dependencies:

```bash
pip install pyboost[all]
```

This will install the following additional packages:
- autoflake
- pyupgrade
- isort
- black
- ruff
- mypy
- bandit
- vulture
- rich

## Development Installation

If you want to contribute to PyBoost, you can install the development dependencies:

```bash
pip install pyboost[dev]
```

This will install the following additional packages:
- pytest
- pytest-cov
- black
- isort
- mypy

## From Source

You can also install PyBoost directly from the source code:

```bash
git clone https://github.com/yourusername/pyboost.git
cd pyboost
pip install -e .
```

To install with all dependencies:

```bash
pip install -e .[all]
```

## Requirements

PyBoost requires Python 3.8 or later.
