from __future__ import annotations

from math import log2
from typing import Sequence


def recall_at_k(
    retrieved_ids: Sequence[str],
    relevant_ids: Sequence[str],
    k: int,
) -> float:
    if k <= 0:
        raise ValueError(
            "k must be greater than zero."
        )

    relevant = set(relevant_ids)

    if not relevant:
        return 0.0

    retrieved = set(
        retrieved_ids[:k]
    )

    return len(
        retrieved & relevant
    ) / len(relevant)


def precision_at_k(
    retrieved_ids: Sequence[str],
    relevant_ids: Sequence[str],
    k: int,
) -> float:
    if k <= 0:
        raise ValueError(
            "k must be greater than zero."
        )

    retrieved = retrieved_ids[:k]

    if not retrieved:
        return 0.0

    relevant = set(relevant_ids)

    return sum(
        item in relevant
        for item in retrieved
    ) / len(retrieved)


def reciprocal_rank(
    retrieved_ids: Sequence[str],
    relevant_ids: Sequence[str],
) -> float:
    relevant = set(relevant_ids)

    if not relevant:
        return 0.0

    for rank, item_id in enumerate(
        retrieved_ids,
        start=1,
    ):
        if item_id in relevant:
            return 1.0 / rank

    return 0.0


def mean_reciprocal_rank(
    rankings: Sequence[
        tuple[
            Sequence[str],
            Sequence[str],
        ]
    ],
) -> float:
    if not rankings:
        return 0.0

    scores = [
        reciprocal_rank(
            retrieved_ids,
            relevant_ids,
        )
        for retrieved_ids, relevant_ids
        in rankings
    ]

    return sum(scores) / len(scores)


def ndcg_at_k(
    retrieved_ids: Sequence[str],
    relevance: dict[str, float],
    k: int,
) -> float:
    if k <= 0:
        raise ValueError(
            "k must be greater than zero."
        )

    retrieved = retrieved_ids[:k]

    if not retrieved:
        return 0.0

    dcg = 0.0

    for rank, item_id in enumerate(
        retrieved,
        start=1,
    ):
        gain = relevance.get(
            item_id,
            0.0,
        )

        dcg += (
            (2**gain - 1)
            / log2(rank + 1)
        )

    ideal_scores = sorted(
        relevance.values(),
        reverse=True,
    )[:k]

    if not ideal_scores:
        return 0.0

    idcg = sum(
        (
            (2**gain - 1)
            / log2(rank + 1)
        )
        for rank, gain in enumerate(
            ideal_scores,
            start=1,
        )
    )

    if idcg == 0:
        return 0.0

    return dcg / idcg