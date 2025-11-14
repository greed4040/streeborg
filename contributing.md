# Contributing to Streebog

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs

Before creating a bug report:
1. Check existing issues to avoid duplicates
2. Verify the bug with the latest version
3. Collect relevant information (Python version, OS, error messages)

When reporting a bug, include:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Code sample if applicable
- Output of `python --version`

### Suggesting Enhancements

Enhancement suggestions are welcome! Please:
1. Check if it's already been suggested
2. Explain the use case clearly
3. Describe the proposed solution
4. Consider backwards compatibility

### Pull Requests

1. **Fork** the repository
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes:**
   - Write clear, readable code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

4. **Test your changes:**
   ```bash
   python test_final_hash.py  # Must pass!
   python test_fixed.py       # Must pass!
   ```

5. **Commit with clear messages:**
   ```bash
   git commit -m "Add feature: brief description"
   ```

6. **Push and create PR:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Standards

### Style Guide

Follow [PEP 8](https://pep8.org/):
- 4 spaces for indentation (no tabs)
- Max line length: 88 characters (Black formatter compatible)
- Use descriptive variable names
- Add docstrings to all public functions

Example:
```python
def hash_512(data: bytes) -> bytes:
    """
    Compute 512-bit Streebog hash.
    
    Args:
        data: Input data to hash
        
    Returns:
        64-byte hash value
        
    Raises:
        ValueError: If data length exceeds 2^512 bits
    """
    # Implementation...
```

### Testing

All new code must include tests:
- Add test cases to appropriate test files
- Ensure all existing tests still pass
- Aim for high test coverage
- Include edge cases

### Documentation

Update documentation for:
- New functions or classes → Add docstrings
- API changes → Update README.md
- Bug fixes → Update CHANGELOG.md
- Breaking changes → Update migration guide

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/streebog.git
cd streebog

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Run tests
python test_final_hash.py
```

## Priority Areas

We especially welcome contributions in:
- **Performance optimizations** (vectorization, Cython, etc.)
- **Additional test vectors** from official GOST documents
- **Documentation improvements**
- **CLI interface** for command-line usage
- **HMAC-Streebog** implementation
- **Benchmarking suite**

## Code Review Process

1. Maintainer reviews within 3-7 days
2. Feedback provided via PR comments
3. Iterate until approved
4. Maintainer merges (squash merge preferred)

## Security Issues

**Do not** open public issues for security vulnerabilities.

Instead:
- Email: security@example.com (replace with actual)
- Include detailed description
- Wait for response before public disclosure
- We aim to respond within 48 hours

## Questions?

- Open a discussion issue
- Check existing issues and discussions
- Read the documentation thoroughly

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Mentioned in relevant documentation

Thank you for helping improve Streebog! 🙏
