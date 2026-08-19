import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Embedding
from app.schemas import CodeMetrics
from app.vector_store.store import RepositoryVectorStore


async def estimate_repository_metrics(
    db: AsyncSession, repository_id: str, file_path: str | None = None
) -> tuple[str, CodeMetrics, list[str]]:
    rows = await db.execute(
        select(Embedding.file_path, Embedding.metadata_json)
        .where(Embedding.repository_id == repository_id)
        .order_by(Embedding.file_path, Embedding.chunk_index)
    )
    grouped: dict[str, list[dict]] = {}
    for path, metadata in rows.all():
        grouped.setdefault(path, []).append(metadata or {})
    grouped = await merge_vector_documents(repository_id, grouped)
    if not grouped:
        return file_path or "src/module.py", CodeMetrics(
            cyclomatic_complexity=1,
            file_size=0,
            dependency_count=0,
            commit_frequency=1,
        ), []

    selected_path = file_path if file_path in grouped else choose_primary_file(grouped)
    chunks = grouped[selected_path]
    text = "\n".join(str(chunk.get("content", "")) for chunk in chunks)
    characters = sum(int(chunk.get("characters", 0)) for chunk in chunks)
    lines = max(1, text.count("\n") + 1 if text.strip() else round(characters / 70))
    dependency_count = len(set(re.findall(r"^\s*(?:import|from)\s+([\w.]+)", text, re.M)))
    branch_count = len(
        re.findall(r"\b(if|elif|for|while|except|case|and|or)\b", text)
    )
    function_count = len(re.findall(r"^\s*def\s+\w+\s*\(", text, re.M))
    complexity = max(1, branch_count + function_count)
    commit_frequency = max(1, min(60, round(lines / 20) + dependency_count))
    return selected_path, CodeMetrics(
        cyclomatic_complexity=float(complexity),
        file_size=float(lines),
        dependency_count=float(dependency_count),
        commit_frequency=float(commit_frequency),
    ), sorted(grouped)


def choose_primary_file(grouped: dict[str, list[dict]]) -> str:
    def score(path: str) -> tuple[int, int]:
        extension_bonus = 2 if path.endswith((".py", ".js", ".ts", ".jsx", ".tsx", ".java")) else 0
        size = sum(int(chunk.get("characters", 0)) for chunk in grouped[path])
        return extension_bonus, size

    return max(grouped, key=score)


async def merge_vector_documents(
    repository_id: str, grouped: dict[str, list[dict]]
) -> dict[str, list[dict]]:
    if grouped and all(any(chunk.get("content") for chunk in chunks) for chunks in grouped.values()):
        return grouped
    try:
        documents = await RepositoryVectorStore().documents(repository_id)
    except Exception:
        return grouped
    for document in documents:
        path = str(document["file_path"])
        chunks = grouped.setdefault(path, [])
        if any(chunk.get("content") == document["content"] for chunk in chunks):
            continue
        chunks.append(document)
    for chunks in grouped.values():
        chunks.sort(key=lambda chunk: int(chunk.get("chunk_index", 0)))
    return grouped
