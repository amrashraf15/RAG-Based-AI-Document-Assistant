from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from app.core.config import get_settings
from app.models.generation import (
    ChatRequest,
    RAGResponse,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=RAGResponse,
)
def chat(
    request: Request,
    body: ChatRequest,
) -> RAGResponse:

    if not body.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty.",
        )

    if body.candidate_k < body.top_k:
        raise HTTPException(
            status_code=400,
            detail=(
                "candidate_k must be greater than "
                "or equal to top_k."
            ),
        )

    if (
        body.dense_weight == 0
        and body.lexical_weight == 0
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "At least one retrieval weight "
                "must be greater than zero."
            ),
        )

    settings = get_settings()

    rag = getattr(
        request.app.state,
        "rag",
        None,
    )

    if rag is None:
        raise HTTPException(
            status_code=503,
            detail="RAG system is not initialized.",
        )

    filters = {}

    if body.document_id:
        filters["document_id"] = body.document_id

    if body.filename:
        filters["filename"] = body.filename

    try:

        results = rag.retriever.retrieve(
            query=body.query,
            top_k=min(
                body.top_k,
                settings.api_max_search_results,
            ),
            candidate_k=min(
                body.candidate_k,
                settings.api_max_candidate_results,
            ),
            filters=filters or None,
        )

        response = rag.generator.answer(
            query=body.query,
            results=results,
        )

        return response

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc