# Architecture

## System overview

The platform is a Docker-first React and FastAPI monorepo. The API owns authentication,
persistence, repository indexing, AI orchestration, ML inference, and exports. React consumes
versioned REST endpoints and a protected WebSocket stream.

```text
Browser -> Nginx -> FastAPI -> PostgreSQL
                       |----> ChromaDB persistent vectors
                       |----> GitHub REST API
                       |----> Local RAG / optional Ollama / optional OpenAI
                       |----> XGBoost / scikit-learn model artifacts
```

## Backend boundaries

| Package | Ownership |
| --- | --- |
| `app/api` | HTTP/WebSocket transport, JWT dependencies, validation |
| `app/services` | GitHub ingestion, chat, agent execution, export behavior |
| `app/agents` | LangGraph workflow and specialist agent prompts |
| `app/vector_store` | Chroma collections and embedding strategy |
| `app/ml` | training, inference, recommendations |
| `app/database` | SQLAlchemy models and sessions |

Specialist agents execute in this order: requirement analysis, repository understanding,
backend generation, frontend generation, documentation, and code review. Agent output and
status events are persisted, and generated deliverables can be downloaded as a ZIP.

## RAG pipeline

1. A user submits a GitHub repository URL.
2. The API uses the GitHub API to read permitted text/code files with file-count and size caps.
3. Files are line-preserving chunks and embedded into a per-repository Chroma collection.
4. By default, a local hashing vectorizer stores embeddings without transmitting source code.
5. If `AI_PROVIDER=ollama`, responses use a local free Ollama model.
6. If `AI_PROVIDER=openai`, OpenAI generation and embeddings are used intentionally.
7. Chat and agent workflows retrieve relevant chunks and place them in a guarded prompt.

## Data and security

Every repository, conversation, generated project, prediction, and agent event is scoped to a
JWT-authenticated user. Passwords are Argon2-hashed. API inputs use Pydantic validation,
WebSocket subscriptions check ownership, basic rate limiting protects the API, and source
content is explicitly treated as untrusted prompt data.

For multi-instance deployment, replace the in-process rate limiter and WebSocket event hub
with Redis-backed implementations and move long-running indexing/agent jobs to a worker queue.
