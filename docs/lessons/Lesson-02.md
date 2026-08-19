# Lesson-02: Architecture, System Diagrams, and Folder Structure

## Objective

Understand the complete architecture before creating code. You will learn why the project is split into backend, frontend, docs, docker, and CI folders.

## Prerequisites

Complete Lesson 01. You should know what frontend, backend, database, API, RAG, agents, and Docker mean at a basic level.

## Concepts

- **Architecture**: The high-level design of how software parts communicate.
- **Folder structure**: The physical organization of files in the repository.
- **Layered design**: Separating responsibilities so UI, API, services, database, ML, and deployment do not become tangled.
- **Data flow**: The path data takes from input to output.
- **Control flow**: The order in which functions/components execute.

## Complete Architecture

```text
Browser
  |
  v
React + Vite + Tailwind Frontend
  |
  v
FastAPI Backend
  |
  +--> SQLAlchemy ORM
  |       |
  |       +--> PostgreSQL in Docker
  |       +--> SQLite in local/test mode
  |
  +--> GitHub API
  |
  +--> ChromaDB Vector Store
  |
  +--> AIService
  |       +--> local deterministic mode
  |       +--> optional Ollama
  |       +--> optional OpenAI
  |
  +--> LangGraph Agent Workflow
  |
  +--> XGBoost / scikit-learn ML Models
  |
  +--> ReportLab PDF / ZipFile ZIP exports
```

## Folder Creation

When rebuilding from scratch, create this root structure first:

```text
Multi-Agent Software Engineering Assistant
├── .github
│   └── workflows
├── backend
│   ├── app
│   ├── migrations
│   ├── scripts
│   └── tests
├── docker
├── docs
└── frontend
    └── src
```

## Why Each Folder Exists

### `.github`

Purpose: Contains GitHub Actions workflows. GitHub Actions is a CI tool that runs checks automatically when code changes.

Knowledge Required: GitHub, YAML, CI, push/pull request triggers.

### `backend`

Purpose: Contains the Python server application.

Knowledge Required: Python, FastAPI, async programming, REST APIs, databases, ML, AI workflow orchestration.

### `frontend`

Purpose: Contains the browser application.

Knowledge Required: HTML, CSS, JavaScript, React, Vite, Tailwind, browser APIs.

### `docs`

Purpose: Contains human-readable documentation and these lessons.

Knowledge Required: Markdown, technical writing, architecture explanation.

### `docker`

Purpose: Contains Nginx reverse proxy configuration used by Docker deployment.

Knowledge Required: Docker, Nginx, HTTP, reverse proxying, WebSockets.

## Data Flow Diagrams

### Authentication Flow

```text
Login form
  -> POST /api/v1/auth/login
  -> backend verifies password hash
  -> backend signs JWT
  -> frontend stores token
  -> future requests include Authorization header
```

### Repository Ingestion Flow

```text
GitHub URL
  -> repository route
  -> repository row saved as queued
  -> background ingestion
  -> GitHub API fetches files
  -> files become chunks
  -> chunks become embeddings
  -> embeddings stored in Chroma
  -> metadata stored in SQL database
  -> repository status becomes ready
```

### Agent Flow

```text
User requirements
  -> agent run route
  -> background workflow
  -> requirements agent
  -> repository understanding agent
  -> backend generation agent
  -> frontend generation agent
  -> documentation agent
  -> code review agent
  -> generated project saved
  -> live events streamed over WebSocket
```

## Commands

No commands are required yet if the project folder already exists. In a brand-new folder, use VS Code Explorer to create folders manually so you learn where each part belongs.

## Common Mistakes

- Creating frontend files inside backend.
- Creating backend files inside frontend.
- Putting business logic directly inside route files.
- Forgetting that generated folders like `node_modules`, `dist`, `venv`, and `__pycache__` should not be manually written.

## Verification

You should be able to explain:

1. Why the backend exists.
2. Why the frontend exists.
3. Why there is a database.
4. Why ChromaDB is separate from PostgreSQL.
5. Why Docker files are outside the backend and frontend source folders.

## Summary

This lesson gave you the map. Future lessons build each layer in order.

