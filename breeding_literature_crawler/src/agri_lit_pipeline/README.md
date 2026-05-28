# `agri_lit_pipeline` Package

This package contains the shared implementation for the literature pipeline. Unlike `scripts/`, this directory holds reusable workflow logic, source-layer modules, cleaning, and reporting.

## Modules

- `config.py` loads YAML configuration.
- `query_builder.py` generates `(crop, technology)` query pairs.
- `tagging.py` adds `retrieval_word` metadata to JSONL records.
- `relevance.py` implements lightweight xRxiv relevance filtering rules.
- `normalize.py` normalizes titles and DOI values.
- `cleaning.py` performs multi-source cleaning and deduplication.
- `reporting.py` generates raw inventory Markdown reports.
- `sources/` contains source-specific retrieval implementations.

## Design Boundary

Entry scripts should stay thin. Shared business logic belongs here so it can be read, reused, and tested independently from command-line entry points.
