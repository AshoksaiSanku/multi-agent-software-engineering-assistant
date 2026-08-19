# Lesson-06: Backend Foundation - Python Package, Settings, Logging, App Startup

## Objective

Create the base FastAPI backend application.

## Folders Created

```text
backend
backend/app
backend/app/core
```

## Files Created

```text
backend/requirements.txt
backend/Dockerfile
backend/app/__init__.py
backend/app/main.py
backend/app/core/__init__.py
backend/app/core/config.py
backend/app/core/logging.py
```

## Knowledge Required

- **Python package**: A folder importable by Python.
- **FastAPI**: Backend framework for APIs.
- **ASGI**: Async server interface used by FastAPI.
- **Uvicorn**: Server that runs FastAPI.
- **Pydantic settings**: Typed environment configuration.
- **Logging**: Runtime messages for debugging/operations.
- **Middleware**: Code that runs around requests.

## Data Flow

Application starts -> settings load -> directories are created -> database tables are prepared later -> routers are attached -> app accepts HTTP requests.

## Common Mistakes

- Missing `PYTHONPATH`.
- Forgetting `__init__.py`.
- Starting app before dependencies are installed.
- Hardcoding secrets instead of using config.

## Verification

Later, this stage is verified with:

```powershell
uvicorn app.main:app --reload --port 8000
```

and:

```text
GET /health
```

