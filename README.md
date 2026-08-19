# Multi-Agent AI Software Engineering Assistant

An AI engineering workspace where specialist agents understand GitHub repositories, retrieve
relevant code, generate full-stack feature artifacts, review security and quality, publish
documentation, and score bug risk with ML.

## Capabilities

- JWT registration/login with user-isolated repository, chat, prediction, and agent data.
- GitHub API ingestion, ChromaDB vector indexing, semantic search, and RAG chat.
- LangGraph workflow for requirements, repository understanding, backend/frontend generation,
  documentation, and code review agents.
- Free local RAG answers by default, optional Ollama local LLM support, and optional OpenAI
  only when you explicitly set `AI_PROVIDER=openai`.
- XGBoost bug probability, scikit-learn maintainability score, and recommendation output.
- React/Tailwind dark-mode SaaS UI with live WebSocket agent activity and markdown/code display.
- PDF architecture exports, ZIP generated projects, PostgreSQL, Alembic, Docker, and CI.

## Structure

```text
.
|-- backend/
|   |-- app/
|   |   |-- agents/          # LangGraph agent team
|   |   |-- api/             # REST/WebSocket routes and dependencies
|   |   |-- database/        # SQLAlchemy models/session
|   |   |-- ml/              # training and inference
|   |   |-- services/        # GitHub, AI, chat, exports, jobs
|   |   `-- vector_store/    # Chroma RAG implementation
|   |-- migrations/          # database migrations
|   `-- tests/
|-- frontend/                # React + Vite + Tailwind application
|-- docker/                  # Nginx reverse proxy configuration
|-- docs/                    # architecture, API, deployment guidance
|-- .github/workflows/       # continuous integration
`-- docker-compose.yml
```

Backend domains are kept under `backend/app` as one deployable Python application while
preserving the requested `agents`, `ml`, `services`, `api`, `database`, and `vector_store`
ownership boundaries.

## Quick Start With Docker

Requirements: Docker Desktop. A paid API key is not required.

```bash
cp .env.example .env
# Edit .env: set SECRET_KEY and optionally GITHUB_TOKEN
docker compose up --build
```

Open the web application at `http://localhost:3000`. The API documentation is exposed at
`http://localhost:8000/docs`.

The default `AI_PROVIDER=local` uses free deterministic local answers and local hashed
embeddings, so it never calls paid APIs. For stronger free answers, install Ollama and run:

```bash
ollama pull qwen2.5-coder:1.5b
```

Then set `AI_PROVIDER=ollama`. Set `AI_PROVIDER=openai` only if you intentionally want paid
OpenAI calls.

## GitHub Rate Limits

Repository upload uses GitHub APIs. If you see `403 rate limit exceeded`, create a free GitHub
personal access token, set it in `.env`, and restart the backend:

```env
GITHUB_TOKEN=github_pat_your_token_here
```

This token is only for GitHub repository access. It is not a paid AI API key.

## Local Development

Backend:

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
copy ..\.env.example .env
# For zero-setup local storage set DATABASE_URL=sqlite+aiosqlite:///./assistant.db
# Also set CHROMA_PATH=./data/chroma and ML_MODEL_PATH=./models
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm ci
npm run dev
```

For PostgreSQL-backed local development, run only the database container and set
`DATABASE_URL=postgresql+asyncpg://assistant:assistant@localhost:5432/assistant`.

## Training ML Models

The API automatically trains starter artifacts from a reproducible synthetic dataset if model
files do not exist. For real predictions, supply a CSV containing the four feature columns plus
`bug_prone` and `maintainability` labels:

```bash
cd backend
python scripts/train_models.py --input data/labeled_defects.csv --output models
```

Input features are cyclomatic complexity, file size, dependency count, and commit frequency.
The synthetic seed is for product demonstration, not release gating.

## Configuration

Important variables in `.env.example`:

| Variable         | Description                                                   |
| ---------------- | ------------------------------------------------------------- |
| `SECRET_KEY`     | Long random JWT signing secret; mandatory in production       |
| `APP_ENV`        | Set to `production` in deployed environments                  |
| `DATABASE_URL`   | Async SQLAlchemy PostgreSQL or local SQLite URL               |
| `AI_PROVIDER`    | `local`, `ollama`, or `openai`; defaults to free `local`      |
| `OLLAMA_BASE_URL` | Local Ollama server URL when using `AI_PROVIDER=ollama`      |
| `OLLAMA_MODEL`   | Free local Ollama model name                                  |
| `OPENAI_API_KEY` | Optional; used only when `AI_PROVIDER=openai`                 |
| `OPENAI_MODEL`   | OpenAI generation model when paid OpenAI mode is selected     |
| `GITHUB_TOKEN`   | Optional; increases GitHub API capacity/private access policy |
| `CHROMA_PATH`    | Persistent vector database location                           |
| `ML_MODEL_PATH`  | Persisted trained model location                              |
| `CORS_ORIGINS`   | Allowed frontend origins                                      |

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API reference](docs/API.md)
- [Deployment guidance](docs/DEPLOYMENT.md)

## Security Notes

Repository excerpts are treated as untrusted model context to reduce prompt-injection risk.
Do not expose GitHub or optional AI provider keys to the frontend. Production deployments should add a
managed secrets store, TLS, Redis-based distributed throttling/events, worker queues,
dependency scanning, backups, and organization-specific authorization controls.
