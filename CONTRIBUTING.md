# Contributing to MediSense-AI

Thank you for your interest in contributing to MediSense-AI! We welcome contributions from the community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)

## Code of Conduct

This project adheres to the Contributor Covenant [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Harikrishnan.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit with a descriptive message
7. Push to your fork
8. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15 (or use Docker)
- Redis 7 (or use Docker)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your configuration
```

### Running with Docker

```bash
docker-compose up --build
```

## How to Contribute

### Types of Contributions

- **Bug Fixes**: Fix issues in existing code
- **New Features**: Add new functionality
- **Documentation**: Improve or add documentation
- **Tests**: Add or improve test coverage
- **Performance**: Optimize existing code
- **Refactoring**: Improve code quality without changing functionality

### Contribution Workflow

1. **Check Existing Issues**: Look for existing issues or create a new one
2. **Discuss**: For major changes, discuss in an issue first
3. **Implement**: Write your code following our standards
4. **Test**: Ensure all tests pass and add new tests
5. **Document**: Update documentation as needed
6. **Submit**: Open a pull request with a clear description

## Coding Standards

### Python (Backend)

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where possible
- Maximum line length: 100 characters
- Use `black` for code formatting
- Use `isort` for import sorting
- Use `flake8` for linting
- Use `mypy` for type checking

```bash
# Format code
black backend/app/
isort backend/app/

# Lint
flake8 backend/app/

# Type check
mypy backend/app/
```

### TypeScript (Frontend)

- Follow TypeScript best practices
- Use ESLint for linting
- Use Prettier for formatting
- Prefer functional components with hooks
- Use meaningful component and variable names

```bash
# Lint and format
npm run lint
npm run format
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(agents): add new symptom analysis agent

Implement new agent for analyzing patient symptoms using
advanced ML models.

Closes #123
```

```
fix(auth): resolve JWT token expiration issue

Fix bug where tokens were expiring prematurely due to
timezone mismatch.

Fixes #456
```

## Testing Guidelines

### Backend Tests

- Write tests for all new features
- Maintain or improve code coverage (target: >80%)
- Use `pytest` for testing
- Use `pytest-asyncio` for async tests
- Mock external dependencies

```bash
# Run tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest app/tests/test_agents.py::test_routing_agent
```

### Frontend Tests

- Write tests for components and utilities
- Use React Testing Library
- Test user interactions, not implementation details

```bash
# Run tests
npm test

# With coverage
npm test -- --coverage
```

### Integration Tests

- Test complete workflows
- Use test database (not production!)
- Clean up test data after tests

## Pull Request Process

1. **Update Documentation**: Ensure README and docs are updated
2. **Add Tests**: Include tests for new functionality
3. **Pass CI**: Ensure all CI checks pass
4. **Code Review**: Address review comments
5. **Squash Commits**: Squash commits if requested
6. **Merge**: Maintainers will merge after approval

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings
```

## Reporting Bugs

### Before Submitting

1. Check existing issues
2. Update to latest version
3. Collect relevant information

### Bug Report Template

```markdown
**Describe the bug**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. Go to '...'
2. Click on '...'
3. See error

**Expected behavior**
What should happen

**Screenshots**
If applicable, add screenshots

**Environment:**
- OS: [e.g. Ubuntu 22.04]
- Python version: [e.g. 3.11.5]
- Docker version: [e.g. 24.0.6]

**Additional context**
Any other relevant information
```

## Suggesting Enhancements

### Enhancement Template

```markdown
**Is your feature request related to a problem?**
Clear description of the problem

**Describe the solution you'd like**
Clear description of desired solution

**Describe alternatives considered**
Alternative solutions or features

**Additional context**
Any other relevant information
```

## Code Review Process

### For Contributors

- Be open to feedback
- Respond to comments promptly
- Make requested changes
- Ask questions if unclear

### For Reviewers

- Be respectful and constructive
- Focus on code, not the person
- Suggest improvements with examples
- Approve when ready

## Additional Resources

- [Architecture Documentation](design/architecture.md)
- [MCP API Specification](docs/MCP_API_SPEC.md)
- [Guardrails Documentation](docs/GUARDRAILS.md)
- [RLHF Guide](docs/RLHF_README.md)

## Questions?

- Open an issue with the `question` label
- Contact maintainers at [medisense@example.com](mailto:medisense@example.com)

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for contributing to MediSense-AI! 🎉
