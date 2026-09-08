from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.core.config import get_settings
from app.embeddings.factory import (
    create_embedding_model,
)
from app.embeddings.pipeline import (
    EmbeddingPipeline,
)
from app.models.chunk import DocumentChunk


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Generate embeddings for document chunks."
        )
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Path to a *_chunks.json file.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Output path for embedded chunks."
        ),
    )

    return parser.parse_args()


def load_chunks(
    input_path: Path,
) -> list[DocumentChunk]:
    with input_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    # The ingestion pipeline may store chunks either
    # directly as a list or inside a dictionary.
    if isinstance(data, list):
        chunk_data = data

    elif isinstance(data, dict):
        # Expected structure:
        # {
        #     "document_id": "...",
        #     "filename": "...",
        #     "chunks": [...]
        # }
        if "chunks" not in data:
            raise ValueError(
                "Chunk JSON does not contain a 'chunks' field."
            )

        chunk_data = data["chunks"]

    else:
        raise ValueError(
            "Invalid chunk JSON format."
        )

    if not isinstance(chunk_data, list):
        raise ValueError(
            "The 'chunks' field must contain a list."
        )

    return [
        DocumentChunk.model_validate(chunk)
        for chunk in chunk_data
    ]


def main():
    args = parse_args()

    settings = get_settings()

    input_path = args.input

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    chunks = load_chunks(
        input_path
    )

    print(
        f"Loaded {len(chunks)} chunks."
    )

    print(
        "Loading embedding model: "
        f"{settings.embedding_model}"
    )

    model = create_embedding_model(
        provider=settings.embedding_provider,
        model_name=settings.embedding_model,
        device=settings.embedding_device,
        batch_size=settings.embedding_batch_size,
        normalize_embeddings=(
            settings.normalize_embeddings
        ),
    )

    print(
        f"Embedding dimension: "
        f"{model.dimension}"
    )

    pipeline = EmbeddingPipeline(
        embedding_model=model
    )

    embedded_chunks = (
        pipeline.embed_chunks(
            chunks
        )
    )

    output_path = args.output

    if output_path is None:
        output_path = (
            input_path.parent
            / (
                input_path.stem
                + "_embeddings.json"
            )
        )

    pipeline.save_embeddings(
        embedded_chunks,
        output_path,
    )

    print(
        f"Embedded chunks: "
        f"{len(embedded_chunks)}"
    )

    print(
        f"Output: {output_path}"
    )


if __name__ == "__main__":
    main()