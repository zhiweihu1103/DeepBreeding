# Known Limitations

This repository open-sources the codebase and workflow, not a complete data release.

## Data Boundary

- Full raw dumps are not included.
- Full cleaned corpora are not included.
- Private datasets are not included.
- Large JSONL outputs, dumps, caches, and private data directories should remain outside version control.

## Relevance Filtering

xRxiv relevance filtering is still under iterative refinement. It is designed to be lightweight and inspectable, not to solve semantic relevance classification completely.

bioRxiv filtering is designed to reduce clearly irrelevant cross-domain noise but may still contain false positives and false negatives.

medRxiv and chemRxiv are treated more conservatively because their candidate retrieval results are noisier for agricultural breeding use cases. This can reduce obvious noise, but it may also reduce recall.

## Cleaning and Deduplication

The current cleaning stage uses rule-based deduplication. It prioritizes DOI matching where possible and otherwise uses normalized titles. This is useful as a transparent first pass, but it is not a final semantic deduplication system.

`retrieval_word` values are merged across duplicate records so that query pair traceability is not lost during deduplication.

## Reporting

The raw inventory report counts raw JSONL records by crop, technology, and source. It does not represent a final cleaned corpus size and should not be used as a final data quality evaluation.

## Engineering Maturity

The current pipeline is a research engineering codebase, not a fully productized turnkey package. It depends on external APIs, local dump availability, third-party package behavior, and configuration choices.

Users should review configuration, source availability, local storage, and generated outputs before running large retrieval jobs or publishing results.
