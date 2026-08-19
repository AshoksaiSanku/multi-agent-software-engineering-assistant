# Lesson-20: Docker Deployment, Verification, Refactoring, and Future Improvements

## Objective

In this lesson you will finish the rebuild by adding the Docker deployment layer, running the full application, verifying every major workflow, and learning how to explain the project clearly in an interview.

By the end of this lesson, your project will run as three coordinated services:

- PostgreSQL database
- FastAPI backend
- React frontend served by Nginx

## What You Will Create

You will create or verify these files:

```text
docker-compose.yml
backend/Dockerfile
frontend/Dockerfile
docker/nginx.conf
.env.example
docs/DEPLOYMENT.md
```

## Important Copy-Paste Rule

For every file in this lesson, do exactly this:

1. Create the file using the command shown.
2. Open that file in VS Code.
3. If the file already has old content, delete all old content from that file.
4. Copy the exact code block shown for that file.
5. Paste that exact code into the file.
6. Save the file.

Do not copy the markdown fence lines such as:

```text
```yaml
```

Only copy the code inside the code block.

Do not skip any line. Do not shorten the code. Do not replace any section with your own version unless the lesson specifically tells you to change a value.

## Folder Setup

From the project root, run:

```powershell
mkdir docker
mkdir docs
```

If PowerShell says the folders already exist, that is fine.

Your project root should now contain:

```text
backend/
docker/
docs/
frontend/
docker-compose.yml
.env.example
```

## File 1: docker-compose.yml

### Why This File Exists

`docker-compose.yml` describes the complete local deployment. Instead of starting PostgreSQL, the API, and the web server manually in different terminals, Docker Compose starts them together and connects them on one private Docker network.

### Responsibility

This file is responsible for:

- Creating the PostgreSQL database container.
- Building and starting the backend container.
- Building and starting the frontend/Nginx container.
- Creating persistent volumes for database data, Chroma vector data, and ML model files.
- Passing production-style environment variables into the containers.

### Create The File

From the project root, run:

```powershell
New-Item -ItemType File -Path docker-compose.yml -Force
```

Now open `docker-compose.yml`.

Delete everything inside the file if it already has content.

Copy this exact code and paste it into `docker-compose.yml`:

```yaml
# Docker Compose runs the whole application stack with one command.
# Each top-level service becomes one container on the same internal network.
services:
  # PostgreSQL stores users, repositories, generated projects, agent runs,
  # and all other relational application data.
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: assistant
      POSTGRES_USER: assistant
      POSTGRES_PASSWORD: assistant
    volumes:
      # This named volume keeps database data even if the container is recreated.
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      # The backend should not start until PostgreSQL is accepting connections.
      test: ["CMD-SHELL", "pg_isready -U assistant"]
      interval: 5s
      timeout: 5s
      retries: 10

  # The API container runs Alembic migrations and then starts FastAPI with Uvicorn.
  api:
    build: ./backend
    env_file: .env
    environment:
      # Inside Docker, the database hostname is the Compose service name: db.
      DATABASE_URL: postgresql+asyncpg://assistant:assistant@db:5432/assistant
      # These paths live inside the backend container and are backed by volumes.
      CHROMA_PATH: /app/data/chroma
      ML_MODEL_PATH: /app/models
    volumes:
      # Chroma vector indexes must persist across container restarts.
      - chroma_data:/app/data/chroma
      # Trained ML artifacts must also persist across restarts.
      - ml_models:/app/models
    ports:
      # Expose the FastAPI server on the host for direct API testing.
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy

  # The web container builds React and serves the static files through Nginx.
  web:
    build:
      context: .
      dockerfile: frontend/Dockerfile
      args:
        # The browser talks to Nginx on the same origin, then Nginx proxies /api.
        VITE_API_URL: /api/v1
        VITE_WS_URL: /api/v1
    ports:
      # Open the finished application at http://localhost:3000.
      - "3000:80"
    depends_on:
      - api

# Named volumes are managed by Docker and survive normal container recreation.
volumes:
  postgres_data:
  chroma_data:
  ml_models:
```

### Important Sections Explained

`services` defines the running containers.

`db` uses the official PostgreSQL image and stores data in the `postgres_data` volume.

`api` builds the backend from `backend/Dockerfile`, reads `.env`, overrides Docker-specific paths, exposes port `8000`, and waits for the database health check.

`web` builds the frontend from `frontend/Dockerfile`, serves the compiled React app with Nginx, and exposes port `3000`.

`volumes` defines named persistent storage managed by Docker.

## File 2: backend/Dockerfile

### Why This File Exists

The backend Dockerfile packages the FastAPI application into a repeatable Python runtime. Anyone with Docker can run the backend without manually installing Python packages on their machine.

### Responsibility

This file is responsible for:

- Choosing the Python base image.
- Installing required operating system libraries.
- Installing Python dependencies.
- Copying the backend source code.
- Creating directories used by Chroma and ML models.
- Running migrations before the API server starts.

### Create The File

From the project root, run:

```powershell
New-Item -ItemType File -Path backend\Dockerfile -Force
```

Now open `backend/Dockerfile`.

Delete everything inside the file if it already has content.

Copy this exact code and paste it into `backend/Dockerfile`:

```dockerfile
# Use a small official Python image for the backend runtime.
FROM python:3.12-slim AS runtime

# Keep Python predictable in containers:
# - Do not write .pyc files.
# - Flush logs immediately so Docker logs show real-time output.
# - Add /app to the Python import path.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# All backend commands run from /app inside the container.
WORKDIR /app

# libgomp1 is required by some ML/scientific Python packages.
# The apt cache is removed to keep the final image smaller.
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*

# Install dependencies before copying source code so Docker can cache this layer.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend application into the container.
COPY . .

# Create persistent-data mount points used by Chroma and ML model artifacts.
RUN mkdir -p /app/data/chroma /app/models

# FastAPI listens on port 8000.
EXPOSE 8000

# Apply database migrations, then start the ASGI server.
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
```

### Important Sections Explained

`FROM python:3.12-slim` gives the backend a clean Python 3.12 Linux environment.

`ENV PYTHONPATH=/app` allows imports like `from app.main import app` to work.

`RUN apt-get ... libgomp1` installs a native dependency used by machine learning packages.

`COPY requirements.txt .` and `RUN pip install ...` install backend packages.

`CMD` first runs `alembic upgrade head`, then starts `uvicorn`.

## File 3: frontend/Dockerfile

### Why This File Exists

The frontend Dockerfile builds the React application into static files and serves them with Nginx. This is closer to production than running the Vite development server.

### Responsibility

This file is responsible for:

- Installing frontend dependencies.
- Building the Vite React app.
- Passing API and WebSocket URLs at build time.
- Copying the built files into Nginx.
- Loading the custom Nginx reverse proxy configuration.

### Create The File

From the project root, run:

```powershell
New-Item -ItemType File -Path frontend\Dockerfile -Force
```

Now open `frontend/Dockerfile`.

Delete everything inside the file if it already has content.

Copy this exact code and paste it into `frontend/Dockerfile`:

```dockerfile
# Stage 1: build the React application with Node.
FROM node:22-alpine AS build

WORKDIR /app

# Install dependencies first so Docker can reuse the npm install layer.
COPY frontend/package*.json ./
RUN npm ci

# Copy the frontend source code into the build container.
COPY frontend/ .

# Vite reads these values while building the browser bundle.
ARG VITE_API_URL=/api/v1
ARG VITE_WS_URL=/api/v1
ENV VITE_API_URL=$VITE_API_URL VITE_WS_URL=$VITE_WS_URL

# Create the production static files in /app/dist.
RUN npm run build

# Stage 2: serve the compiled app with Nginx.
FROM nginx:1.27-alpine

# Copy the Vite build output into Nginx's public web directory.
COPY --from=build /app/dist /usr/share/nginx/html

# Copy the reverse proxy and single-page-app routing rules.
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# Nginx listens on port 80 inside the container.
EXPOSE 80
```

### Important Sections Explained

This Dockerfile uses two stages.

The `build` stage uses Node to run `npm ci` and `npm run build`.

The final Nginx stage contains only static files and the web server, which keeps the final runtime image smaller.

`ARG VITE_API_URL=/api/v1` means the browser calls the same origin instead of directly calling `localhost:8000`.

## File 4: docker/nginx.conf

### Why This File Exists

Nginx serves the frontend and forwards API requests to FastAPI. This lets the browser use `http://localhost:3000` for the whole application.

### Responsibility

This file is responsible for:

- Serving React static files.
- Forwarding REST API requests to the backend container.
- Forwarding WebSocket agent events to the backend container.
- Supporting React Router routes with `try_files`.

### Create The File

From the project root, run:

```powershell
New-Item -ItemType File -Path docker\nginx.conf -Force
```

Now open `docker/nginx.conf`.

Delete everything inside the file if it already has content.

Copy this exact code and paste it into `docker/nginx.conf`:

```nginx
server {
    # Nginx listens on port 80 inside the web container.
    listen 80;
    server_name _;

    # The React build output is copied here by frontend/Dockerfile.
    root /usr/share/nginx/html;
    index index.html;

    # Agent workflow progress uses WebSockets, so this route must preserve
    # the HTTP upgrade headers when proxying to FastAPI.
    location /api/v1/agents/ws/ {
        proxy_pass http://api:8000/api/v1/agents/ws/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # All normal API calls are proxied to the backend service.
    # The hostname api is the Docker Compose service name.
    location /api/ {
        proxy_pass http://api:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # React Router handles client-side routes. If a real file does not exist,
    # return index.html so the frontend router can render the correct page.
    location / {
        try_files $uri /index.html;
    }
}
```

### Important Sections Explained

`location /api/` sends REST API traffic to the backend container.

`location /api/v1/agents/ws/` sends WebSocket traffic to the backend and includes the upgrade headers required for WebSockets.

`try_files $uri /index.html` makes browser refresh work on frontend routes.

## File 5: .env.example

### Why This File Exists

`.env.example` documents every environment variable needed by the application. It is safe to commit because it does not contain real secrets.

### Responsibility

This file is responsible for:

- Showing the required backend settings.
- Showing frontend build settings.
- Showing local AI and OpenAI settings.
- Showing repository ingestion limits.
- Showing Docker-compatible storage paths.

### Create The File

From the project root, run:

```powershell
New-Item -ItemType File -Path .env.example -Force
```

Now open `.env.example`.

Delete everything inside the file if it already has content.

Copy this exact code and paste it into `.env.example`:

```dotenv
# Application mode. Use development locally and production for deployment.
APP_ENV=development

# Human-readable project name shown in API metadata.
PROJECT_NAME=Multi-Agent AI Software Engineering Assistant

# All backend routes are mounted under this prefix.
API_PREFIX=/api/v1

# Replace this before running anything public.
SECRET_KEY=replace-with-a-long-random-secret-key

# JWT access token lifetime in minutes.
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Docker Compose database URL. The hostname db matches the Compose service.
DATABASE_URL=postgresql+asyncpg://assistant:assistant@db:5432/assistant

# Allowed browser origins for development and Docker local usage.
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Optional OpenAI settings. Leave OPENAI_API_KEY empty when using local mode.
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# AI_PROVIDER=local keeps the app usable without paid API calls.
AI_PROVIDER=local
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5-coder:1.5b

# Optional GitHub token for higher GitHub API limits.
GITHUB_TOKEN=

# Docker container paths for persistent Chroma and ML model data.
CHROMA_PATH=/app/data/chroma
ML_MODEL_PATH=/app/models

# Safety limit for repository ingestion.
MAX_REPOSITORY_FILES=180

# Simple in-process API rate limit.
RATE_LIMIT_PER_MINUTE=120

# Frontend development URLs. Docker overrides these during image build.
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/api/v1
```

### Important Settings Explained

`SECRET_KEY` signs JWT tokens. In real deployment, replace it with a long random value.

`DATABASE_URL` uses `db` as the host because Docker Compose service names become internal DNS names.

`AI_PROVIDER=local` lets the project run without OpenAI billing.

`CHROMA_PATH` and `ML_MODEL_PATH` point to persistent Docker volume paths.

`VITE_API_URL` and `VITE_WS_URL` are used by the frontend during local Vite development.

## File 6: docs/DEPLOYMENT.md

### Why This File Exists

`docs/DEPLOYMENT.md` explains how to deploy the project beyond the development environment. It gives a local Docker baseline and outlines hosted deployment options.

### Responsibility

This file is responsible for:

- Explaining the Docker deployment command.
- Explaining which ports are exposed.
- Explaining what should be changed for hosted environments.
- Listing scaling improvements needed before high traffic.

### Create The File

From the project root, run:

```powershell
New-Item -ItemType File -Path docs\DEPLOYMENT.md -Force
```

Now open `docs/DEPLOYMENT.md`.

Delete everything inside the file if it already has content.

Copy this exact code and paste it into `docs/DEPLOYMENT.md`:

```markdown
# Deployment

## Docker production baseline

Create `.env` from `.env.example`, set `APP_ENV=production` and a strong `SECRET_KEY`,
keep `AI_PROVIDER=local` for the free mode, and run:

```bash
docker compose up --build -d
```

The UI is served on port `3000`, the API on port `8000`, and PostgreSQL data, Chroma vectors,
and trained model artifacts are stored in Docker volumes. Use managed PostgreSQL and external
volume/object storage for hosted environments.

## Render and Railway

Deploy the API from `backend/Dockerfile`, set all environment variables, attach a PostgreSQL
database, and mount persistent storage for `/app/data/chroma` and `/app/models`. Deploy the
frontend Dockerfile separately with `VITE_API_URL` and `VITE_WS_URL` directed to the API URL.
For free LLM responses, deploy Ollama separately or use the deterministic local mode.

## AWS outline

Run the API and frontend images on ECS Fargate behind an Application Load Balancer, use RDS
PostgreSQL, and mount EFS for Chroma/model state or replace Chroma with a managed vector store.
Store `SECRET_KEY`, `OPENAI_API_KEY`, and `GITHUB_TOKEN` in AWS Secrets Manager. Use CloudWatch
logs and configure TLS, WAF throttling, automated RDS backups, and private networking.

## Scaling changes before high traffic

- Run ingestion and agent generation through Celery, Dramatiq, or a managed job queue.
- Publish agent events through Redis so WebSockets work across API replicas.
- Replace the local limiter with Redis/API-gateway limits.
- Run migrations as a release task, not in every replica startup.
- Provide labeled defect data and model monitoring for ML predictions.
```

### Important Sections Explained

`Docker production baseline` gives the minimum local production-like deployment.

`Render and Railway` explains how to split backend and frontend deployment on beginner-friendly platforms.

`AWS outline` explains a more professional cloud architecture.

`Scaling changes before high traffic` lists the refactors needed when the app grows beyond one backend instance.

## Create Your Local .env File

`.env.example` is only a template. Docker Compose reads `.env`, so create it now.

From the project root, run:

```powershell
Copy-Item .env.example .env
```

Now open `.env` and change this line:

```dotenv
SECRET_KEY=replace-with-a-long-random-secret-key
```

Use any long random value while learning. Example:

```dotenv
SECRET_KEY=local-development-secret-change-before-production-123456789
```

For free local mode, keep:

```dotenv
AI_PROVIDER=local
OPENAI_API_KEY=
```

## Build And Run The Full Stack

From the project root, run:

```powershell
docker compose up --build
```

Wait until you see logs showing:

- PostgreSQL is healthy.
- Alembic migrations have run.
- Uvicorn is running on port `8000`.
- Nginx is running for the frontend.

Open the application:

```text
http://localhost:3000
```

Open the API docs:

```text
http://localhost:8000/docs
```

If you want the stack to run in the background, stop the foreground process with `Ctrl+C`, then run:

```powershell
docker compose up --build -d
```

To see logs while running in the background:

```powershell
docker compose logs -f
```

To stop the stack:

```powershell
docker compose down
```

## Verification Checklist

Use the browser at:

```text
http://localhost:3000
```

Complete these checks in order:

1. Register a new user.
2. Log in with that user.
3. Add a GitHub repository URL.
4. Wait until the repository status becomes ready.
5. Run semantic code search.
6. Ask a chat question about the repository.
7. Generate architecture analysis.
8. Run ML bug-risk prediction.
9. Start a multi-agent workflow.
10. Watch the workflow events update in the UI.
11. Download the generated ZIP file.
12. Download the generated PDF file.
13. Delete the generated project.
14. Delete the repository.

## Command Verification

Check running containers:

```powershell
docker compose ps
```

Expected result:

```text
NAME                 SERVICE   STATUS
...                  db        running
...                  api       running
...                  web       running
```

Check backend health:

```powershell
Invoke-RestMethod http://localhost:8000/api/v1/health
```

Expected result:

```powershell
status
------
ok
```

Check frontend response headers:

```powershell
Invoke-WebRequest http://localhost:3000
```

Expected result:

```text
StatusCode        : 200
StatusDescription : OK
```

## Troubleshooting

### Docker says the port is already allocated

Another process is already using port `3000` or `8000`.

Run:

```powershell
docker compose down
```

Then check what is using the port:

```powershell
netstat -ano | findstr :3000
netstat -ano | findstr :8000
```

Stop the conflicting process or change the port mapping in `docker-compose.yml`.

### Backend cannot connect to database

Make sure the Docker database URL uses `db`, not `localhost`:

```dotenv
DATABASE_URL=postgresql+asyncpg://assistant:assistant@db:5432/assistant
```

Inside Docker, `localhost` would mean the backend container itself. The database lives in the `db` container.

### Frontend loads but API calls fail

Make sure `docker/nginx.conf` contains this API proxy:

```nginx
location /api/ {
    proxy_pass http://api:8000/api/;
    proxy_http_version 1.1;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

Then rebuild:

```powershell
docker compose up --build
```

### WebSocket events do not appear

Make sure `docker/nginx.conf` contains this WebSocket proxy:

```nginx
location /api/v1/agents/ws/ {
    proxy_pass http://api:8000/api/v1/agents/ws/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

The `Upgrade` and `Connection` headers are required for WebSockets.

## Refactoring Review

The application is now complete, but a production system can still be improved.

Recommended future refactors:

- Replace in-process rate limiting with Redis.
- Replace the in-process WebSocket event hub with Redis pub/sub.
- Move long repository ingestion and generation jobs to Celery, Dramatiq, or a managed queue.
- Add Playwright tests for the main frontend workflows.
- Add dependency and container security scanning.
- Train ML models on real defect history instead of demo features.
- Store production secrets in a managed secret system.
- Add organization and team-based authorization.
- Run database migrations as a release job instead of inside every API container.

## Interview Explanation

Use this short explanation:

```text
I built a full-stack AI engineering workspace with a React frontend, FastAPI backend, JWT authentication, GitHub repository ingestion, ChromaDB semantic search, RAG chat, LangGraph multi-agent generation, ML bug-risk prediction, PDF and ZIP exports, Docker deployment, and CI.
```

Use this deeper explanation:

```text
The project is split into a FastAPI backend and a React frontend. The backend handles authentication, repository ingestion, vector indexing, semantic search, chat, architecture analysis, ML prediction, and agent workflow orchestration. PostgreSQL stores relational data, ChromaDB stores code embeddings, and generated projects can be exported as ZIP and PDF files. The frontend provides the user workflow, while Docker Compose runs PostgreSQL, the API, and the Nginx-served frontend together.
```

## Final Success Criteria

You are done when all of these are true:

- `docker compose up --build` starts without errors.
- `http://localhost:3000` loads the frontend.
- `http://localhost:8000/docs` loads the API documentation.
- You can register and log in.
- You can ingest a repository.
- Semantic search returns results.
- Chat returns an answer.
- Architecture analysis runs.
- ML prediction runs.
- Agent generation runs.
- ZIP and PDF exports download successfully.

At this point, the rebuild is complete in functionality.
