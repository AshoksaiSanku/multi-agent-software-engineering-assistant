import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_current_user
from app.database.models import MLPrediction, User
from app.database.session import get_db
from app.ml.predictor import model_registry
from app.ml.metrics import estimate_repository_metrics
from app.schemas import PredictionRequest, PredictionResponse, RepositoryMetricEstimate
from app.api.routes.repositories import owned_repository


router = APIRouter()


@router.get("/repositories/{repository_id}/estimate", response_model=RepositoryMetricEstimate)
async def estimate_metrics(
    repository_id: str,
    file_path: str | None = None,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await owned_repository(repository_id, user, db)
    selected_path, metrics, files = await estimate_repository_metrics(
        db, repository_id, file_path
    )
    return RepositoryMetricEstimate(
        repository_id=repository_id,
        file_path=selected_path,
        metrics=metrics,
        available_files=files,
    )


@router.post("/predict", response_model=PredictionResponse)
async def predict_risk(
    payload: PredictionRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if payload.repository_id:
        await owned_repository(payload.repository_id, user, db)
    features = payload.metrics.model_dump()
    probability, maintainability, recommendations = await asyncio.to_thread(
        model_registry().predict, features
    )
    prediction = MLPrediction(
        user_id=user.id,
        repository_id=payload.repository_id,
        file_path=payload.file_path,
        features=features,
        bug_probability=probability,
        maintainability_score=maintainability,
        recommendations=recommendations,
    )
    db.add(prediction)
    await db.commit()
    await db.refresh(prediction)
    return prediction


@router.get("/predictions", response_model=list[PredictionResponse])
async def predictions(
    user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.scalars(
        select(MLPrediction)
        .where(MLPrediction.user_id == user.id)
        .order_by(MLPrediction.created_at.desc())
        .limit(100)
    )
    return list(result)
