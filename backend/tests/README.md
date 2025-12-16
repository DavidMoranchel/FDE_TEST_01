# Tests

Unit tests for the backend application.

## Running Tests

```bash
# Ejecutar todos los tests con coverage
docker-compose exec backend pytest --cov=app --cov-report=html --cov-report=term
```

## Ver Reporte de Coverage

El reporte HTML se genera dentro del contenedor pero está disponible en tu máquina local gracias al volumen montado. Simplemente abre:

```
backend/htmlcov/index.html
```

Desde tu editor o navegador.

## Test Structure

- `tests/unit/` - Unit tests for services and core utilities
- `tests/conftest.py` - Shared fixtures and mocks

## Coverage

**Coverage actual: ~31%** (enfoque en lógica de negocio)

**Componentes testeados:**
- ✅ AuthService (register, login) - 100%
- ✅ ProjectService (CRUD operations, role-based filtering) - 97%
- ✅ CommentService (create, get by project) - 100%
- ✅ Security utilities (password hashing, JWT tokens) - 100%

**No testeados (por diseño):**
- Infrastructure layer (repositorios, modelos SQLAlchemy)
- API endpoints (FastAPI routes)
- External libraries

