from __future__ import annotations

from pydantic import BaseModel, Field

from app.models.citation import Citation


class ContextChunk(BaseModel):
    citation_id: str

    chunk_id: str
    document_id: str

    filename: str

    page_number: int = Field(ge=1)

    text: str

    score: float

    title: str | None = None
    source: str


class GenerationRequest(BaseModel):
    query: str

    context: list[ContextChunk]

    conversation_history: list[dict[str, str]] = []


class GenerationResult(BaseModel):
    answer: str

    citations: list[Citation]

    model: str

    prompt_tokens: int | None = None
    completion_tokens: int | None = None

    citation_ids: list[str] = []


class RAGResponse(BaseModel):
    query: str

    answer: str

    citations: list[Citation]

    model: str

    grounded: bool

    citation_ids: list[str]