from fastapi import APIRouter

from app.api.routes import agents, analysis, auth, chat, documents, ml, repositories


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(repositories.router, prefix="/repositories", tags=["repositories"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(ml.router, prefix="/ml", tags=["machine-learning"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])

