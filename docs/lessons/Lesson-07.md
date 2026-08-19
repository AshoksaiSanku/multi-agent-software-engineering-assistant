# Lesson-07: Database Layer - SQLAlchemy Models, Sessions, Alembic

## Objective

Create the database foundation.

## Folders Created

```text
backend/app/database
backend/migrations
backend/migrations/versions
```

## Files Created

```text
backend/app/database/__init__.py
backend/app/database/session.py
backend/app/database/models.py
backend/alembic.ini
backend/migrations/env.py
backend/migrations/versions/0001_initial_schema.py
```

## Knowledge Required

- **Relational database**: Stores data in tables.
- **Table**: Collection of rows with columns.
- **Primary key**: Unique row identifier.
- **Foreign key**: Links one table to another.
- **ORM**: Object-relational mapper; maps Python classes to tables.
- **SQLAlchemy**: Python ORM used here.
- **Async database access**: Non-blocking database operations.
- **Alembic**: Migration tool.

## Tables Implemented

- `users`
- `repositories`
- `embeddings`
- `conversations`
- `ml_predictions`
- `generated_projects`
- `agent_logs`

## Common Mistakes

- Forgetting ownership fields like `user_id`.
- Not committing sessions.
- Using sync drivers with async URLs.
- Changing models without migrations.

## Verification

Backend startup should create tables locally, and Docker startup should run Alembic migrations.

