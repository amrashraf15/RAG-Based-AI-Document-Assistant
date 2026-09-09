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