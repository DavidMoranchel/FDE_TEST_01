# Backend - Client Portal API

FastAPI backend with hexagonal architecture.

## Quick Start

From project root:

```bash
docker-compose up
```

API available at http://localhost:8000
- Swagger UI: http://localhost:8000/docs

## Architecture

**Hexagonal Architecture** (Ports and Adapters):

- **Domain**: Entities (`entities/`) and value objects (`value_objects/`)
- **Application**: Services (business logic)
- **Infrastructure**: Database models and repository implementations
- **Adapters**: FastAPI routes

## Project Structure

```
backend/
├── app/
│   ├── domain/
│   │   ├── entities/       # User, Project, Comment
│   │   ├── value_objects/   # UserRole, ProjectStatus
│   │   └── repositories/    # Repository interfaces
│   ├── application/
│   │   └── services/        # AuthService, ProjectService, CommentService
│   ├── infrastructure/
│   │   ├── models/         # SQLAlchemy models
│   │   └── repositories/   # Repository implementations
│   ├── adapters/
│   │   └── api/v1/        # FastAPI routes
│   ├── core/              # Config, security, database
│   └── main.py            # FastAPI app
├── alembic/               # Migrations
└── requirements.txt
```

## Testing

See [tests/README.md](./tests/README.md) for testing instructions.
