# Project Maintenance Notes

This document records current maintenance guidance for the public repository.

## Current Structure

The repository separates:

- Configuration files under `configs/`
- Entry scripts under `scripts/`
- Shared package logic under `src/agri_lit_pipeline/`
- Source-specific retrieval under `src/agri_lit_pipeline/sources/`
- Public documentation under `docs/`
- Local-only data outputs under `data/`

## Maintenance Boundaries

Entry scripts should primarily load configuration, prepare paths, generate query pairs, and dispatch work.

Source-specific retrieval behavior belongs under `src/agri_lit_pipeline/sources/`. Shared cleaning, normalization, tagging, and reporting logic belongs under `src/agri_lit_pipeline/`.

## Workflow Coverage

The workflow covers:

- Configuration loading
- Query pair generation
- PubMed and arXiv online retrieval
- bioRxiv, medRxiv, and chemRxiv local dump search
- Relevance filtering
- `retrieval_word` tagging
- Cleaning and deduplication
- Raw inventory reporting
- Documentation and CI smoke checks

This is a research engineering pipeline. It should not be described as a fully productized package or as a ready-to-use high-quality corpus release.

## Data Release Boundary

The public repository should include code, configuration, examples, and documentation. It should not include full raw dumps, full cleaned corpora, private datasets, local caches, or generated corpus files.

The `data/` directory should be treated as local runtime space except for explicitly reviewed small samples.

## Review Priorities

Before publishing or merging release changes, review:

- Whether generated or private data files are excluded
- Whether configuration values still match the intended workflow
- Whether documentation accurately describes current behavior
- Whether smoke tests and documentation builds still pass
