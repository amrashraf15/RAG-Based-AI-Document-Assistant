from __future__ import annotations

import hashlib
from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile,
)

from app.core.config import get_settings


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


def build_document_id(
    filename: str,
    content: bytes,
) -> str:
    digest = hashlib.sha256(
        content
    ).hexdigest()[:16]

    return f"doc_{digest}"


def build_document_info(
    path: Path,
) -> dict:
    filename = path.name

    document_id = None
    original_filename = filename

    if filename.startswith("doc_"):
        parts = filename.split(
            "_",
            2,
        )

        if len(parts) == 3:
            document_id = (
                f"{parts[0]}_{parts[1]}"
            )
            original_filename = parts[2]

    if document_id is None:
        document_id = path.stem

    return {
        "document_id": document_id,
        "filename": original_filename,
        "size_bytes": path.stat().st_size,
        "path": str(path),
    }


# ============================================================
# POST /documents/upload
# ============================================================

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
) -> dict:

    settings = get_settings()

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required.",
        )

    suffix = Path(
        file.filename
    ).suffix.lower()

    if suffix != settings.allowed_file_extension:
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    if len(content) > settings.max_pdf_size_bytes:
        raise HTTPException(
            status_code=413,
            detail=(
                f"PDF exceeds the maximum allowed "
                f"size of {settings.max_pdf_size_mb} MB."
            ),
        )

    document_id = build_document_id(
        file.filename,
        content,
    )

    settings.upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        settings.upload_dir
        / f"{document_id}_{file.filename}"
    )

    with output_path.open(
        "wb"
    ) as destination:
        destination.write(content)

    return {
        "status": "uploaded",
        "document_id": document_id,
        "filename": file.filename,
        "size_bytes": len(content),
        "path": str(output_path),
    }


# ============================================================
# GET /documents
# ============================================================

@router.get("")
def list_documents() -> dict:
    settings = get_settings()

    settings.upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    documents = []

    for path in sorted(
        settings.upload_dir.glob("*.pdf")
    ):
        documents.append(
            build_document_info(path)
        )

    return {
        "documents": documents,
        "count": len(documents),
    }


# ============================================================
# GET /documents/{document_id}
# ============================================================

@router.get("/{document_id}")
def get_document(
    document_id: str,
) -> dict:

    settings = get_settings()

    settings.upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    matching_files = list(
        settings.upload_dir.glob(
            f"{document_id}_*.pdf"
        )
    )

    if not matching_files:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Document not found: "
                f"{document_id}"
            ),
        )

    path = matching_files[0]

    return build_document_info(path)


# ============================================================
# DELETE /documents/{document_id}
# ============================================================

@router.delete("/{document_id}")
def delete_document(
    document_id: str,
) -> dict:

    settings = get_settings()

    settings.upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    matching_files = list(
        settings.upload_dir.glob(
            f"{document_id}_*.pdf"
        )
    )

    if not matching_files:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Document not found: "
                f"{document_id}"
            ),
        )

    deleted_files = []

    for path in matching_files:
        path.unlink()
        deleted_files.append(path.name)

    return {
        "status": "deleted",
        "document_id": document_id,
        "deleted_files": deleted_files,
    }