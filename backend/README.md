# Backend - Client Portal API

FastAPI backend with hexagonal architecture for the Client Portal application.

## Architecture

This project follows **Hexagonal Architecture** (Ports and Adapters):

- **Domain**: Business entities and logic (User, Project, Comment)
- **Application**: Use cases and services (AuthService, ProjectService, CommentService)
- **Infrastructure**: Database models, repositories implementation
- **Adapters**: HTTP controllers (FastAPI routes)

## Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

### Running with Docker Compose

From the project root:

```bash
docker-compose up
```

This will:
- Start PostgreSQL database
- Run Alembic migrations
- Start FastAPI server on http://localhost:8000

### API Documentation

Once running, access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Local Development

1. Create virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and configure

4. Run migrations:
```bash
alembic upgrade head
```

5. Start server:
```bash
uvicorn app.main:app --reload
```

## Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

## Project Structure

```
backend/
├── app/
│   ├── domain/              # Business entities
│   ├── application/         # Use cases and services
│   │   ├── interfaces/      # Repository interfaces
│   │   └── services/        # Business logic
│   ├── infrastructure/      # External concerns
│   │   ├── database.py     # SQLAlchemy setup
│   │   ├── models/         # SQLAlchemy models
│   │   └── repositories/   # Repository implementations
│   ├── adapters/           # Adapters layer
│   │   └── api/            # FastAPI routes
│   ├── core/               # Configuration and utilities
│   └── main.py             # FastAPI app
├── alembic/                # Database migrations
├── requirements.txt
└── Dockerfile
```
