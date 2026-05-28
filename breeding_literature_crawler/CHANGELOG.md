# Changelog

All notable changes to this project will be documented in this file.

This project follows semantic versioning in spirit, although it is currently a research engineering module within the DeepBreeding repository rather than a packaged library.

## [Unreleased]

### Documentation

- Clarified the role of `paperscraper` as the retrieval backend and documented dependency-version considerations.
- Documented xRxiv filtered and coarse retrieval modes, including how to disable bioRxiv relevance filtering for exploratory retrieval.

## [0.1.0] - 2026-04-21

### Added

- Initial module version of the agricultural breeding literature pipeline.
- Configuration-driven crop and technology query generation.
- Source adapters for PubMed, arXiv, and xRxiv-family sources.
- Local dump retrieval workflow for bioRxiv, medRxiv, and chemRxiv.
- Source-specific relevance filtering for xRxiv local retrieval.
- `retrieval_word` tagging for query provenance.
- Cleaning and deduplication workflow.
- Raw inventory report generation.
- MkDocs documentation structure.
- Minimal CI smoke checks.

### Notes

- Full raw dumps and cleaned corpora are not included in this repository.
- xRxiv relevance filtering remains under active refinement.
- This module version focuses on codebase and workflow publication.
