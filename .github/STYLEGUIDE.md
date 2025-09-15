# Development Style Guide

## [Русская версия](STYLEGUIDE-RU.md)

## 1. Project Structure
### 1.1 Module and Package Organization
- Each independent component should be separated into a dedicated module (`.py` file)
- Groups of related modules should be combined into packages (directories with `__init__.py`)
- Example packages: `database`, `payment_system`, `utils`

## 2. Naming Conventions
### 2.1 Packages
Format: `[subsystem]_[context]` (optional underscore separator)
Examples:
```plaintext
menu_general  # with subsystem specification
s3
database
payment_system
```

### 2.2 Modules
Format: `[functional_purpose].py`
Examples:
```python
handlers.py
schemas.py
services.py
```

### 2.3 Components
Format: `[context]_[component_type]`
Examples:
```python
# Routers
@menu_general_router.message()

# Handlers
def send_welcome_handler()

# Keyboards
welcome_inline_kb
general_menu_reply_kb
```

## 3. Code Documentation
### 3.1 Single-line Comments
- Placed above the code being commented
- Used for brief explanations and TODO notes

Example:
```python
# Initialize cache with 300-second TTL
cache = LRUCache(ttl=300)

# TODO: Add exception handling
```

### 3.2 Multi-line Documentation (Docstrings)
- Enclosed in triple quotes
- Placed immediately after object declaration
- Supports autodocumentation and IDE hints

Structure:
1. Brief purpose
2. Workflow logic
3. Parameters
4. Return values

Example:
```python
def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculates Euclidean distance between two points.

    :param x1: X coordinate of first point
    :param y1: Y coordinate of first point
    :param x2: X coordinate of second point
    :param y2: Y coordinate of second point
    :return: Distance between points rounded to 2 decimals
    """
    return round(((x2-x1)**2 + (y2-y1)**2)**0.5, 2)
```

## 4. Working with Pydantic Schemas
### 4.1 Organization
- Name modules as `[context]_schemas.py`
- Group schemas by data flow directions

### 4.2 Naming Conventions
- Use CamelCase with data flow suffix
- Examples:
  - `UserCreateInput`
  - `PaymentDetailsOutput`
  - `ProfileUpdateRequest`

### 4.3 Typing and Relationships
- Mandatory field type declarations
- Use postponed imports for schema relationships

Example:
```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .payment_schemas import PaymentSchemaOutput

class OrderSchemaOutput(BaseModel):
    total: float
    payment_details: "PaymentSchemaOutput"
```

## 5. Code Styling
### 5.1 Automated Checks
Use pre-commit with linters:
```bash
# Installation
uv run pre-commit install

# Run checks
uv run pre-commit run -a
```

### 5.2 Core Rules
- PEP8 compliance
- Maximum line length 120 characters
- Type hints for all public methods
- Automatic formatting with ruff and isort

## 6. Git Workflow
### 6.1 Branching
Branch name format: `surname/task_name` or `surname/task_number`
Example: `ivanov/payment_integration` or `ivanov/task_42`

### 6.2 Commits
Format: `type: description` (Conventional Commits)

| Type      | Purpose                                      |
|-----------|----------------------------------------------|
| feat      | New feature                                 |
| fix       | Bug fixes                                   |
| docs      | Documentation changes                       |
| style     | Code formatting                             |
| refactor  | Code refactoring without functional changes |
| test      | Test modifications                          |
| chore     | Dependency/config updates                   |

Example: `feat: add user registration endpoint`

### 6.3 Code Review Process
1. Create branch from `main`
2. Implement changes and push
3. Create Pull Request
4. Complete code review
5. Make revisions (if required)
6. Merge after approval

---

This guide is mandatory for all project participants. Improvement suggestions are welcome via repository Issues.
