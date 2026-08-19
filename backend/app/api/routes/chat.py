from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.database.models import Conversation, User
from app.database.session import get_db
from app.schemas import ChatMessage, ChatRequest, ChatResponse
from app.api.routes.repositories import owned_repository
from app.services.chat_service import ChatService


router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(
    payload: ChatRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if payload.repository_id:
        await owned_repository(payload.repository_id, user, db)
    return await ChatService().answer(db, user, payload.repository_id, payload.question)


@router.get("/history", response_model=list[ChatMessage])
async def history(
    repository_id: str | None = None,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    query = select(Conversation).where(Conversation.user_id == user.id)
    if repository_id:
        query = query.where(Conversation.repository_id == repository_id)
    result = await db.scalars(query.order_by(Conversation.created_at.asc()).limit(200))
    return list(result)
