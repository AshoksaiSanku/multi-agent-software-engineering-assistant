# Multi-Agent Software Engineering Assistant - Complete Project Tree Guide

This document is a rebuild guide and interview study map for the manually written parts of the project. It intentionally does not expand generated dependency folders, cache folders, compiled files, databases, model binaries, virtual environments, or build output.

## Global Knowledge Required

Before rebuilding the full project, learn these concepts:

- **Python**: A backend programming language used here for FastAPI, database access, ML, agents, scripts, and tests.
- **FastAPI**: A Python web framework for building REST APIs and WebSocket endpoints. It provides routing, dependency injection, validation through Pydantic, and automatic OpenAPI docs.
- **REST API**: A request/response HTTP interface where the frontend calls backend endpoints such as `POST /auth/login` or `GET /repositories`.
- **WebSocket**: A persistent browser-to-server connection used here to stream live agent run events.
- **Pydantic**: A Python validation library used to define request/response schemas and settings.
- **SQLAlchemy async ORM**: A Python database toolkit used to map Python classes to database tables and perform async database operations.
- **PostgreSQL**: The production-style relational database used by Docker Compose.
- **SQLite**: A local file database used as the default development/test fallback.
- **Alembic**: A database migration tool that creates and applies schema changes.
- **JWT**: JSON Web Token authentication. The backend signs a token after login, and the frontend sends it in the `Authorization` header.
- **Argon2 password hashing**: A secure one-way password hashing approach used so raw passwords are never stored.
- **GitHub REST API**: Used to read repository metadata, file trees, and source files.
- **RAG**: Retrieval-Augmented Generation. The system retrieves relevant repository chunks before generating an answer.
- **Embedding**: A numeric representation of text used for semantic search.
- **Vector database**: A database optimized for storing embeddings and finding similar vectors.
- **ChromaDB**: The vector database used to persist repository code chunks.
- **HashingVectorizer**: A scikit-learn local text vectorizer used as a free embedding fallback.
- **LLM**: Large Language Model. The project supports deterministic local answers, optional Ollama, and optional OpenAI.
- **Ollama**: A local LLM runtime. It can answer without paid cloud APIs.
- **OpenAI API**: Optional cloud AI provider enabled only when `AI_PROVIDER=openai`.
- **LangGraph**: A workflow library used to define the ordered multi-agent pipeline.
- **LangChain**: Used for prompt template helpers around agent prompts.
- **Machine Learning**: The project uses XGBoost classification and RandomForest regression to predict code risk.
- **React**: A JavaScript frontend library for building component-based user interfaces.
- **Vite**: A frontend build/dev server used for fast React development.
- **Tailwind CSS**: A utility-first CSS framework used for styling.
- **React Router**: Client-side routing for pages such as dashboard, chat, agents, and ML.
- **Nginx**: A web server/reverse proxy used in the production frontend container.
- **Docker**: Containerization tool used to package backend, frontend, database, and Nginx.
- **Docker Compose**: Runs multiple containers together for local production-style deployment.
- **Pytest**: Python testing framework.
- **GitHub Actions**: CI automation for backend tests and frontend build.

## Hierarchical Tree

```text
Multi-Agent Software Engineering Assistant [Full-stack AI engineering workspace. Combines React UI, FastAPI API, JWT auth, GitHub ingestion, Chroma RAG, LangGraph agents, ML predictions, PDF/ZIP exports, Docker deployment, and CI.]
├── .github [CI automation folder. Contains GitHub Actions workflows that validate backend and frontend changes.]
│   └── workflows [GitHub Actions workflow definitions.]
│       └── ci.yml [Runs backend Python compile/tests and frontend npm build on push/PR.]
├── backend [Python FastAPI application. Owns auth, database, repository ingestion, RAG, AI providers, agents, ML, documents, and tests.]
│   ├── app [Main backend source package.]
│   │   ├── __init__.py [Marks app as a Python package.]
│   │   ├── main.py [FastAPI entrypoint. Creates app, middleware, routers, startup lifecycle, health endpoint.]
│   │   ├── schemas.py [Pydantic request/response models shared by routes.]
│   │   ├── agents [LangGraph workflow package.]
│   │   │   ├── __init__.py [Package marker.]
│   │   │   └── workflow.py [Defines six-step specialist agent workflow.]
│   │   ├── api [HTTP/WebSocket transport layer.]
│   │   │   ├── __init__.py [Package marker.]
│   │   │   ├── dependencies.py [JWT current-user dependency.]
│   │   │   ├── middleware.py [In-process rate limiter.]
│   │   │   ├── router.py [Combines all feature routers under /api/v1.]
│   │   │   └── routes [Feature-specific API endpoints.]
│   │   │       ├── __init__.py [Package marker.]
│   │   │       ├── analysis.py [Architecture analysis endpoint.]
│   │   │       ├── agents.py [Agent run, log, project, delete, and WebSocket endpoints.]
│   │   │       ├── auth.py [Register, login, current user endpoints.]
│   │   │       ├── chat.py [Repository-aware chat and history endpoints.]
│   │   │       ├── documents.py [PDF and ZIP export endpoints.]
│   │   │       ├── ml.py [Metric estimation, prediction, prediction history endpoints.]
│   │   │       └── repositories.py [GitHub repo CRUD and semantic search endpoints.]
│   │   ├── core [Cross-cutting backend configuration/security/logging.]
│   │   │   ├── __init__.py [Package marker.]
│   │   │   ├── config.py [Environment settings and runtime paths.]
│   │   │   ├── logging.py [Logging configuration helper.]
│   │   │   └── security.py [Password hashing and JWT helpers.]
│   │   ├── database [Persistence layer.]
│   │   │   ├── __init__.py [Package marker.]
│   │   │   ├── models.py [SQLAlchemy table models.]
│   │   │   └── session.py [Async database engine/session factory.]
│   │   ├── ml [Machine-learning layer.]
│   │   │   ├── __init__.py [Package marker.]
│   │   │   ├── metrics.py [Estimates code metrics from indexed repository files.]
│   │   │   ├── predictor.py [Loads/trains model artifacts and performs predictions.]
│   │   │   └── training.py [Creates seed data and trains XGBoost/RandomForest models.]
│   │   ├── services [Business logic layer between routes and infrastructure.]
│   │   │   ├── __init__.py [Package marker.]
│   │   │   ├── agent_service.py [Executes workflow, records events, streams WebSocket updates.]
│   │   │   ├── ai_service.py [Local/Ollama/OpenAI generation boundary.]
│   │   │   ├── analysis_service.py [Builds architecture reports from retrieved context.]
│   │   │   ├── chat_service.py [RAG chat orchestration and conversation persistence.]
│   │   │   ├── export_service.py [Builds project ZIPs and architecture PDFs.]
│   │   │   ├── generated_project_service.py [Deletes generated project metadata/artifacts.]
│   │   │   ├── github_service.py [Reads repository files through GitHub APIs.]
│   │   │   └── repository_service.py [Chunks files, indexes vectors, builds repository summaries.]
│   │   └── vector_store [Vector search infrastructure.]
│   │       ├── __init__.py [Package marker.]
│   │       └── store.py [ChromaDB collections, embeddings, indexing, querying.]
│   ├── migrations [Alembic database migration project.]
│   │   ├── env.py [Alembic runtime configuration.]
│   │   └── versions [Migration files.]
│   │       └── 0001_initial_schema.py [Initial table schema migration.]
│   ├── scripts [Manual utility scripts.]
│   │   └── train_models.py [CLI for training ML models from optional CSV.]
│   ├── tests [Pytest backend test suite.]
│   │   └── test_health.py [Health, auth, ML, vector search, exports, cleanup tests.]
│   ├── alembic.ini [Alembic configuration file.]
│   ├── Dockerfile [Backend container build instructions.]
│   ├── pytest.ini [Pytest discovery configuration.]
│   ├── requirements.txt [Python dependency list.]
│   ├── models/*.joblib [Generated ML model artifacts. Not manually implemented.]
│   ├── test_models [Generated test model artifacts. Not manually implemented.]
│   ├── data/chroma [Generated Chroma vector data. Not manually implemented.]
│   ├── test_chroma [Generated test Chroma vector data. Not manually implemented.]
│   ├── *.db [Generated SQLite databases. Not manually implemented.]
│   ├── __pycache__ [Generated Python bytecode cache. Not manually implemented.]
│   ├── venv/.venv [Generated virtual environments. Not manually implemented.]
│   └── python-installer.exe [Downloaded installer/binary. Not application source.]
├── docker [Deployment support files.]
│   └── nginx.conf [Nginx config for static React app, REST proxy, WebSocket proxy.]
├── docs [Human-written project documentation.]
│   ├── API.md [Endpoint reference.]
│   ├── ARCHITECTURE.md [System architecture summary.]
│   ├── DEPLOYMENT.md [Deployment instructions.]
│   └── PROJECT_TREE_GUIDE.md [This rebuild/interview guide.]
├── frontend [React + Vite + Tailwind browser application.]
│   ├── src [Frontend source code.]
│   │   ├── App.jsx [React route tree and protected-route wrapper.]
│   │   ├── index.css [Tailwind layers and shared component classes.]
│   │   ├── main.jsx [React app bootstrap with providers.]
│   │   ├── components [Reusable UI components.]
│   │   │   ├── Markdown.jsx [Markdown/code rendering component.]
│   │   │   ├── Shell.jsx [Authenticated app layout and navigation.]
│   │   │   └── Ui.jsx [Loader, status badge, metric card.]
│   │   ├── contexts [Shared React state providers.]
│   │   │   ├── AuthContext.jsx [Login/register/logout/user state.]
│   │   │   ├── ThemeContext.jsx [Dark/light theme state.]
│   │   │   └── ToastContext.jsx [Toast notification system.]
│   │   ├── lib [Frontend utility modules.]
│   │   │   └── api.js [Fetch wrapper, JWT header, downloads, WebSocket URL.]
│   │   └── pages [Top-level routed screens.]
│   │       ├── AgentsPage.jsx [Launches agents, streams logs, downloads/deletes generated projects.]
│   │       ├── AnalysisPage.jsx [Generates repository architecture analysis.]
│   │       ├── ChatPage.jsx [Repository-aware chat UI.]
│   │       ├── DashboardPage.jsx [Overview metrics and recent activity.]
│   │       ├── DocumentsPage.jsx [Preview/export PDFs and generated ZIPs.]
│   │       ├── LoginPage.jsx [Register/login screen.]
│   │       ├── MLPage.jsx [Metric estimation and bug-risk prediction UI.]
│   │       └── RepositoriesPage.jsx [GitHub ingestion, search, delete UI.]
│   ├── Dockerfile [Frontend build and Nginx runtime container.]
│   ├── eslint.config.js [ESLint linting rules.]
│   ├── index.html [Vite HTML entry document.]
│   ├── package.json [Node scripts and frontend dependencies.]
│   ├── package-lock.json [Auto-generated npm lockfile. Not manually implemented.]
│   ├── postcss.config.js [PostCSS/Tailwind processing config.]
│   ├── tailwind.config.js [Tailwind theme, content scanning, plugins.]
│   ├── vite.config.js [Vite React dev-server/build config.]
│   ├── node_modules [Auto-generated npm dependencies. Not manually implemented.]
│   └── dist [Auto-generated production build output. Not manually implemented.]
├── .dockerignore [Files excluded from Docker build context.]
├── .env.example [Template environment variables.]
├── .gitignore [Files excluded from Git.]
├── docker-compose.yml [Multi-container local deployment definition.]
├── README.md [Project overview and quick-start documentation.]
└── venv [Generated root virtual environment. Not manually implemented.]
```

## Detailed Component Explanations

### Root Project

Purpose: The repository is a monorepo: one source control project contains the backend API, frontend app, deployment files, tests, and documentation. This structure was chosen because the frontend and backend are tightly related and easier to run together through Docker Compose.

Knowledge Required: A **monorepo** means multiple application parts live in one Git repository. **Git** tracks source history. **GitHub** hosts repositories and runs CI. **Client-server architecture** means a browser client calls an API server. **Layered architecture** separates UI, routes, services, database, vector search, ML, and deployment so each part has a clear responsibility.

Data Flow: User opens React UI -> React calls FastAPI -> FastAPI checks JWT -> services call database/GitHub/Chroma/AI/ML -> response returns to React.

Common Mistakes: Mixing frontend secrets into browser code; putting database logic directly in UI; skipping ownership checks; committing generated folders.

Why This Approach: A monorepo makes an interview/demo project easier to understand, build, test, and deploy.

### `.env.example`

Purpose: Documents all environment variables required to configure the app: database URL, JWT secret, AI provider, GitHub token, Chroma path, ML path, CORS origins, and frontend API URLs.

Knowledge Required: **Environment variables** are runtime configuration values outside source code. **Secrets** are sensitive values like JWT signing keys and API keys. **CORS** controls which browser origins may call the API. **Provider flags** such as `AI_PROVIDER` let one codebase switch between local, Ollama, and OpenAI behavior.

Interactions: Loaded by backend `app/core/config.py`; used by Docker Compose; frontend uses `VITE_API_URL` and `VITE_WS_URL` at build/dev time.

Inputs/Outputs: Input is developer-provided values in `.env`; output is configured runtime behavior.

Common Mistakes: Using the default development secret in production; putting real secrets in Git; configuring frontend URLs incorrectly.

Why This Approach: A template makes setup repeatable while keeping real secrets outside Git.

What You Must Learn Before Building This File: Learn environment variables, secret management, Docker `.env` files, CORS origins, database connection strings, and the difference between backend runtime variables and Vite frontend variables.

### `.gitignore`

Purpose: Prevents generated files from entering Git: virtualenvs, caches, compiled Python, local DBs, Chroma data, model artifacts, frontend dependencies, and build output.

Knowledge Required: **Git ignore rules** tell Git which files are local artifacts. **Build artifacts** are generated from source. **Virtual environments** isolate installed Python packages.

Interactions: Protects the repository from committing `node_modules`, `venv`, `dist`, `.db`, `*.joblib`, and caches.

Common Mistakes: Ignoring source files accidentally; committing secrets; committing heavy dependency folders.

Why This Approach: Keeps the repository small, portable, and source-focused.

What You Must Learn Before Building This File: Learn Git status, tracked vs untracked files, generated artifacts, dependency installation, and why secrets/build outputs should not be committed.

### `.dockerignore`

Purpose: Keeps Docker build contexts small by excluding files Docker does not need.

Knowledge Required: **Docker build context** is the folder content sent to Docker during image builds. Excluding large folders speeds builds and avoids leaking local files.

Interactions: Used by `docker build` when Compose builds backend/frontend images.

Common Mistakes: Sending `node_modules`, `.env`, or DB files into images; accidentally excluding required source.

Why This Approach: Faster, cleaner, safer container builds.

What You Must Learn Before Building This File: Learn Docker images, build contexts, `.dockerignore` syntax, and which files are runtime source versus local artifacts.

### `docker-compose.yml`

Purpose: Defines the local production-style stack: PostgreSQL database, FastAPI API, and Nginx-served React frontend.

Knowledge Required: **Docker Compose** runs multiple containers. **PostgreSQL volumes** persist DB files. **Health checks** wait until DB is ready. **Service networking** lets `api` connect to `db` by service name. **Named volumes** persist Chroma vectors and ML model artifacts.

Interactions: Builds `backend/Dockerfile` and `frontend/Dockerfile`; injects environment variables; maps API port `8000` and web port `3000`.

Inputs/Outputs: Input is `.env` plus source code; output is running containers.

Common Mistakes: Wrong DB hostname; missing persistent volumes; frontend pointing to localhost inside container instead of proxy path.

Why This Approach: One command can run the whole application.

What You Must Learn Before Building This File: Learn containers, images, volumes, port mapping, service dependencies, environment variables, and Compose networking.

### `README.md`

Purpose: Human-facing project overview, capabilities, structure, quick start, configuration, ML training, and security notes.

Knowledge Required: **Markdown** is a plain-text documentation format. A README should explain what the project does, how to run it, and important operational constraints.

Interactions: Links to `docs/ARCHITECTURE.md`, `docs/API.md`, and `docs/DEPLOYMENT.md`.

Common Mistakes: Listing features that do not exist; missing setup steps; hiding important security assumptions.

Why This Approach: Interviewers and developers often read README first.

What You Must Learn Before Building This File: Learn Markdown, setup documentation, environment documentation, and how to summarize architecture accurately.

## `.github`

Purpose: Contains automation that runs on GitHub when code is pushed or a pull request is opened.

Knowledge Required: **CI/CD** means continuous integration/deployment. **GitHub Actions** executes YAML-defined jobs on cloud runners.

Interactions: Reads backend/frontend dependency manifests and test/build commands.

Common Mistakes: CI commands using wrong working directory; missing dependency install; tests relying on local files not committed.

Why This Approach: Automated checks catch errors before merge/demo.

What You Must Learn Before Building This Folder: Learn GitHub repositories, workflow triggers, YAML, job steps, runners, and separate backend/frontend validation.

### `.github/workflows/ci.yml`

Purpose: Runs two jobs: backend Python checks and frontend Node build checks.

Knowledge Required: **YAML** is a structured config format. **actions/checkout** downloads repo code. **setup-python** and **setup-node** install runtimes. **compileall** checks Python syntax. **pytest** runs tests. **npm ci** installs exact frontend dependencies. **npm run build** verifies React production build.

Interactions: Uses `backend/requirements.txt`, `backend/pytest.ini`, `frontend/package.json`, and `frontend/package-lock.json`.

Inputs/Outputs: Input is pushed code; output is pass/fail CI status.

Common Mistakes: Forgetting `working-directory`; using `npm install` instead of reproducible `npm ci`; CI missing environment overrides for tests.

Why This Approach: It validates both halves of the full-stack app.

What You Must Learn Before Building This File: Learn GitHub Actions syntax, CI triggers, Python/Node setup, pytest, npm scripts, and interpreting CI logs.

## `docs`

Purpose: Contains project knowledge that is not executable code but is essential for understanding, API usage, deployment, and interview preparation.

Knowledge Required: Documentation architecture, Markdown, API references, deployment runbooks.

Interactions: README links here; developers use it to rebuild and explain the system.

Common Mistakes: Letting docs become stale after code changes.

Why This Approach: Separates long-form explanations from code.

What You Must Learn Before Building This Folder: Learn technical writing, architecture diagrams, API documentation, and operational runbooks.

### `docs/ARCHITECTURE.md`

Purpose: Explains system overview, backend boundaries, RAG pipeline, data isolation, and scaling limitations.

Knowledge Required: **Architecture documentation** explains components and interactions. **RAG pipeline** means ingest -> chunk -> embed -> retrieve -> prompt -> answer. **Ownership boundaries** explain which package owns which responsibility.

Interactions: Matches code in `backend/app/api`, `services`, `agents`, `vector_store`, `ml`, and `database`.

Common Mistakes: Drawing architecture that does not match implementation; ignoring security/scaling caveats.

Why This Approach: Gives interviewers a concise mental model.

What You Must Learn Before Building This File: Learn system design diagrams, backend layering, RAG, authentication boundaries, and scaling tradeoffs.

### `docs/API.md`

Purpose: Lists API endpoints, methods, purposes, auth requirements, and ML input shape.

Knowledge Required: **HTTP methods** like GET/POST/DELETE. **Endpoint paths** identify API operations. **Bearer tokens** authenticate requests. **JSON** is the request/response data format.

Interactions: Mirrors route files under `backend/app/api/routes`.

Inputs/Outputs: Input is API route behavior; output is a developer-readable API reference.

Common Mistakes: Forgetting auth details; outdated endpoint names; unclear JSON examples.

Why This Approach: Developers can call the backend without reading all route code.

What You Must Learn Before Building This File: Learn REST conventions, JSON schema examples, auth headers, and OpenAPI basics.

### `docs/DEPLOYMENT.md`

Purpose: Explains Docker deployment, hosted deployment options, AWS outline, and scaling changes.

Knowledge Required: Docker, managed databases, persistent storage, TLS, secrets managers, cloud logs, queues, Redis-backed scaling.

Interactions: References `docker-compose.yml`, `backend/Dockerfile`, `frontend/Dockerfile`, and `.env.example`.

Common Mistakes: Running production with development secrets; losing vector/model state; running migrations from every replica at scale.

Why This Approach: Gives a practical path from local demo to hosted system.

What You Must Learn Before Building This File: Learn containers, cloud services, database persistence, TLS, secret storage, logs, queues, and horizontal scaling.

### `docs/PROJECT_TREE_GUIDE.md`

Purpose: This document. It maps every manually created component and explains how to rebuild it.

Knowledge Required: Documentation structure, source-tree analysis, and beginner-friendly explanations.

Interactions: Depends on the whole repository structure.

Common Mistakes: Expanding generated dependency folders; omitting small glue files like package markers/configs.

Why This Approach: A tree guide is useful for interview prep and from-scratch rebuilding.

What You Must Learn Before Building This File: Learn the entire project architecture and how each file contributes to the system.

## `docker`

Purpose: Holds Docker-adjacent deployment config that is not owned by backend or frontend source.

Knowledge Required: Reverse proxies, HTTP routing, static hosting, WebSocket upgrades.

Interactions: `frontend/Dockerfile` copies `docker/nginx.conf` into the Nginx runtime image.

Common Mistakes: Breaking WebSocket upgrade headers; not falling back to `index.html` for React routes.

Why This Approach: Keeps deployment proxy config separate from app code.

What You Must Learn Before Building This Folder: Learn Nginx server blocks, reverse proxying, WebSocket upgrade headers, and SPA fallback routing.

### `docker/nginx.conf`

Purpose: Serves React static files, proxies `/api/` REST requests to the API container, and proxies `/api/v1/agents/ws/` WebSocket connections.

Knowledge Required: **Nginx** is a high-performance web server/proxy. **Reverse proxy** forwards browser requests to another server. **SPA fallback** uses `try_files $uri /index.html` so React Router routes work on refresh. **WebSocket upgrade headers** switch HTTP to a persistent socket.

Interactions: Talks to Compose service `api:8000`; serves files from `/usr/share/nginx/html`.

Inputs/Outputs: Input is browser HTTP/WebSocket requests; output is static assets or proxied backend responses.

Common Mistakes: Missing `Upgrade` and `Connection` headers for WebSockets; wrong proxy path; no SPA fallback.

Why This Approach: Lets frontend and backend appear under one web origin in Docker.

What You Must Learn Before Building This File: Learn Nginx syntax, proxy_pass, HTTP headers, WebSockets, Docker service DNS, and browser routing.

## `backend`

Purpose: Python backend application that provides all server-side functionality: authentication, persistence, GitHub repository ingestion, RAG search/chat, AI orchestration, ML predictions, agent workflows, documents, and tests.

Knowledge Required: Python packages, FastAPI app layout, async programming, database design, service layering, environment config, testing, Docker.

Interactions: Called by React; calls PostgreSQL/SQLite, GitHub, ChromaDB, optional Ollama/OpenAI, and ML models.

Common Mistakes: Blocking the event loop with heavy CPU work; missing async session commits; exposing secrets to frontend; not checking user ownership.

Why This Approach: Backend centralizes sensitive logic and data access.

What You Must Learn Before Building This Folder: Learn Python, FastAPI, SQLAlchemy, async/await, REST, WebSockets, Pydantic, JWT, ChromaDB, ML basics, Docker, and tests.

### `backend/requirements.txt`

Purpose: Lists Python dependencies with version ranges.

Knowledge Required: **pip** installs packages. **Version constraints** reduce breaking changes while allowing patches. Libraries include FastAPI, SQLAlchemy, Alembic, ChromaDB, LangGraph, OpenAI, scikit-learn, XGBoost, ReportLab, Pytest.

Interactions: Used by local `pip install` and `backend/Dockerfile`.

Common Mistakes: Missing transitive platform packages; unpinned major versions; installing dependencies manually without recording them.

Why This Approach: Reproducible backend setup.

What You Must Learn Before Building This File: Learn Python packaging, pip, dependency resolution, semantic versioning, and why apps need explicit dependency manifests.

### `backend/Dockerfile`

Purpose: Builds backend runtime image using Python 3.12, installs dependencies, copies source, creates data/model directories, and starts Alembic + Uvicorn.

Knowledge Required: **Dockerfile** instructions: `FROM`, `ENV`, `WORKDIR`, `RUN`, `COPY`, `EXPOSE`, `CMD`. **Uvicorn** runs ASGI apps. **ASGI** is the async Python web server interface. **libgomp1** supports XGBoost/scikit-learn native runtime needs.

Interactions: Used by `docker-compose.yml`; executes `alembic upgrade head`; runs `app.main:app`.

Common Mistakes: Forgetting `PYTHONPATH`; missing native OS packages; running migrations unsafely in many replicas; not creating persistent dirs.

Why This Approach: One container image contains the backend app and runtime.

What You Must Learn Before Building This File: Learn Docker layers, Python containers, dependency installation, Uvicorn, Alembic migration startup, and Linux package installation.

### `backend/alembic.ini`

Purpose: Alembic project config: migration folder path, Python path, default DB URL placeholder, logging.

Knowledge Required: Alembic config sections, migration script location, database URL, logging config.

Interactions: Read by `alembic` CLI and `migrations/env.py`.

Common Mistakes: Keeping async DB URL in sync-only Alembic config without conversion; wrong script path.

Why This Approach: Standard Alembic configuration.

What You Must Learn Before Building This File: Learn Alembic commands, config files, database URLs, and migration logging.

### `backend/pytest.ini`

Purpose: Configures Pytest to discover tests in `tests` and include backend root on Python path.

Knowledge Required: Pytest configuration, Python import paths, test discovery.

Interactions: Used by `pytest` locally and in CI.

Common Mistakes: Tests cannot import `app` because `pythonpath` is wrong.

Why This Approach: Keeps test commands simple.

What You Must Learn Before Building This File: Learn pytest discovery, `pythonpath`, and test directory conventions.

## `backend/app`

Purpose: Main importable Python package for the FastAPI application.

Knowledge Required: Python packages, module imports, backend layer separation.

Interactions: Imported by Uvicorn as `app.main:app`.

Common Mistakes: Circular imports between routes/services/models; missing `__init__.py` in packages.

Why This Approach: Standard Python application layout.

What You Must Learn Before Building This Folder: Learn Python modules, packages, import paths, and source organization.

### `backend/app/__init__.py`

Purpose: Marks `app` as a Python package.

Knowledge Required: Python package discovery. Empty `__init__.py` files are often used so modules can import each other cleanly.

Interactions: Enables imports such as `from app.core.config import settings`.

Common Mistakes: Removing it in projects/tools expecting package markers.

Why This Approach: Explicit package boundaries.

What You Must Learn Before Building This File: Learn Python import rules and package initialization.

### `backend/app/main.py`

Purpose: Creates the FastAPI application, configures logging/startup, creates directories/tables, ensures ML models exist, adds rate limiting and CORS, includes API routers, and exposes `/health`.

Knowledge Required: FastAPI app creation, lifespan context managers, middleware, CORS, route inclusion, async startup, health checks.

Interactions: Imports settings, router, middleware, DB table creation, and ML registry.

Inputs/Outputs: Input is HTTP requests; output is API responses. Startup input is environment config; startup output is ready DB/models/directories.

Common Mistakes: Doing heavy work on every request; forgetting CORS; not awaiting async table creation; route prefix mismatch.

Why This Approach: A single app entrypoint keeps startup behavior clear.

What You Must Learn Before Building This File: Learn FastAPI app lifecycle, ASGI, middleware, dependency injection basics, CORS, health endpoints, and async startup patterns.

### `backend/app/schemas.py`

Purpose: Defines Pydantic models for requests and responses: auth payloads, repositories, search results, chat, ML metrics/predictions, agent runs/logs, generated projects.

Knowledge Required: Pydantic `BaseModel`, validation fields, response models, type hints, ORM serialization via `from_attributes`.

Interactions: Imported by route files and services to validate inputs and shape outputs.

Inputs/Outputs: Inputs are raw JSON requests; outputs are validated Python objects or JSON responses.

Common Mistakes: Missing validation bounds; exposing sensitive fields like password hashes; mismatching DB and response field names.

Why This Approach: Centralized schemas make API contracts explicit.

What You Must Learn Before Building This File: Learn JSON, type hints, Pydantic validation, FastAPI request/response models, and API contract design.

## `backend/app/core`

Purpose: Cross-cutting backend utilities: configuration, security, logging.

Knowledge Required: Environment-driven settings, JWT, password hashing, logging.

Interactions: Used throughout routes, services, DB, vector store, and app startup.

Common Mistakes: Hardcoding secrets; inconsistent config access; weak password hashing.

Why This Approach: Shared infrastructure belongs in one core package.

What You Must Learn Before Building This Folder: Learn application configuration, cryptography basics, logging, and secure defaults.

### `backend/app/core/config.py`

Purpose: Loads runtime settings from environment variables and `.env`, validates production secret, creates Chroma/model directories.

Knowledge Required: `pydantic-settings`, `BaseSettings`, cached settings, path handling, environment variables, model validators.

Interactions: Used by almost every backend layer for URLs, paths, API keys, AI provider, limits, and CORS.

Inputs/Outputs: Input is environment; output is a typed `settings` object.

Common Mistakes: Case-sensitive env surprises; unsafe production defaults; not creating persistence directories.

Why This Approach: Typed config avoids scattered `os.environ` reads.

What You Must Learn Before Building This File: Learn environment variables, Pydantic settings, pathlib, validation, and config centralization.

### `backend/app/core/security.py`

Purpose: Hashes/verifies passwords and creates/decodes JWT access tokens.

Knowledge Required: Argon2 password hashing, JWT claims, expiration times, HS256 signing, exception handling.

Interactions: Used by auth routes and auth dependencies/WebSocket auth.

Inputs/Outputs: Input password/user id/token; output hash/boolean/token/user id.

Common Mistakes: Storing plain passwords; using weak secrets; ignoring token expiration; leaking token contents.

Why This Approach: Password and token logic is centralized and reusable.

What You Must Learn Before Building This File: Learn authentication, password hashing, JWT structure, token expiration, signing secrets, and secure error handling.

### `backend/app/core/logging.py`

Purpose: Configures application logging.

Knowledge Required: Python `logging`, log levels, operational observability.

Interactions: Called at app startup from `main.py`.

Inputs/Outputs: Input is runtime events; output is formatted logs.

Common Mistakes: Logging secrets; too much noisy logging; no logs for failures.

Why This Approach: Central logging config makes runtime behavior easier to inspect.

What You Must Learn Before Building This File: Learn Python logging, log levels, handlers, and safe operational logging.

## `backend/app/database`

Purpose: Defines relational persistence: engine/session and table models.

Knowledge Required: Relational databases, primary keys, foreign keys, indexes, ORM relationships, async sessions.

Interactions: Routes/services use sessions to read/write users, repositories, embeddings, conversations, predictions, projects, and logs.

Common Mistakes: Not committing transactions; lazy relationship surprises; missing ownership filters; not indexing lookup columns.

Why This Approach: SQLAlchemy models give a typed Python layer over PostgreSQL/SQLite.

What You Must Learn Before Building This Folder: Learn SQL tables, keys, relationships, SQLAlchemy ORM, async sessions, transactions, and migrations.

### `backend/app/database/session.py`

Purpose: Creates async database engine, session factory, dependency generator, and table-creation helper.

Knowledge Required: SQLAlchemy async engine, sessionmaker, FastAPI dependency yield, declarative base, connection pooling.

Interactions: Imported by routes, services, tests, migration env, and models.

Inputs/Outputs: Input is `DATABASE_URL`; output is DB sessions.

Common Mistakes: Sharing sessions globally; forgetting `expire_on_commit=False`; using sync drivers with async engine.

Why This Approach: Central session management prevents inconsistent database access.

What You Must Learn Before Building This File: Learn database URLs, async SQLAlchemy, sessions, transactions, and FastAPI dependency lifetimes.

### `backend/app/database/models.py`

Purpose: Defines database tables: users, repositories, embeddings, conversations, ML predictions, generated projects, agent logs.

Knowledge Required: ORM classes, mapped columns, JSON columns, dates/timezones, UUIDs, foreign keys, relationships, cascade delete.

Interactions: Used by routes/services/tests/migrations and serialized through schemas.

Data Flow: New user/repository/log/etc. becomes SQLAlchemy object -> session commit -> database row.

Common Mistakes: Missing foreign keys; storing huge source content in wrong place; no user scoping; naive datetimes.

Why This Approach: Models reflect the main domain entities of the app.

What You Must Learn Before Building This File: Learn relational modeling, SQLAlchemy `Mapped`, UUID IDs, timestamps, JSON fields, foreign keys, and user-ownership design.

## `backend/app/api`

Purpose: Transport layer for HTTP and WebSocket endpoints. It validates requests, checks authentication, and delegates real work to services.

Knowledge Required: FastAPI routers, dependencies, status codes, background tasks, WebSockets.

Interactions: Imports schemas, DB sessions, current-user dependency, and service functions.

Common Mistakes: Putting too much business logic in route functions; not checking repository ownership; bad status codes.

Why This Approach: Keeps API surface separate from business logic.

What You Must Learn Before Building This Folder: Learn REST design, FastAPI routers, dependency injection, HTTP errors, WebSockets, and background tasks.

### `backend/app/api/dependencies.py`

Purpose: Provides `get_current_user`, a dependency that decodes bearer JWT and loads the active user.

Knowledge Required: OAuth2 bearer token extraction, JWT decoding, FastAPI dependencies, HTTP 401 responses.

Interactions: Used by protected route files.

Inputs/Outputs: Input is `Authorization: Bearer <token>`; output is authenticated `User`.

Common Mistakes: Returning inactive users; not setting `WWW-Authenticate`; swallowing invalid tokens silently in protected routes.

Why This Approach: Authentication is reusable across all protected endpoints.

What You Must Learn Before Building This File: Learn bearer auth, dependency injection, database lookup, and unauthorized response semantics.

### `backend/app/api/middleware.py`

Purpose: Implements simple per-process rate limiting by client IP.

Knowledge Required: FastAPI/Starlette middleware, monotonic clocks, deques, sliding time windows, HTTP 429.

Interactions: Added in `main.py`.

Inputs/Outputs: Input is each request; output is either pass-through response or 429 JSON.

Common Mistakes: Using system time instead of monotonic time; memory growth; assuming this works across multiple replicas.

Why This Approach: Simple protection for demo/local deployment.

What You Must Learn Before Building This File: Learn middleware flow, request clients, rate limiting, deques, and distributed-limit tradeoffs.

### `backend/app/api/router.py`

Purpose: Combines feature routers under one `APIRouter`.

Knowledge Required: FastAPI router composition, prefixes, tags, API versioning.

Interactions: Imported by `main.py`; imports all route modules.

Common Mistakes: Prefix mismatch with frontend API calls; circular imports.

Why This Approach: Keeps `main.py` clean and supports `/api/v1` versioning.

What You Must Learn Before Building This File: Learn modular route registration and API versioning.

## `backend/app/api/routes`

Purpose: Contains one route module per feature domain.

Knowledge Required: CRUD routing, validation, auth, background jobs, streaming responses.

Interactions: Calls services and DB models.

Common Mistakes: Duplicating ownership logic; returning raw internal exceptions; blocking requests with long work.

Why This Approach: Feature-based files are easier to explain and maintain.

What You Must Learn Before Building This Folder: Learn route organization and when to delegate to service classes/functions.

### `auth.py`

Purpose: Implements user registration, login, and `/me`.

Knowledge Required: Email validation, password hashing, JWT creation, unique constraints, HTTP 409/401.

Interactions: Uses `User`, `get_db`, security helpers, auth schemas.

Inputs/Outputs: Input register/login JSON; output JWT plus user response.

Common Mistakes: Returning password hash; ambiguous login errors that leak account existence; weak password validation.

Why This Approach: Simple token auth fits SPA + API architecture.

What You Must Learn Before Building This File: Learn auth flows, secure password storage, JWT response design, database uniqueness, and status codes.

### `repositories.py`

Purpose: Creates/list/gets/deletes repositories, queues GitHub ingestion, and performs semantic search.

Knowledge Required: Background tasks, CRUD, ownership checks, cascading cleanup, semantic search.

Interactions: Calls `ingest_repository`, `RepositoryVectorStore`, and deletes related DB rows.

Inputs/Outputs: Input GitHub URL/search query; output repository records/search results.

Common Mistakes: Not deleting vectors when deleting repository; allowing users to access other users' repos; searching before indexing is ready.

Why This Approach: Repository ownership and lifecycle are centralized.

What You Must Learn Before Building This File: Learn CRUD, FastAPI background tasks, user-scoped queries, vector cleanup, and HTTP conflict responses.

### `chat.py`

Purpose: Provides repository-aware chat and persistent chat history.

Knowledge Required: RAG, conversation storage, optional repository context, async database queries.

Interactions: Calls `ChatService` and `owned_repository`.

Inputs/Outputs: Input question/repository id; output answer and sources; history endpoint outputs past messages.

Common Mistakes: Chatting against a repo without ownership check; not saving both user and assistant messages.

Why This Approach: Keeps route thin while service handles retrieval/generation.

What You Must Learn Before Building This File: Learn chat APIs, RAG context passing, persistence, and authorization.

### `analysis.py`

Purpose: Generates architecture analysis for an indexed repository.

Knowledge Required: Protected GET endpoints, repository ownership, report generation.

Interactions: Calls `architecture_report` service.

Inputs/Outputs: Input repository id; output repository status, summary, architecture markdown.

Common Mistakes: Running analysis on missing/unowned repo; returning too little summary context.

Why This Approach: Analysis is derived from existing indexed repository summary and retrieved chunks.

What You Must Learn Before Building This File: Learn route parameters, service delegation, and report response design.

### `ml.py`

Purpose: Estimates code metrics from indexed files, predicts bug risk/maintainability, stores prediction history.

Knowledge Required: Request validation, CPU-bound work via `asyncio.to_thread`, ML model inference, history persistence.

Interactions: Uses `estimate_repository_metrics`, `model_registry`, `MLPrediction`.

Inputs/Outputs: Input metrics/file path; output probability, maintainability score, recommendations.

Common Mistakes: Running CPU-heavy model prediction directly on event loop; accepting unbounded metric values; not recording prediction history.

Why This Approach: ML endpoints are useful both manually and from indexed repo estimates.

What You Must Learn Before Building This File: Learn ML inference APIs, async thread offloading, validation bounds, and storing analytic history.

### `agents.py`

Purpose: Starts multi-agent generation runs, lists logs/projects, deletes projects, and streams live events over WebSocket.

Knowledge Required: Background tasks, UUIDs, WebSocket authentication, channel authorization, streaming event hubs.

Interactions: Calls `execute_agent_run`, `delete_generated_project`, `event_hub`, and DB models.

Inputs/Outputs: Input project requirements; output accepted run id, logs, project list, WebSocket JSON events.

Common Mistakes: Unauthenticated WebSockets; not closing unauthorized sockets; using the wrong channel for user vs repository.

Why This Approach: Long agent work runs in background while UI receives progress.

What You Must Learn Before Building This File: Learn WebSockets, background tasks, event streaming, UUIDs, and authorization for real-time channels.

### `documents.py`

Purpose: Streams repository architecture PDFs and generated project ZIPs.

Knowledge Required: FastAPI `StreamingResponse`, binary downloads, content disposition headers, PDF/ZIP generation.

Interactions: Calls `repository_pdf`, `project_zip`, `architecture_report`.

Inputs/Outputs: Input repository/project id; output downloadable binary stream.

Common Mistakes: Wrong MIME type; no ownership check; loading huge files into memory for large projects. Note: this file currently imports `asyncio` at the bottom, which works after module import but should be moved to top for style.

Why This Approach: Keeps export creation server-side and avoids exposing stored internals.

What You Must Learn Before Building This File: Learn streaming responses, file download headers, binary data, authorization, PDF/ZIP libraries.

## `backend/app/services`

Purpose: Business logic layer. Services are called by routes and coordinate databases, vector stores, AI providers, GitHub APIs, exports, and workflows.

Knowledge Required: Service-layer pattern, async orchestration, external APIs, separation of concerns.

Interactions: Sits between route modules and infrastructure packages.

Common Mistakes: Letting service code depend on frontend details; hiding authorization checks too deeply; mixing unrelated domains.

Why This Approach: Routes stay thin and domain logic becomes easier to test.

What You Must Learn Before Building This Folder: Learn layered architecture, service functions/classes, async I/O, and dependency boundaries.

### `github_service.py`

Purpose: Parses GitHub URLs, calls GitHub API, filters supported files, fetches raw text files.

Knowledge Required: GitHub REST API, HTTP clients, URL parsing, file extension filtering, rate limits, async `httpx`.

Interactions: Used by `repository_service.ingest_repository`.

Inputs/Outputs: Input GitHub repo URL; output default branch and `GitHubFile` list.

Common Mistakes: Fetching huge/binary files; ignoring GitHub rate limits; supporting unsafe non-GitHub URLs accidentally.

Why This Approach: Centralizes GitHub-specific logic and makes ingestion cleaner.

What You Must Learn Before Building This File: Learn HTTP APIs, GitHub repository trees, raw file URLs, rate limits, async clients, and content filtering.

### `repository_service.py`

Purpose: Chunks repository files, builds summary metadata, indexes vectors, stores embedding metadata, updates repository status.

Knowledge Required: Text chunking, background jobs, counters, regex code scanning, Chroma indexing, DB transactions.

Interactions: Uses `GitHubRepositoryClient`, `RepositoryVectorStore`, SQLAlchemy models.

Inputs/Outputs: Input repository id; output updated DB repository, embeddings, Chroma collection.

Common Mistakes: Not marking failed ingestion; chunking without line preservation; losing DB/vector consistency.

Why This Approach: Repository ingestion is a multi-step process that belongs outside route functions.

What You Must Learn Before Building This File: Learn background processing, text chunking, regex summaries, vector indexing, transaction handling, and failure states.

### `vector_store/store.py`

Purpose: Manages Chroma collections, embeddings, indexing, document retrieval, query search, and collection deletion.

Knowledge Required: ChromaDB, embeddings, cosine distance, scikit-learn HashingVectorizer, OpenAI embedding API, async thread wrappers for sync libraries.

Interactions: Used by repository ingestion, chat, analysis, ML metric estimation, tests.

Inputs/Outputs: Input text chunks/query; output vectors/search results.

Common Mistakes: Collection names with invalid characters; forgetting to delete old vectors; mixing sync Chroma calls into event loop without thread offload.

Why This Approach: One vector abstraction supports local and OpenAI embedding modes.

What You Must Learn Before Building This File: Learn vector databases, embeddings, nearest-neighbor search, Chroma collections, cosine similarity, and async/sync interop.

### `ai_service.py`

Purpose: Provides one AI generation boundary for local deterministic mode, Ollama, or OpenAI.

Knowledge Required: LLM prompting, provider abstraction, OpenAI Responses API, Ollama HTTP API, fallback behavior, prompt-injection safety.

Interactions: Used by chat, analysis, and agent workflow.

Inputs/Outputs: Input instructions and prompt; output generated text.

Common Mistakes: Sending source code to paid providers unintentionally; trusting repository content as instructions; no fallback when provider fails.

Why This Approach: Keeps provider selection in one place and enables free default behavior.

What You Must Learn Before Building This File: Learn LLMs, prompts, local model runtimes, cloud AI APIs, provider adapters, and prompt safety.

### `chat_service.py`

Purpose: Implements RAG chat: special file-listing intent, vector retrieval, prompt construction, AI call, conversation persistence.

Knowledge Required: RAG orchestration, prompt context formatting, chat history storage, SQLAlchemy inserts.

Interactions: Uses `RepositoryVectorStore`, `AIService`, `Conversation`, schemas.

Inputs/Outputs: Input user question; output answer and source list.

Common Mistakes: Hallucinating beyond retrieved context; not citing file paths; not treating source as untrusted.

Why This Approach: Chat behavior is reusable and route-independent.

What You Must Learn Before Building This File: Learn semantic retrieval, prompt construction, chat UX expectations, source citations, and database persistence.

### `analysis_service.py`

Purpose: Retrieves architecture-related chunks and asks AI service to produce a markdown architecture report.

Knowledge Required: Retrieval queries, markdown reports, software architecture analysis.

Interactions: Used by analysis and document export routes.

Inputs/Outputs: Input `Repository`; output architecture markdown.

Common Mistakes: Asking too broad a retrieval query; not passing summary metrics.

Why This Approach: One report generator serves preview and PDF export.

What You Must Learn Before Building This File: Learn report generation, RAG context selection, markdown formatting, and architecture documentation.

### `agent_service.py`

Purpose: Executes LangGraph workflow, records each agent event, streams events through in-memory WebSocket hub, saves generated project files.

Knowledge Required: Event hubs, WebSocket connection sets, background workflow execution, LangGraph streaming updates, persisted logs.

Interactions: Uses `build_workflow`, `AgentLog`, `GeneratedProject`, `RepositoryVectorStore`.

Inputs/Outputs: Input run id/user/repository/requirements; output logs, WebSocket events, generated project row.

Common Mistakes: No distributed event bus for multiple API replicas; not handling dead sockets; not persisting logs.

Why This Approach: Simple in-process event hub is enough for local/demo, documented for Redis replacement at scale.

What You Must Learn Before Building This File: Learn async iteration, event publishing, WebSocket lifecycle, workflow state, and generated artifact storage.

### `export_service.py`

Purpose: Converts generated project files into ZIP and repository reports into PDFs.

Knowledge Required: Python `zipfile`, in-memory `BytesIO`, ReportLab PDF building, HTML escaping.

Interactions: Called by document routes.

Inputs/Outputs: Input project/repository/report; output binary file-like object.

Common Mistakes: Not seeking `BytesIO` back to zero; unsafe filenames; unescaped PDF text.

Why This Approach: In-memory export is simple for small generated artifacts.

What You Must Learn Before Building This File: Learn binary streams, ZIP archives, PDF generation, escaping, and download response integration.

### `generated_project_service.py`

Purpose: Deletes generated project database rows and any future disk artifacts.

Knowledge Required: File cleanup, async thread offloading, safe deletion, SQLAlchemy delete.

Interactions: Called by `agents.py` delete endpoint.

Inputs/Outputs: Input generated project; output removed DB row and cleaned filesystem candidates.

Common Mistakes: Deleting wrong paths; not committing DB delete; leaving orphan export artifacts.

Why This Approach: Keeps cleanup logic separate from route code.

What You Must Learn Before Building This File: Learn filesystem safety, DB deletion, path handling, and cleanup patterns.

## `backend/app/agents`

Purpose: Defines the multi-agent software engineering workflow.

Knowledge Required: LangGraph, state machines, prompt templates, agent roles.

Interactions: `agent_service.py` executes the compiled workflow.

Common Mistakes: No deterministic order; not carrying state between steps; prompts that ignore security rules.

Why This Approach: LangGraph makes the agent sequence explicit.

What You Must Learn Before Building This Folder: Learn state graphs, nodes, edges, async functions, and prompt orchestration.

### `workflow.py`

Purpose: Creates a six-node workflow: requirements, repository understanding, backend generation, frontend generation, documentation, review.

Knowledge Required: `TypedDict` state, LangGraph `StateGraph`, `START`/`END`, async node functions, LangChain `ChatPromptTemplate`.

Interactions: Uses `AIService.complete`; consumed by `agent_service.execute_agent_run`.

Inputs/Outputs: Input requirements/context state; output plan, code, docs, review.

Common Mistakes: State keys missing before later nodes; graph edges in wrong order; prompts too vague.

Why This Approach: Mimics an engineering team pipeline and produces structured deliverables.

What You Must Learn Before Building This File: Learn workflow graphs, state passing, prompt templates, async agent functions, and secure prompting.

## `backend/app/ml`

Purpose: Training, inference, and metric estimation for bug-risk and maintainability scoring.

Knowledge Required: ML features, classifiers, regressors, train/test split, model persistence, inference APIs.

Interactions: Routes call predictor/metrics; startup ensures models exist; scripts train models.

Common Mistakes: Treating synthetic demo data as production truth; not validating input ranges; not versioning models.

Why This Approach: Adds predictive engineering functionality without requiring external ML services.

What You Must Learn Before Building This Folder: Learn supervised ML, feature engineering, pandas, numpy, scikit-learn, XGBoost, joblib, and model evaluation.

### `training.py`

Purpose: Generates reproducible synthetic training data or loads CSV, trains XGBoost bug classifier and RandomForest maintainability regressor, saves artifacts and metrics.

Knowledge Required: pandas DataFrames, numpy random generation, classification, regression, ROC-AUC, MAE, joblib serialization.

Interactions: Called by `predictor.py` and `scripts/train_models.py`.

Inputs/Outputs: Optional CSV input; output `.joblib` model files and metrics metadata.

Common Mistakes: Training on unrepresentative synthetic data for real decisions; no fixed random seed; feature column mismatch.

Why This Approach: Provides a working demo model even before real defect labels exist.

What You Must Learn Before Building This File: Learn tabular ML, feature columns, train/test split, classifiers vs regressors, evaluation metrics, and model serialization.

### `predictor.py`

Purpose: Ensures model artifacts exist, loads models, predicts bug probability and maintainability, returns recommendations.

Knowledge Required: joblib loading, pandas single-row inference, probability outputs, recommendation rules, LRU cache.

Interactions: Used by `ml.py` route and app startup.

Inputs/Outputs: Input metrics dict; output probability, score, recommendation list.

Common Mistakes: Reloading models too often; not clamping score; missing model artifact bootstrap.

Why This Approach: Encapsulates ML inference behind a small registry.

What You Must Learn Before Building This File: Learn model inference, DataFrame construction, probability interpretation, caching, and rule-based recommendations.

### `metrics.py`

Purpose: Estimates code metrics from indexed repository chunks: complexity, file size, dependency count, commit frequency proxy.

Knowledge Required: Regex parsing, code metrics, vector-store document retrieval, grouping chunks by file.

Interactions: Used by ML estimate route; reads `Embedding` metadata and Chroma documents.

Inputs/Outputs: Input repository/file path; output selected file, `CodeMetrics`, available files.

Common Mistakes: Assuming every language parses like Python; undercounting complexity; missing content when DB metadata lacks it.

Why This Approach: Lets users score real indexed files without manually entering metrics.

What You Must Learn Before Building This File: Learn code metrics, regex, grouping, fallback retrieval, and limitations of static heuristics.

## `backend/migrations`

Purpose: Stores database schema migration code.

Knowledge Required: Database schema evolution, Alembic runtime, sync vs async database drivers.

Interactions: Docker backend startup runs `alembic upgrade head`.

Common Mistakes: Editing production DB manually; migrations not matching models.

Why This Approach: Migrations make schema setup repeatable.

What You Must Learn Before Building This Folder: Learn migrations, upgrade/downgrade, metadata, and schema versioning.

### `migrations/env.py`

Purpose: Configures Alembic to use app settings and model metadata; converts async DB URLs to sync URLs for Alembic.

Knowledge Required: Alembic context, SQLAlchemy engines, metadata, offline/online migrations, driver URL conversion.

Interactions: Imports `settings`, `Base`, and models.

Common Mistakes: Alembic cannot import app; wrong DB driver; metadata not loaded so migrations are empty.

Why This Approach: Uses same config/model metadata as the running app.

What You Must Learn Before Building This File: Learn Alembic env files, metadata autogeneration concepts, database drivers, and migration execution modes.

### `migrations/versions/0001_initial_schema.py`

Purpose: Initial migration that creates/drops all tables from SQLAlchemy metadata.

Knowledge Required: Alembic revision files, upgrade/downgrade functions, table metadata.

Interactions: Uses models loaded through `Base.metadata`.

Common Mistakes: No downgrade; migration not deterministic; relying only on `create_all` for long-term schema evolution.

Why This Approach: Simple initial migration for the first schema.

What You Must Learn Before Building This File: Learn migration revisions, schema creation, downgrade behavior, and how migrations relate to ORM models.

## `backend/scripts`

Purpose: Manual developer/admin scripts.

Knowledge Required: Command-line interfaces, argparse, script entrypoints.

Interactions: Calls backend ML training code.

Common Mistakes: Duplicating app logic in scripts; not accepting paths as arguments.

Why This Approach: Keeps one-off operations reproducible.

What You Must Learn Before Building This Folder: Learn Python CLI scripts and reusing app modules.

### `scripts/train_models.py`

Purpose: CLI wrapper around `app.ml.training.train_models`.

Knowledge Required: `argparse`, pathlib, Python `if __name__ == "__main__"`, optional CSV inputs.

Interactions: Imports `train_models`.

Inputs/Outputs: Input optional CSV/output folder; output printed metrics and saved model artifacts.

Common Mistakes: Running from wrong working directory; CSV missing required feature/label columns.

Why This Approach: Separates CLI concerns from training implementation.

What You Must Learn Before Building This File: Learn command-line arguments, Python script entrypoints, file paths, and ML artifact generation.

## `backend/tests`

Purpose: Verifies backend behavior.

Knowledge Required: Pytest, FastAPI TestClient, async tests, test DB isolation, assertions.

Interactions: Imports app, DB models, vector store, and route endpoints.

Common Mistakes: Tests depending on production database; not cleaning generated artifacts; flaky async code.

Why This Approach: Tests prove key flows work without manual clicking.

What You Must Learn Before Building This Folder: Learn automated testing, test isolation, fixtures/async tests, and integration testing.

### `tests/test_health.py`

Purpose: Tests health endpoint, authenticated ML prediction, offline agent export/delete, repository vector cleanup, repository metric estimation, and vector search.

Knowledge Required: FastAPI `TestClient`, environment overrides before app import, UUIDs, async helper functions, Chroma test collections, HTTP assertions.

Interactions: Touches many backend layers: auth routes, ML, agents, documents, repositories, vector store, database models.

Inputs/Outputs: Input test requests; output pass/fail assertions.

Common Mistakes: Importing app before test env variables; shared IDs causing test collisions; not checking cleanup after delete.

Why This Approach: Covers high-value end-to-end flows in a compact test suite.

What You Must Learn Before Building This File: Learn integration tests, async helper calls, test database setup, HTTP test clients, and validating side effects.

## `frontend`

Purpose: Browser UI for the engineering assistant.

Knowledge Required: JavaScript, React, components, hooks, routing, state, forms, CSS, API calls, WebSockets.

Interactions: Calls backend `/api/v1` endpoints and receives WebSocket events.

Common Mistakes: Storing secrets in frontend; not handling loading/errors; broken protected routes.

Why This Approach: React SPA provides a responsive dashboard-like product experience.

What You Must Learn Before Building This Folder: Learn HTML, CSS, JavaScript, React, Vite, Tailwind, browser fetch, localStorage, and WebSockets.

### `frontend/package.json`

Purpose: Defines frontend project metadata, npm scripts, dependencies, and dev dependencies.

Knowledge Required: Node.js, npm, package manifests, scripts, dependency types.

Interactions: Used by local dev, Docker build, and CI.

Common Mistakes: Missing dependencies after imports; putting build tools in runtime dependencies unnecessarily.

Why This Approach: Standard Node project manifest.

What You Must Learn Before Building This File: Learn Node.js, npm, semantic versions, scripts, dependencies vs devDependencies.

### `frontend/index.html`

Purpose: HTML document Vite serves; contains the root element where React mounts.

Knowledge Required: HTML, document structure, script modules, SPA mounting.

Interactions: `main.jsx` renders into `#root`.

Common Mistakes: Missing root div; wrong script path; adding app logic here instead of React.

Why This Approach: Vite standard entry document.

What You Must Learn Before Building This File: Learn HTML basics, DOM, module scripts, and how React attaches to a page.

### `frontend/vite.config.js`

Purpose: Configures Vite React plugin and local dev server host/port.

Knowledge Required: Vite, ES modules, React plugin, dev server networking.

Interactions: Used by `npm run dev` and build tooling.

Common Mistakes: Wrong port/origin causing CORS mismatch.

Why This Approach: Vite is fast and minimal for React development.

What You Must Learn Before Building This File: Learn Vite, plugins, dev servers, host binding, and frontend build tools.

### `frontend/tailwind.config.js`

Purpose: Configures Tailwind content scanning, dark mode, custom colors, shadows, typography plugin.

Knowledge Required: Tailwind utility CSS, theme extension, dark-mode class strategy, plugins.

Interactions: Used by `index.css` and all JSX class names.

Common Mistakes: Content glob missing source files; dark mode not matching provider; overusing custom colors.

Why This Approach: Central design tokens for UI consistency.

What You Must Learn Before Building This File: Learn Tailwind config, utility classes, CSS themes, dark mode, and plugin usage.

### `frontend/postcss.config.js`

Purpose: Connects Tailwind and Autoprefixer into CSS processing.

Knowledge Required: PostCSS, Tailwind compilation, vendor prefixing.

Interactions: Used by Vite CSS pipeline.

Common Mistakes: Missing Tailwind plugin so classes do not compile.

Why This Approach: Standard Tailwind build pipeline.

What You Must Learn Before Building This File: Learn CSS processing, PostCSS plugins, browser compatibility, and Tailwind compilation.

### `frontend/eslint.config.js`

Purpose: Configures JavaScript/React linting.

Knowledge Required: ESLint, React hooks rules, code quality checks.

Interactions: Used by `npm run lint`.

Common Mistakes: Ignoring hook dependency warnings; lint config not matching modern flat config.

Why This Approach: Catches common frontend mistakes early.

What You Must Learn Before Building This File: Learn linting, ESLint rules, React hooks constraints, and static analysis.

### `frontend/Dockerfile`

Purpose: Builds React app with Node, then serves static output using Nginx.

Knowledge Required: Multi-stage Docker builds, npm ci, Vite build-time env vars, Nginx static hosting.

Interactions: Copies `docker/nginx.conf`; used by Compose `web` service.

Common Mistakes: Runtime env vars expected after Vite build; missing Nginx config; not using lockfile install.

Why This Approach: Small production image with only static assets and Nginx.

What You Must Learn Before Building This File: Learn Docker multi-stage builds, Node build process, static assets, and Nginx runtime serving.

## `frontend/src`

Purpose: Contains all React source code.

Knowledge Required: React components, hooks, JSX, state, effects, routing.

Interactions: Built by Vite into static files.

Common Mistakes: Too much repeated fetch logic; unhandled errors; mixing layout and domain code.

Why This Approach: Standard React source layout.

What You Must Learn Before Building This Folder: Learn React fundamentals, JSX syntax, component props, state, effects, and file organization.

### `frontend/src/main.jsx`

Purpose: Bootstraps React app into DOM, wraps it with theme, toast, router, and auth providers.

Knowledge Required: ReactDOM root rendering, context providers, BrowserRouter, StrictMode.

Interactions: Imports `App`, providers, CSS.

Inputs/Outputs: Input `#root` DOM element; output mounted React application.

Common Mistakes: Provider order wrong; missing CSS import; rendering before root exists.

Why This Approach: Centralizes global app setup.

What You Must Learn Before Building This File: Learn DOM mounting, React context, router providers, and global CSS imports.

### `frontend/src/App.jsx`

Purpose: Defines frontend routes and protected route wrapper.

Knowledge Required: React Router routes, redirects, nested routes, auth loading state.

Interactions: Uses `AuthContext`, `Shell`, page components.

Inputs/Outputs: Input browser path/auth state; output correct page or login redirect.

Common Mistakes: Infinite redirects; rendering protected pages before auth check completes.

Why This Approach: Keeps navigation and auth guard in one file.

What You Must Learn Before Building This File: Learn client-side routing, protected routes, nested layouts, and conditional rendering.

### `frontend/src/index.css`

Purpose: Imports Tailwind layers and defines reusable component classes like `.panel`, `.input`, buttons, labels, ambient background.

Knowledge Required: CSS, Tailwind `@apply`, layers, dark mode classes.

Interactions: Used by every component via class names.

Common Mistakes: Defining classes outside Tailwind layers incorrectly; inconsistent spacing; inaccessible color contrast.

Why This Approach: Shared classes reduce repetition in JSX.

What You Must Learn Before Building This File: Learn CSS cascade, Tailwind directives, utility composition, responsive/dark styling, and design consistency.

## `frontend/src/lib`

Purpose: Shared utility code for backend communication.

Knowledge Required: Fetch API, localStorage, error handling, binary downloads, WebSocket URLs.

Interactions: Used by almost every page and `AuthContext`.

Common Mistakes: Not attaching JWT; assuming every response is JSON; leaking object URLs.

Why This Approach: One API helper avoids duplicate request boilerplate.

What You Must Learn Before Building This Folder: Learn browser APIs, HTTP headers, JSON, Blob downloads, localStorage, and environment variables.

### `frontend/src/lib/api.js`

Purpose: Defines API base URL, WebSocket URL, token reader, JSON fetch wrapper, and download helper.

Knowledge Required: `fetch`, bearer headers, Vite env vars, error parsing, Blob URLs, WebSocket URL schemes.

Interactions: Used by auth context and all pages.

Inputs/Outputs: Input path/options; output JSON data, null for 204, or downloaded file.

Common Mistakes: Sending `Content-Type` on file uploads unnecessarily; not handling 204; wrong ws/wss protocol behind HTTPS.

Why This Approach: Centralized API access keeps frontend consistent.

What You Must Learn Before Building This File: Learn HTTP, JSON, browser storage, fetch promises, error handling, files/blobs, and WebSocket URLs.

## `frontend/src/contexts`

Purpose: Global shared state providers for auth, theme, and toast notifications.

Knowledge Required: React Context API, hooks, provider pattern, localStorage.

Interactions: Wrapped around app in `main.jsx`; used across components/pages.

Common Mistakes: Overusing context for rapidly changing data; missing provider around consumers.

Why This Approach: Avoids prop drilling for global app state.

What You Must Learn Before Building This Folder: Learn React context, providers/consumers, hooks, state persistence, and notification UX.

### `AuthContext.jsx`

Purpose: Manages logged-in user, loading state, register/login/logout actions, JWT storage.

Knowledge Required: React state/effects/memo, localStorage, auth API calls.

Interactions: Calls `/auth/me`, `/auth/login`, `/auth/register` through `api.js`; used by `App`, `Shell`, `LoginPage`, `AgentsPage`.

Inputs/Outputs: Input credentials/token; output user state and auth methods.

Common Mistakes: Leaving stale tokens after failed `/me`; not clearing user on logout.

Why This Approach: Auth state is needed by many screens.

What You Must Learn Before Building This File: Learn SPA authentication, JWT storage tradeoffs, React context, side effects, and memoized provider values.

### `ThemeContext.jsx`

Purpose: Stores dark/light mode and syncs it to `document.documentElement` and localStorage.

Knowledge Required: DOM class toggling, Tailwind dark mode, localStorage, React effects.

Interactions: Used by `Shell` theme toggle and Tailwind classes.

Inputs/Outputs: Input user toggle; output `dark` class on `<html>`.

Common Mistakes: Hydration/theme flash; mismatch with Tailwind dark mode strategy.

Why This Approach: Class-based dark mode is simple and compatible with Tailwind.

What You Must Learn Before Building This File: Learn browser DOM, CSS classes, persistent preferences, and Tailwind dark mode.

### `ToastContext.jsx`

Purpose: Provides global toast notification function and renders temporary success/error messages.

Knowledge Required: React state arrays, timers, context, conditional styling.

Interactions: Used by pages for API success/error feedback.

Inputs/Outputs: Input message/kind; output visible toast that auto-removes.

Common Mistakes: Timer leaks in complex apps; duplicate IDs with rapid notifications; inaccessible alerts.

Why This Approach: Simple feedback system without external dependency.

What You Must Learn Before Building This File: Learn UI notifications, timers, state updates, conditional classes, and accessibility basics.

## `frontend/src/components`

Purpose: Reusable UI building blocks and layout.

Knowledge Required: Component composition, props, icons, markdown rendering.

Interactions: Used by pages and route layout.

Common Mistakes: Putting page-specific business logic into generic components.

Why This Approach: Reduces repeated UI code and keeps pages focused.

What You Must Learn Before Building This Folder: Learn React props, composition, reusable components, and UI consistency.

### `Shell.jsx`

Purpose: Authenticated layout with sidebar navigation, mobile nav, header, theme toggle, logout, and routed content outlet.

Knowledge Required: React Router `NavLink`/`Outlet`, lucide icons, responsive Tailwind, auth/theme contexts.

Interactions: Wraps protected pages from `App.jsx`.

Inputs/Outputs: Input current route/user/theme; output layout and nested page.

Common Mistakes: Not using `end` on index route; mobile nav overflow; logout not clearing token.

Why This Approach: One consistent app frame for all authenticated pages.

What You Must Learn Before Building This File: Learn layouts, nested routing, responsive design, icons, and global state consumption.

### `Ui.jsx`

Purpose: Small reusable UI helpers: loader, status badge, metric card.

Knowledge Required: Props, conditional class maps, animation classes.

Interactions: Used across dashboard, repositories, agents, analysis, ML, login.

Common Mistakes: Missing fallback for unknown statuses; visual inconsistency.

Why This Approach: Keeps repeated UI patterns consistent.

What You Must Learn Before Building This File: Learn component props, conditional rendering, Tailwind styling, and loading/status UX.

### `Markdown.jsx`

Purpose: Renders markdown responses and syntax-highlighted code blocks.

Knowledge Required: Markdown, GitHub-flavored markdown, syntax highlighting, React component overrides.

Interactions: Used by chat, analysis, documents.

Inputs/Outputs: Input markdown string; output rendered HTML-like React UI.

Common Mistakes: Rendering unsafe HTML; not registering needed languages; code blocks overflowing.

Why This Approach: AI/report outputs are markdown, so rendering them improves readability.

What You Must Learn Before Building This File: Learn markdown, React Markdown, syntax highlighting, language registration, and safe rendering.

## `frontend/src/pages`

Purpose: Top-level screens for each product workflow.

Knowledge Required: React forms, API calls, state/effects, loading/errors, domain workflows.

Interactions: Pages call backend through `api.js`, use contexts, and render reusable components.

Common Mistakes: Too much duplicate fetch code; stale data after mutation; no optimistic rollback.

Why This Approach: Each route maps to one page file.

What You Must Learn Before Building This Folder: Learn routed page design, form handling, API integration, and user workflow modeling.

### `LoginPage.jsx`

Purpose: Register/login form and marketing-style intro for unauthenticated users.

Knowledge Required: Controlled inputs, form submission, auth context, toast context, conditional register/login mode.

Interactions: Calls `auth.login` or `auth.register`.

Inputs/Outputs: Input email/password/full name; output stored JWT/user state and redirect through `App`.

Common Mistakes: Sending full name on login unnecessarily is harmless here but should be understood; not disabling while loading.

Why This Approach: One screen handles both registration and sign-in.

What You Must Learn Before Building This File: Learn forms, controlled components, validation attributes, async submit handlers, and auth UX.

### `DashboardPage.jsx`

Purpose: Shows overview counts for repositories, agent logs, and ML risk plus recent activity.

Knowledge Required: `useEffect`, parallel API calls, derived metrics, list rendering.

Interactions: Calls `/repositories`, `/agents/logs`, `/ml/predictions`.

Inputs/Outputs: Input API data; output dashboard cards/lists.

Common Mistakes: Not handling API errors; average calculation with empty list.

Why This Approach: Gives users a home screen summary.

What You Must Learn Before Building This File: Learn dashboard design, data fetching, aggregation, and conditional empty states.

### `RepositoriesPage.jsx`

Purpose: Connects GitHub repositories, lists them, deletes them, and performs semantic search.

Knowledge Required: Forms, REST CRUD, optimistic UI deletion with rollback, select inputs, modal confirmation.

Interactions: Calls `/repositories`, `/repositories/{id}/search`, DELETE `/repositories/{id}`.

Inputs/Outputs: Input repo name/URL/search query; output queued repo/search results/deleted repo state.

Common Mistakes: Searching non-ready repo; deleting selected repo without clearing state; no confirmation for destructive action.

Why This Approach: Repository indexing is the first step for RAG workflows.

What You Must Learn Before Building This File: Learn CRUD UI, optimistic updates, search forms, modal UX, and GitHub URL input validation.

### `ChatPage.jsx`

Purpose: Chat UI for general or repository-specific questions.

Knowledge Required: Chat message state, form submit, markdown rendering, repository selector, history loading.

Interactions: Calls `/repositories`, `/chat/history`, `/chat`.

Inputs/Outputs: Input question/repository id; output chat bubbles and AI response.

Common Mistakes: Losing user message on failed response; not reloading history when repository changes.

Why This Approach: Provides the main RAG assistant user experience.

What You Must Learn Before Building This File: Learn chat UI patterns, async message updates, markdown rendering, and repository context selection.

### `AgentsPage.jsx`

Purpose: Launches multi-agent project generation, opens WebSocket for live events, lists generated projects, downloads ZIPs, deletes projects.

Knowledge Required: WebSocket client, background workflow UX, live logs, forms, downloads, delete confirmation.

Interactions: Calls `/agents/runs`, `/agents/logs`, `/agents/projects`, `/documents/project/{id}/zip`, DELETE `/agents/projects/{id}`, WebSocket `/agents/ws/{channel}`.

Inputs/Outputs: Input project name/requirements/repo; output streamed logs and downloadable generated artifacts.

Common Mistakes: Socket not closed on unmount; wrong channel when repository changes; not refreshing projects on run completion.

Why This Approach: Makes long-running agent work observable.

What You Must Learn Before Building This File: Learn browser WebSockets, event handling, cleanup effects, binary downloads, and long-running job UX.

### `AnalysisPage.jsx`

Purpose: Selects a ready repository and displays architecture summary metrics/report.

Knowledge Required: Select inputs, API calls, loading state, markdown display, metric cards.

Interactions: Calls `/repositories` and `/analysis/{id}`.

Inputs/Outputs: Input selected repo; output summary metrics and markdown report.

Common Mistakes: Allowing analysis before selection; not filtering only ready repos.

Why This Approach: Gives a focused architecture view separate from chat.

What You Must Learn Before Building This File: Learn analysis dashboards, loading buttons, conditional rendering, and report display.

### `MLPage.jsx`

Purpose: Lets users estimate metrics from indexed files or manually enter metrics, then predicts bug risk and maintainability.

Knowledge Required: Numeric controlled inputs, repository file selector, prediction history, progress bars.

Interactions: Calls `/repositories`, `/ml/repositories/{id}/estimate`, `/ml/predict`, `/ml/predictions`.

Inputs/Outputs: Input metrics/repo/file; output prediction card with probability, score, recommendations.

Common Mistakes: Treating model output as absolute truth; not converting numeric input strings to numbers; stale available files.

Why This Approach: Demonstrates predictive engineering capability in UI.

What You Must Learn Before Building This File: Learn forms with numeric data, ML result presentation, API-driven selects, and risk visualization.

### `DocumentsPage.jsx`

Purpose: Previews architecture docs, exports repository PDF, and downloads generated project ZIPs.

Knowledge Required: Document preview, file downloads, markdown rendering, select inputs.

Interactions: Calls `/repositories`, `/agents/projects`, `/analysis/{id}`, `/documents/repository/{id}/pdf`, `/documents/project/{id}/zip`.

Inputs/Outputs: Input selected repo/project action; output preview markdown or downloaded binary.

Common Mistakes: Missing disabled states; wrong downloaded filename; not handling download errors.

Why This Approach: Groups generated/exportable knowledge in one place.

What You Must Learn Before Building This File: Learn document UX, binary downloads, preview vs export flows, and API error feedback.

## Autogenerated / Not Manually Implemented Nodes

These appear in the project but should not be rebuilt by hand:

- `frontend/node_modules`: npm-installed third-party libraries.
- `frontend/dist`: Vite production build output.
- `frontend/package-lock.json`: npm-generated dependency lockfile. It is committed for reproducible installs but normally generated by `npm install`/`npm ci`.
- `backend/venv`, `backend/.venv`, root `venv`: Python virtual environments.
- `backend/__pycache__` and nested `__pycache__`: Python bytecode cache.
- `backend/models/*.joblib`: trained model artifacts generated by `training.py`.
- `backend/test_models`: generated test model artifacts.
- `backend/data/chroma` and `backend/test_chroma`: Chroma vector database data.
- `backend/*.db`: SQLite database files generated during local/test runs.
- `frontend/dist/assets/*`: generated bundled JavaScript/CSS.
- `python-installer.exe`: downloaded executable, not source.

## Rebuild Order From Scratch

1. Create root docs/deployment files: `.gitignore`, `.dockerignore`, `.env.example`, `README.md`, `docs`.
2. Build backend foundation: `requirements.txt`, `app/core/config.py`, `database/session.py`, `database/models.py`, `main.py`.
3. Add auth: `security.py`, `dependencies.py`, `schemas.py`, `routes/auth.py`.
4. Add router composition and middleware.
5. Add GitHub ingestion service and repository routes.
6. Add Chroma vector store and semantic search.
7. Add AI service, chat service, chat route, analysis service/route.
8. Add ML training, predictor, metric estimation, route, and training script.
9. Add LangGraph workflow, agent service, agent routes, WebSocket events.
10. Add export service and document routes.
11. Add migrations and tests.
12. Build frontend: package/config files, `main.jsx`, providers, `App.jsx`, `Shell`, UI helpers.
13. Build pages in user workflow order: login, dashboard, repositories, chat, agents, analysis, ML, documents.
14. Add Dockerfiles, Nginx config, Compose stack.
15. Add GitHub Actions CI.

