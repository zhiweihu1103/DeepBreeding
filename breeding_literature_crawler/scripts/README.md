# Scripts Guide

`scripts/` contains entry scripts. They load `configs/*.yaml`, prepare paths, generate query pairs, and call modules under `src/agri_lit_pipeline/`.

## Categories

### Online Retrieval

- `run_pubmed.py`
- `run_arxiv.py`

### xRxiv Dump Download

- `download_biorxiv_dump.py`
- `download_medrxiv_dump.py`
- `download_chemrxiv_dump.py`

### xRxiv Local Search

- `run_biorxiv_local.py`
- `run_medrxiv_local.py`
- `run_chemrxiv_local.py`

### Downstream Processing

- `run_cleaning.py`
- `run_report.py`

## Maintenance Notes

- Put source-specific retrieval behavior in `src/agri_lit_pipeline/sources/`.
- Put cleaning and reporting behavior in `src/agri_lit_pipeline/cleaning.py` and `src/agri_lit_pipeline/reporting.py`.
- Keep entry scripts focused on configuration loading and dispatch.
