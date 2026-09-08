import argparse
import sys
from pathlib import Path

from app.core.exceptions import DocumentProcessingError
from app.ingestion.pipeline import DocumentIngestionPipeline


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Process and chunk a PDF document "
            "for the RAG pipeline."
        )
    )

    parser.add_argument(
        "pdf",
        type=Path,
        help="Path to the PDF file.",
    )

    args = parser.parse_args()

    pipeline = DocumentIngestionPipeline()

    try:
        document, chunks = (
            pipeline.process_with_chunks(
                args.pdf
            )
        )

    except DocumentProcessingError as exc:
        print(
            f"\nDocument processing failed:\n{exc}\n",
            file=sys.stderr,
        )
        return 1

    except FileNotFoundError as exc:
        print(
            f"\nFile not found:\n{exc}\n",
            file=sys.stderr,
        )
        return 1

    except Exception as exc:
        print(
            f"\nUnexpected error:\n{exc}\n",
            file=sys.stderr,
        )
        return 1

    total_tokens = sum(
        chunk.token_count
        for chunk in chunks
    )

    average_tokens = (
        total_tokens / len(chunks)
        if chunks
        else 0
    )

    print()
    print("=" * 60)
    print("Document processed successfully")
    print("=" * 60)
    print()

    print(f"Document ID: {document.document_id}")
    print(f"Filename:    {document.filename}")
    print(f"Pages:       {document.page_count}")

    print(
        f"Characters:  "
        f"{document.metadata.cleaned_character_count:,}"
    )

    print(f"Chunks:      {len(chunks):,}")

    print(
        f"Avg tokens:  "
        f"{average_tokens:.1f}"
    )

    print()

    print(
        "Chunk configuration:"
    )

    print(
        f"  Size:      "
        f"{pipeline.chunker.config.chunk_size} tokens"
    )

    print(
        f"  Overlap:   "
        f"{pipeline.chunker.config.chunk_overlap} tokens"
    )

    print()

    print(
        "Processed document:"
    )

    print(
        f"  data/processed/"
        f"{document.document_id}.json"
    )

    print()

    print(
        "Chunks:"
    )

    print(
        f"  data/processed/"
        f"{document.document_id}_chunks.json"
    )

    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())