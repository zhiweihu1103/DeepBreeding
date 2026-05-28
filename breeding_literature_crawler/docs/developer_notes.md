# Developer Notes

## Why Entry Scripts Are Thin

Entry scripts are kept thin so that command-line entry points remain easy to inspect and maintain. Their responsibilities are limited to configuration loading, path preparation, query pair generation, and module dispatch.

Business logic should live in package modules under `src/agri_lit_pipeline/`, where it can be reused and tested more directly.

## Why Source Logic Lives Under `sources/`

Each scholarly source has different retrieval behavior, metadata conventions, and noise patterns. Keeping source logic under `src/agri_lit_pipeline/sources/` makes these differences explicit:

- PubMed uses online retrieval.
- arXiv uses online retrieval with source-specific query construction.
- bioRxiv, medRxiv, and chemRxiv use local dump search.

This structure avoids placing source-specific behavior in entry scripts or in the generic query pair builder.

## Why xRxiv Filtering Is Source-Specific

xRxiv relevance filtering is still under iterative refinement. The bioRxiv workflow aims to reduce clearly irrelevant cross-domain noise while preserving potentially relevant agricultural breeding records. medRxiv and chemRxiv are treated more conservatively because their candidate retrieval results are noisier for this use case.

For that reason, relevance filtering belongs near the xRxiv source layer rather than in generic configuration loading or query pair generation.

## Why Cleaning and Reporting Are Separate

Cleaning and reporting answer different questions.

Cleaning standardizes records, filters records, deduplicates by DOI or normalized title, and merges `retrieval_word` values.

Reporting counts raw JSONL outputs by crop, technology, and source. The raw inventory report is useful for workflow inspection, but it is not a final cleaned quality evaluation.

Keeping these layers separate makes it easier to reason about whether a problem comes from retrieval, relevance filtering, cleaning, or reporting.

## Current Maintenance Areas

The most likely areas for continued refinement are:

- `src/agri_lit_pipeline/relevance.py`
- `src/agri_lit_pipeline/sources/xrxiv.py`
- documentation of source-specific assumptions
- tests around cleaning, deduplication, and reporting

The current pipeline is a research engineering codebase, not a fully productized turnkey package.
