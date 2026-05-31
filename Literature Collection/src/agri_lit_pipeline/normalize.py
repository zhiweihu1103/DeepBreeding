"""Text normalization helpers for the cleaning layer."""

from __future__ import annotations

import re


def normalize_title(title: str | None) -> str:
    """Normalize title text for title-based fallback deduplication."""

    if not title:
        return ""

    normalized = title.lower()
    normalized = re.sub(r"[^\w\s]", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def normalize_doi(doi: str | None) -> str:
    """Normalize DOI text for DOI-priority deduplication."""

    if not doi:
        return ""

    normalized = doi.lower().strip()
    normalized = normalized.replace("https://doi.org/", "")
    normalized = normalized.replace("http://doi.org/", "")
    return normalized
