# Literature Collection

## 1. Installation

```powershell
conda create -n deepbreeding_lc python=3.12 -y
conda activate deepbreeding_lc
pip install -r requirements.txt
```

Notes:

- `paperscraper==0.3.6` is pinned in `requirements.txt`.
- Network or proxy availability may affect PubMed retrieval, arXiv retrieval, and xRxiv dump downloads.
  
## 2. Configuration Files

- `configs/crops.yaml`: crop terms used to build retrieval queries
- `configs/technologies.yaml`: breeding technology terms used to build retrieval queries
- `configs/sources.yaml`: source settings, output directories, and the xRxiv relevance-filter switch
- `configs/pipeline.yaml`: final cleaned output and report settings

## 3. Recommended Workflow

Step 1: configure crops, technologies, and sources in the YAML files.

Step 2: run PubMed retrieval if network access is available.

Step 3: run arXiv retrieval if that source is needed.

Step 4: download xRxiv dumps if local dump search is needed.

Step 5: run local bioRxiv retrieval against the prepared dumps.

Step 6: run cleaning and deduplication.

Step 7: run raw inventory report generation.

## 4. Command Examples

```powershell
python scripts/run_pubmed.py
python scripts/run_arxiv.py
python scripts/download_biorxiv_dump.py
python scripts/run_biorxiv_local.py
python scripts/run_cleaning.py
python scripts/run_report.py
```

## 5. xRxiv Relevance Filtering

The bioRxiv local workflows use `enable_relevance_filter` in `configs/sources.yaml`.

- The default value is `true`.
- This setting reduces obvious cross-domain noise.
- It does not guarantee a fully curated or fully clean corpus.
- If coarse retrieval is preferred, set `enable_relevance_filter: false`.
- Coarse retrieval usually increases recall, but it also increases noise.

## 6. Deduplication and Duplicate Count Explanation

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
