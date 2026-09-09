from __future__ import annotations

from pydantic import BaseModel, Field


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