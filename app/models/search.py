from __future__ import annotations

from pydantic import BaseModel, Field

from app.models.hybrid import HybridSearchResult


class SearchResult(BaseModel):
    chunk_id: str
    document_id: str
    filename: str
    page_number: int = Field(ge=1)
    chunk_index: int = Field(ge=0)

    text: str

    score: float

    title: str | None = None

    source: str

    token_count: int = Field(ge=0)

    character_count: int = Field(ge=0)

    embedding_model: str

    embedding_dimension: int = Field(gt=0)

    normalized: bool = True


class SearchRequest(BaseModel):
    query: str

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
    )

    candidate_k: int = Field(
        default=20,
        ge=1,
        le=50,
    )

    dense_weight: float = Field(
        default=0.5,
        ge=0,
    )

    lexical_weight: float = Field(
        default=0.5,
        ge=0,
    )

    document_id: str | None = None

    filename: str | None = None


class SearchResponse(BaseModel):
    query: str

    results: list[HybridSearchResult]

    count: int