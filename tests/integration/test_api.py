from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root() -> None:
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"
    assert data["docs"] == "/docs"


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_upload_requires_pdf() -> None:
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "test.txt",
                b"hello",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400


def test_upload_rejects_empty_file() -> None:
    response = client.post(
        "/documents/upload",
        files={
            "file": (
                "test.pdf",
                b"",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400


def test_search_rejects_empty_query() -> None:
    response = client.post(
        "/search",
        json={
            "query": "",
            "top_k": 5,
            "candidate_k": 20,
        },
    )

    assert response.status_code == 400


def test_chat_rejects_empty_query() -> None:
    response = client.post(
        "/chat",
        json={
            "query": "",
            "top_k": 5,
            "candidate_k": 20,
        },
    )

    assert response.status_code == 400