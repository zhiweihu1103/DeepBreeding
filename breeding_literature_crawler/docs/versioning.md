# Versioning

## Current Version

The current module version is `v0.1.0`, dated 2026-04-21.

This is the current DeepBreeding module version for the codebase and workflow for multi-source agricultural breeding literature retrieval, preprocessing, relevance filtering, `retrieval_word` tagging, cleaning, deduplication, and raw inventory reporting.

## Versioning Policy

This module follows semantic versioning in spirit:

- Patch updates may clarify documentation, fix small bugs, or improve validation checks.
- Minor updates may add source-layer improvements, filtering refinements, tests, or packaging support.
- Major updates would be reserved for substantial workflow or public-interface changes.

The module is a research engineering codebase rather than a fully productized package, so version numbers describe the maintained codebase and workflow state rather than a packaged library release.

## Version Scope

Module version content includes:

- Source code under `src/`
- Entry scripts under `scripts/`
- Configuration templates under `configs/`
- Public documentation under `docs/`
- Validation-related project files
- Citation and repository metadata

Module version content does not include:

- Full raw dumps
- Generated JSONL corpus files
- Full cleaned corpora
- Private datasets
- Local caches or machine-specific runtime outputs

## Current Public Status

`v0.1.0` should be understood as the current module version of a configurable workflow. It supports PubMed, arXiv, bioRxiv, medRxiv, and chemRxiv, but source availability, network conditions, local dump availability, and configuration choices still affect runtime behavior.

xRxiv relevance filtering remains under iterative refinement. bioRxiv uses a relaxed source-specific filtering policy, while medRxiv and chemRxiv use stricter policies because their candidate retrieval results are noisier for agricultural breeding use cases.

The default relevance filtering policy is part of the codebase version. Coarse retrieval mode is available for users who want unfiltered candidate records from local xRxiv search, but coarse outputs are not considered curated corpus releases.

## Dependency Version Policy

The module version tracks the lab-maintained codebase and workflow. Runtime retrieval behavior also depends on third-party libraries, especially `paperscraper`, which provides the PubMed, arXiv, xRxiv dump download, and xRxiv local-search backend used by the source layer.

Future module versions should record tested dependency versions in `requirements.txt`. When `paperscraper` is upgraded, maintainers should revalidate source-layer behavior, lightweight smoke tests, and any workflows that depend on upstream APIs or local dump loading.

## Future Directions

Potential future versions may include:

- Improved xRxiv relevance filtering
- More systematic tests for cleaning, reporting, and source-layer behavior
- Packaging improvements
- Expanded documentation
- Optional Docker support if a Docker workflow is implemented later
