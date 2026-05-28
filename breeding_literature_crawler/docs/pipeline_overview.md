# Pipeline Overview

The pipeline can be read as a staged workflow:

1. Configuration loading
2. Query pair generation
3. Source-specific retrieval
4. xRxiv local dump search
5. Relevance filtering
6. `retrieval_word` tagging
7. Cleaning and deduplication
8. Raw inventory reporting
9. Documentation and CI

## Stage 1: Configuration Loading

Entry scripts load `configs/crops.yaml`, `configs/technologies.yaml`, `configs/sources.yaml`, and `configs/pipeline.yaml` through shared configuration helpers.

The repository uses configuration to define crop vocabularies, technology vocabularies, source parameters, and downstream output paths.

## Stage 2: Query Pair Generation

`src/agri_lit_pipeline/query_builder.py` generates `(crop, technology)` query pairs.

The query builder intentionally produces structured pairs instead of final source query strings. Each source can then translate the pair in a way that fits its retrieval interface.

## Stage 3: Source-Specific Retrieval

PubMed retrieval is started through `scripts/run_pubmed.py` and implemented in `sources/pubmed.py`.

arXiv retrieval is started through `scripts/run_arxiv.py` and implemented in `sources/arxiv.py`. The arXiv source layer can convert query pairs into stricter query strings.

The source adapters wrap `paperscraper` retrieval APIs rather than reimplementing all upstream source clients from scratch. This repository adds configuration-driven query generation, source-specific adaptation, relevance filtering, tagging, cleaning, and reporting around that backend.

## Stage 4: xRxiv Local Dump Search

bioRxiv, medRxiv, and chemRxiv use a dump-first workflow:

- `scripts/download_biorxiv_dump.py`
- `scripts/download_medrxiv_dump.py`
- `scripts/download_chemrxiv_dump.py`

Local search is then run through:

- `scripts/run_biorxiv_local.py`
- `scripts/run_medrxiv_local.py`
- `scripts/run_chemrxiv_local.py`

Shared xRxiv behavior lives in `src/agri_lit_pipeline/sources/xrxiv.py`.

The xRxiv dump download and local-search workflow relies on `paperscraper.get_dumps` and `paperscraper.load_dumps`. Changes in upstream dump availability or `paperscraper` behavior can affect reproducibility.

## Stage 5: Relevance Filtering

xRxiv candidate records can be noisy for agricultural breeding use cases. The pipeline applies lightweight, source-specific relevance filtering before writing final local-search outputs.

bioRxiv filtering is designed to reduce clearly irrelevant cross-domain noise but may still contain false positives and false negatives. medRxiv and chemRxiv are treated more conservatively because their candidate retrieval results are noisier.

## Stage 6: `retrieval_word` Tagging

`src/agri_lit_pipeline/tagging.py` adds `retrieval_word` metadata so downstream processing can preserve which query pair produced a record.

During cleaning and deduplication, duplicate records can merge multiple `retrieval_word` values.

## Stage 7: Cleaning and Deduplication

`scripts/run_cleaning.py` calls the cleaning layer. The cleaning workflow standardizes fields, filters short abstracts, normalizes title and DOI values, deduplicates records, and merges `retrieval_word` values.

The current cleaning stage is rule-based and transparent. It is not a final semantic deduplication system.

## Stage 8: Raw Inventory Reporting

`scripts/run_report.py` generates a raw inventory report by crop, technology, and source.

This report counts raw JSONL records. It should not be interpreted as the size or quality of a final cleaned corpus.
