from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.core.config import get_settings
from app.models.embedding import EmbeddedChunk
from app.retrieval.qdrant_store import QdrantVectorStore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Index embedded chunks into Qdrant."
        )
    )

    parser.add_argument(
        "input",
        type=Path,
        help=(
            "Path to the embeddings JSON file."
        ),
    )

    parser.add_argument(
        "--collection",
        type=str,
        default=None,
        help=(
            "Qdrant collection name."
        ),
    )

    return parser.parse_args()


def load_embeddings(
    input_path: Path,
) -> list[EmbeddedChunk]:
    if not input_path.exists():
        raise FileNotFoundError(
            f"File not found: {input_path}"
        )

    with input_path.open(
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


def main() -> None:
    args = parse_args()

    settings = get_settings()
    settings.ensure_directories()

    chunks = load_embeddings(
        args.input
    )

    if not chunks:
        raise ValueError(
            "Embedding file contains no chunks."
        )

    collection_name = (
        args.collection
        or settings.qdrant_collection_name
    )

    print("=" * 60)
    print("QDRANT INDEXING")
    print("=" * 60)

    print(
        f"Input:      {args.input}"
    )
    print(
        f"Chunks:     {len(chunks)}"
    )
    print(
        f"Collection: {collection_name}"
    )
    print(
        f"Dimension:  "
        f"{chunks[0].embedding_dimension}"
    )

    if settings.qdrant_url:
        print(
            f"Qdrant:     {settings.qdrant_url}"
        )
        store = QdrantVectorStore(
            collection_name=collection_name,
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            timeout=settings.qdrant_timeout,
        )
    else:
        print(
            f"Qdrant:     {settings.qdrant_path}"
        )
        store = QdrantVectorStore(
            collection_name=collection_name,
            path=str(settings.qdrant_path),
        )

    try:
        store.upsert(chunks)

        print()
        print(
            "Indexing completed successfully."
        )
        print(
            f"Vectors in collection: "
            f"{store.count()}"
        )
    finally:
        store.close()


if __name__ == "__main__":
    main()