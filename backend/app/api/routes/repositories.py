from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.database.models import (
    AgentLog,
    Conversation,
    Embedding,
    GeneratedProject,
    MLPrediction,
    Repository,
    User,
)
from app.database.session import get_db
from app.schemas import RepositoryCreate, RepositoryResponse, SearchResult, SemanticSearchRequest
from app.services.repository_service import ingest_repository
from app.vector_store.store import RepositoryVectorStore


router = APIRouter()


@router.post("", response_model=RepositoryResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_repository(
    payload: RepositoryCreate,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = Repository(
        user_id=user.id, name=payload.name, github_url=str(payload.github_url), status="queued"
    )
    db.add(repository)
    await db.commit()
    await db.refresh(repository)
    background_tasks.add_task(ingest_repository, repository.id)
    return repository


@router.get("", response_model=list[RepositoryResponse])
async def list_repositories(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.scalars(
        select(Repository).where(Repository.user_id == user.id).order_by(Repository.created_at.desc())
    )
    return list(result)


async def owned_repository(repository_id: str, user: User, db: AsyncSession) -> Repository:
    repository = await db.scalar(
        select(Repository).where(
            Repository.id == repository_id, Repository.user_id == user.id
        )
    )
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repository


@router.get("/{repository_id}", response_model=RepositoryResponse)
async def get_repository(
    repository_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await owned_repository(repository_id, user, db)


@router.delete("/{repository_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_repository(
    repository_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = await owned_repository(repository_id, user, db)
    await RepositoryVectorStore().delete_repository(repository.id)
    for model in [Embedding, Conversation, MLPrediction, GeneratedProject, AgentLog]:
        await db.execute(delete(model).where(model.repository_id == repository.id))
    await db.delete(repository)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{repository_id}/search", response_model=list[SearchResult])
async def semantic_search(
    repository_id: str,
    payload: SemanticSearchRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = await owned_repository(repository_id, user, db)
    if repository.status != "ready":
        raise HTTPException(status_code=409, detail="Repository is not indexed yet")
    return await RepositoryVectorStore().query(repository.id, payload.query, payload.limit)
