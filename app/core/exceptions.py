class DocumentProcessingError(Exception):
    """Base exception for document processing errors."""

    pass


class InvalidPDFError(DocumentProcessingError):
    """Raised when a file is not a valid PDF."""

    pass


class PDFSizeLimitError(DocumentProcessingError):
    """Raised when a PDF exceeds the configured size limit."""

    pass


class PDFExtractionError(DocumentProcessingError):
    """Raised when PDF text extraction fails."""

    pass


class EmptyPDFError(DocumentProcessingError):
    """Raised when a PDF contains no extractable text."""

    pass