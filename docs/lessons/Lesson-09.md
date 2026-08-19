# Lesson-09: API Router, Dependencies, Middleware, and Route Conventions

## Objective

Create the shared API structure used by all feature modules.

## Files Created

```text
backend/app/api/__init__.py
backend/app/api/router.py
backend/app/api/middleware.py
backend/app/api/routes/__init__.py
backend/app/schemas.py
```

## Knowledge Required

- **Router**: A group of API endpoints.
- **Dependency injection**: FastAPI feature that provides common inputs like DB session/current user.
- **Middleware**: Request wrapper logic.
- **Pydantic schema**: Defines input/output shape.
- **HTTP status code**: Numeric result code for requests.

## Responsibilities

- `router.py`: Combines route modules.
- `middleware.py`: Rate limiting.
- `schemas.py`: API request/response contracts.

## Common Mistakes

- Route prefix mismatch.
- Forgetting response models.
- Duplicating schemas.
- Putting business logic in route composition.

## Verification

FastAPI docs should list grouped endpoints under `/docs` once all routes exist.

