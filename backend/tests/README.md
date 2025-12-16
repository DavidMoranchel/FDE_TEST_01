# Tests

Unit tests for the backend application.

## Running Tests

```bash
# Run all tests with coverage
docker-compose exec backend pytest --cov=app --cov-report=html --cov-report=term
```

## Coverage Report

The HTML report is generated inside the container but available locally via mounted volume. Open:

```
backend/htmlcov/index.html
```

## Test Structure

- `tests/unit/` - Unit tests for services and core utilities
- `tests/conftest.py` - Shared fixtures and mocks

## Coverage

**Current coverage: ~31%** (focused on business logic)

**Tested components:**
- ✅ AuthService (register, login) - 100%
- ✅ ProjectService (CRUD operations, role-based filtering) - 97%
- ✅ CommentService (create, get by project) - 100%
- ✅ Security utilities (password hashing, JWT tokens) - 100%

**Not tested (by design):**
- Infrastructure layer (repositories, SQLAlchemy models)
- API endpoints (FastAPI routes)
- External libraries
