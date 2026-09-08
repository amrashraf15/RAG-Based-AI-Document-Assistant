import re
import unicodedata
from collections import Counter
from typing import List

from app.models.document import PageDocument


class TextCleaner:
    """
    Cleans extracted PDF text while preserving the original text.

    The cleaner is intentionally conservative because aggressive
    preprocessing can destroy information useful for retrieval.
    """

    def clean_document(
        self,
        pages: List[PageDocument],
    ) -> List[PageDocument]:
        """
        Clean all pages in a document.

        Header/footer removal is performed at the document level
        because repeated lines can only be detected reliably when
        multiple pages are available.
        """

        if not pages:
            return pages

        cleaned_texts = []

        for page in pages:
            cleaned = self.clean_text(page.raw_text)
            cleaned_texts.append(cleaned)

        repeated_lines = self._detect_repeated_headers_footers(
            cleaned_texts
        )

        cleaned_pages = []

        for page, cleaned_text in zip(pages, cleaned_texts):
            cleaned_text = self._remove_repeated_lines(
                cleaned_text,
                repeated_lines,
            )

            cleaned_text = self._finalize_text(cleaned_text)

            page_copy = page.model_copy(
                update={
                    "clean_text": cleaned_text,
                    "character_count": len(cleaned_text),
                }
            )

            cleaned_pages.append(page_copy)

        return cleaned_pages

    def clean_text(self, text: str) -> str:
        """
        Perform conservative text cleaning.
        """

        if not text:
            return ""

        # Unicode normalization.
        text = unicodedata.normalize("NFKC", text)

        # Replace common problematic control characters.
        text = text.replace("\x00", "")
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Normalize tabs and other horizontal whitespace.
        text = re.sub(r"[ \t]+", " ", text)

        # Remove spaces immediately around newlines.
        text = re.sub(r" *\n *", "\n", text)

        # Collapse 3+ newlines to two.
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove unusual zero-width characters.
        text = re.sub(
            r"[\u200B\u200C\u200D\uFEFF]",
            "",
            text,
        )

        # Normalize common Unicode punctuation.
        replacements = {
            "\u2018": "'",
            "\u2019": "'",
            "\u201c": '"',
            "\u201d": '"',
            "\u2013": "-",
            "\u2014": "-",
            "\u2212": "-",
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text.strip()

    def _detect_repeated_headers_footers(
        self,
        page_texts: List[str],
    ) -> set[str]:
        """
        Detect lines that occur repeatedly across pages.

        We only consider short lines because headers and footers
        are usually relatively short.

        A line appearing on >= 50% of pages is considered a
        possible repeated header/footer.
        """

        if len(page_texts) < 3:
            return set()

        line_counter: Counter[str] = Counter()

        for text in page_texts:
            lines = self._get_candidate_lines(text)

            # Count a line at most once per page.
            for line in set(lines):
                line_counter[line] += 1

        minimum_occurrences = max(
            3,
            int(len(page_texts) * 0.5),
        )

        repeated_lines = {
            line
            for line, count in line_counter.items()
            if count >= minimum_occurrences
        }

        return repeated_lines

    def _get_candidate_lines(self, text: str) -> List[str]:
        """
        Get possible header/footer lines.
        """

        lines = []

        for line in text.split("\n"):
            normalized = line.strip()

            if not normalized:
                continue

            # Ignore very long lines.
            if len(normalized) > 120:
                continue

            # Ignore lines containing too many words.
            if len(normalized.split()) > 12:
                continue

            lines.append(normalized)

        return lines

    def _remove_repeated_lines(
        self,
        text: str,
        repeated_lines: set[str],
    ) -> str:
        """
        Remove lines detected as repeated headers/footers.
        """

        if not repeated_lines:
            return text

        result = []

        for line in text.split("\n"):
            normalized = line.strip()

            if normalized in repeated_lines:
                continue

            result.append(line)

        return "\n".join(result)

    def _finalize_text(self, text: str) -> str:
        """
        Final cleanup after header/footer removal.
        """

        text = re.sub(r"[ \t]+", " ", text)

        text = re.sub(
            r" *\n *",
            "\n",
            text,
        )

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        return text.strip()

    def is_empty(self, text: str) -> bool:
        """
        Determine whether a page contains meaningful text.
        """

        if not text:
            return True

        normalized = re.sub(
            r"\s+",
            "",
            text,
        )

        return len(normalized) == 0