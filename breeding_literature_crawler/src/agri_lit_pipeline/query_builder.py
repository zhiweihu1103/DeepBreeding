"""Query pair generation utilities."""

from __future__ import annotations


def build_crop_tech_pairs(
    all_crops: list[str],
    technologies: list[str],
) -> list[tuple[str, str]]:
    """Build structured `(crop, technology)` query pairs.

    The query builder only creates source-neutral pairs. Each source layer is
    responsible for translating those pairs into the query representation that
    fits its retrieval interface.
    """

    query_pairs: list[tuple[str, str]] = []
    for crop in all_crops:
        for tech in technologies:
            query_pairs.append((crop, tech))

    return query_pairs
