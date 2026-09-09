from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.core.config import get_settings
from app.embeddings.factory import (
    create_embedding_model,
)
from app.models.embedding import EmbeddedChunk
from app.retrieval.hybrid import HybridRetriever
from app.retrieval.lexical_index import (
    LexicalIndexBuilder,
)
from app.retrieval.qdrant_store import (
    QdrantVectorStore,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Hybrid dense + BM25 retrieval."
        )
    )

    parser.add_argument(
        "query",
        type=str,
        help="Search query.",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Number of final results.",
    )

    parser.add_argument(
        "--candidate-k",
        type=int,
        default=None,
        help="Number of candidates from each retriever.",
    )

    parser.add_argument(
        "--dense-weight",
        type=float,
        default=0.5,
        help="Dense retrieval weight.",
    )

    parser.add_argument(
        "--lexical-weight",
        type=float,
        default=0.5,
        help="BM25 retrieval weight.",
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
        help=(
            "Embedded chunks JSON file. "
            "Can be specified multiple times."
        ),
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
                f"Embedding JSON must contain a list: {path}"
            )

        chunks.extend(
            EmbeddedChunk.model_validate(item)
            for item in data
        )

    return chunks


def main() -> None:
    args = parse_args()

    settings = get_settings()
    settings.ensure_directories()

    if args.top_k <= 0:
        raise ValueError(
            "--top-k must be greater than zero."
        )

    candidate_k = (
        args.candidate_k
        if args.candidate_k is not None
        else settings.reranker_candidate_k
    )

    if candidate_k < args.top_k:
        raise ValueError(
            "--candidate-k must be greater than "
            "or equal to --top-k."
        )

    chunks = load_embeddings(
        args.embeddings
    )

    if not chunks:
        raise ValueError(
            "No embedded chunks were loaded."
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
        filters["filename"] = args.filename

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
            top_k=args.top_k,
            candidate_k=candidate_k,
            filters=filters or None,
        )

        print("=" * 70)
        print("HYBRID SEARCH")
        print("=" * 70)

        print()
        print(f"Query: {args.query}")
        print(f"Candidate K: {candidate_k}")
        print(f"Final K: {args.top_k}")
        print(
            f"Dense weight: "
            f"{args.dense_weight:.2f}"
        )
        print(
            f"Lexical weight: "
            f"{args.lexical_weight:.2f}"
        )

        print()
        print(
            f"Indexed Qdrant vectors: "
            f"{vector_store.count()}"
        )

        print(
            f"Lexical documents: "
            f"{len(lexical_store.results)}"
        )

        if not results:
            print()
            print(
                "No matching documents found."
            )
            return

        print()
        print(
            f"Results: {len(results)}"
        )

        for index, result in enumerate(
            results,
            start=1,
        ):
            print()
            print("-" * 70)
            print(f"Result #{index}")

            print(
                f"Fused score:   "
                f"{result.fused_score:.6f}"
            )

            print(
                f"Dense score:   "
                f"{result.dense_score:.6f}"
            )

            print(
                f"BM25 score:    "
                f"{result.lexical_score:.6f}"
            )

            print(
                f"Document:      "
                f"{result.filename}"
            )

            print(
                f"Page:          "
                f"{result.page_number}"
            )

            print(
                f"Chunk:         "
                f"{result.chunk_id}"
            )

            print()
            print("Text:")
            print(result.text)

        print()
        print("-" * 70)

    finally:
        vector_store.close()


if __name__ == "__main__":
    main()