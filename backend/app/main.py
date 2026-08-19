from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.middleware import RateLimitMiddleware
from app.api.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.database.session import create_tables
from app.ml.predictor import ModelRegistry


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    settings.create_directories()
    await create_tables()
    ModelRegistry().ensure_ready()
    yield


app = FastAPI(
    title=settings.project_name,
    version="1.0.0",
    description="Collaborative AI agents for repository understanding and code engineering.",
    lifespan=lifespan,
)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/health", tags=["operations"])
async def health() -> dict[str, str]:
    return {"status": "healthy", "service": settings.project_name}

