import asyncio
import os
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import select


os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_assistant.db"
os.environ["ML_MODEL_PATH"] = str(Path("./test_models"))
os.environ["CHROMA_PATH"] = str(Path("./test_chroma"))

from app.main import app  # noqa: E402
from app.database.models import Embedding, Repository  # noqa: E402
from app.database.session import AsyncSessionLocal  # noqa: E402
from app.vector_store.store import RepositoryVectorStore, VectorDocument  # noqa: E402


def test_health_endpoint() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_authenticated_prediction_and_offline_agent_export() -> None:
    unique = uuid4().hex
    email = f"engineer-{unique}@example.com"
    project_name = f"Notification Center {unique}"
    with TestClient(app) as client:
        registered = client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "full_name": "Test Engineer",
                "password": "correct-horse-123",
            },
        )
        assert registered.status_code in {201, 409}
        if registered.status_code == 409:
            registered = client.post(
                "/api/v1/auth/login",
                json={"email": email, "password": "correct-horse-123"},
            )
        token = registered.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        prediction = client.post(
            "/api/v1/ml/predict",
            headers=headers,
            json={
                "file_path": "src/payment.py",
                "metrics": {
                    "cyclomatic_complexity": 22,
                    "file_size": 720,
                    "dependency_count": 15,
                    "commit_frequency": 28,
                },
            },
        )
        assert prediction.status_code == 200
        assert 0 <= prediction.json()["bug_probability"] <= 1
        run = client.post(
            "/api/v1/agents/runs",
            headers=headers,
            json={
                "project_name": project_name,
                "requirements": "Create a secure notifications API and React notification preferences page.",
            },
        )
        assert run.status_code == 202
        projects = client.get("/api/v1/agents/projects", headers=headers).json()
        assert projects
        project = next(item for item in projects if item["name"] == project_name)
        files = project["files"]
        assert "create_payment" in files["backend/generated_feature.py"]
        assert "PaymentCreate" in files["backend/generated_feature.py"]
        assert "Generated in free local mode" in files["README.generated.md"]
        assert "placeholder" not in files["backend/generated_feature.py"].lower()
        archive = client.get(
            f"/api/v1/documents/project/{project['id']}/zip", headers=headers
        )
        assert archive.status_code == 200
        assert archive.headers["content-type"] == "application/zip"
        deleted = client.delete(
            f"/api/v1/agents/projects/{project['id']}", headers=headers
        )
        assert deleted.status_code == 204
        projects_after_delete = client.get("/api/v1/agents/projects", headers=headers).json()
        assert project["id"] not in {item["id"] for item in projects_after_delete}
        missing_archive = client.get(
            f"/api/v1/documents/project/{project['id']}/zip", headers=headers
        )
        assert missing_archive.status_code == 404


def test_delete_repository_removes_database_rows_and_vectors() -> None:
    unique = uuid4().hex
    email = f"repo-delete-{unique}@example.com"
    with TestClient(app) as client:
        registered = client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "full_name": "Repo Delete",
                "password": "correct-horse-123",
            },
        )
        token = registered.json()["access_token"]
        user_id = registered.json()["user"]["id"]
        headers = {"Authorization": f"Bearer {token}"}
        repository_id = asyncio.run(seed_repository_with_vectors(user_id))
        response = client.delete(f"/api/v1/repositories/{repository_id}", headers=headers)
        assert response.status_code == 204
        repositories = client.get("/api/v1/repositories", headers=headers).json()
        assert repository_id not in {repository["id"] for repository in repositories}

    assert asyncio.run(repository_deleted(repository_id))
    assert asyncio.run(RepositoryVectorStore().query(repository_id, "delete auth", 1)) == []


def test_repository_metric_estimate_uses_indexed_file_content() -> None:
    unique = uuid4().hex
    email = f"metric-estimate-{unique}@example.com"
    with TestClient(app) as client:
        registered = client.post(
            "/api/v1/auth/register",
            json={
                "email": email,
                "full_name": "Metric Estimate",
                "password": "correct-horse-123",
            },
        )
        token = registered.json()["access_token"]
        user_id = registered.json()["user"]["id"]
        headers = {"Authorization": f"Bearer {token}"}
        repository_id = asyncio.run(seed_repository_for_metrics(user_id))
        response = client.get(
            f"/api/v1/ml/repositories/{repository_id}/estimate", headers=headers
        )

    assert response.status_code == 200
    body = response.json()
    assert body["file_path"] == "t3.py"
    assert "t3.py" in body["available_files"]
    assert body["metrics"]["cyclomatic_complexity"] >= 4
    assert body["metrics"]["dependency_count"] >= 2
    assert body["metrics"]["file_size"] > 5


@pytest.mark.asyncio
async def test_local_repository_vector_search() -> None:
    store = RepositoryVectorStore()
    repository_id = str(uuid4())
    await store.index(
        repository_id,
        [
            VectorDocument(
                vector_id=str(uuid4()),
                path="app/auth.py",
                chunk_index=0,
                content="JWT authentication validates a bearer token during login.",
            ),
            VectorDocument(
                vector_id=str(uuid4()),
                path="app/payments.py",
                chunk_index=0,
                content="Invoices calculate taxes and payment totals.",
            ),
        ],
    )
    results = await store.query(repository_id, "authentication bearer token", 1)
    assert results[0]["file_path"] == "app/auth.py"


async def seed_repository_with_vectors(user_id: str) -> str:
    repository_id = str(uuid4())
    vector_id = str(uuid4())
    async with AsyncSessionLocal() as db:
        repository = Repository(
            id=repository_id,
            user_id=user_id,
            name="Delete Me",
            github_url="https://github.com/example/delete-me",
            default_branch="main",
            status="ready",
            file_count=1,
            summary={},
        )
        db.add(repository)
        db.add(
            Embedding(
                repository_id=repository_id,
                vector_id=vector_id,
                file_path="app/delete_me.py",
                chunk_index=0,
                metadata_json={},
            )
        )
        await db.commit()
    await RepositoryVectorStore().index(
        repository_id,
        [
            VectorDocument(
                vector_id=vector_id,
                path="app/delete_me.py",
                chunk_index=0,
                content="delete repository vector cleanup auth",
            )
        ],
    )
    return repository_id


async def seed_repository_for_metrics(user_id: str) -> str:
    repository_id = str(uuid4())
    vector_id = str(uuid4())
    content = """
import random
from tkinter import Tk


def low():
    if True:
        for item in range(10):
            if item % 2:
                print(random.choice("abc"))
    else:
        print("choose an option")
"""
    async with AsyncSessionLocal() as db:
        repository = Repository(
            id=repository_id,
            user_id=user_id,
            name="Password Generator",
            github_url="https://github.com/example/password-generator",
            default_branch="main",
            status="ready",
            file_count=1,
            summary={},
        )
        db.add(repository)
        db.add(
            Embedding(
                repository_id=repository_id,
                vector_id=vector_id,
                file_path="t3.py",
                chunk_index=0,
                metadata_json={"characters": len(content), "content": content},
            )
        )
        await db.commit()
    await RepositoryVectorStore().index(
        repository_id,
        [
            VectorDocument(
                vector_id=vector_id,
                path="t3.py",
                chunk_index=0,
                content=content,
            )
        ],
    )
    return repository_id


async def repository_deleted(repository_id: str) -> bool:
    async with AsyncSessionLocal() as db:
        repository = await db.get(Repository, repository_id)
        embedding = await db.scalar(
            select(Embedding).where(Embedding.repository_id == repository_id)
        )
        return repository is None and embedding is None
