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

    embedding_provider: str = "huggingface"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    embedding_device: str | None = None
    embedding_batch_size: int = 32
    normalize_embeddings: bool = True

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


@lru_cache
def get_settings() -> Settings:
    return Settings()