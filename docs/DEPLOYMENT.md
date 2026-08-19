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
