#!/usr/bin/env python3
"""
Setup script for pyboost package.
"""

from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="pyboost-toolkit",
    version="1.0.0",
    author="Alexandros Liaskos",
    author_email="alexandros.liaskos@gmail.com",
    description="Ultimate Python Code Maintenance Toolkit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexandrosLiaskos/pyboost",
    project_urls={
        "Documentation": "https://github.com/AlexandrosLiaskos/pyboost/blob/main/README.md",
        "Bug Reports": "https://github.com/AlexandrosLiaskos/pyboost/issues",
        "Source Code": "https://github.com/AlexandrosLiaskos/pyboost",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "mypy>=1.0.0",
        ],
        "rmcm": [],  # No additional dependencies, as rmcm is included
        "all": [
            "autoflake>=2.0.0",
            "pyupgrade>=3.0.0",
            "isort>=5.0.0",
            "black>=23.0.0",
            "ruff>=0.0.1",
            "mypy>=1.0.0",
            "bandit>=1.0.0",
            "vulture>=2.0.0",
            "rich>=13.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pyboost=pyboost.core:main",
            "pybackup=pyboost.backup:main",
            "pyrmcm=pyboost.rmcm:main",
            "pyformat=pyboost.formatter:main",
        ],
    },
)
