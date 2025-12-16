# Frontend - Client Portal

React + TypeScript + Vite frontend application.

## Quick Start

From project root:

```bash
docker-compose up
```

Frontend available at http://localhost:5173

## Tech Stack

- **React 19** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **TanStack Query** - Server state management
- **React Router** - Routing
- **React Hook Form + Zod** - Form handling and validation

## Project Structure

```
frontend/
├── src/
│   ├── api/              # API client and hooks
│   ├── components/       # Reusable components
│   ├── contexts/         # React contexts (Auth, Query)
│   ├── features/         # Feature-based modules
│   ├── hooks/            # Custom hooks
│   ├── pages/            # Page components
│   ├── routes/           # Route configuration
│   └── types/             # TypeScript types
└── package.json
```

## Development

The frontend runs in development mode with hot-reload enabled when using Docker Compose.
