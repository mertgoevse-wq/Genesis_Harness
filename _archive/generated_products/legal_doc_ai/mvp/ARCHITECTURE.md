# System Architecture: Legal Doc AI

## Stack

- **Backend**: FastAPI + SQLAlchemy + Pydantic
- **Database**: PostgreSQL (SQLite for local dev/tests)
- **Frontend**: Static HTML/JS SPA
- **Deployment**: Docker + Docker Compose

## Structure

```
backend/
  main.py              # FastAPI app entrypoint
  app/
    config.py          # Settings & environment
    database.py        # SQLAlchemy session & engine
    models/            # Database models
    schemas/           # Pydantic request/response models
    routers/           # API route modules
    core/              # Security helpers
frontend/
  index.html          # SPA entrypoint
database/migrations/  # SQL migrations
docker/               # Container definitions
```
