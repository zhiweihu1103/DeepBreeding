"""Source-specific xRxiv relevance filtering rules.

The rules are lightweight and interpretable. They use crop aliases, technology
aliases, and source-specific filtering policies to reduce clearly irrelevant
cross-domain noise in local bioRxiv, medRxiv, and chemRxiv retrieval results.

Current policy:

- crop matching remains required for all xRxiv sources;
- author fields are not used for crop matching;
- bioRxiv uses a relaxed technology policy after crop matching;
- medRxiv and chemRxiv use stricter crop-and-technology policies;
- additional scientific crop aliases are enabled only for bioRxiv.
"""

from __future__ import annotations

import re


BIORXIV_EXTRA_CROP_ALIASES: dict[str, list[str]] = {
    "rice": ["oryza sativa", "o. sativa"],
    "maize": ["zea mays", "corn"],
    "wheat": ["triticum aestivum", "bread wheat"],
    "soybean": ["glycine max"],
    "potato": ["solanum tuberosum"],
    "cassava": ["manihot esculenta"],
    "sweet potato": ["ipomoea batatas"],
    "yam": ["dioscorea", "dioscorea alata", "dioscorea rotundata"],
    "sorghum": ["sorghum bicolor"],
    "barley": ["hordeum vulgare"],
    "foxtail millet": ["setaria italica"],
    "finger millet": ["eleusine coracana"],
    "pearl millet": ["pennisetum glaucum", "cenchrus americanus"],
    "proso millet": ["panicum miliaceum"],
    "buckwheat": ["fagopyrum esculentum"],
    "quinoa": ["chenopodium quinoa"],
    "lentil": ["lens culinaris"],
    "chickpea": ["cicer arietinum"],
    "cowpea": ["vigna unguiculata"],
    "mung bean": ["vigna radiata"],
    "pigeon pea": ["cajanus cajan"],
    "fava bean": ["vicia faba"],
    "adzuki bean": ["vigna angularis"],
}


def normalize_text_for_match(text: str | None) -> str:
    """Normalize text into a simple token-like form for rule matching."""

    if not text:
        return ""

    normalized = text.lower()
    normalized = re.sub(r"[^a-z0-9]+", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def get_crop_aliases(crop: str) -> list[str]:
    """Return conservative crop aliases shared across xRxiv sources."""

    normalized_crop = crop.strip().lower()
    crop_alias_map = {
        "maize": ["maize"],
        "wheat": ["wheat"],
        "rice": ["rice"],
        "soybean": ["soybean"],
        "potato": ["potato"],
        "sweet potato": ["sweet potato", "sweetpotato"],
        "mung bean": ["mung bean", "mungbean"],
    }
    return crop_alias_map.get(normalized_crop, [normalized_crop])


def get_biorxiv_scientific_crop_aliases(crop: str) -> list[str]:
    """Return additional scientific/common crop aliases used only by bioRxiv."""

    normalized_crop = crop.strip().lower()
    return BIORXIV_EXTRA_CROP_ALIASES.get(normalized_crop, [])


def get_xrxiv_crop_aliases(crop: str, source_name: str) -> list[str]:
    """Return source-specific crop aliases."""

    base_aliases = [alias.strip().lower() for alias in get_crop_aliases(crop) if alias.strip()]
    normalized_source = source_name.strip().lower()

    if normalized_source != "biorxiv":
        return base_aliases

    extra_aliases = [
        alias.strip().lower()
        for alias in get_biorxiv_scientific_crop_aliases(crop)
        if alias.strip()
    ]

    deduped_aliases: list[str] = []
    for alias in base_aliases + extra_aliases:
        if alias not in deduped_aliases:
            deduped_aliases.append(alias)

    return sorted(deduped_aliases, key=len, reverse=True)


def get_tech_aliases(tech: str) -> list[str]:
    """Return conservative technology aliases for strict matching."""

    normalized_tech = tech.strip().lower()
    tech_alias_map = {
        "qtl mapping": ["qtl mapping", "qtl"],
        "gwas": [
            "gwas",
            "genome wide association study",
            "genome-wide association study",
        ],
        "marker-assisted selection": [
            "marker-assisted selection",
            "marker assisted selection",
            "mas",
        ],
        "gene editing": ["gene editing", "gene-editing"],
        "genomic selection": ["genomic selection"],
        "crispr": ["crispr", "crispr/cas", "crispr-cas"],
        "breeding": ["breeding", "crop breeding", "plant breeding"],
        "germplasm": ["germplasm"],
    }
    return tech_alias_map.get(normalized_tech, [normalized_tech])


def get_xrxiv_filter_mode(source_name: str) -> str:
    """Return the current source-specific xRxiv filtering mode."""

    normalized_source = source_name.strip().lower()
    filter_mode_map = {
        "biorxiv": "relaxed",
        "medrxiv": "strict",
        "chemrxiv": "strict",
    }
    return filter_mode_map.get(normalized_source, "strict")


def get_relaxed_tech_signals(tech: str) -> list[str]:
    """Return lightweight bioRxiv-only technology signals."""

    normalized_tech = tech.strip().lower()
    relaxed_signal_map = {
        "breeding": [
            "breeding",
            "plant breeding",
            "crop breeding",
            "crop improvement",
            "cultivar development",
            "variety improvement",
        ],
        "germplasm": [
            "germplasm",
            "genetic resources",
            "germplasm resources",
            "accession",
            "landrace",
            "cultivar collection",
        ],
        "qtl mapping": [
            "qtl mapping",
            "qtl",
            "quantitative trait locus",
            "trait locus",
            "linkage mapping",
        ],
        "gwas": [
            "gwas",
            "genome-wide association study",
            "genome wide association study",
            "association mapping",
        ],
        "marker-assisted selection": [
            "marker-assisted selection",
            "marker assisted selection",
            "mas",
            "molecular marker",
            "marker-based selection",
            "marker assisted breeding",
            "molecular breeding",
        ],
        "crispr": [
            "crispr",
            "crispr/cas",
            "crispr-cas",
            "cas9",
            "cas12",
            "genome editing by crispr",
        ],
        "gene editing": [
            "gene editing",
            "gene-editing",
            "genome editing",
            "targeted mutagenesis",
            "site directed mutagenesis",
        ],
        "genomic selection": [
            "genomic selection",
            "genome-enabled selection",
            "genomic prediction",
            "gblup",
            "genomic estimated breeding value",
            "genomic estimated breeding values",
        ],
    }
    return relaxed_signal_map.get(normalized_tech, get_tech_aliases(normalized_tech))


def _contains_alias(text_blob: str, alias: str) -> bool:
    """Match an alias with simple phrase boundaries."""

    normalized_text = f" {text_blob} "
    normalized_alias = normalize_text_for_match(alias)
    if not normalized_alias:
        return False
    return f" {normalized_alias} " in normalized_text


def _get_first_matched_alias(text_blob: str, aliases: list[str]) -> str | None:
    """Return the first alias found in normalized text."""

    for alias in aliases:
        if _contains_alias(text_blob, alias):
            return alias
    return None


def _matches_any_alias(text_blob: str, aliases: list[str]) -> bool:
    """Return whether normalized text matches any alias."""

    return any(_contains_alias(text_blob, alias) for alias in aliases)


def is_relevant_xrxiv_record(
    paper: dict,
    crop: str,
    tech: str,
    source_name: str,
) -> tuple[bool, str]:
    """Evaluate whether an xRxiv candidate record matches the current query pair."""

    title = paper.get("title")
    abstract = paper.get("abstract")
    text_blob = normalize_text_for_match(f"{title or ''} {abstract or ''}")

    crop_aliases = get_xrxiv_crop_aliases(crop, source_name)
    tech_aliases = get_tech_aliases(tech)
    filter_mode = get_xrxiv_filter_mode(source_name)

    matched_crop_alias = _get_first_matched_alias(text_blob, crop_aliases)
    if not matched_crop_alias:
        return False, "missing crop token"

    matched_strict_tech = _matches_any_alias(text_blob, tech_aliases)

    if filter_mode == "strict":
        if matched_strict_tech:
            return True, "matched strict tech token"
        return False, "missing tech token"

    relaxed_signals = get_relaxed_tech_signals(tech)
    matched_relaxed_tech = _matches_any_alias(text_blob, relaxed_signals)

    if matched_strict_tech:
        return True, "matched strict tech token"
    if matched_relaxed_tech:
        return True, "matched relaxed tech signal"
    return False, "missing tech token"


def get_matched_crop_alias_for_paper(
    paper: dict,
    crop: str,
    source_name: str,
) -> str | None:
    """Return the crop alias matched by a paper, for lightweight debug logs."""

    text_blob = normalize_text_for_match(
        f"{paper.get('title') or ''} {paper.get('abstract') or ''}"
    )
    crop_aliases = get_xrxiv_crop_aliases(crop, source_name)
    return _get_first_matched_alias(text_blob, crop_aliases)
