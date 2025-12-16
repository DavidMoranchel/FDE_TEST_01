# Client Portal - Technical Assessment

Full-stack application for managing projects and client communication.

## Quick Start

```bash
# Start all services (PostgreSQL, Backend, Frontend)
docker-compose up -d

# Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Project Structure

This project is organized into separate directories, each with its own README:

- **[`backend/`](./backend/README.md)** - FastAPI backend with hexagonal architecture
- **[`frontend/`](./frontend/README.md)** - React + TypeScript + Vite frontend
- **[`backend/tests/`](./backend/tests/README.md)** - Unit tests and coverage

## Features

- **Authentication**: JWT-based auth with Admin and Client roles
- **Project Management**: CRUD operations with role-based access
- **Comments**: Project commenting system
- **Dashboards**: Role-specific views (Admin/Client)

## Tech Stack

- **Backend**: FastAPI, PostgreSQL, SQLAlchemy, Alembic
- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **Infrastructure**: Docker Compose

## Documentation

For detailed information about each component, see:
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
- [Tests README](./backend/tests/README.md)
