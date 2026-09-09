from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from app.models.embedding import EmbeddedChunk
from app.core.config import Settings
from app.embeddings.base import EmbeddingModel
from app.embeddings.factory import create_embedding_model
from app.generation.answer import AnswerGenerator
from app.generation.context import ContextBuilder
from app.generation.factory import create_llm
from app.generation.llm import LLM
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.lexical_index import LexicalIndexBuilder
from app.retrieval.lexical_store import LexicalStore
from app.retrieval.qdrant_store import QdrantVectorStore
from app.retrieval.vector_store import VectorStore


@dataclass
class RAGComponents:
    """
    Application-scoped RAG dependencies.

    These objects are created once during FastAPI startup
    and reused by every request.
    """

    embedding_model: EmbeddingModel

    vector_store: VectorStore

    lexical_store: LexicalStore

    retriever: HybridRetriever

    llm: LLM

    generator: AnswerGenerator


def load_embedded_chunks(
    path: Path,
) -> list[EmbeddedChunk]:
    """
    Load embedded chunks from JSON and convert them
    back into EmbeddedChunk Pydantic models.
    """

    if not path.exists():
        raise FileNotFoundError(
            f"Embedding file does not exist: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "Embedding JSON must contain a list."
        )

    return [
        EmbeddedChunk.model_validate(item)
        for item in data
    ]


def find_embeddings_file(
    settings: Settings,
) -> Path:
    """
    Locate the embeddings JSON file used by the API.

    If a specific configured file is introduced later,
    this function can be replaced by a document registry.
    """

    files = sorted(
        settings.processed_dir.glob(
            "*_chunks_embeddings.json"
        )
    )

    if not files:
        raise FileNotFoundError(
            "No embedding files were found in "
            f"{settings.processed_dir}."
        )

    return files[-1]


def create_rag_components(
    settings: Settings,
    embeddings_path: Path,
) -> RAGComponents:
    """
    Build all RAG dependencies once.
    """

    # --------------------------------------------------------------
    # Embedding model
    # --------------------------------------------------------------

    embedding_model = create_embedding_model(
        provider=settings.embedding_provider,
        model_name=settings.embedding_model,
        device=settings.embedding_device,
        batch_size=settings.embedding_batch_size,
        normalize_embeddings=settings.normalize_embeddings,
    )

    # --------------------------------------------------------------
    # Qdrant
    # --------------------------------------------------------------

    vector_store = QdrantVectorStore(
        collection_name=settings.qdrant_collection_name,
        path=(
            str(settings.qdrant_path)
            if not settings.qdrant_url
            else None
        ),
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        timeout=settings.qdrant_timeout,
    )

    # --------------------------------------------------------------
    # Load embeddings
    # --------------------------------------------------------------

    embedded_data = load_embedded_chunks(
        embeddings_path
    )

    # --------------------------------------------------------------
    # Lexical index
    # --------------------------------------------------------------

    lexical_builder = LexicalIndexBuilder()

    lexical_store = lexical_builder.build(
        embedded_data
    )

    # --------------------------------------------------------------
    # Hybrid retriever
    # --------------------------------------------------------------

    retriever = HybridRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
        lexical_store=lexical_store,
        dense_weight=settings.dense_weight,
        lexical_weight=settings.lexical_weight,
        rrf_k=settings.rrf_k,
    )

    # --------------------------------------------------------------
    # LLM
    # --------------------------------------------------------------

    llm = create_llm(
        provider=settings.llm_provider,
        model_name=settings.llm_model,
        temperature=settings.llm_temperature,
        max_output_tokens=settings.llm_max_output_tokens,
        host=settings.ollama_host,
    )

    # --------------------------------------------------------------
    # Context builder
    # --------------------------------------------------------------

    context_builder = ContextBuilder(
        max_chars=settings.generation_context_max_chars
    )

    # --------------------------------------------------------------
    # Answer generator
    # --------------------------------------------------------------

    generator = AnswerGenerator(
        llm=llm,
        context_builder=context_builder,
        require_citations=settings.require_citations,
    )

    return RAGComponents(
        embedding_model=embedding_model,
        vector_store=vector_store,
        lexical_store=lexical_store,
        retriever=retriever,
        llm=llm,
        generator=generator,
    )