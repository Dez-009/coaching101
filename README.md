# Vida Coach Admin Agent Orchestration System

This project contains the foundational specifications for building the Admin Agent Orchestration System for **Vida Coach**. The system coordinates multiple agents for NLP processing, database querying, security auditing, analytics, performance optimization, and integration testing.

## Key Features
- **FastAPI** backend with SQLAlchemy, Pydantic, and PostgreSQL
- **Next.js 14** frontend using Tailwind CSS, ShadCN, and Zustand
- **Admin Agents** for orchestration, NLP, database operations, security & audit, analytics & reporting, performance optimization, and testing
- **AI-powered** journaling, coaching, PDF export, wearable sync, and admin oversight

## Development Quickstart
```bash
# Run backend tests
pytest -q

# Run frontend development server (requires Node.js and a package.json)
npm run dev
```

Currently no tests or frontend code exist, so the commands above produce no tests and fail without a package.json.

## Documentation Structure
- `agents.md` – Agent specifications for the Admin Orchestration System
- `README.md` – Project overview (this file)

Additional docs will be added as the codebase grows.
