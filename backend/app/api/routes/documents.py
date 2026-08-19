from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.api.routes.repositories import owned_repository
from app.database.models import GeneratedProject, User
from app.database.session import get_db
from app.services.analysis_service import architecture_report
from app.services.export_service import project_zip, repository_pdf


router = APIRouter()


@router.get("/repository/{repository_id}/pdf")
async def export_pdf(
    repository_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repository = await owned_repository(repository_id, user, db)
    report = await architecture_report(repository)
    document = await asyncio.to_thread(repository_pdf, repository, report)
    return StreamingResponse(
        document,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{repository.name}.pdf"'},
    )


@router.get("/project/{project_id}/zip")
async def export_project_zip(
    project_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    project = await db.get(GeneratedProject, project_id)
    if not project or project.user_id != user.id:
        raise HTTPException(status_code=404, detail="Generated project not found")
    return StreamingResponse(
        project_zip(project),
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{project.name}.zip"'},
    )
import asyncio

