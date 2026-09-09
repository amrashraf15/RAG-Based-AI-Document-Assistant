from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    app_name: str = "RAG Document Assistant"
    app_version: str = "0.1.0"

    # ------------------------------------------------------------------
    # PDF processing
    # ------------------------------------------------------------------

    max_pdf_size_mb: int = 50

    upload_dir: Path = Path("data/uploads")
    processed_dir: Path = Path("data/processed")

    allowed_file_extension: str = ".pdf"

    # ------------------------------------------------------------------
    # Chunking
    # ------------------------------------------------------------------

    chunk_size: int = 300
    chunk_overlap: int = 50

    # ------------------------------------------------------------------
    # Embeddings
    # ------------------------------------------------------------------

    embedding_provider: str = "huggingface"

    embedding_model: str = "BAAI/bge-small-en-v1.5"

    embedding_device: str | None = None

    embedding_batch_size: int = 32

    normalize_embeddings: bool = True

    # ------------------------------------------------------------------
    # Qdrant
    # ------------------------------------------------------------------

    qdrant_collection_name: str = "document_chunks"

    qdrant_path: Path = Path("data/qdrant")

    qdrant_url: str | None = None

    qdrant_api_key: str | None = None

    qdrant_timeout: float = 30.0

    # ------------------------------------------------------------------
    # LLM
    # ------------------------------------------------------------------

    llm_provider: str = "ollama"

    llm_model: str = "llama3.2:3b"

    llm_temperature: float = 0.0

    llm_max_output_tokens: int = 1000

    ollama_host: str = "http://localhost:11434"

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    retrieval_top_k: int = 5

    retrieval_candidate_k: int = 20

    dense_weight: float = 0.5

    lexical_weight: float = 0.5

    rrf_k: int = 60

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------

    generation_context_max_chars: int = 12000

    require_citations: bool = True

    # ------------------------------------------------------------------
    # API
    # ------------------------------------------------------------------

    api_title: str = "RAG Document Assistant API"

    api_description: str = (
        "REST API for the RAG-Based AI Document Assistant."
    )

    api_version: str = "1.0.0"

    api_host: str = "127.0.0.1"

    api_port: int = 8000

    api_max_search_results: int = 20

    api_max_candidate_results: int = 50

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def max_pdf_size_bytes(self) -> int:
        return self.max_pdf_size_mb * 1024 * 1024

    def ensure_directories(self) -> None:
        self.upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.processed_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.qdrant_path.mkdir(
            parents=True,
            exist_ok=True,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()