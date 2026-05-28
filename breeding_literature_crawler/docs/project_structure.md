# Project Structure

## Repository Folders

| Path | Purpose | Track in Git |
| --- | --- | --- |
| `README.md` | Main repository entry point | Yes |
| `configs/` | Crop, technology, source, and pipeline configuration | Yes |
| `docs/` | Public documentation and generated report area | Yes, except large generated artifacts |
| `scripts/` | Entry scripts | Yes |
| `src/agri_lit_pipeline/` | Core Python package | Yes |
| `data/sample/` | Small public structural samples | Yes |
| `data/raw/` | Raw retrieval outputs | No |
| `data/cleaned/` | Cleaned datasets | No |
| `data/private/` | Private datasets, dumps, credentials, or caches | No |

## Folder Notes

`configs/` contains `crops.yaml`, `technologies.yaml`, `sources.yaml`, and `pipeline.yaml`. These files separate vocabularies, source settings, and downstream paths from code.

`scripts/` contains entry scripts. They should load configuration, assemble arguments, and call package modules. Source-specific retrieval logic should live under `src/agri_lit_pipeline/sources/`.

`src/agri_lit_pipeline/` contains the shared package modules for configuration loading, query pair generation, relevance filtering, `retrieval_word` tagging, cleaning and deduplication, and reporting.

`docs/` contains documentation for users and maintainers. `docs/generated/` is reserved for script-generated reports, not manually curated corpus documentation.

`data/` is local runtime space. The public repository should not contain full raw dumps, full cleaned corpora, private datasets, or generated corpus files.

## Runtime Outputs

Typical raw output locations are:

- `data/raw/pubmed/`
- `data/raw/arxiv/`
- `data/raw/biorxiv/`
- `data/raw/medrxiv/`
- `data/raw/chemrxiv/`

The cleaning entry script writes to the path configured by `pipeline.outputs.final_clean_dataset`. The reporting entry script writes to the path configured by `pipeline.outputs.report_markdown`.

These outputs are useful during local runs but should be reviewed carefully before any release commit.
