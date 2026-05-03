# Contributing to Real-Time Patient Monitoring System

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone <your-fork>`
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Set up development environment: `docker-compose up`

## Development Workflow

### Local Development

```bash
# Start services
docker-compose up

# Run backend
cd backend
python -m uvicorn app.main:app --reload

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

### Code Style

- Python: Follow PEP 8
- Use `black` for formatting
- Use `flake8` for linting
- Use `mypy` for type checking

```bash
pip install black flake8 mypy
black backend/
flake8 backend/
mypy backend/
```

### Testing

- Write unit tests for all new features
- Maintain minimum 80% code coverage
- Run tests locally before pushing

```bash
pytest tests/ -v --cov=app
```

### Kubernetes Manifests

- Test manifests locally with Minikube/Kind
- Validate YAML: `kubectl apply --dry-run=client -f manifest.yaml`
- Use namespace selectors for isolation

### Helm Charts

- Lint charts: `helm lint ./helm/patient-monitoring`
- Template validation: `helm template ./helm/patient-monitoring`
- Test with different values files

## Commit Messages

Follow conventional commits:

```
type(scope): subject

feat(api): add patient endpoint
fix(database): handle connection timeout
docs(README): update deployment instructions
test(backend): add unit tests for metrics
chore(deps): update dependencies
```

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Create descriptive PR title and description
6. Request review from maintainers

## Reporting Issues

- Use GitHub issues for bug reports
- Include:
  - Description of the issue
  - Steps to reproduce
  - Expected vs actual behavior
  - Environment details (OS, K8s version, etc.)

## Security

For security issues, please email security@patient-monitoring.example.com instead of using GitHub issues.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Questions? Open an issue or contact the maintainers.
