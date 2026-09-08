from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    Values can be loaded from environment variables or a .env file.
    """

    app_name: str = "RAG Document Assistant"
    app_version: str = "0.1.0"

    # Maximum accepted PDF size in megabytes.
    max_pdf_size_mb: int = 50

    # Directories
    upload_dir: Path = Path("data/uploads")
    processed_dir: Path = Path("data/processed")

    # PDF settings
    allowed_file_extension: str = ".pdf"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def max_pdf_size_bytes(self) -> int:
        return self.max_pdf_size_mb * 1024 * 1024


settings = Settings()


def ensure_directories() -> None:
    """
    Create required application directories if they don't exist.
    """
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.processed_dir.mkdir(parents=True, exist_ok=True)