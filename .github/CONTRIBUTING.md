# Project Contributor Guide

## [Русская версия](CONTRIBUTING-RU.md)

## Getting Started

### Requirements
- Python 3.12+
- uv (dependency manager)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/proDreams/taiga_wh_notifier.git && cd taiga_wh_notifier
```
2. Install dependencies:
```bash
uv sync
```
1. Configure pre-commit:
```bash
uv run pre-commit install
```

## Development Process

### Task Selection
- Choose a task from the [Issues list](https://github.com/proDreams/taiga_wh_notifier/issues) or [project task board](https://tasks.pressanybutton.ru/project/taiga-webhook-telegram-notifier/timeline)
- Ensure the task isn't assigned to another developer

### Branching
Create a branch using the template:
`<surname>/<brief_task_description>` or `<surname>/<task_number>`

Examples:
```bash
git checkout -b ivanov/add_payment_webhook

git checkout -b ivanov/task_42
```

### Commits
Follow [Conventional Commits](https://www.conventionalcommits.org/):
```bash
git commit -m "feat: add payment webhook handler"
```

Allowed commit types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Dependency updates

## Code Review

### Pull Request Requirements
2. Link to related task in description
3. Full description of changes
4. Successful CI/CD pipeline
5. Code style compliance (verified by pre-commit)

PR template example:
```markdown
## Change Description
- Added payment webhook handler
- Updated API documentation

Related task: #123
```

### Review Process
6. Assign team reviewers
7. Address comments directly in PR
8. Push fixes to the same branch
9. Merge to main after 2 approvals

## Code Style

Follow the [STYLE GUIDE](STYLEGUIDE.md).

Key rules:
- Type hints for all public methods
- Google-style docstrings documentation
- Code formatting via ruff and isort

Before committing:
```bash
uv run pre-commit run -a
```

## Getting Help

If stuck:
10. Check closed Issues
11. Write to the [project Telegram chat](https://t.me/+Li2vbxfWo0Q4ZDk6)
12. Create an Issue with `question` label

---

Thank you for your contribution! Every edit helps improve the project.
