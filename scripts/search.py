from __future__ import annotations

import argparse

from app.core.config import get_settings
from app.embeddings.factory import (
    create_embedding_model,
)
from app.retrieval.qdrant_store import (
    QdrantVectorStore,
)
from app.retrieval.retriever import (
    SemanticRetriever,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Semantic search over indexed documents."
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
        help="Number of results to return.",
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
        print("=" * 60)
        print("SEMANTIC SEARCH")
        print("=" * 60)

        print(
            f"Query: {args.query}"
        )
        print(
            f"Top K: {args.top_k}"
        )
        print(
            f"Collection: "
            f"{settings.qdrant_collection_name}"
        )
        print(
            f"Indexed vectors: {store.count()}"
        )

        results = SemanticRetriever(
            embedding_model=embedding_model,
            vector_store=store,
        ).retrieve(
            query=args.query,
            top_k=args.top_k,
            filters=filters or None,
        )

        if not results:
            print()
            print(
                "No matching documents found."
            )
            return

        print()
        print(
            f"Found {len(results)} results:"
        )
        print()

        for index, result in enumerate(
            results,
            start=1,
        ):
            print(
                "-" * 60
            )

            print(
                f"Result #{index}"
            )

            print(
                f"Score:       "
                f"{result.score:.4f}"
            )

            print(
                f"Document:    "
                f"{result.filename}"
            )

            print(
                f"Page:        "
                f"{result.page_number}"
            )

            print(
                f"Chunk:       "
                f"{result.chunk_id}"
            )

            print()
            print("Text:")
            print(result.text)

        print()
        print(
            "-" * 60
        )

    finally:
        store.close()


if __name__ == "__main__":
    main()