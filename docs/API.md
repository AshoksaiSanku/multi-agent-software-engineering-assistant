# API Reference

Interactive OpenAPI documentation is available at `/docs` when the FastAPI service is running.
All feature endpoints require `Authorization: Bearer <jwt>` except registration and login.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `POST` | `/api/v1/auth/register` | Create user and issue JWT |
| `POST` | `/api/v1/auth/login` | Authenticate and issue JWT |
| `GET` | `/api/v1/auth/me` | Get current user |
| `POST` | `/api/v1/repositories` | Queue GitHub repository indexing |
| `GET` | `/api/v1/repositories` | List owned repositories |
| `DELETE` | `/api/v1/repositories/{id}` | Delete repository, related rows, and vectors |
| `POST` | `/api/v1/repositories/{id}/search` | Semantic source search |
| `POST` | `/api/v1/chat` | Repository-aware AI answer |
| `GET` | `/api/v1/chat/history` | Persistent message history |
| `GET` | `/api/v1/analysis/{id}` | Architecture report |
| `POST` | `/api/v1/ml/predict` | Bug risk and maintainability prediction |
| `GET` | `/api/v1/ml/predictions` | Prediction history |
| `POST` | `/api/v1/agents/runs` | Launch multi-agent generation |
| `GET` | `/api/v1/agents/logs` | Persisted agent activity |
| `GET` | `/api/v1/agents/projects` | Generated projects |
| `DELETE` | `/api/v1/agents/projects/{id}` | Delete generated artifacts and metadata |
| `WS` | `/api/v1/agents/ws/{repository_or_user_id}?token=...` | Live statuses |
| `GET` | `/api/v1/documents/repository/{id}/pdf` | Export architecture PDF |
| `GET` | `/api/v1/documents/project/{id}/zip` | Export generated code |

If repository indexing returns a GitHub `403 rate limit exceeded` error, set a free
`GITHUB_TOKEN` in `.env` and restart the backend.

## ML input

`POST /api/v1/ml/predict` accepts:

```json
{
  "file_path": "src/payments.py",
  "repository_id": null,
  "metrics": {
    "cyclomatic_complexity": 21,
    "file_size": 680,
    "dependency_count": 12,
    "commit_frequency": 19
  }
}
```

The included bootstrap dataset is synthetic and makes the feature demonstrable. Train on
project-specific labeled defect history before using its probability operationally.
