from __future__ import annotations

from fastapi import APIRouter, Request

from app.core.config import get_settings

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health_check(
    request: Request,
) -> dict:
    settings = get_settings()

    rag = getattr(
        request.app.state,
        "rag",
        None,
    )

    return {
        "status": "ok",
        "application": settings.app_name,
        "version": settings.api_version,
        "rag_initialized": rag is not None,
        "llm_provider": settings.llm_provider,
        "llm_model": settings.llm_model,
        "embedding_model": settings.embedding_model,
        "qdrant_collection": settings.qdrant_collection_name,
    }