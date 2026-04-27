# Contributing to Project Chronos (Rita Job Automator)

Thank you for your interest in contributing to Project Chronos! This document outlines how to contribute effectively.

## Code of Conduct

By contributing to this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Report security issues privately (see Security Policy)
- Provide constructive feedback
- Collaborate in good faith

## Getting Started

### Local Development Setup

```bash
# 1. Fork and clone the repository
git clone https://github.com/YOUR-USERNAME/Rita_Job_Automator.git
cd Rita_Job_Automator

# 2. Create a feature branch
git checkout -b feature/your-feature-name

# 3. Set up Python environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env from template
cp .env.example .env
# Fill in your test credentials

# 6. Run tests locally
python -m coverage run --source=core -m unittest discover
python -m coverage report
```

## Development Guidelines

### Code Style

- **Python**: Follow PEP 8 (indent with 4 spaces)
- **Function names**: Use lowercase with underscores (`validate_lead`)
- **Class names**: Use PascalCase (`AlphaOrchestrator`)
- **Comments**: Use docstrings for all modules and functions
- **Type hints**: Include type hints for function signatures where possible

### Commit Messages

Follow semantic commit format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat` | `fix` | `docs` | `style` | `refactor` | `test` | `chore`

**Example:**
```
feat(telegram): Add /status-live command for real-time metrics

Implements live streaming of current cycle metrics to Telegram.
Updates are pushed every 5 seconds during active automation.

Closes #42
```

### Pull Request Process

1. **Create PR against `main` branch**
2. **Include PR title**: Describe the change briefly
3. **Link related issues**: Use `Closes #<issue-number>`
4. **Test locally**: Run `python -m coverage run` and verify 70%+ coverage
5. **Run CI checks**: All GitHub workflows must pass
6. **Request review**: Tag `@Rita-Cordahi` or relevant maintainers

**PR Template** (auto-populated):
```markdown
## Description
Brief summary of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] Coverage >= 70%

## Related Issues
Closes #<issue-number>
```

## Testing Requirements

### Unit Tests

- **Location**: `tests/test_*.py`
- **Minimum coverage**: 70% of modified code
- **Run locally**: `python -m coverage run --source=core -m unittest discover`
- **View coverage**: `python -m coverage report`

### Test File Structure

```python
import unittest
from unittest.mock import patch, MagicMock
from core.module_name import FunctionOrClass


class TestModuleName(unittest.TestCase):
    """Test suite for module_name module."""
    
    def setUp(self):
        """Initialize test fixtures."""
        pass
    
    def tearDown(self):
        """Clean up after tests."""
        pass
    
    def test_function_success_case(self):
        """Test function with valid inputs."""
        result = function_name(valid_input)
        self.assertEqual(result, expected_value)
    
    def test_function_error_case(self):
        """Test function with invalid inputs."""
        with self.assertRaises(ValueError):
            function_name(invalid_input)


if __name__ == "__main__":
    unittest.main()
```

## Documentation

### Updating Docs

- **Location**: `docs/` and root-level `.md` files
- **Format**: Markdown with clear headings and code examples
- **Update README.md** if adding new features users should know about

### Documentation Standards

- Use clear, concise language
- Include code examples for all features
- Link to related documentation
- Update CHANGELOG.md for significant changes

## Reporting Issues

### Bug Reports

Use the **Bug Report** template:
```markdown
**Describe the bug**
Clear description of the issue

**Steps to reproduce**
1. Step one
2. Step two

**Expected behavior**
What should happen

**Actual behavior**
What actually happens

**Environment**
- OS: [Windows 10, Ubuntu 20.04, etc.]
- Python version: [3.11, 3.12, etc.]
- Branch: [main, feature/xyz, etc.]

**Logs**
Relevant error output
```

### Feature Requests

Use the **Feature Request** template:
```markdown
**Is your feature related to a problem?**
Description of the problem

**Describe the solution**
What you want to implement

**Describe alternatives**
Any alternative approaches

**Additional context**
Any other relevant information
```

## Code Review Process

### What We Look For

✅ **Approved if:**
- All tests pass (70%+ coverage)
- Code follows style guidelines
- Documentation is clear
- Commit messages are descriptive
- Changes are focused and not overly broad

❌ **Request changes if:**
- Tests are missing or insufficient
- Code style doesn't match project conventions
- Documentation is unclear
- Large refactoring mixed with feature work

## Release Process

### Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes (1.0.0)
- **MINOR**: New features (1.1.0)
- **PATCH**: Bug fixes (1.0.1)

### Release Checklist

- [ ] All tests pass
- [ ] CHANGELOG.md updated
- [ ] Documentation updated
- [ ] Version bumped in relevant files
- [ ] Tag created: `git tag -a v1.0.0`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] GitHub release notes auto-generated

## Questions?

- 📖 **Documentation**: See [README.md](README.md) and [QUICK_START.md](QUICK_START.md)
- 🐛 **Issues**: Use GitHub Issues for bug reports and features
- 💬 **Discussions**: Use GitHub Discussions for questions and ideas
- 📧 **Email**: Contact project maintainers

---

Thank you for contributing to Project Chronos! 🚀
