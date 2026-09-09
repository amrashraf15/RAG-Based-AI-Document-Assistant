from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.core.config import get_settings
from app.embeddings.factory import (
    create_embedding_model,
)
from app.generation.answer import (
    AnswerGenerator,
)
from app.generation.context import (
    ContextBuilder,
)
from app.generation.factory import (
    create_llm,
)
from app.models.embedding import EmbeddedChunk
from app.retrieval.hybrid import (
    HybridRetriever,
)
from app.retrieval.lexical_index import (
    LexicalIndexBuilder,
)
from app.retrieval.qdrant_store import (
    QdrantVectorStore,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Ask questions over indexed documents."
        )
    )

    parser.add_argument(
        "query",
        type=str,
        help="Question to ask.",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Number of retrieval results.",
    )

    parser.add_argument(
        "--candidate-k",
        type=int,
        default=None,
        help="Hybrid retrieval candidate count.",
    )

    parser.add_argument(
        "--dense-weight",
        type=float,
        default=0.5,
    )

    parser.add_argument(
        "--lexical-weight",
        type=float,
        default=0.5,
    )

    parser.add_argument(
        "--document-id",
        type=str,
        default=None,
    )

    parser.add_argument(
        "--filename",
        type=str,
        default=None,
    )

    parser.add_argument(
        "--embeddings",
        type=Path,
        action="append",
        required=True,
    )

    return parser.parse_args()


def load_embeddings(
    paths: list[Path],
) -> list[EmbeddedChunk]:

    chunks: list[EmbeddedChunk] = []

    for path in paths:

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {path}"
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

        chunks.extend(
            EmbeddedChunk.model_validate(
                item
            )
            for item in data
        )

    return chunks


def main() -> None:

    args = parse_args()

    settings = get_settings()
    settings.ensure_directories()

    top_k = (
        args.top_k
        if args.top_k is not None
        else settings.retrieval_top_k
    )

    candidate_k = (
        args.candidate_k
        if args.candidate_k is not None
        else settings.reranker_candidate_k
    )

    if top_k <= 0:
        raise ValueError(
            "--top-k must be greater than zero."
        )

    if candidate_k < top_k:
        raise ValueError(
            "--candidate-k must be >= --top-k."
        )

    chunks = load_embeddings(
        args.embeddings
    )

    if not chunks:
        raise ValueError(
            "No embedded chunks were loaded."
        )

    print()
    print(
        f"Loading embedding model: "
        f"{settings.embedding_model}"
    )

    embedding_model = create_embedding_model(
        provider=settings.embedding_provider,
        model_name=settings.embedding_model,
        device=settings.embedding_device,
        batch_size=settings.embedding_batch_size,
        normalize_embeddings=(
            settings.normalize_embeddings
        ),
    )

    lexical_store = (
        LexicalIndexBuilder.build(
            chunks
        )
    )

    if settings.qdrant_url:
        vector_store = QdrantVectorStore(
            collection_name=(
                settings.qdrant_collection_name
            ),
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            timeout=settings.qdrant_timeout,
        )
    else:
        vector_store = QdrantVectorStore(
            collection_name=(
                settings.qdrant_collection_name
            ),
            path=str(settings.qdrant_path),
        )

    filters = {}

    if args.document_id:
        filters["document_id"] = (
            args.document_id
        )

    if args.filename:
        filters["filename"] = (
            args.filename
        )

    try:

        retriever = HybridRetriever(
            embedding_model=embedding_model,
            vector_store=vector_store,
            lexical_store=lexical_store,
            dense_weight=args.dense_weight,
            lexical_weight=args.lexical_weight,
        )

        results = retriever.retrieve(
            query=args.query,
            top_k=top_k,
            candidate_k=candidate_k,
            filters=filters or None,
        )

        print()
        print(
            f"Retrieved {len(results)} "
            f"supporting chunks."
        )

        llm = create_llm(
            provider=settings.llm_provider,
            model_name=settings.llm_model,
            temperature=settings.llm_temperature,
            max_output_tokens=settings.llm_max_output_tokens,
            host=settings.ollama_host,
        )

        generator = AnswerGenerator(
            llm=llm,
            context_builder=ContextBuilder(
                max_chars=(
                    settings
                    .generation_context_max_chars
                )
            ),
            require_citations=(
                settings.require_citations
            ),
        )

        response = generator.answer(
            query=args.query,
            results=results,
        )

        print()
        print("=" * 70)
        print("ANSWER")
        print("=" * 70)

        print()
        print(response.answer)

        print()
        print("=" * 70)
        print("CITATIONS")
        print("=" * 70)

        if not response.citations:
            print("No citations.")

        for citation in response.citations:
            print()
            print(
                f"[{citation.citation_id}] "
                f"{citation.filename}, "
                f"page {citation.page_number}"
            )

        print()
        print(
            f"Grounded: {response.grounded}"
        )

        print(
            f"Model: {response.model}"
        )

    finally:
        vector_store.close()


if __name__ == "__main__":
    main()