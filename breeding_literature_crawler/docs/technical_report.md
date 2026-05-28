# Technical Overview

This document summarizes the current public technical scope of the repository.

## Repository Positioning

Agri Breeding Literature Pipeline open-sources the codebase and workflow for multi-source agricultural breeding literature retrieval, preprocessing, cleaning, deduplication, and reporting.

The repository is a research engineering codebase. It documents how query pairs are generated, how source-specific retrieval is dispatched, how xRxiv candidate records are filtered, and how downstream cleaning and raw inventory reporting are organized.

## Data Boundary

The repository does not include full raw dumps, full cleaned corpora, or private datasets. Local runtime outputs should remain outside version control, especially under:

- `data/raw/`
- `data/cleaned/`
- `data/private/`

Generated reports should be reviewed before publication because they reflect local runs and may not represent final cleaned corpus quality.

## Supported Sources

- PubMed
- arXiv
- bioRxiv
- medRxiv
- chemRxiv

PubMed and arXiv use online retrieval workflows. bioRxiv, medRxiv, and chemRxiv use local dump search workflows after dump preparation.

## Pipeline Stages

1. Configuration loading
2. Query pair generation
3. Source-specific retrieval
4. xRxiv local dump search
5. Relevance filtering
6. `retrieval_word` tagging
7. Cleaning and deduplication
8. Raw inventory reporting
9. Documentation and CI

## Engineering Notes

Entry scripts are kept thin so they can remain readable and predictable. Source-specific retrieval logic lives under `src/agri_lit_pipeline/sources/`. Shared utilities, cleaning, and reporting live under `src/agri_lit_pipeline/`.

xRxiv relevance filtering is source-specific. bioRxiv filtering is designed to reduce clearly irrelevant cross-domain noise while still allowing iterative refinement. medRxiv and chemRxiv are treated more conservatively because candidate retrieval results are noisier for agricultural breeding use cases.

Cleaning and reporting are separated. Cleaning produces a deduplicated output according to configured rules. Reporting produces a raw inventory report and should not be interpreted as a final quality evaluation.

## Current Limitations

- xRxiv relevance filtering is still under iterative refinement.
- bioRxiv filtering may still contain false positives and false negatives.
- medRxiv and chemRxiv filtering may sacrifice recall to reduce noise.
- Rule-based cleaning is not semantic deduplication.
- The raw inventory report is not a final cleaned corpus quality assessment.
- The current pipeline is not a fully productized turnkey package.
