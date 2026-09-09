from __future__ import annotations

import argparse

from app.core.config import get_settings
from app.embeddings.factory import create_embedding_model
from app.retrieval.qdrant_store import (
    QdrantVectorStore,
)
from app.retrieval.reranker_factory import (
    create_reranker,
)
from app.retrieval.reranking import (
    RerankingPipeline,
)
from app.retrieval.retriever import (
    SemanticRetriever,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Semantic retrieval followed by "
            "cross-encoder reranking."
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
        help=(
            "Number of semantic candidates "
            "sent to the reranker."
        ),
    )

    parser.add_argument(
        "--document-id",
        type=str,
        default=None,
        help="Optional document ID filter.",
    )

    parser.add_argument(
        "--filename",
        type=str,
        default=None,
        help="Optional filename filter.",
    )

    return parser.parse_args()


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

    if candidate_k <= 0:
        raise ValueError(
            "--candidate-k must be greater than zero."
        )

    if candidate_k < args.top_k:
        raise ValueError(
            "--candidate-k must be greater than "
            "or equal to --top-k."
        )

    print("=" * 60)
    print("RERANKED SEMANTIC SEARCH")
    print("=" * 60)

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
        normalize_embeddings=settings.normalize_embeddings,
    )

    print(
        f"Loading reranker: "
        f"{settings.reranker_model}"
    )

    reranker = create_reranker(
        provider=settings.reranker_provider,
        model_name=settings.reranker_model,
        device=settings.reranker_device,
        batch_size=settings.reranker_batch_size,
    )

    if settings.qdrant_url:
        store = QdrantVectorStore(
            collection_name=(
                settings.qdrant_collection_name
            ),
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            timeout=settings.qdrant_timeout,
        )
    else:
        store = QdrantVectorStore(
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
        print()
        print(f"Query: {args.query}")
        print(f"Candidate K: {candidate_k}")
        print(f"Final K: {args.top_k}")
        print(
            f"Indexed vectors: {store.count()}"
        )

        retriever = SemanticRetriever(
            embedding_model=embedding_model,
            vector_store=store,
        )

        candidates = retriever.retrieve(
            query=args.query,
            top_k=candidate_k,
            filters=filters or None,
        )

        print()
        print(
            f"Semantic candidates: "
            f"{len(candidates)}"
        )

        pipeline = RerankingPipeline(
            reranker=reranker,
        )

        results = pipeline.rerank(
            query=args.query,
            results=candidates,
            top_k=args.top_k,
        )

        if not results:
            print()
            print(
                "No matching documents found."
            )
            return

        print()
        print(
            f"Final reranked results: "
            f"{len(results)}"
        )

        print()

        for index, result in enumerate(
            results,
            start=1,
        ):
            print("-" * 60)
            print(f"Result #{index}")
            print(
                f"Reranker score: "
                f"{result.reranker_score:.4f}"
            )
            print(
                f"Retrieval score: "
                f"{result.retrieval_score:.4f}"
            )
            print(
                f"Document: "
                f"{result.filename}"
            )
            print(
                f"Page: "
                f"{result.page_number}"
            )
            print(
                f"Chunk: "
                f"{result.chunk_id}"
            )
            print()
            print("Text:")
            print(result.text)

        print()
        print("-" * 60)

    finally:
        store.close()


if __name__ == "__main__":
    main()