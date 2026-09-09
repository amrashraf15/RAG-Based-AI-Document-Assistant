from __future__ import annotations

import pytest

from app.evaluation.metrics import (
    mean_reciprocal_rank,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_recall_at_k() -> None:
    score = recall_at_k(
        retrieved_ids=[
            "a",
            "b",
            "c",
        ],
        relevant_ids=[
            "a",
            "c",
        ],
        k=3,
    )

    assert score == pytest.approx(1.0)


def test_recall_at_k_partial() -> None:
    score = recall_at_k(
        retrieved_ids=[
            "a",
            "x",
            "y",
        ],
        relevant_ids=[
            "a",
            "b",
        ],
        k=3,
    )

    assert score == pytest.approx(0.5)


def test_precision_at_k() -> None:
    score = precision_at_k(
        retrieved_ids=[
            "a",
            "x",
            "b",
        ],
        relevant_ids=[
            "a",
            "b",
        ],
        k=3,
    )

    assert score == pytest.approx(
        2 / 3
    )


def test_reciprocal_rank() -> None:
    score = reciprocal_rank(
        retrieved_ids=[
            "x",
            "b",
            "a",
        ],
        relevant_ids=[
            "a",
        ],
    )

    assert score == pytest.approx(
        1 / 3
    )


def test_reciprocal_rank_missing() -> None:
    score = reciprocal_rank(
        retrieved_ids=[
            "x",
            "y",
        ],
        relevant_ids=[
            "a",
        ],
    )

    assert score == 0.0


def test_mean_reciprocal_rank() -> None:
    score = mean_reciprocal_rank(
        [
            (
                ["a", "x"],
                ["a"],
            ),
            (
                ["x", "b", "y"],
                ["b"],
            ),
        ]
    )

    expected = (
        1.0 + (1 / 2)
    ) / 2

    assert score == pytest.approx(
        expected
    )


def test_ndcg_at_k() -> None:
    score = ndcg_at_k(
        retrieved_ids=[
            "a",
            "b",
            "c",
        ],
        relevance={
            "a": 3,
            "b": 2,
            "c": 1,
        },
        k=3,
    )

    assert score == pytest.approx(1.0)


def test_empty_relevant_ids() -> None:
    assert (
        recall_at_k(
            ["a"],
            [],
            1,
        )
        == 0.0
    )

    assert (
        reciprocal_rank(
            ["a"],
            [],
        )
        == 0.0
    )