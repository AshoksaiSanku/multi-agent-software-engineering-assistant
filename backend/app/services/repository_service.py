import logging
import re
from collections import Counter
from pathlib import PurePosixPath
from uuid import uuid4

from sqlalchemy import delete

from app.database.models import Embedding, Repository
from app.database.session import AsyncSessionLocal
from app.services.github_service import GitHubFile, GitHubRepositoryClient
from app.vector_store.store import RepositoryVectorStore, VectorDocument


logger = logging.getLogger(__name__)


def chunk_files(files: list[GitHubFile], chunk_size: int = 1800) -> list[VectorDocument]:
    chunks: list[VectorDocument] = []
    for file in files:
        lines = file.content.splitlines()
        buffer: list[str] = []
        size = 0
        chunk_index = 0
        for line in lines:
            if buffer and size + len(line) > chunk_size:
                chunks.append(
                    VectorDocument(
                        str(uuid4()), file.path, chunk_index, "\n".join(buffer)
                    )
                )
                buffer, size, chunk_index = [], 0, chunk_index + 1
            buffer.append(line)
            size += len(line) + 1
        if buffer:
            chunks.append(
                VectorDocument(str(uuid4()), file.path, chunk_index, "\n".join(buffer))
            )
    return chunks


def build_summary(files: list[GitHubFile]) -> dict:
    extension_counts = Counter(PurePosixPath(file.path).suffix or "other" for file in files)
    folders = Counter(
        file.path.split("/", 1)[0] if "/" in file.path else "root" for file in files
    )
    source_text = "\n".join(file.content for file in files)
    endpoints = len(re.findall(r"@(app|router)\.(get|post|put|delete|patch)", source_text))
    imports = sorted(
        set(
            re.findall(r"^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))", source_text, re.M)
        )
    )
    normalized_imports = sorted({item for group in imports for item in group if item})
    functions = sorted(set(re.findall(r"^\s*def\s+([a-zA-Z_]\w*)\s*\(", source_text, re.M)))
    features = detect_repository_features(source_text, normalized_imports)
    return {
        "languages": dict(extension_counts.most_common(10)),
        "top_directories": dict(folders.most_common(10)),
        "total_lines": sum(len(file.content.splitlines()) for file in files),
        "total_bytes": sum(file.size for file in files),
        "api_route_markers": endpoints,
        "files": [file.path for file in files],
        "imports": normalized_imports[:20],
        "functions": functions[:30],
        "detected_features": features,
        "project_type": infer_project_type(features, normalized_imports, endpoints),
        "architecture": (
            "Repository indexed for semantic analysis. Ask the assistant for component "
            "relationships, entry points, and recommended changes."
        ),
    }


def detect_repository_features(source_text: str, imports: list[str]) -> list[str]:
    lowered = source_text.lower()
    features: list[str] = []
    if "tkinter" in imports or "combobox" in lowered or "root = tk" in lowered:
        features.append("desktop_gui")
    if "random.choice" in lowered:
        features.append("random_generation")
    if "password" in lowered:
        features.append("password_generation")
    if "pyperclip" in imports or "copy(" in lowered:
        features.append("clipboard_copy")
    if "fastapi" in imports:
        features.append("fastapi_api")
    if "react" in lowered or ".jsx" in lowered:
        features.append("react_frontend")
    return features


def infer_project_type(features: list[str], imports: list[str], endpoints: int) -> str:
    if {"desktop_gui", "password_generation"}.issubset(features):
        return "Tkinter desktop password generator"
    if endpoints or "fastapi" in imports:
        return "FastAPI backend service"
    if "react_frontend" in features:
        return "React frontend application"
    if "desktop_gui" in features:
        return "Python desktop GUI application"
    return "Source code repository"


async def ingest_repository(repository_id: str) -> None:
    async with AsyncSessionLocal() as db:
        repository = await db.get(Repository, repository_id)
        if not repository:
            return
        repository.status = "indexing"
        await db.commit()
        try:
            branch, files = await GitHubRepositoryClient().fetch_files(repository.github_url)
            documents = chunk_files(files)
            await RepositoryVectorStore().index(repository.id, documents)
            await db.execute(
                delete(Embedding).where(Embedding.repository_id == repository.id)
            )
            db.add_all(
                [
                    Embedding(
                        repository_id=repository.id,
                        vector_id=document.vector_id,
                        file_path=document.path,
                        chunk_index=document.chunk_index,
                        metadata_json={
                            "characters": len(document.content),
                            "content": document.content,
                        },
                    )
                    for document in documents
                ]
            )
            repository.default_branch = branch
            repository.file_count = len(files)
            repository.summary = build_summary(files)
            repository.status = "ready"
            repository.error_message = None
            await db.commit()
        except Exception as exc:  # pragma: no cover - network failures are runtime concerns
            logger.exception("Repository ingestion failed for %s", repository_id)
            repository.status = "failed"
            repository.error_message = str(exc)[:500]
            await db.commit()
