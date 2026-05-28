# Agri Breeding Literature Pipeline

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![paperscraper](https://img.shields.io/badge/paperscraper-0.3.6-blueviolet)
![Version](https://img.shields.io/badge/Version-v0.1.0-informational)
![License](https://img.shields.io/badge/License-Apache--2.0-blue)
![Status](https://img.shields.io/badge/Status-Research%20Engineering-orange)
![Data](https://img.shields.io/badge/Data-not%20included-lightgrey)
![Sources](https://img.shields.io/badge/Sources-PubMed%20%7C%20arXiv%20%7C%20xRxiv-blueviolet)

A configurable literature retrieval and preprocessing module under the DeepBreeding project for collecting, filtering, cleaning, deduplicating, and documenting crop breeding literature records from multiple scholarly sources.

This module provides the codebase and workflow for multi-source agricultural breeding literature retrieval, preprocessing, cleaning, deduplication, and reporting within `DeepBreeding/breeding_literature_crawler/`. It does not include full raw dumps, full cleaned corpora, or private datasets.

## Module Status

- Current module version: `v0.1.0`
- Module type: research engineering codebase
- Maintainer: AgriMind Research Group, Shanxi Agricultural University
- Supported sources: PubMed, arXiv, bioRxiv, medRxiv, chemRxiv
- Data policy: raw dumps and cleaned corpora are not versioned in Git

## Supported Sources

- PubMed
- arXiv
- bioRxiv
- medRxiv
- chemRxiv

PubMed and arXiv are handled through online retrieval workflows. BioRxiv, medRxiv, and chemRxiv are handled through local dump retrieval workflows after source dump preparation.

## Core Dependency: paperscraper

This module uses [`paperscraper`](https://github.com/jannisborn/paperscraper) as the underlying retrieval backend. PubMed retrieval is delegated to `paperscraper.pubmed`, arXiv retrieval is delegated to `paperscraper.arxiv`, and bioRxiv, medRxiv, and chemRxiv dump download/local search rely on `paperscraper.get_dumps` and `paperscraper.load_dumps`.

The module adds configuration-driven query generation, source-specific adaptation, relevance filtering, `retrieval_word` tagging, cleaning, deduplication, and reporting around this backend. Upstream API and dump behavior may change over time, so reproducibility depends partly on the installed `paperscraper` version. The tested version is recorded in [requirements.txt](requirements.txt).

## Repository Structure

```text
DeepBreeding/
|-- breeding_literature_crawler/
|   |-- README.md
|   |-- CITATION.cff
|   |-- configs/                  # Crop, technology, source, and pipeline configuration
|   |-- scripts/                  # Entry scripts for retrieval, cleaning, and reporting
|   |-- src/agri_lit_pipeline/    # Shared utilities, source layer, cleaning, and reporting modules
|   |-- docs/                     # Public documentation and MkDocs pages
|   |-- data/                     # Local-only runtime output space, not a versioned corpus
```

- `configs/` defines the configuration-driven workflow without changing source code.
- `scripts/` contains thin entry scripts that load configuration and call package modules.
- `src/agri_lit_pipeline/` contains shared utilities, source-specific retrieval logic, relevance filtering, cleaning and deduplication, and reporting.
- `docs/` contains the public documentation site and manually written technical notes.
- `data/` is reserved for local runtime outputs. Full raw dumps, full cleaned corpora, private datasets, caches, and generated corpus files should not be committed.

## Quick Start

The examples below assume PowerShell on Windows. Use equivalent activation commands on other platforms.

```powershell
cd E:\DL\DeepBreeding\breeding_literature_crawler
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Install documentation dependencies only if you want to build or preview the documentation site:

```powershell
pip install -r requirements-docs.txt
```

Run lightweight local checks that do not trigger full crawling:

```powershell
@'
from pathlib import Path
import py_compile

root = Path(".")
for path in list((root / "src").rglob("*.py")) + list((root / "scripts").glob("*.py")):
    py_compile.compile(str(path), doraise=True)
print("py_compile ok")
'@ | .\.venv\Scripts\python.exe -
```

Representative entry scripts:

```powershell
.\.venv\Scripts\python.exe scripts\run_pubmed.py
.\.venv\Scripts\python.exe scripts\run_arxiv.py
.\.venv\Scripts\python.exe scripts\download_biorxiv_dump.py
.\.venv\Scripts\python.exe scripts\run_biorxiv_local.py
.\.venv\Scripts\python.exe scripts\run_cleaning.py
.\.venv\Scripts\python.exe scripts\run_report.py
```

These commands depend on configuration, API/network availability, and local dump availability. The module should not be interpreted as a turnkey package that can always perform full crawling immediately in a fresh environment.

## Main Workflows

The pipeline is organized around these stages:

1. Configuration loading from `configs/*.yaml`
2. Query pair generation from crop and technology vocabularies
3. Source-specific retrieval for PubMed and arXiv
4. xRxiv local dump search for bioRxiv, medRxiv, and chemRxiv
5. Relevance filtering for xRxiv candidate records
6. `retrieval_word` tagging to preserve the query pair context
7. Cleaning and deduplication across source outputs
8. Raw inventory reporting by crop, technology, and source
9. Documentation and validation checks

Online retrieval is handled by `scripts/run_pubmed.py` and `scripts/run_arxiv.py`. Local dump retrieval uses `download_*_dump.py` followed by `run_*_local.py`. Cleaning is handled by `scripts/run_cleaning.py`, and raw inventory reporting is handled by `scripts/run_report.py`.

By default, xRxiv local retrieval applies source-specific relevance filtering. Users who need coarse bioRxiv retrieval can set `enable_relevance_filter: false` in `configs/sources.yaml`; see [xRxiv Retrieval Modes](docs/xrxiv_retrieval_modes.md).

Build the documentation site with:

```powershell
python -m mkdocs build
```

or, if using the local virtual environment:

```powershell
.\.venv\Scripts\python.exe -m mkdocs build
```

## Documentation

Start with:

- [Architecture](docs/architecture.md)
- [Pipeline Overview](docs/pipeline_overview.md)
- [Configuration](docs/configuration.md)
- [Scripts Guide](docs/scripts_guide.md)
- [xRxiv Retrieval Modes](docs/xrxiv_retrieval_modes.md)
- [Project Structure](docs/project_structure.md)
- [Versioning](docs/versioning.md)
- [Known Limitations](docs/known_limitations.md)
- [Smoke Test](docs/smoke_test.md)

## Versioning

This module follows semantic versioning in spirit. `v0.1.0` is the current module version of the codebase and workflow inside DeepBreeding.

Future versions may improve source adapters, relevance filtering rules, tests, documentation, and packaging. Dataset outputs are not versioned in Git; local raw dumps, generated JSONL files, cleaned corpora, and private datasets remain outside the module version scope.

## Known Limitations

- xRxiv relevance filtering is still under iterative refinement.
- bioRxiv filtering is designed to reduce clearly irrelevant cross-domain noise but may still contain false positives and false negatives.
- medRxiv and chemRxiv are treated more conservatively because their candidate retrieval results are noisier for agricultural breeding use cases.
- The current pipeline is a research engineering codebase, not a fully productized turnkey package.
- This module does not include full raw dumps, full cleaned corpora, or private datasets.
- The raw inventory report is not a final cleaned quality evaluation.

## Citation

Citation metadata is provided in [CITATION.cff](CITATION.cff).

## License

This project is licensed under the [Apache License 2.0](LICENSE).
