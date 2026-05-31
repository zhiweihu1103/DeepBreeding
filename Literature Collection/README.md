# Literature Collection

## Overview

`Literature Collection` is a lightweight `DeepBreeding` module for agricultural breeding literature retrieval, preprocessing, cleaning, deduplication, and raw inventory reporting.

This module is maintained inside the `DeepBreeding` repository rather than as a standalone project. It publishes code, scripts, and configuration only. It does not include raw dumps, cleaned corpus data, private datasets, generated JSONL outputs, or virtual environments.

## Module Capabilities

- PubMed retrieval
- arXiv retrieval
- bioRxiv / medRxiv / chemRxiv local dump retrieval
- crop and technology query generation from YAML configs
- `retrieval_word` tagging for query provenance
- xRxiv relevance filtering
- cleaning and DOI/title-based deduplication
- raw inventory report generation

## Directory Structure

```text
Literature Collection/
|-- README.md
|-- requirements.txt
|-- configs/
|-- scripts/
`-- src/agri_lit_pipeline/
```

- `README.md`: practical usage notes for this module
- `requirements.txt`: pinned runtime dependencies
- `configs/`: crop, technology, source, and pipeline YAML configuration
- `scripts/`: entry scripts for retrieval, cleaning, and reporting
- `src/agri_lit_pipeline/`: shared pipeline logic and source adapters

## Environment Setup

Python 3.11+ is recommended.

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Notes:

- `paperscraper==0.3.6` is pinned in `requirements.txt`.
- Network or proxy availability may affect PubMed retrieval, arXiv retrieval, and xRxiv dump downloads.
- A full crawl is not required for a quick code or configuration check.

## Configuration Files

- `configs/crops.yaml`: crop terms used to build retrieval queries
- `configs/technologies.yaml`: breeding technology terms used to build retrieval queries
- `configs/sources.yaml`: source settings, output directories, and the xRxiv relevance-filter switch
- `configs/pipeline.yaml`: final cleaned output and report settings

If the retrieval vocabulary needs to change, edit the YAML files first before changing anything in code.

## Recommended Workflow

Step 1: configure crops, technologies, and sources in the YAML files.

Step 2: run PubMed retrieval if network access is available.

Step 3: run arXiv retrieval if that source is needed.

Step 4: download xRxiv dumps if local dump search is needed.

Step 5: run local bioRxiv, medRxiv, and chemRxiv retrieval against the prepared dumps.

Step 6: run cleaning and deduplication.

Step 7: run raw inventory report generation.

## Command Examples

```powershell
python scripts/run_pubmed.py
python scripts/run_arxiv.py
python scripts/download_biorxiv_dump.py
python scripts/download_medrxiv_dump.py
python scripts/download_chemrxiv_dump.py
python scripts/run_biorxiv_local.py
python scripts/run_medrxiv_local.py
python scripts/run_chemrxiv_local.py
python scripts/run_cleaning.py
python scripts/run_report.py
```

These commands are the standard workflow entry points. For a quick validation pass, you do not need to run full crawling.

## xRxiv Relevance Filtering

The bioRxiv, medRxiv, and chemRxiv local workflows use `enable_relevance_filter` in `configs/sources.yaml`.

- The default value is `true`.
- This setting reduces obvious cross-domain noise.
- It does not guarantee a fully curated or fully clean corpus.
- If coarse retrieval is preferred, set `enable_relevance_filter: false`.
- Coarse retrieval usually increases recall, but it also increases noise.

## Deduplication and Duplicate Count Explanation

Raw crawler outputs are query-hit records, not unique-paper records.

The same paper may be retrieved multiple times by different crop terms, technology terms, or source-specific queries. As a result, a large duplicate-hit count does not mean that millions of distinct papers are duplicated.

Cleaning uses normalized DOI first and normalized title as a fallback when DOI is missing. In the reporting outputs, `duplicates_merged` should be interpreted as merged redundant query-hit records. `unique_papers_saved` is closer to the final unique-paper count.

Example:

A maize GWAS paper may be retrieved by:

- `maize breeding`
- `maize GWAS`
- `maize genomic selection`
- `marker-assisted selection`

These are multiple hits for one paper, not multiple different papers.

## Minimal Validation

```powershell
python -m compileall -q src scripts
python -c "import yaml, pathlib; files=list(pathlib.Path('configs').glob('*.yaml')); [yaml.safe_load(p.read_text(encoding='utf-8')) for p in files]; print('YAML OK')"
```

These checks validate Python syntax and YAML readability only. They do not run full crawling or generate collection outputs.

## Data Policy

- Do not commit raw dumps.
- Do not commit cleaned corpus files.
- Do not commit private datasets.
- Do not commit generated JSONL outputs.
- Do not commit virtual environments.

## Notes for DeepBreeding Users

- This module should be maintained as part of `DeepBreeding`.
- If the query vocabulary changes, update the YAML configs first.
- If source APIs or `paperscraper` behavior changes, rerun small smoke checks before full collection.
- For formal data statistics, rerun cleaning on the current raw dataset and report `raw records`, `valid records`, `duplicates_merged`, and `unique_papers_saved` separately.
