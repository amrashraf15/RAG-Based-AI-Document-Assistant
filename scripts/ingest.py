import argparse
import sys
from pathlib import Path

from app.core.exceptions import DocumentProcessingError
from app.ingestion.pipeline import DocumentIngestionPipeline


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Process a PDF document for the RAG pipeline."
    )

    parser.add_argument(
        "pdf",
        type=Path,
        help="Path to the PDF file.",
    )

    args = parser.parse_args()

    pipeline = DocumentIngestionPipeline()

    try:
        document = pipeline.process(args.pdf)

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

    print()
    print("=" * 60)
    print("Document processed successfully")
    print("=" * 60)
    print()
    print(f"Document ID: {document.document_id}")
    print(f"Filename:    {document.filename}")
    print(f"Pages:       {document.page_count}")
    print(
        f"Characters:  {document.metadata.cleaned_character_count:,}"
    )
    print(f"Source:      {document.source}")
    print()
    print(
        f"Processed document saved to: "
        f"data/processed/{document.document_id}.json"
    )
    print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())