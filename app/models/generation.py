from __future__ import annotations

from pydantic import BaseModel, Field

from app.models.citation import Citation


class ContextChunk(BaseModel):
    citation_id: str

    chunk_id: str

    document_id: str

    filename: str

    page_number: int = Field(
        ge=1
    )

    text: str

    score: float

    title: str | None = None

    source: str


class GenerationRequest(BaseModel):
    query: str

    context: list[ContextChunk]

    conversation_history: list[
        dict[str, str]
    ] = Field(
        default_factory=list
    )


class ChatRequest(BaseModel):
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

    conversation_history: list[
        dict[str, str]
    ] = Field(
        default_factory=list
    )


class GenerationResult(BaseModel):
    answer: str

    citations: list[Citation]

    model: str

    prompt_tokens: int | None = None

    completion_tokens: int | None = None

    citation_ids: list[str] = Field(
        default_factory=list
    )


class RAGResponse(BaseModel):
    query: str

    answer: str

    citations: list[Citation]

    model: str

    grounded: bool

    citation_ids: list[str] = Field(
        default_factory=list
    )