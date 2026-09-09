from __future__ import annotations

import math
import re
from collections import Counter
from typing import Sequence


class BM25:
    """
    Okapi BM25 lexical retrieval implementation.

    BM25 score:

        IDF(q) * (
            tf * (k1 + 1)
            /
            (tf + k1 * (1 - b + b * dl / avgdl))
        )

    where:

        tf   = term frequency in document
        dl   = document length
        avgdl = average document length
        k1   = term frequency saturation parameter
        b    = document length normalization parameter
    """

    def __init__(
        self,
        documents: Sequence[str],
        k1: float = 1.5,
        b: float = 0.75,
    ) -> None:
        if k1 < 0:
            raise ValueError(
                "k1 must be greater than or equal to zero."
            )

        if not 0 <= b <= 1:
            raise ValueError(
                "b must be between 0 and 1."
            )

        self.k1 = k1
        self.b = b

        self.documents = list(documents)

        self.tokenized_documents = [
            self._tokenize(document)
            for document in self.documents
        ]

        self.document_count = len(
            self.tokenized_documents
        )

        self.document_lengths = [
            len(tokens)
            for tokens in self.tokenized_documents
        ]

        if self.document_count:
            self.average_document_length = (
                sum(self.document_lengths)
                / self.document_count
            )
        else:
            self.average_document_length = 0.0

        self.document_frequencies = self._build_document_frequencies()

    def score(
        self,
        query: str,
    ) -> list[float]:
        if not isinstance(query, str):
            raise TypeError(
                "Query must be a string."
            )

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if not self.documents:
            return []

        query_tokens = self._tokenize(query)

        if not query_tokens:
            return [0.0] * self.document_count

        query_terms = set(query_tokens)

        scores = [
            self._score_document(
                query_terms=query_terms,
                document_index=index,
            )
            for index in range(self.document_count)
        ]

        return scores

    def top_k(
        self,
        query: str,
        k: int = 5,
    ) -> list[tuple[int, float]]:
        if k <= 0:
            raise ValueError(
                "k must be greater than zero."
            )

        scores = self.score(query)

        ranked = sorted(
            enumerate(scores),
            key=lambda item: item[1],
            reverse=True,
        )

        return ranked[:k]

    def _score_document(
        self,
        query_terms: set[str],
        document_index: int,
    ) -> float:
        tokens = self.tokenized_documents[
            document_index
        ]

        term_frequencies = Counter(tokens)

        document_length = len(tokens)

        if document_length == 0:
            return 0.0

        score = 0.0

        for term in query_terms:
            term_frequency = term_frequencies.get(
                term,
                0,
            )

            if term_frequency == 0:
                continue

            document_frequency = (
                self.document_frequencies.get(
                    term,
                    0,
                )
            )

            idf = self._idf(
                document_frequency
            )

            denominator = (
                term_frequency
                + self.k1
                * (
                    1
                    - self.b
                    + self.b
                    * (
                        document_length
                        / self.average_document_length
                    )
                )
            )

            numerator = term_frequency * (
                self.k1 + 1
            )

            score += (
                idf
                * numerator
                / denominator
            )

        return score

    def _idf(
        self,
        document_frequency: int,
    ) -> float:
        return math.log(
            1
            + (
                self.document_count
                - document_frequency
                + 0.5
            )
            / (
                document_frequency
                + 0.5
            )
        )

    def _build_document_frequencies(
        self,
    ) -> dict[str, int]:
        frequencies: dict[str, int] = {}

        for tokens in self.tokenized_documents:
            unique_terms = set(tokens)

            for term in unique_terms:
                frequencies[term] = (
                    frequencies.get(term, 0)
                    + 1
                )

        return frequencies

    @staticmethod
    def _tokenize(
        text: str,
    ) -> list[str]:
        if not isinstance(text, str):
            raise TypeError(
                "Text must be a string."
            )

        return re.findall(
            r"\b\w+(?:[-.]\w+)*\b",
            text.lower(),
        )