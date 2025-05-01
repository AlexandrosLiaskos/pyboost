# Contributing to PyBoost

Thank you for considering contributing to PyBoost! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

1. Clone your fork of the repository
   ```bash
   git clone https://github.com/yourusername/pyboost.git
   cd pyboost
   ```

2. Install development dependencies
   ```bash
   pip install -e .[dev]
   ```

3. Run tests to ensure everything is working
   ```bash
   pytest
   ```

## Testing

We use pytest for testing. To run the tests:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=pyboost
```

## Code Style

We use Black and isort for code formatting. To format your code:

```bash
black pyboost tests
isort pyboost tests
```

We also use mypy for type checking:

```bash
mypy pyboost
```

## Documentation

We use Markdown for documentation. Please update the documentation when you add or modify features.

## Pull Request Process

1. Ensure your code passes all tests and linting
2. Update the documentation if necessary
3. Update the README.md if necessary
4. The PR should work for Python 3.8 and later
5. Include tests for new features

## Release Process

1. Update version number in:
   - pyboost/__init__.py
   - setup.py
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Publish to PyPI

## License

By contributing to PyBoost, you agree that your contributions will be licensed under the project's MIT License.
