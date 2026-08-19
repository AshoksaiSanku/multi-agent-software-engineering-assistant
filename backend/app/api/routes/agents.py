from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Response, WebSocket, WebSocketDisconnect, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.core.security import decode_access_token
from app.api.routes.repositories import owned_repository
from app.database.models import AgentLog, GeneratedProject, Repository, User
from app.database.session import AsyncSessionLocal, get_db
from app.schemas import AgentLogResponse, AgentRunAccepted, AgentRunRequest, GeneratedProjectResponse
from app.services.agent_service import event_hub, execute_agent_run
from app.services.generated_project_service import delete_generated_project


router = APIRouter()


@router.post("/runs", response_model=AgentRunAccepted, status_code=202)
async def start_run(
    payload: AgentRunRequest,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if payload.repository_id:
        await owned_repository(payload.repository_id, user, db)
    run_id = str(uuid4())
    background_tasks.add_task(
        execute_agent_run,
        run_id,
        user.id,
        payload.repository_id,
        payload.project_name,
        payload.requirements,
    )
    return AgentRunAccepted(run_id=run_id)


@router.get("/logs", response_model=list[AgentLogResponse])
async def logs(
    repository_id: str | None = None,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(AgentLog).where(AgentLog.user_id == user.id)
    if repository_id:
        query = query.where(AgentLog.repository_id == repository_id)
    result = await db.scalars(query.order_by(AgentLog.created_at.desc()).limit(100))
    return list(result)


@router.get("/projects", response_model=list[GeneratedProjectResponse])
async def projects(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.scalars(
        select(GeneratedProject)
        .where(GeneratedProject.user_id == user.id)
        .order_by(GeneratedProject.created_at.desc())
    )
    return list(result)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    project = await db.get(GeneratedProject, project_id)
    if not project or project.user_id != user.id:
        raise HTTPException(status_code=404, detail="Generated project not found")
    await delete_generated_project(db, project)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.websocket("/ws/{channel}")
async def status_stream(websocket: WebSocket, channel: str, token: str = Query(...)):
    user_id = decode_access_token(token)
    async with AsyncSessionLocal() as db:
        user = await db.get(User, user_id) if user_id else None
        permitted = channel == user_id if user else False
        if user and not permitted:
            repository = await db.get(Repository, channel)
            permitted = bool(repository and repository.user_id == user.id)
    if not user or not permitted:
        await websocket.close(code=1008)
        return
    await event_hub.connect(channel, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        event_hub.disconnect(channel, websocket)
