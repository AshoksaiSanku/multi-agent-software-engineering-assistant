import asyncio
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.database.models import GeneratedProject


async def delete_generated_project(db: AsyncSession, project: GeneratedProject) -> None:
    await cleanup_generated_project_files(project.id)
    await db.delete(project)
    await db.commit()


async def cleanup_generated_project_files(project_id: str) -> None:
    """Remove generated export artifacts if a future storage backend writes them to disk."""
    candidates = [
        settings.ml_model_path.parent / "generated_projects" / project_id,
        settings.ml_model_path.parent / "exports" / f"{project_id}.zip",
    ]
    for candidate in candidates:
        await asyncio.to_thread(remove_path_if_exists, candidate)


def remove_path_if_exists(path: Path) -> None:
    if path.is_file():
        path.unlink()
    elif path.is_dir():
        for child in path.rglob("*"):
            if child.is_file():
                child.unlink()
        for child in sorted(path.rglob("*"), reverse=True):
            if child.is_dir():
                child.rmdir()
        path.rmdir()
