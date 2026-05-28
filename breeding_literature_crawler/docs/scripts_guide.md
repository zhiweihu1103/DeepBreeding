# Scripts Guide

The files under `scripts/` are entry scripts. They load configuration, prepare paths and query pairs, and call modules under `src/agri_lit_pipeline/`.

## Online Retrieval

### `scripts/run_pubmed.py`

Runs PubMed online retrieval.

Typical command:

```powershell
.\.venv\Scripts\python.exe scripts\run_pubmed.py
```

It reads crop, technology, and PubMed configuration, generates query pairs, and calls the PubMed source layer.

### `scripts/run_arxiv.py`

Runs arXiv online retrieval.

Typical command:

```powershell
.\.venv\Scripts\python.exe scripts\run_arxiv.py
```

It reads crop, technology, and arXiv configuration, generates query pairs, and calls the arXiv source layer.

## xRxiv Dump Download

### `scripts/download_biorxiv_dump.py`

Downloads or prepares the bioRxiv dump workflow through the xRxiv source layer.

### `scripts/download_medrxiv_dump.py`

Downloads or prepares the medRxiv dump workflow through the xRxiv source layer.

### `scripts/download_chemrxiv_dump.py`

Downloads or prepares the chemRxiv dump workflow through the xRxiv source layer.

Typical commands:

```powershell
.\.venv\Scripts\python.exe scripts\download_biorxiv_dump.py
.\.venv\Scripts\python.exe scripts\download_medrxiv_dump.py
.\.venv\Scripts\python.exe scripts\download_chemrxiv_dump.py
```

The underlying `paperscraper` behavior may influence where downloaded dump files are stored. The configured `dump_dir` documents the intended local dump area and prepares local paths where the repository controls them.

## xRxiv Local Search

### `scripts/run_biorxiv_local.py`

Searches a local bioRxiv dump and applies bioRxiv-oriented relevance filtering.

By default, `configs/sources.yaml` sets:

```yaml
biorxiv:
  enable_relevance_filter: true
```

This filtered mode is recommended for the default lab workflow. For coarse retrieval experiments, set `enable_relevance_filter: false`. Coarse mode writes all valid local search candidates returned by `paperscraper`, which can increase recall but also increases noise. Coarse output is not a curated corpus.

When switching between filtered and coarse modes, use a separate `output_dir`, move existing outputs, or set `skip_if_exists: false` intentionally. Otherwise, existing JSONL files may be skipped. See [xRxiv Retrieval Modes](xrxiv_retrieval_modes.md).

### `scripts/run_medrxiv_local.py`

Searches a local medRxiv dump with a more conservative relevance filtering policy.

### `scripts/run_chemrxiv_local.py`

Searches a local chemRxiv dump with a more conservative relevance filtering policy.

Typical commands:

```powershell
.\.venv\Scripts\python.exe scripts\run_biorxiv_local.py
.\.venv\Scripts\python.exe scripts\run_medrxiv_local.py
.\.venv\Scripts\python.exe scripts\run_chemrxiv_local.py
```

All three scripts use query pairs and delegate local dump behavior to `src/agri_lit_pipeline/sources/xrxiv.py`.

## Downstream Processing

### `scripts/run_cleaning.py`

Runs cleaning and deduplication across raw JSONL outputs.

Typical command:

```powershell
.\.venv\Scripts\python.exe scripts\run_cleaning.py
```

The output path is configured by `pipeline.outputs.final_clean_dataset`.

### `scripts/run_report.py`

Generates the raw inventory report by crop, technology, and source.

Typical command:

```powershell
.\.venv\Scripts\python.exe scripts\run_report.py
```

The output path is configured by `pipeline.outputs.report_markdown`.

## Suggested First Runs

For orientation, start with the smoke-test checks in [smoke_test.md](smoke_test.md). If local raw JSONL outputs already exist, `run_cleaning.py` and `run_report.py` are useful first downstream checks.

Avoid running the full query matrix or full xRxiv dump workflows until configuration, network requirements, and local storage assumptions are clear.
