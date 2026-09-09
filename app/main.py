from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI

from app.api.dependencies import (
    create_rag_components,
    find_embeddings_file,
)
from app.api.routes.chat import (
    router as chat_router,
)
from app.api.routes.documents import (
    router as documents_router,
)
from app.api.routes.health import (
    router as health_router,
)
from app.api.routes.search import (
    router as search_router,
)
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    """
    FastAPI application lifespan.

    Startup:
        - load configuration
        - initialize embedding model
        - initialize Qdrant
        - build lexical index
        - initialize hybrid retriever
        - initialize Ollama
        - initialize answer generator

    Shutdown:
        - close Qdrant client
    """

    settings = get_settings()

    settings.ensure_directories()

    print("=" * 70)
    print("Starting RAG Document Assistant")
    print("=" * 70)

    print(
        f"Embedding model: "
        f"{settings.embedding_model}"
    )

    print(
        f"LLM: "
        f"{settings.llm_provider} / "
        f"{settings.llm_model}"
    )

    print(
        f"Qdrant collection: "
        f"{settings.qdrant_collection_name}"
    )

    try:

        embeddings_path = find_embeddings_file(
            settings
        )

        print(
            f"Embeddings: "
            f"{embeddings_path}"
        )

        rag = create_rag_components(
            settings=settings,
            embeddings_path=embeddings_path,
        )

        app.state.rag = rag

        print(
            "RAG components initialized successfully."
        )

        print("=" * 70)

        yield

    finally:

        print("=" * 70)
        print("Shutting down RAG Document Assistant")

        rag = getattr(
            app.state,
            "rag",
            None,
        )

        if rag is not None:

            try:
                rag.vector_store.close()

                print(
                    "Qdrant client closed."
                )

            except Exception as exc:

                print(
                    f"Error while closing Qdrant: "
                    f"{exc}"
                )

        print("=" * 70)


settings = get_settings()


app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    health_router
)

app.include_router(
    documents_router
)

app.include_router(
    search_router
)

app.include_router(
    chat_router
)


@app.get("/")
def root() -> dict:

    return {
        "application": settings.app_name,
        "version": settings.api_version,
        "status": "running",
        "docs": "/docs",
    }