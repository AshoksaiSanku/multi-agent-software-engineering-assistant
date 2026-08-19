from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.database.models import User
from app.database.session import get_db
from app.services.analysis_service import architecture_report
from app.api.routes.repositories import owned_repository


router = APIRouter()


@router.get("/{repository_id}")
async def analyze_repository(
    repository_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = await owned_repository(repository_id, user, db)
    return {
        "repository_id": repository.id,
        "status": repository.status,
        "summary": repository.summary,
        "architecture_report": await architecture_report(repository),
    }

