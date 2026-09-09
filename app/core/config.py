from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RAG Document Assistant"
    app_version: str = "0.1.0"

    max_pdf_size_mb: int = 50

    upload_dir: Path = Path("data/uploads")
    processed_dir: Path = Path("data/processed")
    allowed_file_extension: str = ".pdf"

    chunk_size: int = 500
    chunk_overlap: int = 100

    # Embeddings
    embedding_provider: str = "huggingface"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    embedding_device: str | None = None
    embedding_batch_size: int = 32
    normalize_embeddings: bool = True

    # Qdrant
    qdrant_collection_name: str = "document_chunks"
    qdrant_path: Path = Path("data/qdrant")
    qdrant_url: str | None = None
    qdrant_api_key: str | None = None
    qdrant_timeout: float = 30.0

    # Reranker
    reranker_provider: str = "sentence_transformers"

    reranker_model: str = (
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    )

    reranker_device: str | None = None
    reranker_batch_size: int = 16
    reranker_candidate_k: int = 20

    # LLM
    llm_provider: str = "ollama"
    llm_model: str = "llama3.2:3b"

    # OpenAI
    openai_api_key: str | None = None

    # Ollama
    ollama_host: str = "http://localhost:11434"

    # Generation
    llm_temperature: float = 0.0
    llm_max_output_tokens: int = 1000

    retrieval_top_k: int = 5

    generation_context_max_chars: int = 12000

    require_citations: bool = True

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